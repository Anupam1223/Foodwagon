$(document).ready(function () {

    $('#login-form').submit(function (e) {
        e.preventDefault();
        var username = $('.username').val();
        var password = $('.password').val();
        var remember = $('.agree-term').val();

        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        // set csrf header
        $.ajaxSetup({
            beforeSend: function (e, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    e.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $.ajax({
            url: "",
            method: "POST",
            data: { logins: '1', username: username, password: password, rememberMe: remember },
            dataType: 'json',
            success: function (response) {
                $('.alert').hide();
                //console.log(response);
                var res = response;
                if (res.hasOwnProperty('success')) {

                    if (res.success == 'user') {
                        console.log("user")
                        $('.sign-in .signin-form').prepend('<div class="alert alert-success">LoggedIn Successfully.</div>');
                        setTimeout(function () { location.reload(); }, 1000);
                        window.location.href = '../';
                    }
                    else if (res.success == 'admin') {
                        console.log("admin")
                        $('.sign-in .signin-form').prepend('<div class="alert alert-success">LoggedIn Successfully.</div>');
                        setTimeout(function () { location.reload(); }, 1000);
                        window.location.href = '../admins/admin';
                    }
                    else {
                        console.log("staff")
                        $('.sign-in .signin-form').prepend('<div class="alert alert-success">LoggedIn Successfully.</div>');
                        setTimeout(function () { location.reload(); }, 1000);
                        window.location.href = '../admins/admin';
                    }

                } else if (res.hasOwnProperty('error')) {
                    $('.sign-in .signin-form').prepend('<div class="alert alert-danger">' + res.error + '</div>');
                }

            }
        });
    });


    $('#register-form').submit(function (e) {
        e.preventDefault();
        var username = $('.username').val();
        var password1 = $('.password').val();
        var name = $('.name').val();
        var password2 = $('.re-password').val();
        var address = $('.address').val();

        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        // set csrf header
        $.ajaxSetup({
            beforeSend: function (e, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    e.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $.ajax({
            url: "",
            method: "POST",
            data: { logins: '1', username: username, pass1: password1, pass2: password2, name: name, add: address },
            dataType: 'json',
            success: function (response) {
                $('.alert').hide();
                //console.log(response);
                var res = response;
                if (res.hasOwnProperty('success')) {
                    $('.signup-form').prepend('<div class="alert alert-success">check mail to verify account</div>');
                    setTimeout(function () { location.reload(); }, 1000);
                    window.location.href = '../';
                } else if (res.hasOwnProperty('error')) {
                    $('.signup-form').prepend('<div class="alert alert-danger">' + res.error + '</div>');
                }

            }
        });
    });

    $('#changePassword2').submit(function (e) {
        e.preventDefault();
        var password = $('.password').val();
        var password1 = $('.newpassword').val();
        var password2 = $('.renewpassword').val();

        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        // set csrf header
        $.ajaxSetup({
            beforeSend: function (e, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    e.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $.ajax({
            url: "changepassword",
            method: "POST",
            data: { pass: password, pass1: password1, pass2: password2 },
            dataType: 'json',
            success: function (response) {
                $('.alert').hide();
                //console.log(response);
                var res = response;
                if (res.hasOwnProperty('success')) {
                    $('#changePassword2').prepend('<div class="alert alert-success">password changed successfully</div>');
                    setTimeout(function () { location.reload(); }, 1000);
                    window.location.href = '../';
                } else if (res.hasOwnProperty('error')) {
                    $('#changePassword2').prepend('<div class="alert alert-danger">' + res.error + '</div>');
                }

            }
        });
    });
});