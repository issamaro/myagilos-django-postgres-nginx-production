document.addEventListener("DOMContentLoaded", () => {
    const sendButton = document.querySelector("#reference-case-submit-button");
    sendButton.disabled = true;

    form = document.querySelector("#reference-case-form");
    form.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            console.log("unauthorized");
        }
    })
});
