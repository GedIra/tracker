const searchBar = document.querySelector("#searchBar");
const table = document.querySelector(".incomesTable");
const noMatch = document.querySelector(".noMatch");
const paginationWrapper = document.getElementById("paginationWrapper");
const outputTable = document.querySelector(".tableOutput");
const tbody = outputTable.querySelector(".outputTableBody");
const business = document.getElementById("business").textContent;


outputTable.style.display = "none";
noMatch.style.display = "none";
table.style.display = "block";    //original table must be visible initially

searchBar.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if(searchValue.trim().length > 0){
        // Immediately hide the main table to prevent flickering
        table.style.display = "none";
        paginationWrapper.style.display = "none";

        fetch("/incomes/search-incomes/", {
            body: JSON.stringify({ searchStr: searchValue, business: business }),
            method: 'POST',
        })
        .then((res) => res.json())
        .then((data) => {
            tbody.innerHTML = ""; // Clear previous results

            if (data.length === 0) {
                outputTable.style.display = "none"; // Keep search table hidden
                noMatch.style.display = "block";  // Show "No Match" message
                
            }
            else {
                noMatch.style.display = "none";  // Hide "No Match" message
                outputTable.style.display = "block"; // Show search results

                data.forEach(income => {
                    const editUrl = `/edit-income/${income.id}/`;  // Construct URL dynamically
                    const deleteUrl = `/delete-income/${income.id}/`; 
                    const formattedAmount = Number(income.amount).toLocaleString(undefined, {
                        maximumSignificantDigits: 3,
                    });

                    const row = `<tr class="text-center">
                        <td class="text-left">${income.name}</td>
                        <td>${income.source}</td>
                        <td>${formattedAmount}</td>
                        <td>${income.date}</td>
                        <td class="text-sm-center">
                            <a class="btn btn-sm btn-outline-primary mr-sm-2" href="${editUrl}">Edit</a>
                            <a class="btn btn-sm btn-outline-danger" href="${deleteUrl}">Delete</a>
                        </td>
                    </tr>`;

                    tbody.innerHTML += row;
                });
            }
        }).catch(error => console.error("Error fetching search results:", error));
    }else{
        // Reset to default state when search is empty
        outputTable.style.display = "none";
        noMatch.style.display = "none";
        table.style.display = "block"; // Restore original table
        paginationWrapper.style.display = "block";
    }
})
