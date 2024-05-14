
instruction_example = [
    {
        "transcript": """
        Now we will move our discussion towards some important types of Probability Distribution functions. In the coming slide, I would like to differnciate between PDF and CDF functions. Next slide please. 
        """,
        "summary": """
        Slide 1: Gaussian Distributions.
        This slide introduces the Gaussian distribution, highlighting its bell-shaped curve defined by mean (mu) and variance (sigma squared). The key parameters determine the center and width of the distribution. It includes the Probability Density Function (PDF) equation for the Gaussian distribution, showcasing the formula for the curve's shape. The slide provides a foundational understanding of the Gaussian distribution's fundamental properties and how mean and variance play a crucial role in defining its shape and characteristics.
        """,
        "slide_templates": """["Introduction", "Content", "Example", "Comparision", "Summary"]""",
        "elements": """["description", "enumeration", "url", "equations", "tables", "diagram"]""",
        "reasoning": """
         Based on the transcript, the speakers will require a comparision slide which can compare Probability Density Function (PDF) and Culminative Density Function (CDF)\n
        """,
        "output": """
        {
         "slide_number": 2,
         "slide_template": "comparision"
         "title": PDF v/s CDF,
         "elements": [{
         "element_type": "table", "element_desc": "A table which comprehensively provides the difference between PDF and CDF "
         }]
        }
        """
    }
]
instruction_prompt = ("human", """There is a discussion between a lecture presenter and his students. The raw audio transcript of the discussion is as follows:\n\n
                      {transcript}
                      \n\n
                      I am providing you some prior context of the conversation through the summary of the slide in discussion, the summary is as follows:\n
                      {summary}
                      \n\n
                      Based on the transcript and the associated summary of the slide, I want you to decide what content is demanded from the next lecture slide or if nothing is demanded that what will be the most logicial next slide in the presenation.\n
                      The slide templates can be one of the following : {slide_templates}
                      Think out loud and walk me through your chain of thought as you first determine what is asked in the discussion and then based on the context determine what slide template should the next slide be.\n
                      The elements you can choose for any particular slide template are : {elements}
                      Depending on the template, here's how you will choose which elements to generate:\n
                      1. Introduction : For introduction slide you can choose upto two elements, one of them will be either description or enumeration, and other might be a chart or a diagram.\n
                      2. Example : For example slide, you can choose upto two elements, one should be a diagram and other should be a description which is related to the diagram\n
                      3. Comparsion : For comparsion slide, you should focus on generating a table which differenciates between two things in a point wise manner.\n
                      4  Content: For content slide, you should generate atleast two elements. One can be a description or enummeration and the other can be any visual element - a chart, diagram, equation, etc.\n
                      5. Summary : For summary slide, you should generate a single enumeration element.\n

                      After determining the slide template and the associated slide elements, you should formulate the output in form of a Python dict.
                      Hence, the output should be a Python dict having keys as reasoning and output. Reasoning will be your thought process in determining the slide template and it's associated elements while output will have keys as slide_number, title, and elements. Total number of elements including all descriptions, enumeration, tables, and equations should strictly not exceed three.\n
                 """)



instruction_example_prompt = [
                ("human", """
                      There is a discussion between a lecture presenter and his students. The raw audio transcript of the discussion is as follows:\n\n
                      {transcript}
                      \n\n
                      I am providing you some prior context of the conversation through the summary of the slide in discussion, the summary is as follows:\n
                      {summary}
                      \n\n
                      Based on the transcript and the associated summary of the slide, I want you to decide what content is demanded from the next lecture slide or if nothing is demanded that what will be the most logicial next slide in the presenation.\n
                      The slide templates can be one of the following : {slide_templates}
                      Think out loud and walk me through your chain of thought as you first determine what is asked in the discussion and then based on the context determine what slide template should the next slide be.\n
                      The elements you can choose for any particular slide template are : {elements}
                      Depending on the template, here's how you will choose which elements to generate:\n
                      1. Introduction : For introduction slide you can choose upto two elements, one of them will be either description or enumeration, and other might be a chart or a diagram.\n
                      2. Example : For example slide, you can choose upto two elements, one should be a diagram and other should be a description which is related to the diagram\n
                      3. Comparsion : For comparsion slide, you should focus on generating a table which differenciates between two things in a point wise manner.\n
                      4  Content: For content slide, you should generate atleast two elements. One can be a description or enummeration and the other can be any visual element - a chart, diagram, equation, etc.\n
                      5. Summary : For summary slide, you should generate a single enumeration element.\n

                      After determining the slide template and the associated slide elements, you should formulate the output in form of a Python dict.
                      Hence, the output should be a Python dict having keys as reasoning and output. Reasoning will be your thought process in determining the slide template and it's associated elements while output will have keys as slide_number, title, and elements. Total number of elements including all descriptions, enumeration, tables, and equations should strictly not exceed three.\n
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
       {
        "slide_number": 2,
        "slide_template": "comparision",
        "title": PDF v/s CDF,
        "elements": [{
         "element_type": "table", "element_desc": "A table which comprehensively provides the difference between PDF and CDF "
        }
        ]
       }
       """,
       "output": """
        {
            "slide_number": 2,
            "title": "PDF v/s CDF",
            "description": "A Probability Density Function (PDF) characterizes the probability distribution of a continuous random variable, representing the likelihood of the variable falling within a specific range of values. In contrast, a Cumulative Density Function (CDF) provides the cumulative probability that a random variable is less than or equal to a given value.",
            "enumeration": [],
            "equations": [],
            "tables":["
\begin{table}[h]
\centering
\begin{tabular}{|l|l|}
\hline
\textbf{Probability Distribution Function (PDF)} & \textbf{Cumulative Distribution Function (CDF)}   \\ \hline
Describes likelihood of a value or range. & Describes probability up to a given value. \\ \hline
Range: Typically 0 to 1. & Always 0 to 1. \\ \hline
Area under curve represents probabilities. & Area under curve represents probabilities up to a point. \\ \hline
Gives probability density at a value. & Gives cumulative probability up to a value. \\ \hline
Notation: $f(x)$ or $p(x)$ & $F(x)$ \\ \hline
Examples: Normal, Poisson, Exponential & Examples: Normal, Poisson, Exponential \\ \hline
\end{tabular}
\caption{Comparison of PDF and CDF}
\label{tab:pdf_cdf_comparison}
\end{table}
"],
            "figures": []
        }
       """ 
    },
    {
       "instructions": """{
        "slide_number": 5,
        "title": Working of BFS,
        "slide_template": "Comparision"
        "elements": [{
        "element_type": "diagram", "element_desc": "A flow-chart representing the entire working flow of breadth first search"
        },
        {
        "element_type": "enumeration", "element_desc": "Steps of BFS in very short points"
        }
        ]
       }
       """,
       "output": """
        {
            "slide_number": 5,
            "title": "Working of BFS",
            "description": "",
            "enumeration": ['Initialize Nodes', 'Explore Neighbors', 'Enqueue Neighbors', 'Repeat', 'Terminate'],
            "equations": [],
            "tables":[],
            "figures": [{
            "fig_desc": "A flowchart representing the working of Breadth First Search",
            "fig_code": "digraph BFS {
    node [shape = rectangle, style=filled, fillcolor=lightblue, fontname=Helvetica]
    edge [fontname=Helvetica]

    start [label="Start", shape=circle]

    start -> initialize
    initialize [label="Initialize\nqueue with start node"]
    
    initialize -> explore
    explore [label="Dequeue a node\nand explore its neighbors"]

    explore -> visit [label="Visit node"]
    visit [label="Check if\nit's the goal"]
    
    visit -> goal [label="Found goal"]
    visit -> enqueue [label="Not found goal"]
    
    enqueue [label="Enqueue unvisited\nneighbors"]
    goal [label="Goal reached"]

    explore -> goal [label="Found goal"]
    
    goal -> stop [label="Stop"]
    stop [label="Stop", shape=circle]

    explore -> stop [label="No more nodes"]
    enqueue -> explore [label="Repeat"]
    goal -> stop [label="Stop"]
}"
            }]
        }
       """   
    }]
generation_prompt_example =  [
                ("human", """
                 I am a university professor and I want to create lecture slides based on the instructions provided for the slide.\n
                 \n
                 {instructions}
                 \n
                 \t a. For element_type = 'description', 'enumeration', or 'url', you have to generate paragraph style element named description, or point-wise style element named enumeration.\n
                 \t b. For element_type = 'equation' or 'table', you have to generate LaTex Code depending on the instruction given in element_caption.\n
                 \t c. For element_type = 'diagram', you have to generate DOT Language Code depending on the instruction given in element_caption.\n

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
                 \t c. For element_type = 'diagram', you have to generate DOT Language Code depending on the instruction given in element_caption.\n
                 Also keep in mind:\n
                 \t a. While generating an enumeration, the first point is the heading of the enumeration.\n
                 \t\t Example. enumeration = ['Properties of Dynammic Programming', 'Overlapping subproblems', 'Optimal substructure']\n
                 \t b. The title should not be more than 4 words long.\n
                 \t c. The description should not be more than 30 words long.\n
                 \t d. The enumeration should not have more than 4 points.\n
                 The presentation content should be generated in form of a JSON object.
                 While generating LaTeX code, make sure to escape the string as it will be part of a JSON object. Do not add any line breaks or other escape sequences in the JSON object.
                 """)
