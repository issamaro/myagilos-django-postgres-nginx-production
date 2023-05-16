document.addEventListener("DOMContentLoaded", () => {
    const labels = document.querySelectorAll("label")
    labels.forEach((label) => {
        label.innerText = label.innerText.slice(0, -1)
    })
})