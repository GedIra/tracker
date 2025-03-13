const usernameField = document.querySelector("#usernameField");
const passwordField = document.querySelector("#passwordField");
const loginBtn = document.querySelector(".login-btn");

let usernameBtn = true;
let passwordBtn = true;

console.log("Amen")

const toggleLoginBtn = () => {
    if (!usernameBtn && !passwordBtn){
        loginBtn.removeAttribute("disabled");
    }
    else{
        loginBtn.setAttribute('disabled', 'true');
    }
}

usernameField.addEventListener('keyup', (e) => {
    const usernameFieldValue = e.target.value;
    if (usernameFieldValue.length > 0){
        usernameBtn = false;
    }else{
        usernameBtn = true;
    }
    toggleLoginBtn();
})

passwordField.addEventListener('keyup', (e) => {
    const passwordFieldValue = e.target.value
    if (passwordFieldValue.length > 0){
        passwordBtn = false;
    }
    else{
        passwordBtn = true;
    }
    toggleLoginBtn();
})

