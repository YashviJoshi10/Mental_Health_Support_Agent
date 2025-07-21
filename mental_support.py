import streamlit as st
import ollama

st.set_page_config(page_title="Mental Health Chatbot")

st.session_state.setdefault("conversation_history",[])

def generate_response(user_input):
    st.session_state["conversation_history"].append({"role":"user","content":user_input})

    response = ollama.chat(model="llama3",messages=st.session_state["conversation_history"])
    ai_response = response["message"]["content"]

    st.session_state["conversation_history"].append({"role":"ai","content":ai_response})
    return ai_response

def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed"
    response=ollama.chat(model="llama3",messages=[{"role":"user","content":prompt}])
    return response["message"]["content"]

def generate_meditation_guide():
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress"
    response=ollama.chat(model="llama3",messages=[{"role":"user","content":prompt}])
    return response["message"]["content"]

st.title("Mental Health Support Agent")

for msg in st.session_state["conversation_history"]:
    role="You" if msg["role"]=="user" else "AI"
    st.markdown(f"{role} : {msg['content']}")

user_message =  st.text_input("How can I help you today")

if user_message:
    with st.spinner("thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"AI : {ai_response}")

col1,col2,col3 = st.columns(3)

with col1:
    if st.button("Give me a positive affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"Affirmation:{affirmation}")

with col2:
    if st.button("Give me a guided meditation"):
        meditation = generate_meditation_guide()
        st.markdown(f"meditation:{meditation}")

with col3:
    if st.button("Mental health test"):
        st.session_state["show_test"]=True

if st.session_state.get("show_test"):
    st.header("Mental Health Assesment")

    st.markdown("Please answer the following questions about how you've been feeling over the **past 2 weeks**:")

    questions = [
        "Have you been finding it hard to enjoy things you used to like?",
        "Have you been feeling really down, sad, or empty most of the time?",
        "Are you having trouble sleeping — either too much or not enough?",
        "Do you feel constantly tired, even after resting?",
        "Have your eating habits changed a lot (eating too much or too little)?",
        "Have you been feeling bad about yourself, like you're not good enough?",
        "Is it harder than usual to focus on tasks, like reading or watching shows?",
        "Do you feel like you're moving slower than usual or struggling to get going?",
        "Do you feel disconnected from people or things around you?",
    ]

    options = ["Not at all (0)", "Several days (1)", "More than half the days (2)", "Nearly every day (3)"]
    scores = []

    for index,ques in enumerate(questions):
        response=st.radio(f"{index+1}. {ques}", options, key=f"q{index}")
        score = int(response[-2])
        scores.append(score)

    if st.button("Submit"):
        total_score=sum(scores)

        if total_score <= 4:
            result = "You're feeling normal — keep taking care of your well-being. "
        elif total_score <= 9:
            result = "You seem a bit tensed — try to slow down and give yourself a break. "
        elif total_score <= 14:
            result = "You're feeling stressed — it's okay to ask for help or take some time for yourself. "
        elif total_score <= 19:
            result = "You're quite overwhelmed — talking to someone might really help. "
        else:
            result = "You're likely feeling depressed — you're not alone, and support is available. "


        st.success(f"Your total score is: {total_score}")
        st.info(f"Assessment result: **{result}**")

        st.markdown("""
        *Note:* This test is a basic screening tool and not a diagnosis. 
        If you're struggling, consider speaking with a mental health professional.
        """)