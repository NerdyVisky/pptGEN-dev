from langchain_core.pydantic_v1 import BaseModel, Field


class EquationObject(BaseModel):
    eq_desc: str = Field(description='The description of what the equation represents')
    tex_code: str = Field(description='Equation in LaTeX format')

class FigureObject(BaseModel):
    label: str = Field(description='Type of figure, for example like chart, diagram, graph')
    fig_desc: str = Field(description='Description of the what the figure represents (Element Caption)')
    path: str = Field(description='Path to the file where the figure is located')

class TableObject(BaseModel):
    tab_desc: str = Field(description='The description of what the table represents')
    tex_code: str = Field(description='Table in LaTeX format')

class SlideContentJSON(BaseModel):
    slide_number: int = Field(description="The number of the slide in the presentation")
    title: str = Field(description="Title content of the slide")
    description: str = Field(description="Body content represented as a paragraph anywhere around 5 to 30 words long")
    enumeration: list = Field(description="Body Content represented as a list of points where each point is a string of around 2 to 5 words long")
    equations: list[EquationObject] = Field(description="Information about equations to explain a mathematical concept")
    tables: list[TableObject] = Field(description='Tables related to the slide')
    figures: list[FigureObject] = Field(description="Figures related to the slide")
