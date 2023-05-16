document.addEventListener("DOMContentLoaded", () => {
    const currentYear = new Date().getFullYear();
    const currentYearId = `${currentYear}`;
    const divs = document.querySelector("#allcases");
    const children = [...divs.children].filter(child => child.tagName !== "P");
    const groupedByYear = children.reduce((acc, child) => {
        const year = child.id;
        if (!acc[year]) {
            acc[year] = document.createElement("div");
            acc[year].id = `${year}-group`;
            const headline = document.createElement("p");
            headline.setAttribute("class", "mycases-year");
            headline.innerText = year;
            acc[year].appendChild(headline);
        }
        acc[year].appendChild(child);
        return acc;
    }, {});
    if (!groupedByYear[currentYear]) {
        const currentYearDiv = document.createElement("div");
        currentYearDiv.id = `${currentYear}-group`;
        const headline = document.createElement("p");
        headline.setAttribute("class", "mycases-year");
        headline.innerText = currentYear;
        const nothingParent = document.createElement("div");
        nothingParent.id = `${currentYear}-nothing`;
        nothingParent.setAttribute("class", "nothing-to-show-parent");
        const nothing = document.createElement("div");
        nothing.setAttribute("class", "nothing-to-show");
        const noCasesYet = document.createElement("p");
        noCasesYet.innerHTML = "You have <strong>not</strong> sent any cases yet.";
        const sendCaseButton = document.createElement("button");
        sendCaseButton.id = "sendcase";
        const sendCaseAnchor = document.createElement("a");
        sendCaseAnchor.innerText = "Send a case";
        const sendCaseLink = document.querySelector("#header-cases-sendcase-link");
        sendCaseAnchor.setAttribute("href", `${sendCaseLink.getAttribute("href")}`);


        currentYearDiv.appendChild(headline);
        nothing.appendChild(noCasesYet);
        sendCaseButton.appendChild(sendCaseAnchor);
        nothing.appendChild(sendCaseButton);
        nothingParent.appendChild(nothing);
        currentYearDiv.appendChild(nothingParent);

        groupedByYear[currentYear] = currentYearDiv;
      }
    const sortedByYear = Object.values(groupedByYear).sort((a, b) => {
        const yearA = parseInt(a.id);
        const yearB = parseInt(b.id);
        return yearB - yearA;
    });
    for (const group of sortedByYear) {
        divs.appendChild(group);
    }
});
