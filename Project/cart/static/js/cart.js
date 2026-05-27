import { addToCart } from "./countProducts.js"
import { deleteInCart } from "./countProducts.js"

function parsePrice(price) {
    if (!price) {
        return 0
    }

    return Number(String(price).replace("₴", "").replace(/\s/g, "").replace(",", "."))
}

function formatPrice(price) {
    return Math.round(price).toLocaleString("uk-UA")
}

function updateCartSummary() {
    const products = document.querySelectorAll(".cart-product")

    const oldTotalPriceElement = document.getElementById("old_total_price")
    const totalPriceElement = document.getElementById("total_price")
    const savedPriceElement = document.getElementById("saved_price")

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

function checkEmptyCart() {
    const products = document.querySelectorAll(".cart-product")

    if (products.length === 0) {
        window.location.reload()
    }
}

const addButtons = document.querySelectorAll(".addButton")

addButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        const result = await addToCart(button.value)

        const container = button.closest(".cart-product")
        const countProduct = container.querySelector(".renderCount")

        countProduct.textContent = result

        updateCartSummary()
    })
})

const deleteButtons = document.querySelectorAll(".deleteButton")

deleteButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        const result = await deleteInCart(button.value)

        const container = button.closest(".cart-product")
        const countProduct = container.querySelector(".renderCount")

        if (result <= 0) {
            container.remove()
            checkEmptyCart()
            return
        }

        countProduct.textContent = result

        updateCartSummary()
    })
})

const removeButtons = document.querySelectorAll(".remove-product")

removeButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        const container = button.closest(".cart-product")
        const countProduct = container.querySelector(".renderCount")

        let count = Number(countProduct.textContent)

        while (count > 0) {
            count = await deleteInCart(button.value)
        }

        container.remove()

        updateCartSummary()
        checkEmptyCart()
    })
})

window.addEventListener("DOMContentLoaded", () => {
    updateCartSummary()
})