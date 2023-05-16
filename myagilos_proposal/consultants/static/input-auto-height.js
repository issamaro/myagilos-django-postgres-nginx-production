document.addEventListener("DOMContentLoaded", () => {
    const textareas = document.querySelectorAll("textarea");
    if (textareas.length > 0) {
        textareas.forEach((input) => {
            input.addEventListener("input", () => {
                console.log("textarea element:", input);
                console.log("textarea height before update:", input.style.height);

                input.style.height = '36px';
                input.style.height = `${input.scrollHeight}px`;

                console.log("textarea height after update:", input.style.height);
                console.log("scrollHeight value:", input.scrollHeight);
            });
        });
    }
    else {
        console.error('No input elements found with selector "input[type=\'text\']"');
    }
});
