import streamlit as st
import openai
import textract
from io import StringIO 
import pandas as pd
import os
import tempfile
import shutil
from PIL import Image
hide_streamlit_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
image = Image.open('PICTURES/output-onlinepngtools1.png')

st.image(image,output_format='PNG', width=100)
openai.api_key = "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"

uploaded_file = st.file_uploader("Choose a file to upload - limit approximately 1,300 words")

if uploaded_file:
    file = tempfile.NamedTemporaryFile(delete=False)
    file_path = file.name
    shutil.copyfileobj(uploaded_file, file)
    file.close()
    # st.write(f"File path: {file_path}")
    file_path = file_path.replace("\\", "/")
    # st.write(f"File path: {(file_path)}")
    if '.docx' in uploaded_file.name:
        os.rename(file_path, f"{file_path}.docx")
        document = textract.process(f"{file_path}.docx")
    elif '.rtf' in uploaded_file.name:
        os.rename(file_path, f"{file_path}.rtf")
        document = textract.process(f"{file_path}.rtf")
    document = document.decode("utf-8") 
    document = document.replace("\\n", " ")
    


    if uploaded_file is not None:
        choose_numWords = st.number_input("How many words do you want in your summary?")
        choose_numWords = round(choose_numWords)
        if st.button("Click to Summarise"):
            summary = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Write a summary and key findings of the following text under the headings 'SUMMARY' and 'KEY FINDINGS'. The 'SUMMARY' and 'KEY FINDINGS' sections should total {choose_numWords} words. Include only 'SUMMARY' and 'KEY FINDINGS'. Write briefly, formally, and in bullet points. \n\n {document}",
                temperature=0.9,
                max_tokens=1100,
            
            )
            summary = summary["choices"][0]["text"]
            summary = summary.replace("•", "\n•")
            st.write(summary)
    
        question = st.text_input("Ask a question about the text.")


        if question:
            # Use openai gpt to answer the user's question
            answer = openai.Completion.create(
                engine="text-davinci-003",
                # engine = "text-curie-001",
                prompt=f"In the following text, {question}\n. Answer briefly, in bullet points, citing where in the text you found the answer: {document}",
                temperature=0.,
                max_tokens=1500, 
                # n=1
            )
            answer = answer["choices"][0]["text"]
            answer = answer.replace("•", "\n•")
            st.write(answer)
        print(type(document))