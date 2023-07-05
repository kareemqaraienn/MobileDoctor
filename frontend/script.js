document.getElementById('addDropdown').addEventListener('click', function() {
    // Create new select
    var newSelect = document.createElement("select");
    var options = ["S1", "S2", "S3"];
    for (var i = 0; i < options.length; i++) {
        var option = document.createElement("option");
        option.value = "option" + (i + 1);
        option.text = options[i];
        newSelect.appendChild(option);
    }

    var currentSelects = document.querySelectorAll("select");
    var newSelectWidth = currentSelects.length > 0 ? currentSelects[0].offsetWidth : 200; 
    newSelect.style.width = newSelectWidth + "px";

    var newDiv = document.createElement("div");
    newDiv.classList.add("dropdownContainer");
    newDiv.appendChild(newSelect);

    var deleteButton = document.createElement("button");
    deleteButton.textContent = "-";
    deleteButton.classList.add("deleteDropdown");
    deleteButton.addEventListener("click", function() {
        newDiv.remove(); 
    });

    newDiv.appendChild(deleteButton);
    var addDropdownButton = document.getElementById('addDropdown');
    addDropdownButton.parentNode.insertBefore(newDiv, addDropdownButton);
    
});

document.getElementById('submitButton').addEventListener('click', function(e) {
    e.preventDefault(); 
    window.location.href = "Results.html"; 
});

document.getElementById('topLeftButton').addEventListener('click', function() {
    // Add Functionality 
});
