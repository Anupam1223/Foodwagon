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
        var collectionday = $('.collectionday').find(":checked").val();
        var address = $('.address').val();
        var streetaddress = $('.streetaddress').val();
        var region = $('.region').val();
        var postal = $('.postal').val();
        var country = $('.country').val();

        var clicks = 0;
        function linkClick() {
            document.getElementById('checkoutform').value = ++clicks;
        }

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
            proid.push(product.value)

            var price = parseFloat(priceElement.innerText.replace('$', ''))
            pric.push(price)

            var quantity = quantityElement.value
            quan.push(quantity)

            total = total + (price * quantity)
        }

        //csrf safe code settings-----------------------------------------
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
        //csrf settings closed--------------------------------------------

        $.ajax({
            url: '../../add_to_order/',
            method: 'POST',
            data: {
                price: pric,
                quantity: quan,
                product: proid,
                totalprice: total,
                collectionday: collectionday,
                address: address,
                streetaddress: streetaddress,
                region: region,
                postal: postal,
                country: country,
            },
            dataType: 'json',
            success: function (response) {
                $('.alert').hide();

                var res = response;
                if (res.hasOwnProperty('success')) {
                    $('.show_error').append('<div class="alert alert-success mt-3">Order placed successfully</div>');
                    setTimeout(function () { location.reload(); }, 1000);
                    //window.location.href = 'after-checkout.php';
                } else if (res.hasOwnProperty('error')) {
                    $('.show_error').append('<div class="alert alert-danger mt-3">' + res.error + '</div>');
                }

            }
        });
    });
});