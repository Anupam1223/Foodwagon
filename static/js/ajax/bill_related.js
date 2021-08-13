$(document).ready(function () {
    $("#order-table").on('click', 'tr', function () {
        var id = $(this).find("td:first-child").text();
        console.log(id);
        $(this).toggleClass("select");
        $.ajax({
            url: '../view_bill',
            method: 'GET',
            data: { id: id },
            success: function (result) {
                var vat_amount = result.vat_amount;
                var vat = result.vat;
                var service_charge = result.service_charge;
                var subtotal = result.subtotal;
                var product = result.product;
                var trader = result.trader;
                var total = result.total;
                var to_pay = "£" + result.to_pay;
                var invoice_data = jQuery.parseJSON(result.invoice_data);
                var invoice = jQuery.parseJSON(result.invoice);
                var count = 0
                const price = []
                const quantity = []

                console.log(invoice)

                $.each(invoice_data, function (key, value) {
                    oid = value.pk
                    date = value.fields.date_of_order
                    day = value.fields.day
                    address = value.fields.address
                    streetaddress = value.fields.streetaddress
                    region = value.fields.region
                });

                $(".js-open-modal").trigger("click");
                $("#total").html(to_pay).show();
                $("#streetaddress").html(streetaddress).show();
                $("#address").html(address).show();
                $("#region").html(region).show();
                $("#oid").html(oid).show();
                $("#date").html(date).show();
                $("#day").html(day).show();

                $.each(invoice, function (key, value) {
                    price.push(value.fields.price)
                    quantity.push(value.fields.quantity)
                });

                for (let i = 0; i < invoice.length; i++) {
                    count = count + 1;
                    document.getElementById("toreplace").innerHTML = `
                    <div class="text-95 text-secondary-d3">
                        <div class="row mb-2 mb-sm-0 py-25">
                            <div class="d-none d-sm-block col-1 linkcolor">`+ count + `</div>
                            <div class="col-5 col-sm-3 linkcolor" id="desc">`+ product[i] + `</div>
                            <div class="d-none d-sm-block col-1 col-sm-2 linkcolor">`+ trader[i] + `
                            </div>
                            <div class="d-none d-sm-block col-2 linkcolor" id="qty">`+ quantity[i] + `</div>
                            <div class="d-none d-sm-block col-2 text-95 linkcolor" id="uprice">`+ price[i] + `</div>
                            <div class="col-2 text-secondary-d2 linkcolor" id="amt">
                            `+ total[i] + `
                            </div>
                            <br />
                            <br>
                            <div class="col-12 col-sm-12 text-grey text-90 order-first order-sm-last">
                                <div class="row my-2">
                                <div class="col-10 text-right linkcolor">
                                    VAT(`+ vat[i] + ` %):
                                </div>
                                <div class="col-2">
                                    <span class="text-110 text-secondary-d1 linkcolor" id="vat">£ `+ vat_amount[i] + `
                                    </span>
                                </div>
                                </div>

                                <div class="row my-2">
                                <div class="col-10 text-right linkcolor">
                                    Service Charge:
                                </div>
                                <div class="col-2">
                                    <span class="text-110 text-secondary-d1 linkcolor" id="service">£ `+ service_charge[i] + `
                                    </span>
                                </div>
                                </div>
                                <div class="row my-2">
                                <div class="col-10 text-right linkcolor">
                                    Subtotal
                                </div>
                                <div class="col-2">
                                    <span class="text-110 text-secondary-d1 linkcolor" id="subtotal">£ `+ subtotal[i] + `
                                    </span>
                                </div>
                                </div>
                        </div>
                    </div>
                    <hr class="row brc-default-l1 mx-n1 mb-4" />

                  </div>`;
                }

            }
        });
    });
});