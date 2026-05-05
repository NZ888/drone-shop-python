import { addToCart, deleteInCart } from "../../../cart/static/js/countProducts.js"

const categoriesObj = document.getElementById("categories")
const productContainer = document.getElementById("filter_products")
const paginationContainer = document.getElementById("pagination")


productContainer.addEventListener("click", (event)=>{
    if(event.target.classList.contains("addButton")){
        addToCart(event.target.value)
    }
    if(event.target.classList.contains("deleteButton")){
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
            selectCategory: categoriesObj.value,
            page: page
        })
    })
    
    const data = await response.json()
    productContainer.innerHTML = ``
    let html = ``
    data.filtrated_products.forEach(product => {
        html += `
            <div class="product">
                <a href="/catalog/${product.id}" class="product_container">
                    <h1>${product.name}</h1>
                    <img src="/catalog/static/media/${product.image_url}" alt="">
                </a>
                <div class="buttons">
                <button class="addButton" value="${product.id}">+</button>
                <button class="deleteButton" value="${product.id}">-</button>
                </div>
            </div>
        `
    });
    productContainer.innerHTML += html
    renderPaginate(data.pagination)
}

function renderPaginate(pagination){
    let paginationHtml = ``
    if (pagination.has_prev){
        paginationHtml += `
        <button class="paginationBtn" value=${pagination.has_prev}>
            <img src="/catalog/static/images/prev.png" alt="prev">
        </button>
        `
    }
    for (let page = 1; page <= pagination.total_count; page++) {
        paginationHtml += `
            <button class="paginationBtn" value=${page}>${page}</button>
        `
    }

    if (pagination.has_next){
        paginationHtml += `
        <button class="paginationBtn" value=${pagination.has_next}>
            <img src="/catalog/static/images/next.png" alt="next">
        </button>
        `
        console.log(pagination.has_next)
    }
    paginationContainer.innerHTML = paginationHtml
    const paginationBtns = document.querySelectorAll(".paginationBtn")
    paginationBtns.forEach((btn)=>{
        btn.addEventListener('click', (event)=>{
            filterProducts(Number(event.currentTarget.value))
        })
    })
}

categoriesObj.addEventListener("change", ()=>{
    filterProducts(1)
})
window.addEventListener("DOMContentLoaded", ()=>{
    filterProducts(1)
})