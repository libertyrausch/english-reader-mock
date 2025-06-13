import streamlit as st
import random

# Sample passages data (1 full English passage for now)
passages_data = [
    {
        "title": "The Rise of Urban Gardening",
        "level": "Intermediate High",
        "text": [
            "Urban gardening has gained significant popularity in recent years as people seek more sustainable and health-conscious lifestyles. In densely populated cities, where green spaces are often limited, individuals and communities are turning to creative solutions to grow their own food. Whether it's a rooftop garden, a balcony herb planter, or a shared community plot, urban gardening allows people to reconnect with nature and enjoy the fruits (and vegetables) of their labor.",
            "One major benefit of urban gardening is the ability to produce fresh, organic food locally. This not only reduces the environmental impact associated with transporting produce over long distances but also provides access to healthier food options in areas that might otherwise lack them. In many urban neighborhoods, especially those labeled as food deserts, residents struggle to find affordable, nutritious food. Community gardens have become a way to address these issues, fostering food security and encouraging neighbors to collaborate.",
            "Moreover, urban gardening promotes mental well-being. Studies have shown that spending time around plants and engaging in gardening activities can reduce stress and improve mood. For people living in concrete-heavy urban environments, even a small garden can offer a peaceful refuge from the hustle and bustle of city life. Gardening also fosters a sense of responsibility and accomplishment, especially when people watch their plants thrive under their care.",
            "However, urban gardening also comes with challenges. Limited space can make it difficult to grow large quantities of food, and gardeners must be resourceful in using vertical space or container systems. Soil quality in cities may be poor or even contaminated, requiring raised beds and imported soil. Access to water, pests, and municipal regulations can also create obstacles.",
            "Despite these challenges, the urban gardening movement continues to grow. Cities are beginning to recognize the benefits and are implementing policies that support gardening initiatives, such as allowing vacant lots to be converted into community gardens or offering tax incentives for green rooftops. Urban gardening reflects a growing awareness of sustainability and the desire for a closer connection to what we eat. As more people dig in and start growing, the concrete jungle might just become a little greener."
        ],
        "questions": [
            {"type": "multiple_choice", "question": "What is one benefit of urban gardening mentioned in the text?", "options": ["It increases food transport", "It provides fresh, local food", "It eliminates the need for water"], "answer": "It provides fresh, local food"},
            {"type": "true_false", "question": "Urban gardening is beneficial for mental health.", "answer": True},
            {"type": "short_answer", "question": "Name one challenge urban gardeners face.", "answer": "Limited space"}
        ]
    }
]

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
