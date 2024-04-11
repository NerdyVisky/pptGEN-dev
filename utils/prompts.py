


outline_prompt = [
            ("system", "You are a helpful university professor and you are guiding your PhD student to create an outline for the lecture he will deliver to a class."),
            ("human", "I would like to get help designing a detailed Table of Contents for an advanced university lecture on {topic}. Please help me create the Table of Content in form of a {format}. Just return the output without the conversation.")
        ]
instruction_example = [
    {
        "topic": "Divide and Conquer Approach",
        "outline": """
        {{
  "Introduction": {{
    "Overview of Divide and Conquer Approach": null,
    "Applications in Real-life": null
  }},
  "The Divide and Conquer Strategy": {{
    "Characteristics": null,
    "Algorithm Design Process": {{
      "Divide": null,
      "Conquer": null,
      "Combine": null
    }},
    "Pseudocode Examples": null
  }},
  "Analysis of Divide and Conquer Algorithms": {{
    "Recurrence Relations": null,
    "Master Theorem": null,
    "Examples": null
  }},
  "Advanced Topics": {{
    "Parallel Divide and Conquer": null,
    "Strassen's Algorithm for Matrix Multiplication": null,
    "Implementation Tips": null
  }},
  "Comparative Analysis": {{
    "Divide and Conquer vs. Dynamic Programming": null,
    "Divide and Conquer vs. Greedy Method": null,
    "Complexity Analysis": null
  }},
  "Challenges and Limitations": {{
    "Overhead": null,
    "Subproblem Overlapping": null
  }},
  "Conclusion": {{
    "Summary": null,
    "Future Directions": null
  }}
}}""",
   "elements": ['chart', 'graph', 'diagram', 'description', 'table', 'equation', 'url'],
   "output": """
{{
  "Introduction": {{
    "Overview of Divide and Conquer Approach": [{{"element_type: "description", "element_caption": "Define Divide and Conquer Approach" }}, {{"element_type: "enumeration", "element_caption": "Short key points describing properties of Divide and Conquer."}}],
    "Applications in Real-life": [{{"element_type": "enumeration", "element_caption": "Listing major applications of Divide of Conquer apprach."}}, {{"element_type": "url", "element_caption": "The URL of an article on the internet discussing applications of divide and conquer"}}]
  }},
  "The Divide and Conquer Strategy": {{
    "Characteristics": null,
    "Algorithm Design Process": {{
      "Divide": [{{"element_type": "diagram", "element_caption": "diving the problem in the divide phase "}}]
      "Conquer": [{{"element_type": "diagram", "element_caption": "solving subproblems in the conquer phase "}}],
      "Combine": [{{"element_type": "enumeration", "element_caption": "List "}}]
    }},
    "Pseudocode Examples": [{{"element_type": "enumeration", "element_caption": "step-by-step implementation in Python for a Divide and Conquer problem"}}, {{"element_type": "url", "element_caption": "The URL of an article on the internet discussing the pseudo code of a Divide and Conquer problem"}}]
  }},
  "Analysis of Divide and Conquer Algorithms": {{
    "Recurrence Relations": [{{"element_type": "graph", "element_caption": "the recurrence relation visualized as a graph"}}, {{"element_type": "equation", "element_caption": "The mathematical expression of a recurrence relation."}}],
    "Master Theorem": [{{"element_type": "description", "element_caption": "Definition of Master's theorem"}}, {{"element_type": "equation", "element_caption": "The mathematical expression of Master's Theorem"}}],
    "Examples": [{{"element_type": "enumeration", "element_caption": "Listing algorithms that use divide and conquer strategy"}}, {{"element_type": "table", "element_caption": "Comparing the common divide and conquer algorithms by their characteritics, implementation details, and use-cases."}}]
  }},
  "Advanced Topics": {{
    "Parallel Divide and Conquer": [{{"element_type": "description", "element_caption": "explaining what how parallel divide and conquer works."}}, {{"element_type": "url", "element_caption": "The URL of a research paper explaining parallel divide and conquer"}}],
    "Strassen's Algorithm for Matrix Multiplication": [{{"element_type": "enumeration", "element_caption": "Information about history, concepts, and usage of the algorithm in short bullet points"}}, {{"element_type": "equation", "element_caption": "A mathematical expression showing the multiplication of two 2x2 matrices for Strassen's algorithm"}}],
    "Implementation Tips": [{{"element_type": "enumeration", "element_caption": "Implementation tips for Strassen's algorithm in short bullet points"}}]
  }},
  "Comparative Analysis": {{
    "Divide and Conquer vs. Dynamic Programming": [{{"element_type": "table", "element_caption": "Providing a detailed comparision and differenciation of Divide and Conquer and Dyanamic Programming strategies."}}],
    "Divide and Conquer vs. Greedy Method": [{{"element_type": "table", "element_caption": "Providing a detailed comparision and differenciation of Divide and Conquer and Greedy Approach strategies."}}],
    "Complexity Analysis": [{{"element_type": "chart", "element_caption": "Comparing the time and space complexity of divide and conquer approach with other approaches."}}]
  }},
  "Challenges and Limitations": {{
    "Overhead": [{{"element_type": "description", "element_caption": "Describing how recrusive function calls create overhead."}}],
    "Subproblem Overlapping": [{{"element_type": "description", "element_caption": "Describe a the subproblem overlapping problem"}}]
  }},
  "Conclusion": {{
    "Summary": [{{"element_type": "enumeration", "element_caption": "Key takeaways from the presentation in short bullet points"}}],
    "Future Directions": [{{"element_type": "diagram", "element_caption": "Showing the areas of research where divide and conquer can possibly be used."}}, {{"element_type": "url", "element_caption": "Link to article having a novel application of the Divide and Conquer algorithm"}}]
  }}
}}
"""}
]
instruction_prompt = ("human", """Hello. I want you to help me prepare lecture slides on {topic}. I am providing you with the outline of the lecture in form of a nested dictionary.\n
                 Outline :{outline}
                 Each subsection has empty values. I want you to add two keys namely 'element_type' and 'element_caption' for each subsection and determine which types of elements would be most beneficial to understand that subsection.\n
                 The elements can be as follows: {elements}.\n
                 You should provide three elements per subheading.\n
                 Whenever possible generate atleast one text based element (Description, URL, or Enumeration) and one visual element (Graph, Figure, Chart, Diagram, Equation, Figure) per subsection, such that there is diversity in elements.\n
                 As a rule of thumb, make sure the distribution of elements is nearly same for the entire presentation.\n 
                 I want you to generate the results within the outline and only output the revised outline without any conversation.\n
                 """)



instruction_example_prompt = [
                ("human", """Hello. I want you to help me prepare lecture slides on {topic}. I am providing you with the outline of the lecture in form of a nested dictionary.\n
                 Outline :{outline}
                 Each subsection has empty values. I want you to add two keys namely 'element_type' and 'element_caption' for each subsection and determine which types of elements would be most beneficial to understand that subsection.\n
                 The elements can be as follows: {elements}.\n
                 You can suggest upto 3 elements per subtopic. I want you to generate the results within the outline and only output the revised outline without any conversation.\n
                 """),
                 ("ai", "{output}")
            ]


generation_prompt =  [
                ("system", "You are an capable and expert content creator. You can create multi-modal content such as text, images, code, etc. You also have access to all internet sources at your discretion."),
                ("human", """
                 I am a university professor and I want to create lecture slides on the topic of {topic}\n
                 I am providing you the Table of Contents for the same:\n
                 {outline}
                 \n
                 Within each subsection of the Table of Contents, I have the list of element types I want to render while explaining that particular subsection with element_caption as the instruction to generate the element.\n
                 Generate presentation content by keeping the following instructions in mind:\n
                 1. Each section in the Table of Contents must be a title slide with no body elements.\n
                 2. Each subsection in the Table of Contents should have the key name as the title with the body elements described by element_type, and element_caption.\n
                 3. Depending on the element_type for each element in a subsection, you have to generate appropriate modality of the content. Consider the following guidelines for specific element_types:\n
                 \t a. For element_type = 'description' or 'enumeration', you have to generate paragraph style element named description, or point-wise style element named enumeration, respectively.\n
                 \t b. For element_type = 'equation' or 'table' or 'pseudocode', you have to generate LaTex Code depending on the instruction given in element_caption.\n
                 \t c. For element_type = 'chart' or 'graph' or 'diagram', you have to generate an image depending on the instruction given in element_caption and provide the link to the image path\n

                 The presentation content should be generated in form of a JSON object. The presentation ID is {presentation_ID}

                 """)
            ]