const menuButtons = document.querySelectorAll(".dashboard-menu-btn")
const tabs = document.querySelectorAll(".dashboard-tab")
const orderToggles = document.querySelectorAll(".order-toggle")
const dashboardForms = document.querySelectorAll(".dashboard-form")
const deliveryRadios = document.querySelectorAll(".delivery-radio")
const editAddressButtons = document.querySelectorAll(".edit-address-btn")
const deleteAddressButtons = document.querySelectorAll(".delete-address-btn")
const addAddressButton = document.querySelector(".add-address-btn")
const cancelOrderButtons = document.querySelectorAll(".cancel-order-btn")
const copyTrackButtons = document.querySelectorAll(".copy-track-btn")

function showTab(tabId) {
    tabs.forEach((tab) => {
        tab.classList.toggle("active", tab.id === tabId)
    })

    menuButtons.forEach((button) => {
        button.classList.toggle("active", button.dataset.tab === tabId)
    })

    localStorage.setItem("dashboard_tab", tabId)
}

function showMessage(container, message, isError = false) {
    if (!container) {
        return
    }

    container.textContent = message || ""
    container.classList.toggle("error", isError)
}

function fillDeliveryForm(data) {
    const deliveryId = document.getElementById("delivery_id")
    const deliverySelected = document.getElementById("delivery_selected")
    const city = document.getElementById("city")
    const streat = document.getElementById("streat")
    const house = document.getElementById("house")
    const flat = document.getElementById("flat")
    const block = document.getElementById("block")

    if (!deliveryId || !city || !streat || !house || !flat || !block) {
        return
    }

    deliveryId.value = data.id || ""
    city.value = data.city || ""
    streat.value = data.streat || ""
    house.value = data.house || ""
    flat.value = data.flat || ""
    block.value = data.block || ""

    if (deliverySelected) {
        deliverySelected.value = data.isSelected ? "1" : "0"
    }
}

async function postForm(url, body = null) {
    const response = await fetch(url, {
        method: "POST",
        body
    })

    const data = await response.json().catch(() => ({
        success: false,
        message: "Помилка відповіді сервера"
    }))

    return {
        ok: response.ok && data.success,
        status: response.status,
        data
    }
}

const savedTabId = localStorage.getItem("dashboard_tab")

if (savedTabId && document.getElementById(savedTabId)) {
    showTab(savedTabId)
}

menuButtons.forEach((button) => {
    button.addEventListener("click", () => {
        showTab(button.dataset.tab)
    })
})

orderToggles.forEach((button) => {
    button.addEventListener("click", () => {
        button.closest(".order-card").classList.toggle("is-open")
    })
})

dashboardForms.forEach((form) => {
    form.addEventListener("submit", async (event) => {
        event.preventDefault()

        const message = form.querySelector("[data-form-message]")
        showMessage(message, "")

        const result = await postForm(form.action, new FormData(form))

        if (!result.ok) {
            showMessage(message, result.data.message || "Не вдалося зберегти", true)
            return
        }

        form.classList.add("saved")
        showMessage(message, result.data.message || "Збережено")

        window.setTimeout(() => {
            form.classList.remove("saved")
        }, 1200)

        if (form.classList.contains("delivery-form")) {
            localStorage.setItem("dashboard_tab", "delivery-page")
            window.setTimeout(() => {
                window.location.reload()
            }, 500)
        }
    })
})

deliveryRadios.forEach((radio) => {
    radio.addEventListener("change", async () => {
        const result = await postForm(radio.dataset.selectUrl)

        if (!result.ok) {
            radio.checked = false
            return
        }

        document.querySelectorAll(".delivery-saved-address").forEach((address) => {
            address.classList.remove("selected")
        })
        radio.closest(".delivery-saved-address").classList.add("selected")

        fillDeliveryForm({
            id: radio.dataset.id,
            city: radio.dataset.city,
            streat: radio.dataset.streat,
            house: radio.dataset.house,
            flat: radio.dataset.flat,
            block: radio.dataset.block,
            isSelected: true
        })
    })
})

editAddressButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
        event.preventDefault()
        event.stopPropagation()

        fillDeliveryForm({
            id: button.dataset.id,
            city: button.dataset.city,
            streat: button.dataset.streat,
            house: button.dataset.house,
            flat: button.dataset.flat,
            block: button.dataset.block,
            isSelected: button.closest(".delivery-saved-address").classList.contains("selected")
        })

        document.getElementById("city").focus()
    })
})

deleteAddressButtons.forEach((button) => {
    button.addEventListener("click", async (event) => {
        event.preventDefault()
        event.stopPropagation()

        if (!window.confirm("Видалити адресу?")) {
            return
        }

        const result = await postForm(button.dataset.deleteUrl)

        if (result.ok) {
            localStorage.setItem("dashboard_tab", "delivery-page")
            window.location.reload()
        }
    })
})

if (addAddressButton) {
    addAddressButton.addEventListener("click", () => {
        fillDeliveryForm({
            id: "",
            city: "",
            streat: "",
            house: "",
            flat: "",
            block: "",
            isSelected: true
        })

        document.querySelectorAll(".delivery-saved-address").forEach((address) => {
            address.classList.remove("selected")
        })

        document.getElementById("city").focus()
    })
}

cancelOrderButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        if (!window.confirm("Скасувати замовлення?")) {
            return
        }

        const card = button.closest(".order-card")
        const message = card.querySelector("[data-order-message]")
        const result = await postForm(button.dataset.cancelUrl)

        if (!result.ok) {
            showMessage(message, result.data.message || "Не вдалося скасувати", true)
            return
        }

        card.remove()

        if (!document.querySelector(".order-card")) {
            localStorage.setItem("dashboard_tab", "orders-page")
            window.location.reload()
        }
    })
})

copyTrackButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        const value = button.dataset.track

        if (navigator.clipboard) {
            await navigator.clipboard.writeText(value)
        }

        button.textContent = "✓"

        window.setTimeout(() => {
            button.textContent = "□"
        }, 1200)
    })
})
