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
try:
    key = st.sidebar.text_input("Free trial - Please enter your account access phrase.", type="password")

    image = Image.open('PICTURES/output-onlinepngtools1.png')

    st.image(image,output_format='PNG', width=100)
    openai.api_key = key
    if key is not None:
        st.write("This version only supports .docx and .rtf files")
        uploaded_file = st.file_uploader("Choose a file to upload. Documents over 1,000 words may fail to summarise or answer questions. Please contact bseota@gmail.com for an account upgrade.")
        
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
                st.subheader("Questions")
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
                    answer = answer.replace("???", "\n???")
                    st.write(answer)

                st.subheader("Summary section (optional)*")
                st.write("If your document is a case, you may click the below button to summarise the uploaded document. If it is not a case, this function may not work as expected")
                
                
                choose_numWords = st.number_input("How many words do you want in your summary?")
                choose_numWords = round(choose_numWords)
                if st.button("Click to Summarise"):
                    summary = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=f"Write a summary and key findings of the following text under the headings 'SUMMARY', 'KEY FINDINGS', and 'KEY DATES AND EVENTS'. These three sections should total {choose_numWords} words. Write briefly, formally, and in bullet points. \n\n {document}",
                        temperature=0.,
                        max_tokens=1100,
                    
                    )
                    summary = summary["choices"][0]["text"]
                    summary = summary.replace("???", "\n???")
                    st.write(summary)
except:
    pass
            