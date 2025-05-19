// add product to comparison
$(document).ready(function () {
  $(".add-to-compare").click(function () {
    const productId = $(this).data("product-id");

    $.ajax({
      url: `/compare/add/${productId}/`,
      type: "GET",
      // if the data is successfully added to comparison
      success: function (data) {
        // shows the new compare count in the page
        $("compare-count").text(data.count);
        // displays toast for is successfully added
        showToast("Item added to comparison");
      },
    });
  });
});

// remove product from comparison
$(document).ready(function () {
  $(".remove-from-compare").click(function () {
    const productId = $(this).data("product-id");

    $.ajax({
      url: `/compare/remove/${productId}/`,
      type: "GET",
      // if the data is successfully deleted
      success: function (data) {
        // reload the page to reflect data
        location.reload();
      },
    });
  });
});

function showToast(message) {
  // toast notification here
}
