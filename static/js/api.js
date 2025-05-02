// add product to comparison
$(document).ready(function () {
  $(".add-to-compare").click(function () {
    const productId = $(this).data("product-id");

    $ajax({
      url: `/compare/add/${productId}/`,
      success: function (data) {
        $("compare-count").text(data.count);
        showToast("Item added to comparison");
      },
    });
  });
});

// remove product from comparison
$(document).ready(function () {
  $(".remove-from-compare").click(function () {
    const productId = $(this).data("product-id");

    $ajax({
      url: `/compare/remove/${productId}/`,
      success: function (data) {
        location.reload();
      },
    });
  });
});

function showToast(message) {
  // toast notification here
}
