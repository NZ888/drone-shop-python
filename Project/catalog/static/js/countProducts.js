(
    async () => {
        const response = await fetch("/count_products/")
        const data = await response.json()
        document.getElementById("count").textContent = data.productsCount
    }
)()