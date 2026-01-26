import getCookie from "../js/getCsrfToken.js";

$(document).ready(() => {
    $(".star").click(function () {
        const rating = $(this).data("value");
        const productId = $(this).closest(".rating").data("id");
        const url = $(this).data("url");
        const csrfToken = getCookie("csrftoken");

        $.ajax({
            url: url,
            method: "POST",
            data: {
                product_id: productId,
                rating: rating,
                csrfmiddlewaretoken: csrfToken,
            },
            success: function (response) {
                const ratingBlock = $(`.rating[data-id="${productId}"]`);
                ratingBlock.find(".avg-rating").text(response.new_rating);
                ratingBlock.find(".rating-count").text(`(${response.rating_count})`);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(textStatus, errorThrown);
            }
        });
    });
});