const openAdminProductModal = document.getElementById("openAdminProductModal")
const closeAdminProductModal = document.getElementById("closeAdminProductModal")
const adminProductModal = document.getElementById("adminProductModal")
const adminProductBackdrop = document.getElementById("adminProductBackdrop")

function setAdminProductModal(isOpen) {
    adminProductModal.classList.toggle("active", isOpen)
    adminProductBackdrop.classList.toggle("active", isOpen)
    adminProductModal.setAttribute("aria-hidden", String(!isOpen))
}

if (openAdminProductModal) {
    openAdminProductModal.addEventListener("click", () => {
        setAdminProductModal(true)
    })
}

if (closeAdminProductModal) {
    closeAdminProductModal.addEventListener("click", () => {
        setAdminProductModal(false)
    })
}

if (adminProductBackdrop) {
    adminProductBackdrop.addEventListener("click", () => {
        setAdminProductModal(false)
    })
}

window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        setAdminProductModal(false)
    }
})
