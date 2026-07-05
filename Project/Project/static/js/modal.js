const loginBtn = document.getElementById("login")
const cartBtn = document.getElementById("cart_btn")

const modalBg = document.getElementById("modal_bg")

const registerDiv = document.getElementById("register_div")
const verifyDiv = document.getElementById("verify_div")
const loginDiv = document.getElementById("login_div")
const cartDiv = document.getElementById("cart_div")


function closeModal() {
    if (!modalBg) {
        return
    }

    modalBg.classList.remove("active")

    loginDiv?.classList.remove("active")
    registerDiv?.classList.remove("active")
    verifyDiv?.classList.remove("active")
    cartDiv?.classList.remove("active")
}


function showLogin() {
    if (!modalBg || !loginDiv) {
        return
    }

    modalBg.classList.add("active")

    loginDiv.classList.add("active")
    registerDiv?.classList.remove("active")
    verifyDiv?.classList.remove("active")
    cartDiv?.classList.remove("active")
}


function showRegister() {
    if (!modalBg || !registerDiv) {
        return
    }

    modalBg.classList.add("active")

    registerDiv.classList.add("active")
    loginDiv?.classList.remove("active")
    verifyDiv?.classList.remove("active")
    cartDiv?.classList.remove("active")
}


function showVerify() {
    if (!modalBg || !verifyDiv) {
        return
    }

    modalBg.classList.add("active")

    verifyDiv.classList.add("active")
    registerDiv?.classList.remove("active")
    loginDiv?.classList.remove("active")
    cartDiv?.classList.remove("active")
}


function showCart() {
    if (!modalBg || !cartDiv) {
        return
    }

    modalBg.classList.add("active")

    cartDiv.classList.add("active")
    loginDiv?.classList.remove("active")
    registerDiv?.classList.remove("active")
    verifyDiv?.classList.remove("active")
}


async function sendModalForm(form) {
    const formData = new FormData(form)

    const response = await fetch(form.action, {
        method: form.method,
        body: formData
    })

    const data = await response.json()

    if (data.success) {
        window.location.href = data.redirect
        return
    }

    if (data.modal === "login") {
        loginDiv.innerHTML = data.html
        showLogin()
    }

    if (data.modal === "register") {
        registerDiv.innerHTML = data.html
        showRegister()
    }

    if (data.modal === "verify") {
        verifyDiv.innerHTML = data.html
        showVerify()
    }
}


async function loadCartModal() {
    const response = await fetch("/cart/?modal=1")
    const data = await response.json()

    cartDiv.innerHTML = data.html

    showCart()
    initCartModal()
}


window.loadCartModal = loadCartModal


async function addToCartFromModal(idProduct) {
    const response = await fetch("/add-to-cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ product_id: idProduct })
    })

    const result = await response.json()

    return result.productsCount
}


async function deleteInCartFromModal(idProduct) {
    const response = await fetch("/delete_in_cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ product_id: idProduct })
    })

    const result = await response.json()

    return result.productsCount
}


function parsePrice(price) {
    if (!price) {
        return 0
    }

    return Number(String(price).replace("₴", "").replace(/\s/g, "").replace(",", "."))
}


function formatPrice(price) {
    return Math.round(price).toLocaleString("uk-UA")
}


function updateCartModalSummary() {
    const products = cartDiv.querySelectorAll(".cart-product")

    const oldTotalPriceElement = cartDiv.querySelector("#old_total_price")
    const totalPriceElement = cartDiv.querySelector("#total_price")
    const savedPriceElement = cartDiv.querySelector("#saved_price")

    if (!oldTotalPriceElement || !totalPriceElement || !savedPriceElement) {
        return
    }

    let oldTotal = 0
    let total = 0

    products.forEach((product) => {
        const count = Number(product.querySelector(".renderCount").textContent)

        const price = parsePrice(product.dataset.price)
        const oldPrice = parsePrice(product.dataset.oldPrice)

        total += price * count
        oldTotal += oldPrice * count
    })

    const saved = oldTotal - total

    oldTotalPriceElement.textContent = formatPrice(oldTotal)
    totalPriceElement.textContent = formatPrice(total)
    savedPriceElement.textContent = formatPrice(saved)
}


async function reloadCartModal() {
    const response = await fetch("/cart/?modal=1")
    const data = await response.json()

    cartDiv.innerHTML = data.html

    showCart()
    initCartModal()
}


function checkEmptyCartModal() {
    const products = cartDiv.querySelectorAll(".cart-product")

    if (products.length === 0) {
        reloadCartModal()
    }
}


function initCartModal() {
    updateCartModalSummary()

    const addButtons = cartDiv.querySelectorAll(".addButton")

    addButtons.forEach((button) => {
        button.addEventListener("click", async () => {
            const result = await addToCartFromModal(button.value)

            const container = button.closest(".cart-product")
            const countProduct = container.querySelector(".renderCount")

            countProduct.textContent = result

            updateCartModalSummary()
        })
    })

    const deleteButtons = cartDiv.querySelectorAll(".deleteButton")

    deleteButtons.forEach((button) => {
        button.addEventListener("click", async () => {
            const result = await deleteInCartFromModal(button.value)

            const container = button.closest(".cart-product")
            const countProduct = container.querySelector(".renderCount")

            if (result <= 0) {
                container.remove()

                updateCartModalSummary()
                checkEmptyCartModal()

                return
            }

            countProduct.textContent = result

            updateCartModalSummary()
        })
    })

    const removeButtons = cartDiv.querySelectorAll(".remove-product")

    removeButtons.forEach((button) => {
        button.addEventListener("click", async () => {
            const container = button.closest(".cart-product")
            const countProduct = container.querySelector(".renderCount")

            let count = Number(countProduct.textContent)

            while (count > 0) {
                count = await deleteInCartFromModal(button.value)
            }

            container.remove()

            updateCartModalSummary()
            checkEmptyCartModal()
        })
    })
}


if (loginBtn) {
    loginBtn.addEventListener("click", () => {
        showLogin()
    })
}


if (cartBtn) {
    cartBtn.addEventListener("click", (event) => {
        event.preventDefault()

        loadCartModal()
    })
}


document.addEventListener("click", (event) => {
    if (event.target.classList.contains("modal-close")) {
        closeModal()
    }

    if (event.target.classList.contains("modal-cancel")) {
        closeModal()
    }

    if (event.target.id === "render_register") {
        showRegister()
    }

    if (event.target.id === "render_login") {
        showLogin()
    }

    if (event.target.id === "render_login_from_register") {
        showLogin()
    }

    if (event.target === modalBg) {
        closeModal()
    }
})


document.addEventListener("submit", (event) => {
    const form = event.target

    if (!form.classList.contains("modal-form")) {
        return
    }

    event.preventDefault()

    sendModalForm(form)
})


document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closeModal()
    }
})


document.addEventListener("input", (event) => {
    if (!event.target.closest(".verify-inputs")) {
        return
    }

    const input = event.target

    input.value = input.value.replace(/\D/g, "")

    if (input.value.length === 1) {
        const nextInput = input.nextElementSibling

        if (nextInput) {
            nextInput.focus()
        }
    }
})


document.addEventListener("keydown", (event) => {
    if (!event.target.closest(".verify-inputs")) {
        return
    }

    const input = event.target

    if (event.key === "Backspace" && input.value === "") {
        const previousInput = input.previousElementSibling

        if (previousInput) {
            previousInput.focus()
        }
    }
})


const urlParams = new URLSearchParams(window.location.search)
const modalName = urlParams.get("modal")

if (modalName === "login") {
    showLogin()
}

if (modalName === "register") {
    showRegister()
}

if (modalName === "verify") {
    showVerify()
}

if (modalName === "cart") {
    loadCartModal()
}
