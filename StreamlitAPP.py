import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging
import streamlit as st
from src.mcqgenerator.MCQGenerator import mcqs


with open(r"C:\Users\Coditas\Documents\GenAi\freeCodeCampResources\testopenai\projects\mcq\response.json","r") as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQ application")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("upload a pdf or txt file")
    no_of_question = st.number_input("Enter the number of questions",min_value=3,max_value=50)
    level = st.text_input(placeholder="Simple, Medium, Hard",label="level")
    button = st.form_submit_button("Create_MCQ")


    if button and uploaded_file is not None and level and no_of_question:
        with st.spinner("loading"):
            try:
                text = read_file(uploaded_file)
                print(text)
                with get_openai_callback() as callback:
                    response = mcqs({"data" : text, "number_of_questions" : no_of_question, "level" : level , "format" : RESPONSE_JSON})
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            else:
                print(callback)
                if isinstance(response,dict):
                    # print(response)
                    quiz = response.get("final_mcq", None)
                    print((quiz))
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        print(table_data)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label = "Review")
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)  