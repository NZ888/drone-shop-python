export async function addToCart(idProduct) {
    const response = await fetch("/add-to-cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({product_id: idProduct})
    })
    const result = await response.json()
    return result.productsCount
}


export async function deleteInCart(idProduct) {
    const response = await fetch("/delete_in_cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({product_id: idProduct})
    })
    const result = await response.json()
    return result.productsCount
}