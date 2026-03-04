import streamlit as st
from rag_query import answer_question

st.title("📚 Student Policy Chatbot (RAG)")

question = st.text_input("Ask something from the document:")
if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        response = answer_question(question)
    st.write(response)
