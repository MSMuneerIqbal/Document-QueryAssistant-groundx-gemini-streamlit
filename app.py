import streamlit as st
import google.generativeai as genai
from groundx import GroundX

# Access API keys from st.secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
GROUNDX_API_KEY = st.secrets["GROUNDX_API_KEY"]

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize GroundX with API key from secrets
groundx = GroundX(api_key=GROUNDX_API_KEY)

# Set up the Gemini model
model = genai.GenerativeModel("gemini-pro")

# Instruction for the model
instruction = "You are a helpful virtual assistant that answers questions using the content below. Your task is to create detailed answers to the questions by combining your understanding of the world with the content provided below. Do not share links."

# Streamlit UI setup
st.title("Document Query Assistant")
st.write("Ask a question about Muneer Iqbal")

# Chat input for user query
query = st.chat_input("Enter your query here (e.g., 'who is muneer iqbal')")

# Placeholder for chat-like conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle query submission
if query:
    # Display user query in chat
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # Get content from GroundX (using the query to filter content)
    content_response = groundx.search.content(id=15876, query=query)
    results = content_response.search
    llm_text = results.text
    raw_score = results.score

    # Normalize the score to 0-1 (assuming max score of 500)
    max_score = 500  # Adjust based on GroundX's actual max score if known
    normalized_score = min(raw_score / max_score, 1.0)

    # Prepare the prompt for Gemini
    prompt = f"""{instruction}
===
{llm_text}
===
{query}"""

    # Generate response using Gemini
    with st.spinner("Generating response..."):
        response = model.generate_content(prompt)

    # Display assistant response in chat
    with st.chat_message("assistant"):
        response_text = f"**Result:**\n{response.text}\n\n**Score:** {normalized_score:.2f}"
        st.markdown(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})
