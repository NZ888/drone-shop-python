const openBtn = document.getElementById("openModal")
const modalDiv = document.getElementById("modal")
const closeBtn = document.getElementById("closeModal")
openBtn.addEventListener("click", ()=>{
    modalDiv.style.display = "flex";
})
closeBtn.addEventListener("click", ()=>{
    modalDiv.style.display = "none";
})