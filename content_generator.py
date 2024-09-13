import os
import json
import re
import warnings
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import (ChatPromptTemplate, FewShotChatMessagePromptTemplate)
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_community.utils.openai_functions import (convert_pydantic_to_openai_function)
from utils.data_validation import SlideContentJSON
from utils.prompts import instruction_example, instruction_example_prompt, instruction_prompt, generation_prompt, generation_example, generation_prompt_example

# Old branch code



def configure_llm(TEMPERATURE=0,LLM_MODEL='gpt-3.5-turbo', print_API_KEY=True):
     model = ChatOpenAI(
       model_name=LLM_MODEL, 
       temperature=TEMPERATURE,
       )
     if print_API_KEY:
         print(os.environ['OPENAI_API_KEY'])
     return model

def generate_slide_summary(model, content_json):
    summary = "[There is no previous slide in the presenation to make a summary.]"
    if content_json is not None:
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
        try:
            summary = chain.invoke({"content": content_json})
            print(f"🟢 (2/5) Generated slide summary of current slide")
        except:
            print(f"🔴 ERROR: Could not generate slide summary of current slide")
    else:
        print(f"🟢 (2/5) No summaries to generate for first slide of the presentation")


    return summary

def generate_insights(model, curr_slide_summary, disc_transcript):
    example_prompt = ChatPromptTemplate.from_messages(
            instruction_example_prompt
        )

    few_shot_prompt = FewShotChatMessagePromptTemplate(
            examples=instruction_example,
            example_prompt=example_prompt
        )
    
    prompt = ChatPromptTemplate.from_messages(
            [
                ('system', 'You are a helpful assistant. You have access to the internet'),
                few_shot_prompt,
                instruction_prompt

            ]
        )
    slide_templates = ['introduction', 'content', 'example', 'comparision', 'summary']
    elements = ['description', 'enumeration', 'url', 'tables', 'equations', 'diagram']
    chain = prompt | model 
    output = chain.invoke({"transcript": disc_transcript, "summary": curr_slide_summary, "slide_templates": slide_templates, "elements": elements})
    # dict_output = json.loads(output.content)

    try:
        output = chain.invoke({"transcript": disc_transcript, "summary": curr_slide_summary, "slide_templates": slide_templates, "elements": elements})
        dict_output = json.loads(output.content)
        print(f"🟢 (3/5) Constructed insights from the discussion and current slide summary")
    except:
        print(f"🔴 ERROR: Could not generate insights from discussion")

    return dict_output["output"]

def generate_content(model, instructions, curr_slide_summary):
    example_prompt = ChatPromptTemplate.from_messages(
            generation_prompt_example
        )

    few_shot_prompt = FewShotChatMessagePromptTemplate(
            examples=generation_example,
            example_prompt=example_prompt
        )
    
    prompt = ChatPromptTemplate.from_messages(
            [
                ('system', 'You are a helpful assistant. You have access to the internet'),
                few_shot_prompt,
                generation_prompt

            ]
        )
    with warnings.catch_warnings(action="ignore"):
        openai_functions = [convert_pydantic_to_openai_function(SlideContentJSON)]
        parser = JsonOutputFunctionsParser()
        model = ChatOpenAI(
        model_name='gpt-4-turbo', 
        temperature=0,
        )
        chain = prompt | model.bind(functions=openai_functions) | parser
        # chain = prompt | model.bind(functions=openai_functions)

        try:
            output = chain.invoke({"instructions": instructions, "summary": curr_slide_summary})
            print(f"🟢 (4/5) Generated content for the next slide")
        except:
            print(f"🔴 ERROR: Could not generate content for the next slide")

   
    return output 

def find_current_slide_number(path):
    files = os.listdir(path)
    txt_files = [file for file in files if re.match(r'\d+\.txt', file)]
    numbers = [int(re.match(r'(\d+)\.txt', file).group(1)) for file in txt_files]
    max_number = max(numbers) if numbers else None
    return max_number

def generate_next_slide(content_json, transcript):
    model = configure_llm()
    curr_slide_summary = generate_slide_summary(model, content_json)
    nxt_slide_instructs = generate_insights(model, curr_slide_summary, transcript)
    nxt_slide_content = generate_content(model, nxt_slide_instructs, curr_slide_summary)
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
    PRESENTATION_ID = 1234
    TRANSCRIPTS_PATH = f'output/buffer/transcripts'
    slide_num = find_current_slide_number(TRANSCRIPTS_PATH)
    load_dotenv(find_dotenv())
    print("\nRunning Content Generation Module...")
    CURR_SLIDE_PATH = f'data/1234.json'
    if os.path.exists(CURR_SLIDE_PATH):
        content_json = fetch_seed_content(CURR_SLIDE_PATH)
    else:
        content_json = {
            'presentation_ID': PRESENTATION_ID,
            'topic': 'Heap',
            'slides': []
            }
        
    try:
        transcript = fetch_transcript(os.path.join(TRANSCRIPTS_PATH, f'{slide_num}.txt'))
        print(f"🟢 (1/5) Successfully fetched transcript for slide {slide_num}")
    except:
        print(f"🔴 ERROR: Could not fetch trancript for slide {slide_num}")
    

    if content_json["slides"] != []:
        next_slide_content = generate_next_slide(content_json["slides"][-1], transcript)
    else:
        next_slide_content = generate_next_slide(None, transcript)

    content_json["slides"].append(next_slide_content)
    OUTPUT_PATH = 'output/buffer/content_json/'
    try:
        save_slide_content_to_json(content_json, os.path.join(OUTPUT_PATH, f'{PRESENTATION_ID}.json'))
        print(f"🟢 (5/5) Saved content to {OUTPUT_PATH}")
    except:
        print(f"🔴 ERROR: Could not save content to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
