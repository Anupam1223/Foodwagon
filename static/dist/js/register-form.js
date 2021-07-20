
$(document).ready(function () {
  $(".input").focus(function () {
    $(this).parent().find(".label-txt").addClass("label-active");
  });

  $(".input").focusout(function () {
    if ($(this).val() == "") {
      $(this).parent().find(".label-txt").removeClass("label-active");
    }
  });
});

const togglePassword = document.querySelector(".togglePassword");
const password = document.querySelector(".password");
togglePassword.addEventListener("click", function (e) {
  // toggle the type attribute
  const type =
    password.getAttribute("type") === "password" ? "text" : "password";

  password.setAttribute("type", type);
  // toggle the eye slash icon
  this.classList.toggle("fa-eye-slash");
});
