import os
import json
import pandas as pd
import traceback
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
KEY = os.getenv("OPENAI_API_KEY")
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from langchain.document_loaders import PyPDFLoader
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging


# data = PyPDFLoader("./javase8.pdf")
# page = data.load_and_split()
# req_data = page[47:55]
client = ChatOpenAI(openai_api_key = KEY, model = "gpt-3.5-turbo",temperature = 0.2)
generate_template = """
using the below data generate me {number_of_questions} with a {level} difficulty level.
{data} generate me output in the below format 
{format}
"""

generate_mcq_prompt = PromptTemplate(
    input_variables=["data","number_of_questions","level","format"],
    template= generate_template
)

generate_mcq_chain = LLMChain(llm = client, prompt=generate_mcq_prompt, output_key="base_mcq")

validate_template_prompt = """
validate these mcqs {base_mcq} are they correct. 
if there are any mistakes in the {base_mcq} correct them and return all the mcqs in a json format, 
including the {base_mcq} and the corrected mcq

"""

validate_mcq_prompt = PromptTemplate(
    input_variables=["base_mcq"],
    template= validate_template_prompt
)

validate_mcq_chain = LLMChain(llm = client, prompt= validate_mcq_prompt, output_key="final_mcq")

mcqs = SequentialChain(chains= [generate_mcq_chain, validate_mcq_chain],input_variables=["data","number_of_questions","level","format"],output_variables=["base_mcq","final_mcq"])




# response = mcqs({"data" : req_data, "number_of_questions" : "5", "level" : "Easy" , "format" : format})

# mcq_questions = json.loads(response["final_mcq"])

# questions = []
# for question in mcq_questions:
#    questions.append(mcq_questions[question])

# csv = pd.DataFrame(questions)

# with get_openai_callback() as callback:
#     response = mcqs({"data" : req_data, "number_of_questions" : "5", "level" : "Easy" , "format" : format})

# csv.to_csv("questions.csv")