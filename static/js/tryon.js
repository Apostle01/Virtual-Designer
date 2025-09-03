document.addEventListener("DOMContentLoaded", () => {
    const modal = new bootstrap.Modal(document.getElementById("tryOnModal"));
    const userPhotoPreview = document.getElementById("user-photo-preview");
    const tryOnCanvas = document.getElementById("try-on-canvas");
    const ctx = tryOnCanvas.getContext("2d");

    document.querySelectorAll(".try-on-btn").forEach(button => {
        button.addEventListener("click", () => {
            const photoUrl = button.dataset.photo;
            userPhotoPreview.src = photoUrl;
            tryOnCanvas.width = 500;
            tryOnCanvas.height = 500;
            ctx.clearRect(0, 0, tryOnCanvas.width, tryOnCanvas.height);
            const img = new Image();
            img.src = photoUrl;
            img.onload = () => ctx.drawImage(img, 0, 0, tryOnCanvas.width, tryOnCanvas.height);
            modal.show();
        });
    });

    document.querySelectorAll(".style-btn").forEach(button => {
        button.addEventListener("click", () => {
            const styleUrl = button.dataset.style;
            const styleImg = new Image();
            styleImg.src = styleUrl;
            styleImg.onload = () => ctx.drawImage(styleImg, 0, 0, tryOnCanvas.width, tryOnCanvas.height);
        });
    });
});
