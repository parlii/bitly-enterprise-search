# Retrieval QA Streamlit App

This Streamlit application assists Bitly Engineers in searching internal documentation. The app leverages Google's Enterprise Search DB and Vertex AI LLM for precise and efficient results.

## Overview

Given a question, the app:

- Searches internal documents.
- Retrieves relevant answers and their source documents.
- Constructs URLs to the exact documentation where the answer originates.

## Setup

1. **Environment Variables**: Ensure that the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set to the path of your Google Cloud credentials JSON file.

2. **Dependencies**: The app utilizes multiple custom libraries including `langchain`. Make sure to install all the required libraries.

## Usage

1. **Launch the Streamlit App**: Use the command `streamlit run <filename>.py`.
2. **Input**: Enter your question in the provided text field.
3. **Query**: Click the "Ask" button to query the internal documentation.
4. **Results**: The app will display the most relevant answer, sourced from the internal documents.
5. **Source Documents**: For each answer, a link to the source document will be provided. This will direct you to the exact GitHub file from either the `bitly` or `docs` repository.

## Note

Please remember to respond in markdown format and adhere to the instructions provided in the app, including providing answers in as much detail as possible without deviating from the source summaries.

## Support

For any issues, questions, or recommendations, please reach out to Parli.
