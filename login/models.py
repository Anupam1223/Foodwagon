from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# manager class for User, from this manager class we manage our user model
class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        password=None,
    ):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


# user model which extends AbstractBaseUser, have all the ability of django's default user model
# we can customize it according to our need
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, default="a@gmail.com")
    address = models.TextField(max_length=30, blank=True)
    first_name = models.TextField(max_length=30, blank=True, default="eg aster")
    last_name = models.TextField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)  # non super-user
    is_active = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)  # a superuser
    last_login = models.DateTimeField(blank=True, null=True, verbose_name="last login")
    profile_pic = models.ImageField(blank=True, null=True, upload_to="images/")

    # email will be used for login credentials
    USERNAME_FIELD = "email"

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def __str__(self):
        return self.email

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
