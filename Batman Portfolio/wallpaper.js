// --- SEARCH FUNCTION ---
const searchBox = document.getElementById("searchBox");
const gallery = document.getElementById("gallery");
const wallpapers = gallery.getElementsByTagName("img");

searchBox.addEventListener("input", function () {
  let filter = searchBox.value.toLowerCase();
  for (let i = 0; i < wallpapers.length; i++) {
    let altText = wallpapers[i].alt.toLowerCase();
    wallpapers[i].style.display = altText.includes(filter) ? "" : "none";
  }
});

// --- UPLOAD FUNCTION ---
const uploadInput = document.getElementById("uploadInput");
const uploadOption = document.querySelector(".upload-option");

uploadOption.addEventListener("click", () => {
  uploadInput.click();
});

uploadInput.addEventListener("change", function () {
  const file = uploadInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const newImg = document.createElement("img");
      newImg.src = e.target.result;
      newImg.alt = file.name;
      gallery.appendChild(newImg);
    };
    reader.readAsDataURL(file);
  }
});




