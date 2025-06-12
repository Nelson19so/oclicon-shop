"use strict";

document.addEventListener("DOMContentLoaded", function () {
  const modal = document.querySelector(".web-model");

  const toggleModal = () => modal.classList.toggle("active");

  modal.addEventListener("click", () => {
    if (sidebar.classList.contains("active")) {
      sidebar.classList.remove("active");
    }
    toggleModal();
  });

  // handle sidebar
  const displaySidebar = document.getElementById("display-sidebar");
  const sidebar = document.getElementById("page-sidebar");
  const closeSidebar = document.getElementById("close_navbar");

  displaySidebar.addEventListener("click", function () {
    sidebar.classList.add("active");
    toggleModal();
  });

  closeSidebar.addEventListener("click", function () {
    if (sidebar.classList.contains("active")) {
      sidebar.classList.remove("active");
      toggleModal();
    }
  });

  // navbar on scroll effect

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

// Faq_ page
const faqItem = document.querySelectorAll(".container-main-faqs--");
const otherFaq = document.querySelectorAll(".container-main-faqs--");

faqItem.forEach((faq) => {
  const faqToggle = faq.querySelector(".show-faq-description");
  const faqSubject = faq.querySelector(".faq-subject-container-");

  faqToggle.addEventListener("click", function () {
    otherFaq.forEach((otherfaqs) => {
      if (otherfaqs != faq) {
        otherfaqs.classList.remove("active-faq-container");
        otherfaqs
          .querySelector(".faq-subject-container-")
          .classList.remove("active-faq");
      } else {
        if (!faq.classList.contains(".active-faq-container")) {
          faq.classList.toggle("active-faq-container");
          faqSubject.classList.toggle("active-faq");
        }
      }
    });
  });
});
