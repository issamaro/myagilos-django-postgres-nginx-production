function loader(id, choice) {
    if (typeof id === "string") {
        if (choice === 0) {
            const div = document.querySelector(id);
            div.classList.add("loader");
        }
        else {
            const div = document.querySelector(id);
            div.classList.remove("loader");
        }
    }
    else {
        console.error("Loader function expects a string as an argument.");
    }
}
