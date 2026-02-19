const addReviewButton = document.querySelector("#addReviewButton")
addReviewButton.addEventListener("click", () => {
    const commentContent = document.querySelector("#commentTextarea").value
    const movieId = addReviewButton.dataset.movieId;
    const userName = document.querySelector("#userName")
    const form = new FormData();
    form.set("movieId", movieId);
    form.set("content", commentContent);
    if(userName){
        form.set("guest_name", userName.value);
    }

    fetch("/users/review/create/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        },
        body: form,
        mode: "same-origin"
    })
    .then(response => response.json())
    .then((data) => {
        if(data.created){
            window.location.reload()
        }
    })
})
