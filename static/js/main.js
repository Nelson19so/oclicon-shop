const navLink = document.querySelectorAll("#mainLink");
const containerBrand = document.querySelectorAll(".container-menu");

navLink.forEach((navLinkItems) => {
  navLinkItems.addEventListener("mouseenter", () => {
    containerBrand.forEach((containerBrands) => {
      containerBrands.classList.add("active-brands");
    });
  });
});

navLink.forEach((navLinkItem) => {
  navLinkItem.addEventListener("mouseleave", () => {
    // if (containerBrand.classList.contains("active-brands")) {
    //   containerBrand.classList.remove("active-brands");
    // }
    containerBrand.forEach((containerBrans_) => {
      containerBrans_.classList.remove("active-brands");
    });
  });
});
