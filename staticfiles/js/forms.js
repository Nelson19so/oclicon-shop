const minInputQuantity = 4; // minimum characters for validation

// Real-time validation
const inputContainers = document.querySelectorAll(".input-container");

inputContainers.forEach((allContainers) => {
  const input = allContainers.querySelector("input");
  const allMessage = allContainers.querySelector(".error-msg");

  input.addEventListener("input", function () {
    if (!this.value.length) {
      this.classList.add("wrong_input_field");
      allMessage.textContent = "This field is required";
    } else if (this.value.length <= minInputQuantity) {
      // this.classList.remove("correct_input_field");
      this.classList.add("wrong_input_field");
      allMessage.textContent =
        "field should be more than 4 characters in length*";
      loginServerMsg.textContent = "";
    } else {
      this.classList.remove("wrong_input_field");
      // this.classList.add("correct_input_field");
      allMessage.textContent = "";
      loginServerMsg.textContent = "";
    }
  });

  input.onclick = function () {
    if (!this.value.length) {
      // this.classList.remove("correct_input_field");
      this.classList.add("wrong_input_field");
      allMessage.textContent = "This field is required";
    } else if (this.value.length <= minInputQuantity) {
      this.classList.add("wrong_input_field");
      allMessage.textContent =
        "field should be more than 4 characters in length*";
    } else {
      this.classList.remove("wrong_input_field");
      // this.classList.add("correct_input_field");
      allMessage.textContent = "";
    }
  };
});

// password show
const loginForm = document.querySelector(".login_form");
const LoginPassword = loginForm.querySelector("#password");
const toggleLoginPassword = loginForm.querySelector("#login-svg-eye");

toggleLoginPassword.addEventListener("click", () => {
  if (LoginPassword.type === "password") {
    LoginPassword.type = "text";
  } else {
    LoginPassword.type = "password";
  }
});
