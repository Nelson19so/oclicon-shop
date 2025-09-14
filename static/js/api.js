// Get CSRF token from meta tag
function getCSRFToken() {
  return document
    .querySelector('meta[name="csrf-token"]')
    ?.getAttribute("content");
}

// add product to comparison
$(document).ready(function () {
  $(".add-to-compare").click(function () {
    const productId = $(this).data("product-id");

    $.ajax({
      url: `/home/compare/add/${productId}/`,
      type: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },

      // if the process went successful
      success: function (data) {
        $(".compare-count").text(data.count);
        showToast("Item added to comparison");
      },

      // if the process didn't go successful
      error: function (xhr, status, error) {
        console.error("AJAX Error →", {
          status: xhr.status,
          message: error,
          response: xhr.responseText,
        });
      },
    });
  });
});

// remove product from comparison
$(document).ready(function () {
  $(".remove-from-compare").click(function () {
    const productId = $(this).data("product-id");

    $.ajax({
      url: `/home/compare/add/${productId}/`,
      type: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
      // if the data is successfully deleted
      success: function (data) {
        // reload the page to reflect data
        // location.reload();

        // display message from the server to th UI
        showToast("Item removed from comparison");
      },

      error: function (xhr, status, error) {
        console.error("AJAX Error →", {
          status: xhr.status,
          message: error,
          response: xhr.responseText,
        });
      },
    });
  });
});

// add product to wishlist ---
$(document).ready(function () {
  $(".add-to-wishlist").click(function () {
    const productId = $(this).data("product-id");

    $.ajax({
      url: `/home/wishlist/add/${productId}/`,
      type: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },

      // if the process went successful
      success: function (data) {
        $(".compare-count").text(data.count);
        showToast("Item added to wishlist");
      },

      // if the process didn't go successful
      error: function (xhr, status, error) {
        console.error("AJAX Error →", {
          status: xhr.status,
          message: error,
          response: xhr.responseText,
        });
      },
    });
  });
});

// removing product from wishlist
$(document).ready(function () {
  $(".remove-from-wishlist").click(function () {
    const productId = $(this).data("product-id");

    $.ajax({
      url: `/home/wishlist/remove/${productId}/`,
      type: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },

      // if the process went successful
      success: function (data) {
        $(".compare-count").text(data.count);
        showToast("Item added to wishlist");
        location.reload();
      },

      // if the process didn't go successful
      error: function (xhr, status, error) {
        console.error("AJAX Error →", {
          status: xhr.status,
          message: error,
          response: xhr.responseText,
        });
      },
    });
  });
});

// creating or adding product to cart list ---
$(document).ready(function () {
  $("#add-to-cart_btn").click(function () {
    const productId = $(this).data("product-id");
    const productQuantity = $("#quantity-input").val();
    const memory = $("#memory").val();
    const size = $("#size").val();
    const storage = $("#storage").val();

    $.ajax({
      url: `/home/cart/add/${productId}/`,
      type: "POST",
      data: {
        product_quantity: productQuantity,
        size: size,
        storage: storage,
        memory: memory,
      },
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },

      // if the process went successful
      success: function (data) {
        showToast("Item added to cart list");
      },

      // if the process didn't go successful
      error: function (xhr, status, error) {
        console.error("AJAX Error →", {
          status: xhr.status,
          message: error,
          response: xhr.responseText,
        });
      },
    });
  });
});

// removing product from cart list ---
$(document).ready(function () {
  $("#remove-cart_btn").click(function () {
    const productId = $(this).data("product-id");

    $.ajax({
      url: `/home/cart/remove/${productId}/`,
      type: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },

      // if the process went successful
      success: function (data) {
        window.location.reload();
        showToast("Item removed from cart list");
      },

      // if the process didn't go successful
      error: function (xhr, status, error) {
        console.error("AJAX Error →", {
          status: xhr.status,
          message: error,
          response: xhr.responseText,
        });
      },
    });
  });
});

// filters home page computer accessories
$(document).ready(function () {
  $(".computer_acc_category_child").click(function () {
    const category_child = $(this).data("category_child");
    $.ajax({
      url: "/home/",
      type: "GET",
      data: {
        category_child: category_child,
      },
      success: function (response) {
        $("#computer-accessories-products").html(response.html);
      },
      error: function (xhr, status, error) {
        console.error("AJAX Error →", {
          status: xhr.status,
          message: error,
          response: xhr.responseText,
        });
      },
    });
  });
});

// toast config for dynamic changes and update

const toast = document.getElementById("toast");
// toast.classList.add("disabled");

function showToast(message) {
  if (toast.classList.contains("disabled")) {
    toast.classList.remove("disabled");
    document.getElementById("toast_msg").textContent = message;

    setTimeout(() => {
      closeToast();
    }, 7000); // seconds to collapse the toast
  }
}

function closeToast() {
  toast.classList.add("disabled");
}

// showToast("Item added to comparison successfully");
