function getGuestName() {
    let guestName = document.querySelector("#userName")
    if (guestName) {
        return guestName.value
    }
    return ""
}
document.body.addEventListener("htmx:afterRequest", function (event) {
    const form = document.querySelector("form#reviewForm");
    if (!form) return;

    if (form.contains(event.detail.elt) && event.detail.successful) {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }
});
