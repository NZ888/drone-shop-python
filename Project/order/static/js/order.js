import { addToCart, deleteInCart } from "../../../cart/static/js/countProducts.js"

const select = document.getElementById("warehouse")
const cityInput = document.getElementById("cityName")
const modalForDelivery = document.getElementById("modal_for_delivery")
const radioBtns = document.querySelectorAll("input[name='delivery']")

const modalBg = document.getElementById("order_product_modal_bg")
const productModal = document.getElementById("order_product_modal")
const closeProductModal = document.getElementById("close_order_product_modal")
const cancelProductModal = document.getElementById("cancel_order_product_modal")
const saveProductModal = document.getElementById("save_order_product_modal")
const modalProductName = document.getElementById("order_product_modal_name")
const modalProductCount = document.getElementById("order_product_count")
const modalProductPrice = document.getElementById("order_product_price")
const modalProductOptions = document.getElementById("order_product_options")

let currentProduct = null

radioBtns.forEach((btn) => {
    btn.addEventListener("change", async () => {
        modalForDelivery.style.display = "block"

        if (cityInput.value.trim()) {
            await updateWarehouses()
        }
    })
})

async function getWarehouses(cityName, type) {
    const response = await fetch(`/order/${cityName}?type=${type}`)
    const result = await response.json()
    return result.warehouses
}

cityInput.addEventListener("change", async () => {
    await updateWarehouses()
})

async function updateWarehouses() {
    const city = cityInput.value.trim()
    const deliveryType = document.querySelector("input[name='delivery']:checked")?.value

    if (!city || !deliveryType) {
        return
    }

    const warehouses = await getWarehouses(city, deliveryType)

    select.options.length = 0

    if (warehouses.length === 0) {
        const option = document.createElement("option")
        option.textContent = "Нічого не знайдено"
        option.value = ""
        select.appendChild(option)
        return
    }

    warehouses.forEach((warehouse) => {
        const option = document.createElement("option")
        option.textContent = warehouse
        option.value = warehouse
        select.appendChild(option)
    })
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

    oldTotalPriceElement.textContent = formatPrice(oldTotal)
    totalPriceElement.textContent = formatPrice(total)
    savedPriceElement.textContent = formatPrice(oldTotal - total)
}

function openProductModal(product) {
    currentProduct = product

    modalProductName.textContent = product.dataset.productName
    modalProductCount.value = product.querySelector(".renderCount").textContent
    modalProductPrice.value = parsePrice(product.dataset.price)
    modalProductOptions.value = product.dataset.options || ""

    modalBg.classList.add("active")
    productModal.classList.add("active")
    productModal.setAttribute("aria-hidden", "false")
}

function closeModal() {
    modalBg.classList.remove("active")
    productModal.classList.remove("active")
    productModal.setAttribute("aria-hidden", "true")
    currentProduct = null
}

async function saveProductChanges() {
    if (!currentProduct) {
        return
    }

    const productId = currentProduct.dataset.productId
    const countElement = currentProduct.querySelector(".renderCount")
    const oldCount = Number(countElement.textContent)
    const newCount = Math.max(Number(modalProductCount.value), 1)
    const price = Math.max(Number(modalProductPrice.value), 0)

    if (newCount > oldCount) {
        for (let index = oldCount; index < newCount; index++) {
            await addToCart(productId)
        }
    }

    if (newCount < oldCount) {
        for (let index = oldCount; index > newCount; index--) {
            await deleteInCart(productId)
        }
    }

    countElement.textContent = newCount
    currentProduct.dataset.price = price
    currentProduct.dataset.options = modalProductOptions.value
    currentProduct.querySelector(".price").textContent = `${formatPrice(price)} ₴`

    updateCartSummary()
    closeModal()
}

document.querySelectorAll(".edit-order-product").forEach((button) => {
    button.addEventListener("click", () => {
        openProductModal(button.closest(".cart-product"))
    })
})

closeProductModal.addEventListener("click", closeModal)
cancelProductModal.addEventListener("click", closeModal)
modalBg.addEventListener("click", closeModal)
saveProductModal.addEventListener("click", saveProductChanges)

window.addEventListener("DOMContentLoaded", () => {
    updateCartSummary()
})
