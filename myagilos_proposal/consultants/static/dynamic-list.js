document.addEventListener("DOMContentLoaded", () => {
    const currentYear = new Date().getFullYear();
    const company = "aws";
    fetch(`/static/certifications/${currentYear}_${company}Certifications.json`)
      .then(response => response.json())
      .then(data => {
        // do something with the data
        console.log(data);
      })
      .catch(error => console.error(error));
})

