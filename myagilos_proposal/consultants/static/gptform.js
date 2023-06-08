document.addEventListener("DOMContentLoaded", () => {

    // Get form HTML element
    const form = document.querySelector("#reference-case-form");
    const inputs = form.querySelectorAll("input");
    inputs.forEach((input) => {
        if (input.type === "text") {
            input.setAttribute(
                'size',
                input.getAttribute('placeholder').length
            );
        }
    });


    const processButton = document.querySelector("#process-button");
    processButton.addEventListener("click", (e) => {



        // Create a Form Object (an iterator) from the form html element, containing the data
        const formData = new FormData(form);

        // Create a useable object by iterating over FormData object,
        // with key = name of the paramter, and value = data
        const items = Object.fromEntries(formData);

        // API TO OPENAI: parameters
        const GPT_KEY = "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";
        const gptURL = "https://api.openai.com/v1/completions";
        const gptRequest = new Request(
            gptURL,
            {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${GPT_KEY}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    model: "text-davinci-003",
                    prompt: `You are a sales manager with 20 years experienced skills.
                    Your task is to write a case study that will be displayed on our website with the information I am going to give you.
                    The purpose is to prove our knowledge in Data Analytics projects and as well as to communicate the benefits of business intelligence.
                    Here is the inputs you will need to achieve your task:
                    customer's name: ${items.company},
                    customer's industry: ${items.industry},
                    project start date: ${items["start-date"]},
                    project end date: ${items["end-date"]},
                    issue: ${items.issue},
                    architecture: ${items.architecture},
                    the challenge in the project: ${items.challenge},
                    solution: ${items.solution},
                    used tools: ${items.tools},
                    why the customer chose agilos: ${items["why-agilos"]}`,
                    max_tokens: 3500
                })
            }
        );
        // API TO OPENAI: call
        fetch(gptRequest)
            .then((response) => response.json())
            .then((data) => {
                const gptContent = data.choices[0].text;
                const gptElement = document.querySelector("#id_gpt_content");
                gptElement.innerText = gptContent;
                gptElement.style.height = "auto";
                const gptDiv = document.querySelector(".gpt-content");
                gptDiv.classList.remove("hide");
                loader("#loader", 1);
                const sendButton = document.querySelector("#reference-case-submit-button");
                sendButton.disabled = false;
            })
            .catch((e) => console.log(e));
        loader("#loader", 0);

    });
});

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
};