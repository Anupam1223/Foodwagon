SignIn
------------------
**METHOD:POST**

http://127.0.0.1:8000/login/

- When we hit this api we get a from where we can submit login credentials

**SIGNIN FORM FIELDS**

- email: email(required)
- password: string(required)
- rememberMe: checkbox()

.. code-block:: python
   :caption: Json Response

   When form is submitted Ajax is called, which hit the views thats validates and logs in the validated user,
   either the case json response is sent back to ajax, which shows errors if wrong credentials are provided,
   but redirects to their respective urls if logged-in is successful

   if admin:
      redirected to super-admin panel
   if staff:
      redirected to admin panel
   if user: 
      redirected to website with user profile
