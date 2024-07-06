from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain import PromptTemplate, LLMChain
from langchain.llms import Cohere
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0.5,openai_api_key=openai_api_key)

# llm=Cohere(temperature=0.5)

st.title("ChatBot for Book Search")

input_text = st.text_input("Enter any genre to search top 100 books")

template = """Please provide a simple list of hundred well-known
                books that center around the theme of {theme}.
                Do not include book description"""

book_name_prompt_template = PromptTemplate(
    input_variables=["theme"],
    template= template
)

book_name_chain = LLMChain(llm=llm,
                           prompt = book_name_prompt_template,
                           output_key="list_of_book_names")

if input_text:
  response = book_name_chain.run({"theme": input_text})
  book_list = response.split("\n")  # Assuming books are separated by newlines
  top_10_books = book_list[:10]  # Take the first 10 books
  st.write("Here are the top 10 books:")
  book_selection = st.selectbox("Select a book to get its summary:", top_10_books)

  if book_selection:
      summary_template = """Please provide a brief summary of the book titled "{book_name}"."""
      summary_prompt_template = PromptTemplate(
          input_variables=["book_name"],
          template=summary_template
      )

      summary_chain = LLMChain(
          llm=llm,
          prompt=summary_prompt_template,
          output_key="summary"
      )

      summary_response = summary_chain.run({"book_name": book_selection})
      st.write("Summary of the selected book:")
      st.write(summary_response)