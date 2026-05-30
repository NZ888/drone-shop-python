import { addToCart } from "../../../cart/static/js/countProducts.js"

const addButton = document.querySelector(".addButton")
const countProduct = document.querySelector(".renderCount")

if (addButton) {
    addButton.addEventListener("click", async () => {
        const result = await addToCart(addButton.value)

        if (countProduct) {
            countProduct.textContent = result
        }
    })
}