"use strict";

const dropHolder = document.querySelectorAll(".container-drop-down-top-nav");
const dropHolder1 = document.querySelectorAll(".container-drop-down-top-nav-1");

dropHolder.forEach((dropHolderContainer) => {
  dropHolderContainer.addEventListener("click", () => {
    dropHolderContainer
      .querySelector(".container-currency")
      .classList.toggle("display-block");
  });
});

dropHolder1.forEach((dropHolderContainer1) => {
  dropHolderContainer1.addEventListener("click", () => {
    dropHolderContainer1
      .querySelector(".container-Lang")
      .classList.toggle("display-block");
  });
});

// login dropdown
const dropContainer = document.querySelector("#container-signin-dropdown");
const dropItem = document.querySelector("#dropItem");

function dropSignInContainer() {
  dropItem.classList.toggle("display-block");
  return dropItem;
}

// drop container
dropContainer.addEventListener("click", (e) => {
  if (e.target === dropContainer) {
    dropSignInContainer();
  }
  return;
});

// Sub total for cart items
const cartProductPrice = document.querySelectorAll("#cart-product-price");
const displayPrice = document.querySelectorAll(".total-sum");
const numberOfProduct = document.querySelectorAll("#numberOfProduct");
const Product = document.querySelectorAll(".container-cart-product-container");

let sum = 0;

cartProductPrice.forEach((cartPrices) => {
  sum += Number(cartPrices.textContent);
  return sum;
});

displayPrice.forEach((totalPrice) => {
  totalPrice.textContent = sum;
});

numberOfProduct.forEach((products) => {
  products.textContent = `(0${Product.length})`;
});
