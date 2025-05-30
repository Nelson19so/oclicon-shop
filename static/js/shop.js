"use strict";

document.addEventListener("DOMContentLoaded", function () {
  // Sub total for cart items
  const cartProductPrice = document.querySelectorAll("#cart-product-price");
  const displayPrice = document.querySelectorAll(".total-sum");
  const numberOfProduct = document.querySelectorAll("#numberOfProduct");
  const Product = document.querySelectorAll(
    ".container-cart-product-container"
  );

  // let sum = 0;

  // // summing all cart product prices
  // cartProductPrice.forEach((cartPrices) => {
  //   sum += Number(cartPrices.textContent);
  //   return sum;
  // });

  // // displaying cart prices to the html
  // displayPrice.forEach((totalPrice) => {
  //   totalPrice.textContent = sum;
  // });

  // calculating number of cart product
  numberOfProduct.forEach((products) => {
    products.textContent = `(0${Product.length})`;
  });

  // increment and decrement btn for product quantity
  document.querySelectorAll(".container-product-amount").forEach((wrapper) => {
    const decrementBtn = wrapper.querySelector(".btn-decrement");
    const incrementBtn = wrapper.querySelector(".btn-increment");
    const input = wrapper.querySelector(".input-number");

    // Optional: Get the parent product element and ID
    const productElement = wrapper.closest(".product");
    const productId = productElement?.dataset?.productId;

    // Increase quantity
    incrementBtn.addEventListener("click", (e) => {
      e.preventDefault();
      let quantity = parseInt(input.value) || 1;
      input.value = quantity + 1;
      console.log(
        `Product ID ${productId}: Quantity increased to ${input.value}`
      );
    });

    // Decrease quantity
    decrementBtn.addEventListener("click", (e) => {
      e.preventDefault();
      let quantity = parseInt(input.value) || 1;
      if (quantity > 1) {
        input.value = quantity - 1;
        console.log(
          `Product ID ${productId}: Quantity decreased to ${input.value}`
        );
      }
    });
  });

  // show image for product details
  const mainView = document.getElementById("product-view");
  const productImgSelect = document.querySelectorAll("#product-img-Select");

  // document
  //   .getElementById(".container-imgs-product-details-list")
  //   .firstChild.classList.add("img-list-container-activate");

  productImgSelect.forEach((otherContainer) => {
    if (otherContainer.classList.contains("img-list-container-activate")) {
      otherContainer.classList.remove("img-list-container-activate"); // removing class from the image box not being clicked
    }
  });

  // event listener to display image
  productImgSelect.forEach((ImgSelect) => {
    ImgSelect.addEventListener("click", () => {
      const mainSelectImg = ImgSelect.querySelector("img");
      const mainViewImg = mainView.querySelector("img");

      mainViewImg.src = mainSelectImg.src;

      // other img container not being clicked
      productImgSelect.forEach((otherContainer) => {
        if (otherContainer.classList.contains("img-list-container-activate")) {
          otherContainer.classList.remove("img-list-container-activate"); // removing class from the image box not being clicked
        }
      });

      // adding a class to the none clicked img
      ImgSelect.classList.add("img-list-container-activate");
    });
  });
});

// search for shop
// const shopSearchInputForm = document.getElementById("search-shop-form");
// const shopSearchInput = document.getElementById("search-shop");

// shopSearchInput.addEventListener("input", function () {
//   shopSearchInputForm.submit();
// });
