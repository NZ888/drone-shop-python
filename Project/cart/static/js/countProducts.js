export async function addToCart(idProduct) {
    const response = await fetch("/add-to-cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({product_id: idProduct})
    })
    const result = await response.json()
    console.log(result.productsCount)
    // кол-во одного вида товара
    return result.productsCount
}

const addButtons = document.querySelectorAll(".addButton")
addButtons.forEach((button)=>{
    button.addEventListener("click", ()=>{
    addToCart(button.value)
})
})


export async function deleteInCart(idProduct) {
    const response = await fetch("/delete_in_cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({product_id: idProduct})
    })
    const result = await response.json()
    console.log(result.productsCount)
    return result.productsCount
}

const deleteButtons = document.querySelectorAll(".deleteButton")

deleteButtons.forEach((button) => {
    button.addEventListener("click", ()=>{
    deleteInCart(button.value)
})
})


