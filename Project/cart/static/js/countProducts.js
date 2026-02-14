import { addToCart, deleteInCart } from "./cart.js"

(
    async () => {
        const response = await fetch("/count_products/")
        const data = await response.json()
        const countElement = document.getElementById("count")
        if (countElement) {
            countElement.textContent = data.productsCount
        }
    }
)()

const addButtons = document.querySelectorAll(".addButton")
addButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        const result = await addToCart(button.value)
        const container = button.closest(".product_container")
        const countProduct = container.querySelector(".renderCount")
        if (countProduct) {
            countProduct.textContent = result
        }
    })
})

const deleteButtons = document.querySelectorAll(".deleteButton")
deleteButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        const result = await deleteInCart(button.value)
        const container = button.closest(".product_container")
        const countProduct = container.querySelector(".renderCount")
        if (countProduct) {
            countProduct.textContent = result
        }
    })
})
