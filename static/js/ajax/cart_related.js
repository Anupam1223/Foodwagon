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

    $('.item-qty').change(function () {
        var cartRows = document.getElementsByClassName("cart-border");
        total_price = 0;
        for (var i = 0; i < cartRows.length; i++) {

            total = 0
            total_quantity = 0
            var cartRow = cartRows[i]
            var priceElement = cartRow.getElementsByClassName('cart-price')[0]
            var quantityElement = cartRow.getElementsByClassName('item-qty')[0]
            var price = parseFloat(priceElement.innerText.replace('$', ''))
            var quantity = quantityElement.value
            total_price += (price * quantity)
        }

        document.getElementById("total_price").innerHTML = "&nbsp;" + total_price;
    });
});