import { addToCart, deleteInCart } from "../../../cart/static/js/countProducts.js"

const categoryBtns = document.querySelectorAll(".category-btn")
const productContainer = document.getElementById("filter_products")
const paginationContainer = document.getElementById("pagination")

let selectedCategory = "all"

productContainer.addEventListener("click", (event) => {
    if (event.target.classList.contains("addButton")) {
        addToCart(event.target.value)
    }

    if (event.target.classList.contains("deleteButton")) {
        deleteInCart(event.target.value)
    }
})

async function filterProducts(page) {
    const response = await fetch("/catalog/filter", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            selectCategory: selectedCategory,
            page: page
        })
    })

    const data = await response.json()

    let html = ``

    data.filtrated_products.forEach(product => {
        const productUrl = product.slug ? `/product/${product.slug}/` : `/catalog/${product.id}/`
        const oldPrice = product.old_price ? `${product.old_price} ₴` : ""
        const oldPriceClass = product.old_price ? "old-price" : "old-price empty"

        html += `
            <div class="product">
                <a href="${productUrl}" class="product_container">
                    <img
                        src="/catalog/static/media/${product.image_url}"
                        alt="${product.name}"
                    >

                    <h1>${product.name}</h1>

                    <div class="price-container">
                        <p class="${oldPriceClass}">${oldPrice}</p>
                        <p class="price">${product.price} ₴</p>
                    </div>
                </a>
            </div>
        `
    })

    productContainer.innerHTML = html

    renderPaginate(data.pagination)
}

function renderPaginate(pagination) {
    let paginationHtml = ``

    if (pagination.has_prev) {
        paginationHtml += `
            <button class="paginationBtn" value="${pagination.prev_num}">
                <img src="/catalog/static/images/prev.png" alt="prev">
            </button>
        `
    }

    for (let page = 1; page <= pagination.total_count; page++) {
        paginationHtml += `
            <button class="paginationBtn" value="${page}">
                ${page}
            </button>
        `
    }

    if (pagination.has_next) {
        paginationHtml += `
            <button class="paginationBtn" value="${pagination.next_page}">
                <img src="/catalog/static/images/next.png" alt="next">
            </button>
        `
    }

    paginationContainer.innerHTML = paginationHtml

    const paginationBtns = document.querySelectorAll(".paginationBtn")

    paginationBtns.forEach((btn) => {
        btn.addEventListener("click", (event) => {
            filterProducts(Number(event.currentTarget.value))
        })
    })
}

categoryBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
        categoryBtns.forEach((item) => {
            item.classList.remove("active")
        })

        btn.classList.add("active")

        selectedCategory = btn.dataset.category

        filterProducts(1)
    })
})

window.addEventListener("DOMContentLoaded", () => {
    filterProducts(1)
})
