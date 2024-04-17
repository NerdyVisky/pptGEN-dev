
instruction_example = [
    {
        "transcript": """
        Okay so I have a question regarding caution distributions. You talked about PDF and it's related equation, but I have also heard about CDF quite often associated as well. So exactly what is the difference between the two? Okay, so CDF stands for Culminative Density Function, what do you want me to explain about it? Umm, if you can explain the difference between CDF and PDF and what they represent, also maybe how they differ in equations. Sure, the next slide will provide the same. Next. 
        """,
        "summary": """
        Slide 1: Definition and Characteristics.
        This slide introduces the Gaussian distribution, highlighting its bell-shaped curve defined by mean (mu) and variance (sigma squared). The key parameters determine the center and width of the distribution. It includes the Probability Density Function (PDF) equation for the Gaussian distribution, showcasing the formula for the curve's shape. The slide provides a foundational understanding of the Gaussian distribution's fundamental properties and how mean and variance play a crucial role in defining its shape and characteristics.
        """,
        "elements": """["description", "enumeration", "equations", "tables"]""",
        "reasoning": """
        """,
        "output": """
        {{
         "slide_number": 2,
         "title": PDF v/s CDF,
         "elements": [{{
         "element_type": "description", "element_desc": "A short paragraph differenciating Probability Density Function and Culminative Density Function."
         }},
         {{
         "element_type": "equation", "element_desc": "Mathematical equation of the Probability Density Function"
         }},
         {{
         "element_type": "equation", "element_desc": "Mathematical equation of the Culminative Density Function"
         }}]
        }}
        """
    }
]
instruction_prompt = ("human", """There is a discussion between a lecture presenter and his students. The raw audio transcript of the discussion is as follows:\n\n
                      {transcript}
                      \n\n
                      I am providing you some prior context of the conversation through the summary of the slide in discussion, the summary is as follows:\n
                      {summary}
                      \n\n
                      Based on the transcript and the associated summary of the slide, I want you to extract the query posed in the transcript and how the query can be addressed in the next slide of the presentation.
                      Think out loud and walk me through your chain of thought as you first determine what is asked in the discussion and then based on the context determine the contents of the next slide.\n
                      The output should be a Python dict having keys as reasoning and output. Output will have keys as slide_number, title, and elements. Total number of elements including all descriptions, enumeration, tables, and equations should strictly not exceed three. The elements types are as follows:\n
                      {elements}
                 """)



instruction_example_prompt = [
                ("human", """
                      There is a discussion between a lecture presenter and his students. The raw audio transcript of the discussion is as follows:\n\n
                      {transcript}
                      \n\n
                      The discussion is between two people however the above transcript is in raw string format with no entity recognition as to who is speaking. You will have to first determine that interally based on the natural language.\n
                      Also, the transcript is generated using a Speech-to-Text API which can have word errors. Based on the context, you can auto-correct certain words in the transcript.
                      I am providing you some prior context of the conversation through the summary of the slide in discussion, the summary is as follows:\n
                      {summary}
                      \n\n
                      Based on the transcript and the associated summary of the slide, I want you to extract the query posed in the transcript and how the query can be addressed in the next slide of the presentation.
                      Think out loud and walk me through your chain of thought as you first determine what is asked in the discussion and then based on the context determine the contents of the next slide. The output should be a Python dict having keys as reasoning and output.
                      The output should be a Python dict having keys as reasoning and output. Output will have keys as slide_number, title, and elements. Generate upto 3 elements for the slide. The elements types are as follows:\n
                      {elements}
                 """),
                 ("ai", """
                    {{
                     "reasoning": {reasoning},\n
                     "output": {output}\n
                    }}
                  """)
            ]

generation_example = [
       {
       "instructions": """
       {{
        "slide_number": 2,
        "title": PDF v/s CDF,
        "elements": [{{
        "element_type": "descirption", "element_desc": "A short paragraph differenciating Probability Density Function and Culminative Density Function."
        }},
        {{
        "element_type": "equation", "element_desc": "Mathematical equation of the Probability Density Function"
        }},
        {{
        "element_type": "equation", "element_desc": "Mathematical equation of the Culminative Density Function"
        }}
        ]
       }}
       """,
       "output": """
        {{
            "slide_number": 2,
            "title": "PDF v/s CDF",
            "description": "A Probability Density Function (PDF) characterizes the probability distribution of a continuous random variable, representing the likelihood of the variable falling within a specific range of values. In contrast, a Cumulative Density Function (CDF) provides the cumulative probability that a random variable is less than or equal to a given value.",
            "enumeration": [],
            "equations": [
                {{
                    "eq_desc": "Mathematical equation of the Probability Density Function",
                    "tex_code": "f(x | \mu, \sigma) = \\frac{{1}}{{\sigma \sqrt{{2\pi}}}} \exp\left(-\\frac{{(x - \mu)^2}}{{2\sigma^2}}\\right)"
                }},
                {{
                    "eq_desc": "Mathematical equation of the Culminative Density Function",
                    "tex_code": "F(x | \mu, \sigma) = \\frac{1}{2} \left[1 + \\text{erf}\left(\\frac{{x - \mu}}{{\sigma \sqrt{{2}}}}\\right)\\right]"
                }}
            ],
            "tables":[],
            "figures": []
        }}
       """ 
    }]
generation_prompt_example =  [
                ("human", """
                 I am a university professor and I want to create lecture slides based on the instructions provided for the slide.\n
                 \n
                 {instructions}
                 \n
                 \t a. For element_type = 'description' or 'enumeration', you have to generate paragraph style element named description, or point-wise style element named enumeration, respectively.\n
                 \t b. For element_type = 'equation' or 'table', you have to generate LaTex Code depending on the instruction given in element_caption.\n

                 Also keep in mind:\n
                 \t a. While generating an enumeration, the first point is the heading of the enumeration.\n
                 \t\t Example. enumeration = ['Properties of Dynammic Programming', 'Overlapping subproblems', 'Optimal substructure']\n
                 \t b. The title should not be more than 4 words long.\n
                 \t c. The description should not be more than 30 words long.\n
                 \t d. The enumeration should not have more than 4 points.\n
    
                 The presentation content should be generated in form of a JSON object.
                 While generating LaTeX code, make sure to escape the string as it will be part of a JSON object.
                 """),
                 ("ai", "{output}")
            ]
generation_prompt = ("human", """
                 I am providing you the summary of the current presentation slide and the instruction template for the next slide. Your job is to generate actual content of presentation provided by the JSON function binding:\n
                 Summary of previous slide:\n
                 {summary}
                 \n
                 Suggestion Template for next slide:\n
                 {instructions}
                 \n
                 Here you need generate content for each element given in the instruction such that\n
                 \t a. For element_type = 'description' or 'enumeration', you have to generate paragraph style element named description, or point-wise style element named enumeration, respectively.\n
                 \t b. For element_type = 'equation' or 'table', you have to generate LaTex Code depending on the instruction given in element_caption.\n
                
                 Also keep in mind:\n
                 \t a. While generating an enumeration, the first point is the heading of the enumeration.\n
                 \t\t Example. enumeration = ['Properties of Dynammic Programming', 'Overlapping subproblems', 'Optimal substructure']\n
                 \t b. The title should not be more than 4 words long.\n
                 \t c. The description should not be more than 30 words long.\n
                 \t d. The enumeration should not have more than 4 points.\n
                 The presentation content should be generated in form of a JSON object.
                 While generating LaTeX code, make sure to escape the string as it will be part of a JSON object.
                 """)
