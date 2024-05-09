import streamlit as st
import random
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

QUESTIONS = os.getenv("QUESTIONS", "questions.json")
NUMBEROFQUESTIONS = int(os.getenv("NUMBEROFQUESTIONS", 0))


def initialize():
    # Load your Bible trivia data
    print(f"Loading questions from {QUESTIONS}")
    with open(QUESTIONS) as f:
        data = json.load(f)
    questions = data["questions"]

    number_of_questions_to_play = (
        len(questions) if NUMBEROFQUESTIONS == 0 else NUMBEROFQUESTIONS
    )
    print(f"Number of questions to play: {number_of_questions_to_play}")
    st.session_state.number_of_questions_to_play = (
        number_of_questions_to_play  # Save to session state
    )

    # Game logic
    print("Shuffling questions...")
    random.shuffle(questions)
    st.session_state.questions = questions  # Save to session state

    print("Starting game...")


def check_answer(user_answer, correct_answer):
    def normalize_answer(answer):
        """Removes extra spaces, punctuation, and makes it lowercase"""
        return "".join(c for c in answer if c.isalnum()).lower()

    normalized_user_answer = normalize_answer(user_answer)
    normalized_correct_answer = normalize_answer(correct_answer)

    # Check for direct match
    if normalized_user_answer == normalized_correct_answer:
        return True

    # Check for answers with multiple verses
    if "and" in normalized_correct_answer:
        verse_options = normalized_correct_answer.split("and")
        return all(verse in normalized_user_answer for verse in verse_options)

    # Check for answers with 'or'
    if "or" in normalized_correct_answer:
        verse_options = normalized_correct_answer.split("or")
        return any(verse in normalized_user_answer for verse in verse_options)

    return False  # Default to incorrect


def submit_answer(current_question_index, current_question, current_answer):
    user_answer = st.session_state.user_answer
    print(f"Submit answer: {user_answer} / Correct answer: {current_answer}")
    st.session_state.last_result["last_question_index"] = current_question_index
    st.session_state.last_result["last_question"] = current_question
    st.session_state.last_result["last_user_answer"] = user_answer
    st.session_state.last_result["last_answer"] = current_answer
    if check_answer(user_answer, current_answer):
        st.session_state.correct_answers += 1
        st.session_state.last_result["last_result"] = "Correct!"
    else:
        st.session_state.incorrect_answers += 1
        st.session_state.last_result["last_result"] = "Wrong!"

    st.session_state.current_question_index = current_question_index + 1
    st.session_state.user_answer = ""
    st.rerun()


# Initialize session state
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
    st.session_state.last_result = {}
    st.session_state.correct_answers = 0
    st.session_state.incorrect_answers = 0
    initialize()

st.markdown(
    f'<div style="border:2px solid red; padding:10px; font-size: medium; height: 50px; overflow: auto; white-space: pre-wrap;">Welcome to Bible Trivia (Isaiah - Malachi Edition)</div>',
    unsafe_allow_html=True,
)
st.write("\n" * 6)

number_of_questions_to_play = st.session_state.number_of_questions_to_play
questions = st.session_state.questions
if st.session_state.current_question_index < number_of_questions_to_play:
    print(f"Current question index: {st.session_state.current_question_index}")
    question = questions[st.session_state.current_question_index]
    current_question = question["question"]
    current_answer = question["answer"]
    current_question_index = st.session_state.current_question_index

    # If previous question was answered, display the result
    if st.session_state.last_result:
        last_question = st.session_state.last_result["last_question"]
        last_user_answer = st.session_state.last_result["last_user_answer"]
        last_answer = st.session_state.last_result["last_answer"]
        last_result = st.session_state.last_result["last_result"]
        st.markdown(
            f'<div style="border:2px solid red; padding:10px; font-size: medium; height: 200px; overflow: auto; white-space: pre-wrap;">Score: {st.session_state.correct_answers}/{number_of_questions_to_play}\nLast question: {last_question}\nYour answer: {last_user_answer}\nCorrect answer: {last_answer}\nResult: {last_result}</div>',
            unsafe_allow_html=True,
        )
        st.write("\n" * 8)

    st.markdown(f"**Question {current_question_index + 1}:** {current_question}")
    st.write("\n")
    st.session_state.user_answer = st.text_input(
        "Your Answer:",
        key=f"answer_{current_question_index}",
    )

    if st.button("Submit Answer"):
        print(f"User Answer: {st.session_state.user_answer}")
        submit_answer(current_question_index, current_question, current_answer)

# Display final results
if st.session_state.current_question_index >= number_of_questions_to_play:
    st.write("Game Over!")
    st.write(f"Correct Answers: {st.session_state.correct_answers}")
    st.write(f"Incorrect Answers: {st.session_state.incorrect_answers}")

# Use streamlit run bible_trivia.py to run the app
