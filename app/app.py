import streamlit as st
import openai

# Load OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else ""

# --- App Title and Description ---
st.title("Study Buddy: Your Friendly AI Study Assistant")
st.write("""
Welcome! Study Buddy helps you review course material with empathy, transparency, and control.
Choose a study mode, ask questions, and get clear explanations designed to support your learning journey.
""")

# --- Accessibility settings ---
st.sidebar.header("Accessibility Settings")
text_size = st.sidebar.selectbox("Select Text Size", options=["Small", "Medium", "Large"], index=1)
high_contrast = st.sidebar.checkbox("Enable High Contrast Mode")

if text_size == "Small":
    st.markdown("<style>body { font-size:12px; }</style>", unsafe_allow_html=True)
elif text_size == "Medium":
    st.markdown("<style>body { font-size:16px; }</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>body { font-size:20px; }</style>", unsafe_allow_html=True)

if high_contrast:
    st.markdown("""
        <style>
        body { background-color: black; color: white; }
        .stButton>button { background-color: yellow; color: black; }
        </style>
    """, unsafe_allow_html=True)

# --- User controls ---
st.sidebar.header("Choose Study Mode")
study_mode = st.sidebar.radio("Study Mode", ["Summarize Reading", "Flashcards", "Quiz Questions"], index=0)

st.sidebar.header("Select Topic Difficulty")
difficulty = st.sidebar.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"], index=1)

# --- Input box ---
user_input = st.text_area("Enter your study material or question here:", height=150)

def empathetic_feedback():
    st.info("Keep up the great work! Remember, mistakes are just opportunities to learn.")

def build_prompt(user_text, mode, level):
    return (
        "You are Study Buddy, an empathetic and transparent AI study assistant. "
        "You explain concepts clearly, use supportive language, and help students learn effectively.\n"
        f"Study Mode: {mode}\n"
        f"Difficulty: {level}\n"
        "Instructions: Provide answers, explanations, and highlight key ideas. Use encouraging language.\n\n"
        f"User Input:\n{user_text}"
    )

# ✅ Corrected OpenAI usage for v1.91.0
def query_openai(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful, empathetic educational assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# --- Main app interaction ---
if st.button("Get Help"):
    if not user_input.strip():
        st.warning("Please enter some text or a question to get help.")
    else:
        prompt = build_prompt(user_input, study_mode, difficulty)
        with st.spinner("Study Buddy is thinking..."):
            answer = query_openai(prompt)

        st.subheader("Study Buddy's Response")
        st.write(answer)

        st.markdown("---")
        st.subheader("How Study Buddy Arrived at This Answer")
        st.write(
            "Study Buddy bases its responses on patterns in the text you provide and tries to explain key points clearly. "
            "If anything is unclear, feel free to ask follow-up questions!"
        )
        empathetic_feedback()

# --- Privacy Note ---
st.sidebar.markdown("""
---
**Privacy Notice:** Study Buddy does not store or track your inputs. Your privacy and autonomy are respected.
""")
