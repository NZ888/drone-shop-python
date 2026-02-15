const cartLink = document.getElementById("cartLink")
const cartModal = document.getElementById("cartModal")
const cartModalBody = document.getElementById("cartModalBody")

async function loadCartModal() {
    const response = await fetch("/cart-modal/")
    const html = await response.text()
    cartModalBody.innerHTML = html
}

if (cartLink && cartModal && cartModalBody) {
    cartLink.addEventListener("click", async (event) => {
        event.preventDefault()

        const isOpen = cartModal.classList.contains("open")
        if (isOpen) {
            cartModal.classList.remove("open")
            return
        }

        await loadCartModal()
        cartModal.classList.add("open")
    })

    document.addEventListener("click", (event) => {
        if (!cartModal.contains(event.target) && !cartLink.contains(event.target)) {
            cartModal.classList.remove("open")
        }
    })
}