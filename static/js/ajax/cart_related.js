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
    $('#checkoutform').click(function (e) {
        e.preventDefault();

        var clicks = 0;
        function linkClick() {
            document.getElementById('checkoutform').value = ++clicks;
        }

        console.log(clicks);

        var cartRows = document.getElementsByClassName("cart-border");

        total = 0
        total_quantity = 0
        const quan = [];
        const pric = [];
        const proid = [];

        for (var i = 0; i < cartRows.length; i++) {
            var cartRow = cartRows[i]
            var priceElement = cartRow.getElementsByClassName('cart-price')[0]
            var quantityElement = cartRow.getElementsByClassName('item-qty')[0]

            var product = cartRow.getElementsByClassName('productid')[0]
            proid.push(product.getAttribute('data-id'))

            var price = parseFloat(priceElement.innerText.replace('$', ''))
            pric.push(price)

            var quantity = quantityElement.value
            quan.push(quantity)

            total = total + (price * quantity)
            var total_quantity = total_quantity + parseInt(quantity)
        }

        $.ajax({
            url: 'actions.php',
            method: 'POST',
            data: {
                price: pric,
                quantity: quan,
                product: proid,
                totalprice: total,
            },
            dataType: 'json',
            success: function (response) {
                $('.alert').hide();
                // console.log("response");
                var res = response;
                if (res.hasOwnProperty('success')) {
                    $('.card').append('<div class="alert alert-success mt-3">Cart Saved</div>');
                    setTimeout(function () { location.reload(); }, 1000);
                    window.location.href = 'after-checkout.php';
                } else if (res.hasOwnProperty('error')) {
                    $('.card').append('<div class="alert alert-danger mt-3">' + res.error + '</div>');
                }

            }
        });
    });
});