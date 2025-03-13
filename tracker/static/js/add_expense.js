document.addEventListener("DOMContentLoaded", function () {
    let businessSelect = document.getElementById("business");
    
    if (businessSelect.value) {  // If a business is pre-selected, fetch categories
        fetchCategories(businessSelect.value);
    }

    businessSelect.addEventListener("change", function () {
        fetchCategories(this.value);
    });
});

function fetchCategories(businessId) {
    let categorySelect = document.getElementById("category");

    // Clear previous options
    categorySelect.innerHTML = '<option value="" disabled selected>Select expense category</option>';

    if (businessId) {
        fetch(`/get-categories/${businessId}/`)
        .then(response => response.json())
        .then(data => {
            data.forEach(category => {
                let option = new Option(category.name, category.id);
                categorySelect.appendChild(option);
            });

            // Restore previously selected category (if form was reloaded with errors)
            let selectedCategory = categorySelect.getAttribute("data-selected");
            if (selectedCategory) {
                categorySelect.value = selectedCategory;
            }
        })
        .catch(error => console.error("Error fetching categories:", error));
    }
}
