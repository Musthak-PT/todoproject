





// function checkImageSize(event) {
//     var logoPreview = document.getElementById('logo-preview');
//     const file = event.target.files[0];
//     const fileSize = file.size / 1024 / 1024; // in MB
//     const errorElement = document.getElementById("logo-error");
//     if (fileSize > 1) {
//         errorElement.style.display = "block";
//         // event.target.value = ""; // reset the input element
//         logoPreview.src = URL.createObjectURL(event.target.files[0]);
//         logoPreview.style.display = "block";
//         event.preventDefault();
//     } else {
//         errorElement.style.display = "none";
//         previewImage(event);
//     }
// }