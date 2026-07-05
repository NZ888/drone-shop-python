import { addToCart } from "../../../cart/static/js/countProducts.js"

const cartButton = document.querySelector(".product-cart-btn")

if (cartButton) {
    cartButton.addEventListener("click", async () => {
        await addToCart(cartButton.value)

        if (window.loadCartModal) {
            window.loadCartModal()
        } else {
            window.location.href = "/cart/"
        }
    })
}
