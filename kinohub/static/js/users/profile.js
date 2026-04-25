
let deleteAvatar = false;

const deleteBtn = document.querySelector("#deleteAvatarBtn");

if (deleteBtn) {
    deleteBtn.addEventListener("click", () => {
        deleteAvatar = true;

        document.getElementById("avatarPreview").src = "/media/images/default-avatar.png";

        document.getElementById("profile_image").value = "";
    });
}
document.getElementById("profile_image").addEventListener("change", function (event) {
    const [file] = event.target.files;
    if (file) {
        document.getElementById("avatarPreview").src = URL.createObjectURL(file);
    }
});
