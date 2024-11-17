// Exibir nome do arquivo selecionado
document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.querySelector('input[type="file"]');
    const fileNameDisplay = document.querySelector("#file-name-display");

    if (fileInput) {
        fileInput.addEventListener("change", function () {
            if (fileInput.files.length > 0) {
                fileNameDisplay.textContent = `Selected file: ${fileInput.files[0].name}`;
            } else {
                fileNameDisplay.textContent = "No file selected";
            }
        });
    }
});

// Feedback visual ao carregar
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const submitButton = document.querySelector('button[type="submit"]');
    if (form) {
        form.addEventListener("submit", function () {
            if (submitButton) {
                submitButton.textContent = "Uploading...";
                submitButton.disabled = true;
            }
        });
    }
});
