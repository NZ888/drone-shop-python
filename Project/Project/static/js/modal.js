const loginBtn = document.getElementById("login")
const registerDiv = document.getElementById("register_div")
const verifyDiv = document.getElementById("verify_div")
const loginDiv = document.getElementById("login_div")
const registerBtn = document.getElementById("render_register")
const login = document.getElementById("render_login")
const verifyBtn = document.getElementById("render_verify")
const registerForm = document.getElementById("register_form")

function showLogin() {
    loginDiv.style.display = "flex"
    loginDiv.style.zIndex = "1000"
    registerDiv.style.display = "none"
    verifyDiv.style.display = "none"
}
function showRegister() {
    registerDiv.style.display = "flex"
    registerDiv.style.zIndex = "1000"
    loginDiv.style.display = "none"
    verifyDiv.style.display = "none"
}
function showVerify() {
    verifyDiv.style.display = "flex"
    verifyDiv.style.zIndex = "1000"
    registerDiv.style.display = "none"
    loginDiv.style.display = "none"
}

loginBtn.addEventListener("click", ()=>{
    showLogin()
})
registerBtn.addEventListener("click", ()=>{
    showRegister()
})
login.addEventListener("click", ()=>{
    showLogin()  
})
registerForm.addEventListener("submit", async(e)=>{
    e.preventDefault()
    const formData = new FormData(registerForm)
    const res = await fetch("/register", {
        method: "post",
        body: formData
    })
    const data = await res.json()
    if(data.message === "Successfully"){
        showVerify()
    }
    else{
        throw new Error("not found")
    }
})