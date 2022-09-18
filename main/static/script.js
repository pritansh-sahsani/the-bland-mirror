// Variable for table and cells inside it
var table = document.getElementById('table');
var cells = table.getElementsByTagName('td');

// Loop through the cells
for (var i = 0; i < cells.length; i++) {
    cells[i].onclick = function () {
        // If cell is not active, change the CSS back to original
        if (this.hasAttribute('data-clicked')) {
            return;
        }

        // Set attributes to check status of cells
        this.setAttribute('data-clicked', 'yes');
        this.setAttribute('data-text', this.innerHTML);

        // Declare the editing cell in a variable
        var input = document.createElement('input');

        // Change CSS of cell while editing
        input.setAttribute('type', 'text');
        input.value = this.innerHTML;
        input.style.border = "0px";
        input.style.fontFamily = "inherit";
        input.style.fontSize = "inherit";
        input.style.textAlign = "inherit";
        input.style.backgroundColor = "lightgray";

        // Check if data is changed and edit attributes accordingly
        input.onblur = function () {
            var td = input.parentElement;
            var original_text = input.parentElement.getAttribute('data-text');
            var current_text = this.value;

            if (original_text != current_text) {
                td.removeAttribute('data-clicked');
                td.removeAttribute('data-text');
                td.innerHTML = current_text;
            }
            else {
                td.removeAttribute('data-clicked');
                td.removeAttribute('data-text');
                td.innerHTML = original_text;
            }
        }

        // Change data when pressed enter
        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                this.blur();
            }
        })

        // Apply the changes
        this.innerHTML = '';
        this.append(input);
        this.firstElementChild.select();
    }
}