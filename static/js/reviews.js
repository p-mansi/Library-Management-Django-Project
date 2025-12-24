
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById("submit-review").addEventListener("click", function() {
    let bookId = this.getAttribute("data-book-id");
    submitReview(bookId);
});


function submitReview(bookId) {
    let reviewText = document.getElementById("review-text").value;
    let rating = document.getElementById("review-rating").value;

    fetch(`/books/${bookId}/review/add/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),  
        },
        body: JSON.stringify({
            review: reviewText,
            rating: rating
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Review submitted successfully!");
            location.reload();
        } else {
            alert("Error submitting review: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}
