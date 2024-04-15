import random
from datetime import datetime

FONT_STYLES = ['Arial', 'Times New Roman', 'Georgia', 'Calibiri']
PRESENTERS = [
    "Dr. Marcella Nguyen",
    "Prof. Benjamin Frost",
    "Dr. Isabella Patel",
    "Prof. Nathanial Lawson",
    "Dr. Lydia Chen",
    "Prof. Winston Harper",
    "Dr. Gabrielle Santiago",
    "Prof. Marcus Sinclair",
    "Dr. Elena Petrov",
    "Prof. Desmond Washington",
    "Dr. Sophia Alvarez",
    "Prof. Samuel Fitzgerald",
    "Dr. Emily Roberts",
    "Prof. Xavier Lee",
    "Dr. Fiona O'Malley",
    "Prof. Harrison Grant",
    "Dr. Vivian Chang",
    "Prof. Gregory Jensen",
    "Dr. Jasmine Khan",
    "Prof. Oliver Martin"
]


def generate_random_color():
    return {"r": random.randint(0, 255), "g": random.randint(0, 255), "b": random.randint(0, 255)}

def generate_random_font(element):
    bold = False
    underline = False
    italics = False
    if element == "title":
        font_size = random.randint(18, 27) * 2
    elif element == "description":
        font_size = random.randint(16, 20)
    elif element == 'enumeration':
        font_size = random.randint(18, 24)
    return {
        "font_size": font_size,
        "bold": bold,
        "underline": underline,
        "italics": italics
    }

def generate_random_value(type, lb, ub):
    if type == int:
        return random.randint(lb, ub)
    elif type == float:
        return random.uniform(lb, ub)

def pick_random_presenter():
    return pick_random(PRESENTERS)

def generate_random_date():
    formats = ["%d %b %Y", "%B %dth", "%d %b %Y", "%B %Y"]
    chosen_format = random.choice(formats)
    
    if "th" in chosen_format:
        date_str = datetime(year=random.randint(2018, 2024), month=random.randint(1, 12), day=random.randint(1, 28))  # Assuming maximum 28 days in a month for simplicity
    else:
        date_str = datetime(year=random.randint(2018, 2024), month=random.randint(1, 12), day=random.randint(1, 30))
    
    return date_str.strftime(chosen_format)

def generate_footer_obj():
    showSN = random.random() > 0.25
    showDt = random.random() > 0.5
    showFN = random.random() > 0.75 
    total_footer_elements = 0
    if showSN:
        total_footer_elements += 1
    if showDt:
        total_footer_elements += 1
    if showFN:
        total_footer_elements += 1
    inds = random.sample(range(3), total_footer_elements)
    i = 0
    footer_inds = []
    if showSN:
        footer_inds.append({"slideNr": inds[i]})
        i+=1
    if showDt:
        footer_inds.append({"date": inds[i]})
        i+=1
    if showFN:
        footer_inds.append({"footnote": inds[i]})
        i+=1
    return footer_inds


    
def generate_random_style_obj():
    style_obj = {}
    style_obj["bg_color"] = generate_random_color()
    style_obj["title_font_family"] = pick_random(FONT_STYLES) 
    style_obj["title_font_bold"] = random.random() > 0.75
    style_obj["title_font_attr"] = generate_random_font("title")
    style_obj["desc_font_family"] = pick_random(FONT_STYLES)
    style_obj["desc_font_attr"] = generate_random_font("description")
    style_obj["date"] = generate_random_date()
    return style_obj

def pick_random(list_name):
    return random.choice(list_name)

def generate_random_layout(total_body_elements):
    layout_mapping = {
        0: [0],
        1: [1], 
        2: [2, 3],
        3: [4, 5, 6, 7, 8]
        }
    return random.choice(layout_mapping[total_body_elements])

def generate_n_numbers_with_sum(sum_value, n):
    numbers = [0] * n
    for i in range(n-1):
        numbers[i] = random.randint(0, sum_value - sum(numbers))

    numbers[-1] = sum_value - sum(numbers[:-1])
    return numbers

def calculate_relative_luminance(color):
    """
    Calculate the relative luminance of a color.
    Input: color - a dictionary with 'r', 'g', 'b' keys representing RGB values.
    Output: float - relative luminance value.
    """
    r, g, b = color['r'], color['g'], color['b']
    # Convert RGB values to sRGB
    r_srgb = r / 255.0
    g_srgb = g / 255.0
    b_srgb = b / 255.0
    
    # Calculate relative luminance
    luminance = 0.2126 * r_srgb + 0.7152 * g_srgb + 0.0722 * b_srgb
    return luminance

def generate_contrasting_font_color(bg_color):
    """
    Generate a contrasting font color for a given background color.
    Input: bg_color - a dictionary with 'r', 'g', 'b' keys representing RGB values.
    Output: dictionary - a dictionary with 'r', 'g', 'b' keys representing RGB values of the font color.
    """
    luminance = calculate_relative_luminance(bg_color)
    
    # Choose a contrasting color based on the luminance
    if luminance > 0.5:
        # Background is light, use dark font color
        font_color = {"r": 0, "g": 0, "b": 0} # Black
    else:
        # Background is dark, use light font color
        font_color = {"r": 255, "g": 255, "b": 255} # White
        
    return font_color

