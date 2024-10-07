function toggleCheckboxes(source) {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i] != source)
            checkboxes[i].checked = source.checked;
    }
}

function toggleSearchRow() {
    var searchRow = document.getElementById("search-row");
    var searchButton = document.getElementById("search-button");
    searchRow.style.visibility = searchRow.style.visibility == "visible" ? "collapse" : "visible";
    searchButton.textContent = searchRow.style.visibility == "visible" ? "Hide" : "Search"
}