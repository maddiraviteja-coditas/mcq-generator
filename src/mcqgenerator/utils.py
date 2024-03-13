import json 
import PyPDF2
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            print(text)
            return text
        
        except Exception as e:
            raise Exception("Error Reading the file")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception("file format not supported")


def get_table_data(quiz_str):
    try:
        quiz_str = quiz_str.replace("'",""" " """)
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        for question in quiz_dict:
            quiz_table_data.append(quiz_dict[question])
        return quiz_table_data
    except Exception as e:
       traceback.print_exception(type(e), e, e.__traceback__)
       return False 
    