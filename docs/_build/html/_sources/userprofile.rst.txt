
User Profile
------------------
**METHOD:GET**

*view user profile*

`/admins/userprofile/`_

- after normal user login page is redirected to website where we can see user profile

**INSIDE USER PROFILE**

- user profile info(name. address, profile pic)
- user update form
- change password form
- invoice(view all the purchase history)
- delete account(deactivate your account)

**METHOD:POST**

*Update Profile Picture or Update user address*

`/admins/updatecustomer/`_

- when we click on change profile picture, program flow moves to above url and profile picture is changed
.. code-block:: python
   :caption: program execution

    When we hit change profile picture url then first of all we get the email of the user which is stored 
    in session, after that we create a object of form with form data sent from template, check the validation
    of the form and update the logged-in user with data that we got from form. After the completion of updation
    of profile picture the program is redirected to "/admins/userprofile"

*Change password*

`/admins/changecustomerpassword/`_

- when we click on change passowrd, program flow moves to ajax and after that above url is called
.. code-block:: python
   :caption: program execution

    When we hit change passowrd url then first of all we check all the form data sent from change password form
    if all the data sent is not validated then an error json response is sent else we get the user object from 
    User table and update its password


