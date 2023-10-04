import streamlit as st
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.llms import VertexAI
from langchain.retrievers import GoogleCloudEnterpriseSearchRetriever
from langchain.prompts import PromptTemplate
import os

# Initialize session state for conversation history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

INSTRUCTIONS = "Further instructions: Respond your answer in as much detail as possible. Do not make stuff up, use the summaries to provide a response. Respond in markdown format."

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
                url = url.replace("gs://bitly-enterprise-search-docs/bitly_bitly_markdown_files/", "")
            elif "prepared_data_clean_plus_summary" in url:
                base_url = "https://github.com/bitly/docs/blob/master/"
                url = url.replace("gs://bitly-enterprise-search-docs/prepared_data_clean_plus_summary/", "")
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

if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/drizal/parli/keys/bitly-ai-experiments-f0eacba17094.json"
    
    PROJECT_ID = "bitly-ai-experiments"  # Set to your Project ID
    SEARCH_ENGINE_ID = "bitly-docs-enterprise-sear_1696274081167"  # Set to your data store ID

    retriever = GoogleCloudEnterpriseSearchRetriever(
        project_id=PROJECT_ID,
        search_engine_id=SEARCH_ENGINE_ID,
        max_documents=3,
    )

    parameters = {
    "temperature": 0,
    "max_output_tokens": 2000,
    "model_name":"text-bison@latest"
    }

    chain = RetrievalQAWithSourcesChain.from_chain_type(
    VertexAI(**parameters), chain_type="stuff", retriever=retriever, return_source_documents = True)

    main()
