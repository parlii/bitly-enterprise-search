import tempfile
import json
import os
import streamlit as st
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.llms import VertexAI
from langchain.retrievers import GoogleCloudEnterpriseSearchRetriever
from google.oauth2 import service_account

# Initialize session state for conversation history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

INSTRUCTIONS = "Further instructions: Respond your answer in as much detail as possible. Do not make stuff up, use the summaries to provide a response. Respond in markdown format."

temp_credentials_file = tempfile.NamedTemporaryFile(delete=False)


def main():
    st.title("Retrieval QA Streamlit App")
    question = st.text_input("Enter your question:")

    # Retrieve the conversation history from the session state
    chat_history = st.session_state['chat_history']

    if st.button("Ask"):
        # Pass the question and conversation history to the chain
        result = chain({"question": question})

        # Add the question to the conversation history
        chat_history.append(question)

        # Add the answer to the conversation history (if needed)
        chat_history.append(result["answer"])

        # Display the answer and source documents
        # print(result)
        st.markdown(result["answer"])

        st.subheader("Source Documents")
        for source_document in result["source_documents"]:
            url = source_document.metadata["source"]

            # Check the path to determine the base URL
            if "bitly_bitly_markdown_files" in url:
                base_url = "https://github.com/bitly/bitly/blob/master/"
                url = url.replace(
                    "gs://bitly-enterprise-search-docs/bitly_bitly_markdown_files/", "")
            elif "prepared_data_clean_plus_summary" in url:
                base_url = "https://github.com/bitly/docs/blob/master/"
                url = url.replace(
                    "gs://bitly-enterprise-search-docs/prepared_data_clean_plus_summary/", "")
            else:
                # Handle other cases or unknown URLs if needed
                base_url = ""

            # Modify the URL as per your previous logic
            url = url.replace("--", "/")
            url = url.replace(".txt", ".md")

            # Construct the complete GitHub URL
            github_url = f"{base_url}{url}"

            # st.markdown(f"[{github_url}]({github_url})")
            st.link_button(github_url, github_url)

        expander = st.expander("See full json response")
        expander.write(result)

    # Update the session state with the new conversation history
    st.session_state['chat_history'] = chat_history


def create_secrets_file():
    try:
        # Extract the credentials from st.secrets
        credentials_data = st.secrets["connections"].gcs

        # Write the credentials data to the temporary file
        with open(temp_credentials_file.name, 'w') as file:
            json.dump(credentials_data, file)

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_credentials_file.name
    except Exception as e:
        st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    create_secrets_file()
    # Create API client.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["connections"].gcs
    )

    retriever = GoogleCloudEnterpriseSearchRetriever(
        project_id=st.secrets["PROJECT_ID"],
        search_engine_id=st.secrets["SEARCH_ENGINE_ID"],
        max_documents=3,
        credentials=credentials
    )

    parameters = {
        "temperature": 0,
        "max_output_tokens": 2000,
        "model_name": "text-bison@latest"
    }

    llm = VertexAI(**parameters, credentials=credentials)

    chain = RetrievalQAWithSourcesChain.from_llm(
        llm=llm, retriever=retriever, return_source_documents=True)

    # chain = RetrievalQAWithSourcesChain.from_chain_type(
    #     llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

    main()
    # At the end of your code or when the credentials are no longer needed
    os.unlink(temp_credentials_file.name)
