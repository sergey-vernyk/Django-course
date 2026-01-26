import getCookie from "../js/getCsrfToken.js"

$(document).ready(() => {
    const csrfToken = getCookie("csrftoken");
    const addToCartUrl = $(".add-to-cart").data("url");
    const removeFromCartUrl = $(".remove-from-cart").data("url");

    const updateCart = (url, productId) => {
        $.ajax({
            url: url,
            method: "POST",
            data: {
                product_id: productId,
                csrfmiddlewaretoken: csrfToken,
            },
            success: function(response) {
                $("#cart-count").text(response.cart_count);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(textStatus, errorThrown);
            }
        })
    }

    $(".add-to-cart").click(function() {
        updateCart(addToCartUrl, $(this).data("id"));
    });

    $(".remove-from-cart").click(function() {
        updateCart(removeFromCartUrl, $(this).data("id"));
    });
})