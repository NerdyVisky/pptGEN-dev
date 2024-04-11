import os
import json
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import (PromptTemplate, ChatPromptTemplate)
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.utils.openai_functions import (convert_pydantic_to_openai_function)
from utils.data_validation import SlideContentJSON


def configure_llm(TEMPERATURE=0,LLM_MODEL='gpt-3.5-turbo'):
     model = ChatOpenAI(
       model_name=LLM_MODEL, 
       temperature=TEMPERATURE,
       )
     return model

def generate_slide_summary(model, content_json):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant to the professor. Your job is provide summary of slides from the content provided by the professor"),
            ("human", """
             I am providing you with a python dictionary which describes the content of a presentation slide in the following manner:\n.
             slide_number : Represents the relative numbering of the slide in the presentation.\n
             title : The title of the slide.\n
             description : Body content of the slide in form of a descriptive paragraph.\n
             enumeration : Body content of the slide in form of bullet points.
             equations : Description and LaTeX code related to mathematical equation described in the slide. Here tex_code is the LaTeX code of the equation and eq_desc is the caption for the equation.\n
             tables : Description and LaTeX code related to tables described in the slide. Here tex_code is the LaTeX code of the table and tab_desc is the caption for the tables.
             figures : Figure type and Description of figures provided in the slide.\n

             Keep in mind that some elements in the dict might be empty as the slide may not contain all elements.\n
             Now I want you to carefully analyze this dictonary object by understanding the content of each element and provide a textual summary of not more than 100 words on what the slide as a whole describes.\n 
             Make sure the summary is as descriptive as possible and can completely summarize the content of the slide\n
             Here is the content dict for the slide:\n
             {content}
             """)
        ]
        )
    parser = StrOutputParser()
    chain = prompt | model | parser
    summary = chain.invoke({"content": content_json})
    print(summary)
    return summary

def generate_content(model, curr_slide_summary, disc_transcript):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant to the professor. Your job is to generate the content for the next slide in a presentation based on the current slide and the transcript of the discussion on the current slide."),
            ("human", """
             I am providing you the summary of the current presentation slide and the corresponding transcript of the discussion that took place while presenting the slide.\n
             Your job is analyze the conversation and the context of discussion using the transcript and current slide summary to generate the content of the next slide.\n
             The discussion is provided in raw string format with no entity recognition as to who is speaking, hence you will have to extract information as to what content is requested for the next slide.\n
             You have to generate the content in form of a JSON object, where:
             slide_number : Represents the relative numbering of the slide in the presentation.\n
             title : The title of the slide.\n
             description : Body content of the slide in form of a descriptive paragraph.\n
             enumeration : Body content of the slide in form of bullet points.
             equations : Description and LaTeX code related to mathematical equation described in the slide. Here tex_code is the LaTeX code of the equation and eq_desc is the caption for the equation.\n
             tables : Description and LaTeX code related to tables described in the slide. Here tex_code is the LaTeX code of the table and tab_desc is the caption for the tables.\n
             
             While generating content for equations and tables, also provide the Tex code and Description to render it in the presentation.\n
             The summary of current slide being discussed:\n
             {slide_summary}
             \n
             The transcript of the discussion on current slide:\n
             {transcript}
             \n
             """)
        ]
        )
    openai_functions = [convert_pydantic_to_openai_function(SlideContentJSON)]
    parser = JsonOutputFunctionsParser()
    chain = prompt | model.bind(functions=openai_functions) | parser
    nxt_slide_obj = chain.invoke({"slide_summary": curr_slide_summary, "transcript": disc_transcript})
    print(nxt_slide_obj)
    return nxt_slide_obj


def generate_next_slide(content_json, transcript):
    model = configure_llm()
    curr_slide_summary = generate_slide_summary(model, content_json)
    nxt_slide_content = generate_content(model, curr_slide_summary, transcript)
    return nxt_slide_content

def fetch_transcript(trs_file_path):
    with open(trs_file_path, 'r') as file:
        transcript = file.read()
    return transcript
        
def fetch_seed_content(json_file_path):
    with open(json_file_path, 'r') as file:
        slide_seed = json.load(file)
    return slide_seed

def save_slide_content_to_json(slide_content, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(slide_content, json_file, indent=3)


def main():
    slide_num = 1
    load_dotenv(find_dotenv())
    print(os.environ['OPENAI_API_KEY'])
    PREV_SLIDE_PATH = f'data/{slide_num}.json'
    TRANSCRIPTS_PATH = f'output/buffer/transcripts/{slide_num}.txt'
    content_json = fetch_seed_content(PREV_SLIDE_PATH)
    # transcript = """
    # I have a doubt related to Gaussian Distributions.
    # Sure, ask.
    # I am confused between Culminative Density Function and Probibility function, can you explain the difference between them?
    # Sure, I can, but let me know what kind of difference you would like to know.
    # Yes, so if you can provide and differenciate the definitions between the two. 
    # I see, should I also provide mathematical expressions for each, will that help to differenciate between them?
    # Yes that would be quite helpful.
    # Sure, the next slide will have the difference between the two and differnciate their mathematical expressions.
    # """
    transcript = fetch_transcript(TRANSCRIPTS_PATH)
    print(transcript)

    next_slide_content = generate_next_slide(content_json["slides"][-1], transcript)
    content_json["slides"].append(next_slide_content)
    OUTPUT_PATH = 'output/1.json'
    save_slide_content_to_json(content_json, OUTPUT_PATH)

if __name__ == "__main__":
    main()
