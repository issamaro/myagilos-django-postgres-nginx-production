// Function to fetch certification data
async function fetchCertifications() {
  try {
    const currentYear = new Date().getFullYear();
    const response = await fetch(`/static/static/certifications/${currentYear}_allCertifications_.json`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
    throw new Error('Failed to fetch certification data');
  }
}

// Function to filter certification titles based on the selected company
function filterCertifications(data, selectedCompany) {
  const selectedCompanyData = data.find(item => item.company === selectedCompany);
  if (selectedCompanyData) {
    return selectedCompanyData.certifications;
  }
  return [];
}

// Function to update the certification titles in the form
function updateCertificationTitles(data, selectedCompany) {
  const titleSelect = document.querySelector("#id_title");
  const certifications = filterCertifications(data, selectedCompany);
  titleSelect.innerHTML = ""; // Clear existing options

  if (certifications.length > 0) {
    certifications.forEach(certification => {
      const option = document.createElement("option");
      option.value = `${certification["code"]} - ${certification["name"]}`;
      option.textContent = `${certification["code"]} - ${certification["name"]}`;
      titleSelect.appendChild(option);
    });
  } else {
    // Handle case when no certifications available for the selected company
    const option = document.createElement("option");
    option.textContent = "No certifications available";
    titleSelect.appendChild(option);
  }
}

// Function to handle the change event of the company select
function onCompanyChange(data) {
  const companySelect = document.querySelector("#id_company");
  const selectedCompany = companySelect.value;
  updateCertificationTitles(data, selectedCompany);
}

// Initialize the form behavior when the DOM is ready
document.addEventListener("DOMContentLoaded", async () => {

  try {
    const data = await fetchCertifications();
    const companySelect = document.querySelector("#id_company");
    companySelect.addEventListener("change", () => onCompanyChange(data));
    onCompanyChange(data); // Initial call to populate certification titles
  } catch (error) {
    // Handle any errors that occur during initialization
    console.error(error);
    // Optionally, display an error message to the user
  }
});
