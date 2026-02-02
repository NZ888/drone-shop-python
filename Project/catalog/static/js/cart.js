async function addToCart(idProduct) {
    const response = await fetch("/add-to-cart/", {
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

const addButton = document.getElementById("addButton")

addButton.addEventListener("click", ()=>{
    addToCart(addButton.value)
})


async function deleteInCart(idProduct) {
    const response = await fetch("/delete_in_cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({product_id: idProduct})
    })
    const result = await response.json()
    console.log(result.productsCount)
}

const deleteButton = document.getElementById("deleteButton")

deleteButton.addEventListener("click", ()=>{
    deleteInCart(deleteButton.value)
})


