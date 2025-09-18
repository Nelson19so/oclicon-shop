document.addEventListener("DOMContentLoaded", function () {
  const minInputQuantity = 4;

  const inputContainers = document.querySelectorAll(".input-container");
  inputContainers.forEach((allContainers) => {
    const input = allContainers.querySelector("input");
    const allMessage = allContainers.querySelector(".error-msg");

    input.addEventListener("input", function () {
      if (!this.value.length) {
        this.classList.add("wrong_input_field");
        allMessage.textContent = "This field is required*";
      } else if (this.value.length <= minInputQuantity) {
        this.classList.add("wrong_input_field");
        allMessage.textContent =
          "field should be more than 4 characters in length*";
      } else {
        this.classList.remove("wrong_input_field");
        allMessage.textContent = "";
      }
    });

    input.onclick = function () {
      if (!this.value.length) {
        this.classList.add("wrong_input_field");
        allMessage.textContent = "This field is required*";
      } else if (this.value.length <= minInputQuantity) {
        this.classList.add("wrong_input_field");
        allMessage.textContent =
          "field should be more than 4 characters in length*";
      } else {
        this.classList.remove("wrong_input_field");
        allMessage.textContent = "";
      }
    };
  });

  // ✅ Handle register form (if it exists)
  const registerForm = document.querySelector("#register_form");

  if (registerForm) {
    const registerPassword1 = registerForm.querySelector("#password1");
    const toggleRegisterPassword1 =
      registerForm.querySelector("#register-svg-eye1");

    if (registerPassword1 && toggleRegisterPassword1) {
      toggleRegisterPassword1.addEventListener("click", () => {
        registerPassword1.type =
          registerPassword1.type === "password" ? "text" : "password";
      });
    }

    const registerPassword2 = registerForm.querySelector("#password2");
    const toggleRegisterPassword2 =
      registerForm.querySelector("#register-svg-eye2");

    if (registerPassword2 && toggleRegisterPassword2) {
      toggleRegisterPassword2.addEventListener("click", () => {
        registerPassword2.type =
          registerPassword2.type === "password" ? "text" : "password";
      });
    }
  }

  // ✅ Handle login form (if it exists)
  const loginForm = document.querySelector("#login_form");
  if (loginForm) {
    const loginPassword = loginForm.querySelector("#password");
    const toggleLoginPassword = loginForm.querySelector("#login-svg-eye");

    if (loginPassword && toggleLoginPassword) {
      toggleLoginPassword.addEventListener("click", () => {
        loginPassword.type =
          loginPassword.type === "password" ? "text" : "password";
      });
    }
  }
});
