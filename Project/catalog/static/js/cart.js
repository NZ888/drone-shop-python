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
}

const addButton = document.getElementById("addButton")

addButton.addEventListener("click", ()=>{
    addToCart(addButton.value)
})