document.addEventListener("DOMContentLoaded", () => {
    const target = document.querySelector("#mycases-target");
    const firstChar = parseInt(target.textContent.charAt(0), 10);
    const targetChar = parseInt(target.textContent.charAt(2), 10);
    if (!isNaN(firstChar)) {
        if (firstChar >= targetChar) {
            target.style.color = "#2CE300";
        }
        else
        {
            target.style.color = "#FF4545";
        }
    }
    else
    {
        target.textContent = "<<error: need a digit as first character. for devs: check red-target.js>>";
    }
});