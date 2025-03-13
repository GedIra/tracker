const emailField = document.querySelector("#emailField");
const emailFieldFeedBack = document.querySelector(".taken_email");
const emailCheckMsg = document.querySelector(".emailCheckMsg");
const usernameField = document.querySelector("#usernameField");
const usernameFeedbackField = document.querySelector(".invalidfeedback");
const usernameCheckMsg = document.querySelector(".usernameCheckMsg");
const passwordHideShowButton = document.querySelector(".passwordHideShowButton");
const passwordField = document.querySelector("#passwordField");
const registerBtn = document.querySelector(".register-btn");

let email_registerBtn = true;
let username_registerBtn = true;

const togglePasswordField = () => {
    if (passwordHideShowButton.innerHTML === 'SHOW') {
        passwordHideShowButton.innerHTML = 'HIDE';
        passwordField.setAttribute("type", "text");
    } else {
        passwordHideShowButton.innerHTML = 'SHOW';
        passwordField.setAttribute("type", "password");
    }
};

const toggleRegisterButton = () => {
    if (!email_registerBtn && !username_registerBtn) {
        registerBtn.removeAttribute("disabled");
    } else {
        registerBtn.setAttribute("disabled", "true");
    }
};

emailField.addEventListener('keyup', (e) => {
    const emailFieldValue = e.target.value;
    emailField.classList.remove('is-invalid');
    emailFieldFeedBack.style.display = 'none';
    emailCheckMsg.style.display = "none";

    if (emailFieldValue.length > 0) {
        emailCheckMsg.style.display = "block";
        emailCheckMsg.innerHTML = `Checking ${emailFieldValue}`;

        fetch("/auth/register/email-auth/", {
            body: JSON.stringify({ email: emailFieldValue }),
            method: 'POST'
        })
        .then((res) => res.json())
        .then((data) => {
            emailCheckMsg.style.display = "none";

            if (data.email_error1 || data.email_error2) {
                emailField.classList.add('is-invalid');
                emailFieldFeedBack.style.display = 'block';
                emailFieldFeedBack.innerHTML = `<p>${data.email_error1 || data.email_error2}</p>`;
                email_registerBtn = true;
            } else {
                emailField.classList.remove('is-invalid');
                emailFieldFeedBack.remove('text-danger')
                emailFieldFeedBack.style.display = 'none';
                email_registerBtn = false;
            }

            toggleRegisterButton();
        });
    }
});

usernameField.addEventListener('keyup', (e) => {
    const usernameFieldValue = e.target.value;
    usernameField.classList.remove('is-invalid', 'is-valid');
    usernameCheckMsg.style.display = "none";
    usernameFeedbackField.style.display = "none";

    if (usernameFieldValue.length > 0) {
        usernameCheckMsg.style.display = 'block';
        usernameCheckMsg.innerHTML = `Checking ${usernameFieldValue}`;

        fetch("/auth/register/username-auth/", {
            body: JSON.stringify({ username: usernameFieldValue }),
            method: 'POST'
        })
        .then((res) => res.json())
        .then((data) => {
            usernameCheckMsg.style.display = "none";

            if (data.username_error) {
                usernameField.classList.add('is-invalid');
                usernameFeedbackField.classList.remove("text-success")
                usernameFeedbackField.classList.add('text-danger')
                usernameFeedbackField.style.display = "block";
                usernameFeedbackField.innerHTML = `<p> ${data.username_error} </p>`;
                username_registerBtn = true;
            } else {
                usernameField.classList.add('is-valid');
                usernameFeedbackField.classList.remove('text-danger')
                usernameFeedbackField.classList.add("text-success")
                usernameFeedbackField.style.display = "block";
                usernameFeedbackField.innerHTML = `<p> ${data.username} </p>`;
                username_registerBtn = false;
            }

            toggleRegisterButton();
        });
    }
});

passwordHideShowButton.addEventListener('click', togglePasswordField);





