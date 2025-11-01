// Application State
const state = {
    selectedModule: null,      // 'K' or 'T1'
    selectedMode: null,        // 'practice', 'exam', or 'study'
    questions: [],             // All questions for selected module
    currentQuestions: [],      // Questions for current session
    currentIndex: 0,           // Current question index
    answers: [],               // User's answers
    settings: {
        shuffleQuestions: true,
        shuffleOptions: true
    }
};

// Load questions from JSON files
async function loadQuestions() {
    try {
        const response = await fetch('all_questions.json');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error loading questions:', error);
        alert('Failed to load questions. Please ensure all_questions.json is available.');
        return null;
    }
}

// Initialize application
let allQuestions = null;

window.addEventListener('DOMContentLoaded', async () => {
    allQuestions = await loadQuestions();
    if (!allQuestions) {
        document.getElementById('startButton').textContent = 'Error: Questions not loaded';
    }
});

// Menu Functions
function selectModule(module) {
    state.selectedModule = module;

    // Update UI - highlight selected button
    document.querySelectorAll('.menu-section:first-child .btn').forEach(btn => {
        btn.style.opacity = '0.6';
    });
    event.target.style.opacity = '1';

    checkStartButton();
}

function selectMode(mode) {
    state.selectedMode = mode;

    // Update UI - highlight selected button
    document.querySelectorAll('.menu-section:nth-child(2) .btn').forEach(btn => {
        btn.style.opacity = '0.6';
    });
    event.target.style.opacity = '1';

    checkStartButton();
}

function checkStartButton() {
    const startButton = document.getElementById('startButton');
    if (state.selectedModule && state.selectedMode) {
        startButton.disabled = false;
    }
}

// Session Management
function startSession() {
    // Get settings
    state.settings.shuffleQuestions = document.getElementById('shuffleQuestions').checked;
    state.settings.shuffleOptions = document.getElementById('shuffleOptions').checked;

    // Load questions for selected module
    if (state.selectedModule === 'K') {
        state.questions = [...allQuestions.k_module];
    } else {
        state.questions = [...allQuestions.t1_module];
    }

    // Prepare questions based on mode
    if (state.selectedMode === 'study') {
        startStudyMode();
    } else {
        startQuizMode();
    }
}

function startQuizMode() {
    // For exam mode, select 60 random questions
    if (state.selectedMode === 'exam') {
        if (state.settings.shuffleQuestions) {
            state.currentQuestions = shuffleArray([...state.questions]).slice(0, 60);
        } else {
            state.currentQuestions = state.questions.slice(0, 60);
        }
    } else {
        // Practice mode - use all questions
        if (state.settings.shuffleQuestions) {
            state.currentQuestions = shuffleArray([...state.questions]);
        } else {
            state.currentQuestions = [...state.questions];
        }
    }

    // Initialize answers array
    state.answers = new Array(state.currentQuestions.length).fill(null);
    state.currentIndex = 0;

    // Show question screen
    document.getElementById('mainMenu').style.display = 'none';
    document.getElementById('questionScreen').style.display = 'block';

    // Display first question
    displayQuestion();
}

function startStudyMode() {
    state.currentQuestions = [...state.questions];
    state.currentIndex = 0;

    // Show study screen
    document.getElementById('mainMenu').style.display = 'none';
    document.getElementById('studyScreen').style.display = 'block';

    displayStudyQuestion();
}

// Question Display
function displayQuestion() {
    const question = state.currentQuestions[state.currentIndex];

    // Update progress
    const progress = ((state.currentIndex + 1) / state.currentQuestions.length) * 100;
    document.getElementById('progressFill').style.width = progress + '%';
    document.getElementById('progressText').textContent =
        `Question ${state.currentIndex + 1} of ${state.currentQuestions.length}`;

    // Update question header
    document.getElementById('questionId').textContent =
        `${question.module}-${question.id}`;
    document.getElementById('questionModule').textContent =
        `${question.module} Module`;

    // Update question text
    document.getElementById('questionText').textContent = question.text;

    // Hide feedback
    document.getElementById('feedback').style.display = 'none';

    // Display appropriate options
    if (question.type === 'true_false') {
        displayTrueFalseOptions(question);
    } else {
        displayMultipleChoiceOptions(question);
    }

    // Update navigation buttons
    updateNavigationButtons();

    // If answer exists, show it
    if (state.answers[state.currentIndex] !== null) {
        showPreviousAnswer();
    }
}

function displayTrueFalseOptions(question) {
    document.getElementById('trueFalseOptions').style.display = 'flex';
    document.getElementById('multipleChoiceOptions').style.display = 'none';

    // Reset button states
    const buttons = document.querySelectorAll('#trueFalseOptions .option-btn');
    buttons.forEach(btn => {
        btn.className = 'option-btn';
        btn.disabled = false;
    });
}

function displayMultipleChoiceOptions(question) {
    document.getElementById('trueFalseOptions').style.display = 'none';
    document.getElementById('multipleChoiceOptions').style.display = 'flex';

    const container = document.getElementById('multipleChoiceOptions');
    container.innerHTML = '';

    // Get options (shuffle if needed)
    let options = [...question.options];
    if (state.settings.shuffleOptions && state.answers[state.currentIndex] === null) {
        options = shuffleArray(options);
    }

    // Create option buttons
    options.forEach(option => {
        const button = document.createElement('button');
        button.className = 'option-btn';
        button.onclick = () => selectAnswer(option.letter);

        const letter = document.createElement('span');
        letter.className = 'option-letter';
        letter.textContent = option.letter;

        const text = document.createElement('span');
        text.className = 'option-text';
        text.textContent = option.text;

        button.appendChild(letter);
        button.appendChild(text);
        button.dataset.letter = option.letter;
        button.dataset.isCorrect = option.is_correct;

        container.appendChild(button);
    });
}

// Answer Selection
function selectAnswer(answer) {
    const question = state.currentQuestions[state.currentIndex];

    // Store answer
    state.answers[state.currentIndex] = answer;

    // Update UI based on mode
    if (state.selectedMode === 'practice') {
        showFeedback(answer, question);
    } else {
        // Exam mode - just highlight selection
        highlightSelection(answer);
    }

    // Show next button
    document.getElementById('nextButton').style.display = 'inline-block';

    // If last question, show finish button instead
    if (state.currentIndex === state.currentQuestions.length - 1) {
        document.getElementById('nextButton').style.display = 'none';
        document.getElementById('finishButton').style.display = 'inline-block';
    }
}

function highlightSelection(answer) {
    const question = state.currentQuestions[state.currentIndex];

    if (question.type === 'true_false') {
        const buttons = document.querySelectorAll('#trueFalseOptions .option-btn');
        buttons.forEach(btn => {
            btn.classList.remove('selected');
            const isTrue = btn.querySelector('.option-letter').textContent === '✓';
            if ((isTrue && answer === true) || (!isTrue && answer === false)) {
                btn.classList.add('selected');
            }
        });
    } else {
        const buttons = document.querySelectorAll('#multipleChoiceOptions .option-btn');
        buttons.forEach(btn => {
            btn.classList.remove('selected');
            if (btn.dataset.letter === answer) {
                btn.classList.add('selected');
            }
        });
    }
}

function showFeedback(answer, question) {
    let isCorrect = false;

    if (question.type === 'true_false') {
        isCorrect = (answer === question.correct_answer);

        // Highlight correct/incorrect
        const buttons = document.querySelectorAll('#trueFalseOptions .option-btn');
        buttons.forEach(btn => {
            btn.disabled = true;
            const isTrue = btn.querySelector('.option-letter').textContent === '✓';

            if ((isTrue && question.correct_answer) || (!isTrue && !question.correct_answer)) {
                btn.classList.add('correct');
            }

            if ((isTrue && answer === true) || (!isTrue && answer === false)) {
                if (!isCorrect) {
                    btn.classList.add('incorrect');
                }
            }
        });
    } else {
        // Multiple choice
        const correctAnswers = question.correct_answers;
        isCorrect = correctAnswers.includes(answer);

        const buttons = document.querySelectorAll('#multipleChoiceOptions .option-btn');
        buttons.forEach(btn => {
            btn.disabled = true;

            if (btn.dataset.isCorrect === 'true') {
                btn.classList.add('correct');
            }

            if (btn.dataset.letter === answer && btn.dataset.isCorrect === 'false') {
                btn.classList.add('incorrect');
            }
        });
    }

    // Show feedback message
    const feedback = document.getElementById('feedback');
    const feedbackText = document.getElementById('feedbackText');

    if (isCorrect) {
        feedback.className = 'feedback correct';
        feedbackText.innerHTML = '<strong>✓ Correct!</strong>';
    } else {
        feedback.className = 'feedback incorrect';
        if (question.type === 'true_false') {
            feedbackText.innerHTML = `<strong>✗ Incorrect.</strong> The correct answer is: ${question.correct_answer ? 'True' : 'False'}`;
        } else {
            const correctAnswerText = question.correct_answers.join(', ');
            feedbackText.innerHTML = `<strong>✗ Incorrect.</strong> The correct answer(s): ${correctAnswerText}`;
        }
    }

    feedback.style.display = 'block';
}

function showPreviousAnswer() {
    const answer = state.answers[state.currentIndex];
    const question = state.currentQuestions[state.currentIndex];

    if (state.selectedMode === 'practice') {
        showFeedback(answer, question);
    } else {
        highlightSelection(answer);
    }

    // Show next button
    document.getElementById('nextButton').style.display = 'inline-block';

    if (state.currentIndex === state.currentQuestions.length - 1) {
        document.getElementById('nextButton').style.display = 'none';
        document.getElementById('finishButton').style.display = 'inline-block';
    }
}

// Navigation
function nextQuestion() {
    if (state.currentIndex < state.currentQuestions.length - 1) {
        state.currentIndex++;
        displayQuestion();
    }
}

function previousQuestion() {
    if (state.currentIndex > 0) {
        state.currentIndex--;
        displayQuestion();
    }
}

function skipQuestion() {
    if (state.currentIndex < state.currentQuestions.length - 1) {
        state.currentIndex++;
        displayQuestion();
    }
}

function updateNavigationButtons() {
    const prevButton = document.getElementById('prevButton');
    const skipButton = document.getElementById('skipButton');
    const nextButton = document.getElementById('nextButton');
    const finishButton = document.getElementById('finishButton');

    prevButton.disabled = state.currentIndex === 0;
    skipButton.style.display = state.selectedMode === 'exam' ? 'inline-block' : 'none';
    nextButton.style.display = 'none';
    finishButton.style.display = 'none';
}

// Exam Completion
function finishExam() {
    calculateResults();
    showResults();
}

function calculateResults() {
    let correct = 0;
    let incorrect = 0;
    let unanswered = 0;

    state.currentQuestions.forEach((question, index) => {
        const answer = state.answers[index];

        if (answer === null) {
            unanswered++;
        } else {
            if (question.type === 'true_false') {
                if (answer === question.correct_answer) {
                    correct++;
                } else {
                    incorrect++;
                }
            } else {
                if (question.correct_answers.includes(answer)) {
                    correct++;
                } else {
                    incorrect++;
                }
            }
        }
    });

    state.results = {
        correct,
        incorrect,
        unanswered,
        total: state.currentQuestions.length,
        percentage: Math.round((correct / state.currentQuestions.length) * 100)
    };
}

function showResults() {
    // Hide question screen
    document.getElementById('questionScreen').style.display = 'none';

    // Show results screen
    document.getElementById('resultsScreen').style.display = 'block';

    // Display score
    document.getElementById('scoreNumber').textContent = state.results.correct;
    document.getElementById('scoreCircle').querySelector('.score-total').textContent =
        `/ ${state.results.total}`;
    document.getElementById('scorePercentage').textContent =
        state.results.percentage + '%';

    // Determine pass/fail
    const passThreshold = state.selectedModule === 'K' ? 45 : 45; // 45 out of 60
    const isPassed = state.results.correct >= passThreshold;

    const resultStatus = document.getElementById('resultStatus');
    if (isPassed) {
        resultStatus.className = 'result-status pass';
        resultStatus.innerHTML = '🎉 <strong>Passed!</strong> Congratulations!';
    } else {
        resultStatus.className = 'result-status fail';
        resultStatus.innerHTML = '❌ <strong>Not Passed</strong> - Keep studying!';
    }

    // Show breakdown
    const breakdown = document.getElementById('resultBreakdown');
    breakdown.innerHTML = `
        <h3>Detailed Breakdown</h3>
        <p><strong>Correct answers:</strong> ${state.results.correct}</p>
        <p><strong>Incorrect answers:</strong> ${state.results.incorrect}</p>
        <p><strong>Unanswered:</strong> ${state.results.unanswered}</p>
        <p><strong>Passing score:</strong> ${passThreshold} / ${state.results.total}</p>
        <p><strong>Your score:</strong> ${state.results.correct} / ${state.results.total} (${state.results.percentage}%)</p>
    `;
}

function reviewAnswers() {
    // Go back to question screen in review mode
    state.currentIndex = 0;
    document.getElementById('resultsScreen').style.display = 'none';
    document.getElementById('questionScreen').style.display = 'block';
    displayQuestion();

    // Update all answers to show feedback
    if (state.selectedMode === 'exam') {
        state.selectedMode = 'practice'; // Switch to practice mode for review
    }
}

function restartSession() {
    document.getElementById('resultsScreen').style.display = 'none';
    startQuizMode();
}

function returnToMenu() {
    // Reset state
    state.selectedModule = null;
    state.selectedMode = null;
    state.currentIndex = 0;
    state.answers = [];

    // Reset UI
    document.querySelectorAll('.btn').forEach(btn => {
        btn.style.opacity = '1';
    });
    document.getElementById('startButton').disabled = true;

    // Show main menu
    document.getElementById('mainMenu').style.display = 'block';
    document.getElementById('questionScreen').style.display = 'none';
    document.getElementById('resultsScreen').style.display = 'none';
    document.getElementById('studyScreen').style.display = 'none';
}

function quitSession() {
    if (confirm('Are you sure you want to quit? Your progress will be lost.')) {
        returnToMenu();
    }
}

// Study Mode Functions
function displayStudyQuestion() {
    const question = state.currentQuestions[state.currentIndex];

    // Update progress
    document.getElementById('studyProgress').textContent =
        `Question ${state.currentIndex + 1} of ${state.currentQuestions.length}`;

    // Update question
    document.getElementById('studyQuestionId').textContent =
        `${question.module}-${question.id}`;
    document.getElementById('studyQuestionText').textContent = question.text;

    // Show answer
    const answerDiv = document.getElementById('studyAnswer');

    if (question.type === 'true_false') {
        answerDiv.innerHTML = `
            <h3>Answer</h3>
            <p class="correct-option"><strong>${question.correct_answer ? 'True' : 'False'}</strong></p>
        `;
    } else {
        const correctOptions = question.options
            .filter(opt => opt.is_correct)
            .map(opt => `<p class="correct-option"><strong>${opt.letter}:</strong> ${opt.text}</p>`)
            .join('');

        answerDiv.innerHTML = `
            <h3>Correct Answer(s)</h3>
            ${correctOptions}
        `;
    }
}

function nextStudyQuestion() {
    if (state.currentIndex < state.currentQuestions.length - 1) {
        state.currentIndex++;
        displayStudyQuestion();
    }
}

function previousStudyQuestion() {
    if (state.currentIndex > 0) {
        state.currentIndex--;
        displayStudyQuestion();
    }
}

// Utility Functions
function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}
