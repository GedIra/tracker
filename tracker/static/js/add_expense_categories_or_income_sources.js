document.addEventListener("DOMContentLoaded", function () {
    const businessSelect = document.getElementById("business");
    const targetSelectCategory = document.getElementById("category"); // For expenses
    const targetSelectSource = document.getElementById("source"); // For incomes

    if (businessSelect) {
        businessSelect.addEventListener("change", function () {
            const businessId = this.value;

            if (businessId) {
                // For Expenses: Fetch Categories
                if (targetSelectCategory) {
                    fetchAndPopulate(targetSelectCategory, "/get-categories/" + businessId + "/");
                }

                // For Incomes: Fetch Sources
                if (targetSelectSource) {
                    fetchAndPopulate(targetSelectSource, "/incomes/get-sources/" + businessId + "/");
                }
            }
        });

        // Trigger change to populate the category/source if a business is pre-selected
        if (businessSelect.value) {
            businessSelect.dispatchEvent(new Event("change"));
        }
    }
});

function fetchAndPopulate(targetSelect, fetchUrl) {
    // Clear previous options
    targetSelect.innerHTML = `<option value="" disabled selected>Select an option</option>`;
    targetSelect.disabled = true;

    fetch(fetchUrl)
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const option = new Option(item.name, item.id);
                targetSelect.appendChild(option);
            });

            targetSelect.disabled = false;
        })
        .catch(error => {
            console.error("⚠️ Error fetching data:", error);
            targetSelect.disabled = true;
        });
}
