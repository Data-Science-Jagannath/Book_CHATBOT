import openai
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

# from langchain_core.prompts import ChatPrompt

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable in the .env file.")
else:
    # Initialize OpenAI model
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)

    # Define prompt template for listing books
    # prompt_template = ChatPromptTemplate.from_messages(
    #     [
    #         ("system", "You are a helpful assistant. Please provide a list of the top 100 books in the {theme} genre."),
    #         ("user", "Question:{context}")
    #     ]
    # )

    
    # Initialize Streamlit app
    st.title('Book Chatbot')

    # User input for the genre
    input_genre = st.text_input("Enter the genre you want to search for top 100 books:")

    if input_genre:
        # Create prompt for the genre
        prompt = f"You are a helpful assistant. Please provide a list of the top 100 books in the {input_genre} genre."

        # Invoke the OpenAI model to get the list of top 100 books
        output_parser = StrOutputParser()
        chain = ChatPromptTemplate(prompt) | llm | output_parser
        response = chain.invoke()

        # Display the list of top 100 books
        books = response['text'].split('\n')
        st.subheader(f"Top 100 books in {input_genre} genre")
        st.write(books)

        # Filter top 10 books from the list
        top_10_books = books[:10]
        st.subheader("Top 10 books from the list")
        for i, book in enumerate(top_10_books, start=1):
            st.write(f"{i}. {book}")

        # User selects a book from the top 10
        selected_book = st.selectbox("Select a book from the top 10", top_10_books)

        if selected_book:
            st.write(f"You selected: {selected_book}")
            st.write("Thank you for using the Book Chatbot!")
