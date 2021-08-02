$(document).ready(function () {

    $('.add-to-cart').click(function (e) {
        e.preventDefault();
        var p_id = $(this).attr('data-id');
        console.log(p_id);
        $.ajax({
            url: '../../add_to_cart/',
            method: 'GET',
            data: {
                addCart: p_id
            },
            success: function (data) {

                if (data.hasOwnProperty('error')) {
                    window.location.href = '../login';
                }
                else if (data.hasOwnProperty('sucess')) {
                    location.reload();
                }

            }
        });
    });

    $('.remove-from-cart').click(function (e) {
        e.preventDefault();
        var p_id = $(this).attr('data-id');
        console.log(p_id);
        $.ajax({
            url: '../../remove_from_cart/',
            method: 'GET',
            data: {
                removeCartItem: p_id
            },
            success: function (data) {
                if (data.hasOwnProperty('error')) {
                    window.location.href = '../login';
                }
                else if (data.hasOwnProperty('sucess')) {
                    location.reload();
                }

            }
        });
    });

});