
Admin Profile
------------------
**METHOD:GET**

*view Admin profile*

`/admins/profile/<int:id>`_

- after admin or super-admin is logged in, we can see their profile by hiting above provided url

**INSIDE ADMIN PROFILE**

- user profile info(name. address, profile pic)

*view user add form*

`/admins/addadmin/`_

- when super-admin is logged-in a admin add page is rendered

.. list-table:: **user add form**
   :widths: 25 25 25
   :header-rows: 1

   * - Fields
     - Input Type
     - Attribute
   * - Address
     - String
     - Required
   * - Email
     - Email
     - Required
   * - First Name
     - String
     - Required
   * - Last Name
     - String
     - Required
   * - Logo
     - File
     - -
   * - Active
     - Choose
     - -
   * - Staff
     - Choose
     - -
   * - Admin
     - Choose
     - -

*view Product add form*

`/admins/productadd/`_

- Super admin and admin can view the add product form before submitting form

.. list-table:: **product add form**
   :widths: 25 25 25
   :header-rows: 1

   * - Fields
     - Input Type
     - Attribute
   * - Name
     - String
     - Required
   * - Price
     - Decimal
     - Required
   * - Image
     - File
     - Required
   * - Category
     - category
     - Required

*view catgeory add form*

`/product/addcategory/`_

- Super admin can view the add category form before submitting it

.. list-table:: **product add form**
   :widths: 25 25 25
   :header-rows: 1

   * - Fields
     - Input Type
     - Attribute
   * - Name
     - String
     - Required
   * - Status
     - Boolean
     - Required

*Update Admin*

`/admins/updatecustomer/`_

- when we click on submit after filling all the information about user above url is called with user id

*program execution*

- All the data submitted in this form is validated in addadmin view
- If data is clean then it is updated in database

*Update Product*

`/admins/updateproduct/`_

- when we click on submit after filling all the information about user above url is called with product id

*program execution*

- All the data submitted in this form is validated in addadmin view
- If data is clean then it is updated in database

*Update Category*

`/admins/updatecategory/`_

- when we click on submit after filling all the information about user above url is called with category id

*program execution*

- All the data submitted in this form is validated in addadmin view
- If data is clean then it is updated in database

**METHOD:POST**

*Update Profile Picture*

`admins/profile/<int:id>/`_

- when we click on change profile picture, program flow moves to above url and profile picture is changed
.. code-block:: python
   :caption: program execution

    When we hit change profile picture url then first of all we get the email of the user which is stored 
    in session, after that we create a object of form with form data sent from template, check the validation
    of the form and update the logged-in user with data that we got from form. After the completion of updation
    of profile picture the program is redirected to "/admins/profile/<int:id>/"

*Change password*

`/admins/changePass/`_

- when we click on change passowrd the above url is called and password is validated,
  if validation successfull then password is changed

*program execution*

- modal-box is popped-up where it ask for old, new and re-enter new passowrd
- When we enter incorrect form data then we will get error message
- if correct data is sent then password will be updated

*Add User*

`/admins/addadmin/`_

- when we click on submit after filling all the information about user above url is called

*program execution*

- All the data submitted in this form is validated in addadmin view
- If data is clean then it is saved in database

*Add Product*

`/product/productadd/`_

- when we click on submit after filling all the information about user above url is called

*program execution*

- All the data submitted in this form is validated in addadmin view
- If data is clean then it is saved in database

*Add Category*

`/product/addcategory/`_

- when we click on submit after filling all the information about user above url is called

*program execution*

- All the data submitted in this form is validated in addadmin view
- If data is clean then it is saved in database

*Add Offer*

`/product/addoffer/`_

- admin and super-admin can click on submit after filling all the information about offer

*program execution*

- All the data submitted in this form is validated in addoffer view
- If data is clean then it is saved in database

*Delete Offer*

`/product/addoffer/`_

- admin and super-admin can click on delete offer

*program execution*

- deletes the offer
