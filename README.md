## Project Foodwagon
### Developed by: @anupam
### Framework: django

Foodwagon is a online delivery system, this system contains two main regions:
1) Admin panel for super-admin and restaurents 
2) A website where user can order the food and have user interface where they can modify, update their 
profile and also see paid orders and bills

Admin panel where a user can login, if the user is admin then they can add, update, disable user, product and category.
Super-admin and restaurent both can add offers to product, both can change password, chnage profile image, etc

Order, product and offer are shown for particular restaurent if the logged-in user is restaurent owner, but if the logged-in user 
is super admin then they can view all the order, user, product, product offer and category, also super-admin can add
user and category.

Virtual environment setup is done with poetry, all the required dependencies(help or plugins needed to develop this project) are already
present in pyproject.toml file, you dont have to worry about all the dependencies, but if you are new to django then you must install some 
of the plugins
```
pip install pillow
pip install django-utils-six
pip install django-mathfilters 
pip install xhtml2pdf
```

automatically, project will setup in your device, incase if you dont have poetry in your device use `pip install poetry` to add poetry 
steps to run the code after cloning the project:
```
cd path/to/this/cloned/folder
POETRY INSTALL
POETRY RUN PYTHON MANAGE.PY RUNSERVER
```
for more information visit:
- [Poetry Docs] (https://python-poetry.org/docs/)
- [django documenation] (https://docs.djangoproject.com/)

```NOTE:
    go to
    - mullbery
    - settings.py
    - go down you will see email configuration
    - update EMAIL_HOST_USER with your valid email
    - update EMAIL_HOST_PASSWORD with your valid email password
```
hit `127.0.0.1/user` for accessing the website.

If you have any query regarding this project you can contact me @ mail anupam.siwakoti@gmail.com
