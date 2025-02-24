# GroundX AI Document Query Project

## Author

* **Name:** Muneer Iqbal**
* **Email:** muneeriqbal729@gmail.com

## Overview

This project leverages GroundX AI for document storage and retrieval, combined with Google’s Gemini Pro model for generating intelligent, context-aware responses. The core idea is to create a system where documents are uploaded to a GroundX bucket, accessed via Python code using an API key and bucket ID, and then processed to answer user queries. The project demonstrates a practical application of AI-driven document management and natural language processing, enabling users to extract meaningful insights from stored documents efficiently.
You just upload the user's resume and ask the questions about the resume.and many more questions.about other any type of the documents.you can upload 10 types of the documents.the model will trained automatically on your documents.

## Objectives

* **Document Management:** Use GroundX AI to create a bucket, upload documents, and retrieve content programmatically.
* **Query Processing:** Allow users to submit queries about the documents and receive detailed, contextually relevant responses.
* **Response Generation:** Integrate the Gemini Pro model to generate human-like answers based on document content retrieved from GroundX.

## Technologies Used

* **GroundX AI:** A platform for storing and searching documents, providing an API to access bucket contents.
[GroundX AI Dashboard](https://dashboard.eyelevel.ai/)
* **Gemini Pro Model:** Google’s multimodal AI model (via the `google-generativeai` library) for generating responses.
* **Python:** The programming language used to orchestrate API calls, process data, and build the application.
* **Streamlit:** A Python library used to create an interactive web-based UI for user input and response display.
* **dotenv:** For securely managing API keys via a `.env` file.

## Implementation Details

### GroundX AI Setup
[GroundX AI Dashboard](https://dashboard.eyelevel.ai/)
* **Bucket Creation:**
    * A bucket was created in GroundX AI to store documents. In this project, a single bucket with ID `15876` is used.
* **Document Upload:**
    * Documents (e.g., a PDF named `t-short.pdf`) were uploaded to this bucket, making them accessible for search and retrieval.
* **API Access:**
[GroundX AI Dashboard](https://dashboard.eyelevel.ai/)
    * An API key (`661d1241-7ccb-4260-a7c45`) is used to authenticate requests to GroundX.
    * The Python code accesses the bucket using the GroundX library:

        ```python
        groundx = GroundX(api_key=GROUNDX_API_KEY)
        content_response = groundx.search.content(id=15876, query=query)
        ```

* **Content Retrieval:**
    * The `search.content` method retrieves text from the bucket based on the user’s query.
    * The response includes a score (e.g., 381.88), indicating relevance, and text, which is the extracted document content.

### Gemini Pro Integration

* **Model Configuration:**
    * The Gemini Pro model (`gemini-pro`) is initialized using the `google-generativeai` library:

        ```python
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-pro")
        ```

    * An instruction is provided to ensure responses are detailed and based on the document content:

        ```python
        instruction = "You are a helpful virtual assistant that answers questions using the content below. Your task is to create detailed answers to the questions by combining your understanding of the world with the content provided below. Do not share links."
        ```

* **Response Generation:**
    * The retrieved GroundX content (`llm_text`) is combined with the user query and instruction into a prompt:

        ```python
        prompt = f"{instruction}\n===\n{llm_text}\n===\n{query}"
        response = model.generate_content(prompt)
        ```

    * Gemini Pro generates a natural-language response based on this prompt.

### Streamlit UI

* The project uses Streamlit to create an interactive web interface:
    * Users enter queries via `st.chat_input`.
    * Responses are displayed in a chat-like format with `st.chat_message`.
* **Example:**

    ```python
    query = st.chat_input("Enter your query here (e.g., 'Tell about Muneer Iqbal CGPA')")
    if query:
        with st.chat_message("assistant"):
            response_text = f"**Result:**\n{response.text}\n\n**Score:** {normalized_score:.2f}"
            st.markdown(response_text)
    ```

### Score Normalization

* GroundX returns a raw relevance score (e.g., 381.88), which was normalized to a 0–1 range for better interpretability:
    * Assumed a maximum score of 500:

        ```python
        max_score = 500
        normalized_score = min(raw_score / max_score, 1.0)
        ```

    * Displayed as `Score: 0.76` for a raw score of 381.88.

### Workflow

* **User Input:** A user submits a query (e.g., "Tell about Muneer Iqbal CGPA") via the Streamlit UI.
* **GroundX Search:** The query is sent to GroundX, which searches the bucket (ID: 15876) and returns relevant text and a score.
* **Gemini Processing:** The retrieved text is fed into Gemini Pro, which generates a detailed response.
* **Output:** The response and normalized score are displayed in the Streamlit chat interface.

### Example Output

* **Query:** "Tell about Muneer Iqbal CGPA"

* **Response:**

    ```
    **Result:**
    Muneer Iqbal is a student with a CGPA of 3.8, reflecting strong academic performance...

    **Score:** 0.76
    ```

### Key Features

* **Document-Specific Answers:** Responses are grounded in the uploaded document, not generic knowledge.
* **Interactive UI:** Streamlit provides a user-friendly way to interact with the system.
* **Secure API Management:** API keys are stored in a `.env` file and loaded with dotenv.

### Challenges and Solutions

* **Raw Score Interpretation:** GroundX’s unnormalized score (e.g., 381.88) was confusing. Normalized it to 0–1 for clarity.
* **Scope Limitation:** Initially, GroundX returned all document content. Adjusted queries (e.g., "Muneer Iqbal CGPA") to filter results more precisely.
* **UI Errors:** Fixed a `NameError` by removing premature access to `content_response` outside the query block.

### Future Enhancements

* **Dynamic Max Score:** Track the highest observed score to improve normalization accuracy.
* **Multi-Document Support:** Extend to multiple buckets or documents for broader querying.
* **Error Handling:** Add `try-except` blocks for API failures or invalid queries.
* **Advanced Filtering:** Enhance GroundX query precision with additional parameters if supported.

### Conclusion

This project showcases a powerful combination of GroundX AI for document management and Gemini Pro for response generation, wrapped in a Streamlit UI. It provides a scalable foundation for building document-based query systems, with potential applications in education, research, or customer support.