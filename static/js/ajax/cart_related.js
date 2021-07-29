$(document).ready(function () {

    $('.add-to-cart').click(function (e) {
        e.preventDefault();
        var p_id = $(this).attr('data-id');
        console.log(p_id);
        $.ajax({
            url: 'add_to_cart/',
            method: 'GET',
            data: {
                addCart: p_id
            },
            success: function (data) {

                if (data.hasOwnProperty('error')) {
                    window.location.href = '../login';
                }
                else if (data.hasOwnProperty('sucess')) {
                    $('.showcart').load(' .cart', function () {
                        $('#item-holder').append('<h5 style="color:#ffb30e; margin:0; padding:0; font-size: 0.8rem; ">' + data.sucess + '</h5>');
                        //document.getElementById("item-holder").innerHTML = data.sucess;
                    });
                }

            }
        });
    });

});