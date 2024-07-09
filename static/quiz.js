var currentIndex = 0;
var definitions = {{ definitions|safe }};
var terms = {{ terms|safe }};
var numFlashcards = {{ num_flashcards }};
var answerInput = document.getElementById('answer');
var termContent = document.getElementById('term-content');
var flashcardContent = document.getElementById('flashcard-content');
var card = document.querySelector('.card__inner');

function showFlashcard(direction) {
    if (direction === 'next') {
        currentIndex = (currentIndex + 1) % numFlashcards;
    } else if (direction === 'prev') {
        currentIndex = (currentIndex - 1 + numFlashcards) % numFlashcards;
    }

    termContent.textContent = terms[currentIndex];
    flashcardContent.textContent = definitions[currentIndex];
    answerInput.value = '';
}

document.getElementById('boton').addEventListener('click', function () {
    const userAnswer = answerInput.value.trim();
    const correctAnswer = terms[currentIndex].trim();

    if (userAnswer === correctAnswer) {
        alert('Your answer is correct');
        card.classList.toggle('is-flipped');
    } else {
        alert('Your answer is wrong');
    }
});

// Initial display
showFlashcard('');
