const select = document.getElementById("warehouse")
const cityInput = document.getElementById("cityName")
const modalForDelivery = document.getElementById("modal_for_delivery")
const radioBtns = document.querySelectorAll("input[name='delivery']")

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