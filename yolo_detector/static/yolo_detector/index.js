var imageName = document.getElementById("image-name")
var imageInput = document.querySelector("input[type=file]")
function handleChange() {
    if (imageInput.files.length > 0) {
        imageName.innerText = imageInput.files[0].name;
    }
}
handleChange();