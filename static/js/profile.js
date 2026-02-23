document.querySelector("#avatarUpload").addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            document.querySelector("#avatarPreview").src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});