const loginBtn = document.getElementById("login")

const modalBg = document.getElementById("modal_bg")

const registerDiv = document.getElementById("register_div")
const verifyDiv = document.getElementById("verify_div")
const loginDiv = document.getElementById("login_div")

const registerBtn = document.getElementById("render_register")
const loginTab = document.getElementById("render_login")
const loginFromRegister = document.getElementById("render_login_from_register")

const registerForm = document.getElementById("register_form")

const closeBtns = document.querySelectorAll(".modal-close")
const cancelBtns = document.querySelectorAll(".modal-cancel")

function closeModal() {
    modalBg.classList.remove("active")

    loginDiv.classList.remove("active")
    registerDiv.classList.remove("active")
    verifyDiv.classList.remove("active")
}

function showLogin() {
    modalBg.classList.add("active")

    loginDiv.classList.add("active")
    registerDiv.classList.remove("active")
    verifyDiv.classList.remove("active")
}

function showRegister() {
    modalBg.classList.add("active")

    registerDiv.classList.add("active")
    loginDiv.classList.remove("active")
    verifyDiv.classList.remove("active")
}

function showVerify() {
    modalBg.classList.add("active")

    verifyDiv.classList.add("active")
    registerDiv.classList.remove("active")
    loginDiv.classList.remove("active")
}

if (loginBtn) {
    loginBtn.addEventListener("click", () => {
        showLogin()
    })
}

if (registerBtn) {
    registerBtn.addEventListener("click", () => {
        showRegister()
    })
}

if (loginTab) {
    loginTab.addEventListener("click", () => {
        showLogin()
    })
}

if (loginFromRegister) {
    loginFromRegister.addEventListener("click", () => {
        showLogin()
    })
}

closeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
        closeModal()
    })
})

cancelBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
        closeModal()
    })
})

modalBg.addEventListener("click", () => {
    closeModal()
})

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closeModal()
    }
})

if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault()

        const formData = new FormData(registerForm)

        const res = await fetch("/register", {
            method: "POST",
            body: formData
        })

        const data = await res.json()

        if (data.message === "Successfully") {
            showVerify()
        } else {
            console.log(data)
        }
    })
}