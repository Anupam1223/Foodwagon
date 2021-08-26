
Cart and Order
------------------
**METHOD:GET**

*Add to Cart*

`/delivery/add_to_cart/`_

- when order now button is clicked program flow moves to ajax and ajax call the above URL

.. code-block:: python
   :caption: program execution

    Program flow is redirected to above url and after that all the selected product is saved in a list,
    this list is saved in a session so that we can access it afterwards. Duplicate values cant be stored in 
    this cart because we convert this cart list into set and again that set to list 

*Remove from Cart*

`/delivery/remove_from_cart/`_

- when remove button clicked, program flow moves to ajax and ajax call the above URL

.. code-block:: python
   :caption: program execution

    food id that we select to remove from cart is sent to ajax, ajax calls the above view and then removes the
    selected food from the list

*View Order*

`/delivery/view_order/`_

- when we hit this url we will get to see all the placed order with date and time

*program execution*

- If incase of normal user, paid order are shown in user profile(in website)
- If incase, admin then all the order either paid or un-paid related to it is shown(in admin panel)
- If incase, super-admin then all the order either paid or un-paid is shown(in admin panel)

*View Cart*

`/delivery/cart/`_

- when we hit this url we will get to see all the food ordered and kept in cart

*program execution*

- in this cart page, all the food kept in cart is shown
- We can remove food from cart
- Just below the list of food, there is an order form
- We select quantity of order and other details such as address etc for delivery
- When we click place order, all od this information is sent to ajax, where ajax call
   '/delivery/cart/' url and all the information is stored in database, all of the 
   validation is done inside this cart view

*View Bill*

`/delivery/view_bill/`_

- when we hit this url we will get all the paid orders by logged-in user
.. code-block:: python
   :caption: program execution

    Ajax is called when we click on the orders, ajax will indeed call "/admins/view_bill/" url and after that
    all the data manipulation is done i.e all the order and its details are made ready to be shown, json data 
    is sent back to ajax and ajax will show the data in html template 

*Generate PDF*

`/delivery/download_file/<int:id>/`_

- when we hit this url we see the provided bill in pdf format and also can download it

*program execution*

- we declared different template for invoice alone
- when we hit `/delivery/download_file/<int:id>/` url with order id then this view will return all the values to be shown in pdf
