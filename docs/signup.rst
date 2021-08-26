
SignUp
------------------
**METHOD:POST**

http://127.0.0.1:8000/login/register/

- When we hit this api we get a from where we can submit registration data

**SIGNUP FORM FIELDS**

- email: email(required)
- first_name: string(required)
- address: string(required)
- password: string(required)
- re_pass: string(reqiured)
- terms: checkbox()
- rememberMe: checkbox()

.. code-block:: python
   :caption: Json Response

   When form is submitted Ajax is called, which hit the views thats validates and register the validated user,
   either the case json response is sent back to ajax, which shows errors if wrong informations are provided,
   but redirects to login page with *check mail for verifying account* message

