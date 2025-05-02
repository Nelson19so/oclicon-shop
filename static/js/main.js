"use strict";

document.addEventListener("DOMContentLoaded", function () {
  // navbar scroll fixed effect
  const navbar = document.querySelector(".Middle_Nav__");
  const scrollThreshold = window.innerHeight * 0.4; // 30% of viewport height

  window.addEventListener("scroll", function () {
    if (window.scrollY > scrollThreshold) {
      navbar.classList.add("fixed-navbar"); // Add class when scrolling past 30%
    } else {
      navbar.classList.remove("fixed-navbar"); // Remove class when scrolling back up
    }
  });

  // dropdown handler
  const dropHolder = document.querySelectorAll(".container-drop-down-top-nav");
  const dropHolder1 = document.querySelectorAll(
    ".container-drop-down-top-nav-1"
  );

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
});
