function submitFeedback(event) {
    event.preventDefault(); 

    const reviewText = document.getElementById('reviewText').value;

    if (reviewText.trim() === "") {
        alert("Please enter a review.");
        return;
    }

    console.log("Review Submitted: ", reviewText);

    document.getElementById('feedbackForm').style.display = 'none';
    document.getElementById('thankYouMessage').style.display = 'block';
}

