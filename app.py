import streamlit as st
import random
from english_passages import passages_data

st.set_page_config(page_title="English Reading Comprehension App")

if "current_passage" not in st.session_state:
    st.session_state.current_passage = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

st.title("📘 English Reading Comprehension")

passage = passages_data[st.session_state.current_passage]
st.subheader(passage["title"])
st.markdown(f"**Difficulty Level:** {passage['level']}")

for paragraph in passage["text"]:
    st.write(paragraph)

st.markdown("---")
st.subheader("Comprehension Questions")

for i, q in enumerate(passage["questions"]):
    key = f"q{st.session_state.current_passage}_{i}"
    if q["type"] == "multiple_choice":
        user_answer = st.radio(q["question"], q["options"], key=key, index=None)
    elif q["type"] == "true_false":
        user_answer = st.radio(q["question"], ["True", "False"], key=key, index=None)
    elif q["type"] == "short_answer":
        user_answer = st.text_input(q["question"], key=key)
    else:
        user_answer = None
    st.session_state.answers[key] = user_answer

if st.button("Check Answers"):
    correct = 0
    for i, q in enumerate(passage["questions"]):
        key = f"q{st.session_state.current_passage}_{i}"
        user = st.session_state.answers.get(key, "")
        correct_answer = q["answer"]
        if isinstance(correct_answer, bool):
            user = True if user == "True" else False
        elif isinstance(correct_answer, str):
            user = user.strip().lower()
            correct_answer = correct_answer.strip().lower()
        if user == correct_answer:
            correct += 1
    st.session_state.score += correct
    st.success(f"You got {correct} out of {len(passage['questions'])} correct.")

if st.button("Next Passage"):
    if st.session_state.current_passage < len(passages_data) - 1:
        st.session_state.current_passage += 1
        st.session_state.answers = {}
        st.rerun()
    else:
        st.info("You’ve completed all passages!")

st.markdown("---")
st.caption(f"Progress: Passage {st.session_state.current_passage + 1} of {len(passages_data)} | Score: {st.session_state.score}")
