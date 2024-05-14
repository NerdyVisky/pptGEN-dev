import os
import random
import json
from utils.layouts import CustomLayouts
from utils.random_generator import (generate_random_style_obj, 
                              generate_random_font, 
                              generate_random_value, 
                              pick_random, 
                              generate_footer_obj,
                              generate_random_layout, 
                              generate_n_numbers_with_sum, 
                              generate_contrasting_font_color,
                              generate_random_date,
                              pick_random_presenter)
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO 
import subprocess
import fitz
import graphviz



def count_footer_elements(date, showFN, showSN):
    footer_elements = []
    if date != None:
        footer_elements.append("date")
    if showSN == True:
        footer_elements.append("slideNr")
    if showFN == True:
        footer_elements.append("footnote")
    return footer_elements

def count_body_elements(data, slide_number):
    ttl_desc = 0
    ttl_enum = 0
    ttl_eq = 0
    ttl_tb = 0
    ttl_fig = 0
    for k, v in data["slides"][slide_number - 1].items():
        if k == 'description' and v != "":
            ttl_desc = 1
        elif k == 'enumeration' and v:
            ttl_enum = 1
        elif k == 'equations' and v:
            ttl_eq = len(v)
        elif k == 'tables' and v:
            ttl_tb = len(v)
        elif k == 'figures' and v:
            ttl_fig = len(v)
    return [ttl_desc, ttl_enum, ttl_eq, ttl_tb, ttl_fig]

def resize_image(input_image_path, slide_number, i, output_image_dir, box_width, box_height, dpi=96):
    box_width_pixels = int(box_width * dpi)
    box_height_pixels = int(box_height * dpi)
    with Image.open(input_image_path) as img:
        img_width, img_height = img.size
        img_aspect_ratio = img_width / img_height
        box_aspect_ratio = box_width_pixels / box_height_pixels
        if img_aspect_ratio > box_aspect_ratio:
            new_width = box_width_pixels
            new_height = int(box_width_pixels / img_aspect_ratio)
        else:
            new_height = box_height_pixels
            new_width = int(box_height_pixels * img_aspect_ratio)
        resized_img = img.resize((new_width, new_height))
        new_img_path = os.path.join(output_image_dir, f'{slide_number}_{i}.png')
        resized_img.save(new_img_path)
        new_width_inches = new_width / dpi
        new_height_inches = new_height / dpi
        return new_img_path, new_width_inches, new_height_inches

def get_eq_img_path(tex_code, slide_number, eq_num):
    img_dir = 'output/equations/'
    img_name = f'eq_{slide_number}_{eq_num + 1}.png'
    dpi = 600
    tex_file = f'tmp.tex'
    with open(tex_file, 'w') as latexfile:
        latexfile.write('\\documentclass[preview]{standalone}\n')
        latexfile.write('\\usepackage{tikz}\n')
        latexfile.write('\\usepackage{graphicx}\n')
        latexfile.write('\\begin{document}\n')
        latexfile.write('%s\n' % tex_code)
        latexfile.write('\\end{document}\n')
    subprocess.call(['pdflatex', '-interaction=nonstopmode', tex_file], creationflags=subprocess.CREATE_NO_WINDOW)
    doc = fitz.open(f'tmp.pdf')
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
    pix.save(img_name)
    img_path = os.path.join(img_dir, img_name)
    os.rename(img_name, img_path)
    return img_path

def get_tab_img_path(tex_code, slide_number, tab_num):
    img_dir = 'output/tables/'
    img_name = f'tab_{slide_number}_{tab_num + 1}.png'
    dpi = 600
    tex_file = f'tmp.tex'
    with open(tex_file, 'w') as latexfile:
        latexfile.write('\\documentclass[preview]{standalone}\n')
        latexfile.write('\\usepackage{tikz}\n')
        latexfile.write('\\usepackage{graphicx}\n')
        latexfile.write('\\begin{document}\n')
        latexfile.write('%s\n' % tex_code)
        latexfile.write('\\end{document}\n')
    subprocess.call(['pdflatex', '-interaction=nonstopmode', tex_file], creationflags=subprocess.CREATE_NO_WINDOW)
    doc = fitz.open(f'tmp.pdf')
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
    pix.save(img_name)
    img_path = os.path.join(img_dir, img_name)
    os.rename(img_name, img_path)
    return img_path

def get_fig_img_path(dot_code, slide_number, fig_num):
    img_dir = 'output/figures/'
    img_name = f'fig_{slide_number}_{fig_num + 1}'
    try:
        graph = graphviz.Source(dot_code)
        img_path_wo_ext = os.path.join(img_dir, img_name)
        graph.render(filename=img_path_wo_ext, format='png', cleanup=True)
        img_path = img_path_wo_ext + '.png'
    except Exception as e:
        print(f"Error rendering figure: {e}.")

    return img_path    



def remove_tmp_files():
    os.remove(f'tmp.tex')
    os.remove(f'tmp.aux')
    os.remove(f'tmp.log')
    os.remove(f'tmp.pdf')
    tmp_eqs = 'output/equations'
    for filename in os.listdir(tmp_eqs):
            file_path = os.path.join(tmp_eqs, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                
    tmp_tabs = 'output/tables'
    for filename in os.listdir(tmp_tabs):
            file_path = os.path.join(tmp_tabs, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            
    tmp_figs = 'output/figures'
    for filename in os.listdir(tmp_figs):
            file_path = os.path.join(tmp_figs, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


def generate_random_slide(slide_number, data, style_obj, footer_obj, date, presentation_ID):
    bg_color, title_font_family, title_font_bold, title_font_attr, desc_font_family, desc_font_attr = style_obj["bg_color"], style_obj["title_font_family"], style_obj["title_font_bold"], style_obj["title_font_attr"], style_obj["desc_font_family"], style_obj["desc_font_attr"]
    # Determining when a slide has BG as White
    THRES = 0.667
    if generate_random_value(float, 0, 1) < THRES:
        bg_color = {"r": 255, "g": 255, "b": 255}
    # # Define total number of body elements
    # if slide_number == 1:
    #     total_body_elements = 0
    # else:
    #     total_body_elements = generate_random_value(int, 1, 3)
    n_elements_list = count_body_elements(data, slide_number)
    total_body_elements = sum(n_elements_list)
    # n_elements_list = [descriptions, enumerations, figures]
    # n_elements_list = generate_n_numbers_with_sum(total_body_elements, 3)
    # Distribute the total count among the three categories


    # Generate random slide layout
    layout_id = generate_random_layout(total_body_elements)
    layouts = CustomLayouts()
    all_dims = layouts.get_layout_dimensions(layout_id)

    ## Skeleton Slide object with Slide-level metadata
    slide = {
        "pg_no": slide_number,
        "bg_color": bg_color,
        "slide_layout": layout_id,
        "elements": {}
    }

    # Title Generation
    ## Generate Font-level random values for Title
    font_color = generate_contrasting_font_color(bg_color)

    ## Fetch Random content
    title_content = data["slides"][slide_number - 1]["title"]
    # print(title_content)

    ## Putting it together for the title object
    slide['elements']['title'] = [{
            "label": "text",
            "value": title_content,
            "xmin": all_dims['title']['left'],
            "ymin": all_dims['title']['top'],
            "width": all_dims['title']['width'],
            "height": all_dims['title']['height'],
            "style": {
                "font_name": title_font_family,
                "font_size": title_font_attr["font_size"],
                "font_color": font_color,
                "bold": title_font_bold,
                "italics": False,
                "underlined": False
            }
        }]    
       
    if total_body_elements != 0:
        # Body Generation
        ## Randomly shuffle the bounding box dimensions of the body elements
        random.shuffle(all_dims['body'])
        element_index = 0

        ## Generate Descriptions
        slide['elements']['description'] = []
        for _ in range(n_elements_list[0]):
            font_obj = generate_random_font("description")
            desc = data["slides"][slide_number - 1]["description"]
            desc_instance = {
            "label": "text",
            "value": desc,
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'],
            "width": all_dims['body'][element_index]['width'],
            "height": all_dims['body'][element_index]['height'],
            "style": {
                "font_name": desc_font_family,
                "font_size": desc_font_attr["font_size"],
                "font_color": font_color,
                "bold": False,
                "italics": False,
                "underlined": False
               }
            } 
            slide['elements']['description'].append(desc_instance)
            element_index += 1

        ## Generate Enumerations
        for _ in range(n_elements_list[1]):
            font_obj = generate_random_font("enumeration")
            enum = data["slides"][slide_number - 1]["enumeration"]
            enum_instance = {
            "label": "enumeration",
            "heading": {
                "value": enum[0],
                "xmin": all_dims['body'][element_index]['left'],
                "ymin": all_dims['body'][element_index]['top'],
                "width": all_dims['body'][element_index]['width'],
                "height": 0.5,
            },
            "value": enum[1:],
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'] + 0.5,
            "width": all_dims['body'][element_index]['width'],
            "height": max(all_dims['body'][element_index]['height'], 0.5*len(enum)),
            "style": {
                "font_name": desc_font_family,
                "font_size": desc_font_attr["font_size"],
                "font_color": font_color,
                "bold": font_obj["bold"],
                "italics": font_obj["italics"],
                "underlined": font_obj["underline"]
               }
            } 
            slide['elements']['description'].append(enum_instance)
            element_index += 1
        
        # Render Equations
        resized_path = f'output/equations/{presentation_ID}'
        if not os.path.exists(resized_path):
            os.makedirs(resized_path)

        slide['elements']['equations'] = []
        for i in range(n_elements_list[2]):
            img_path = get_eq_img_path(data["slides"][slide_number - 1]["equations"][i]['tex_code'], slide_number, i)
            resized_img_path, n_w, n_h = resize_image(img_path, slide_number, i, resized_path, all_dims['body'][element_index]['width'], all_dims['body'][element_index]['height'])
            eq_instance = {
            "label": "equation",
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'],
            "width": n_w,
            "height": n_h,
            "desc": data["slides"][slide_number - 1]["equations"][i]["eq_desc"],
            "path": resized_img_path
            }
            slide['elements']['equations'].append(eq_instance)
            element_index += 1
            remove_tmp_files()

        # Render Tables
        resized_path = f'output/tables/{presentation_ID}'
        if not os.path.exists(resized_path):
            os.makedirs(resized_path)

        slide['elements']['tables'] = []
        for i in range(n_elements_list[3]):
            img_path = get_tab_img_path(data["slides"][slide_number - 1]["tables"][i]['tex_code'], slide_number, i)
            resized_img_path, n_w, n_h = resize_image(img_path, slide_number, i, resized_path, all_dims['body'][element_index]['width'], all_dims['body'][element_index]['height'])
            tab_instance = {
            "label": "table",
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'],
            "width": n_w,
            "height": n_h,
            "desc": data["slides"][slide_number - 1]["tables"][i]["tab_desc"],
            "path": resized_img_path
            }
            slide['elements']['tables'].append(tab_instance)
            element_index += 1
            remove_tmp_files()

        # Render Figures
        resized_path = f'output/figures/{presentation_ID}'
        if not os.path.exists(resized_path):
            os.makedirs(resized_path)

        slide['elements']['figures'] = []
        for i in range(n_elements_list[4]):
            font_obj = generate_random_font("enumeration")
            # if data["slides"][slide_number - 1]["figures"][i]["label"] == "diagram":    
            #     img_path = get_fig_img_path_matplot(data["slides"][slide_number - 1]["figures"][i]['fig_code'], slide_number, i)
            # else:
            img_path = get_fig_img_path(data["slides"][slide_number - 1]["figures"][i]['fig_code'], slide_number, i)
            resized_img_path, n_w, n_h = resize_image(img_path, slide_number, i, resized_path, all_dims['body'][element_index]['width'], all_dims['body'][element_index]['height'])
            fig_instance = {
            "label": "diagram",
            "caption": {
                "value": data["slides"][slide_number - 1]["figures"][i]["fig_desc"],
                "xmin": all_dims['body'][element_index]['left'],
                "ymin": all_dims['body'][element_index]['top'] + (all_dims['body'][element_index]['height'] - 0.25),
                "width": all_dims['body'][element_index]['width'],
                "height": 0.5,
                "style": {
                    "font_name": desc_font_family,
                    "font_size": 14,
                    "font_color": font_color,
                    "bold": font_obj["bold"],
                    "italics": True,
                    "underlined": font_obj["underline"]
               }
            },
            "xmin": all_dims['body'][element_index]['left'],
            "ymin": all_dims['body'][element_index]['top'],
            "width": all_dims['body'][element_index]['width'],
            "height": all_dims['body'][element_index]['height'] - 0.25,
            "desc": data["slides"][slide_number - 1]["figures"][i]["fig_desc"],
            "path": resized_img_path
            }
            slide['elements']['figures'].append(fig_instance)
            element_index += 1
            remove_tmp_files()
        

    ##Footer generation
    slide['elements']['footer'] = []
    for i, obj in enumerate(footer_obj):
        footer_type = ''
        if 'slideNr' in obj.keys():
            footer_type = 'slideNr'
            value = str(slide_number)
        if 'footnote' in obj.keys():
            footer_type = 'footnote'
            value = "This is a footnote"
        if 'date' in obj.keys():
            footer_type = 'date'
            value = date         
        footer_dim = all_dims['footer'][obj[footer_type]]
        foot_instance = {
                "label": footer_type,
                "location": footer_dim["type"],
                "value": value,
                "xmin": footer_dim['left'],
                "ymin": footer_dim['top'],
                "width": footer_dim['width'],
                "height": footer_dim['height'],
                "style": {
                    "font_name": desc_font_family,
                    "font_size": desc_font_attr["font_size"],
                    "font_color": font_color,
                    "bold": False,
                    "italics": False,
                    "underlined": False
                }
            }
        slide['elements']['footer'].append(foot_instance)
    
    return slide

def generate_base_template():
    style_obj = generate_random_style_obj()
    footer_obj = generate_footer_obj()
    new_data = {
            "presentation_id": presentation_id,
            "topic" : data["topic"],
            "n_slides": 0,
            "presenter": pick_random_presenter(),
            "date": generate_random_date(),
            "slides": []
        }
    date = new_data["date"]
    return [style_obj, footer_obj, new_data, date]
    
def fetch_base_template(json_data):
    new_data = json_data
    footer_obj = []
    prev_slide_temp = new_data["slides"][-1]
    for ele in prev_slide_temp["elements"]["footer"]:
        ele_type = ele["label"]
        ele_location = ele["location"] - 1
        footer_obj.append({ele_type: ele_location})
    style_obj = {}
    style_obj["bg_color"] = prev_slide_temp["bg_color"]
    style_obj["title_font_bold"] = prev_slide_temp["elements"]["title"][0]["style"]["bold"]
    style_obj["title_font_family"] = prev_slide_temp["elements"]["title"][0]["style"]["font_name"] 
    style_obj["title_font_attr"] = {
        "font_size": prev_slide_temp["elements"]["title"][0]["style"]["font_size"],
        "bold": prev_slide_temp["elements"]["title"][0]["style"]["bold"],
        "underline": prev_slide_temp["elements"]["title"][0]["style"]["underlined"],
        "italics": prev_slide_temp["elements"]["title"][0]["style"]["italics"]
    }
    style_obj["desc_font_family"] = prev_slide_temp["elements"]["description"][0]["style"]["font_name"] 
    style_obj["desc_font_attr"] = {
        "font_size": prev_slide_temp["elements"]["description"][0]["style"]["font_size"],
        "bold": prev_slide_temp["elements"]["description"][0]["style"]["bold"],
        "underline": prev_slide_temp["elements"]["description"][0]["style"]["underlined"],
        "italics": prev_slide_temp["elements"]["description"][0]["style"]["italics"]
    }
    date = new_data["date"]
    return [style_obj, footer_obj, new_data, date] 
    

if __name__ == "__main__":
    print("\nGenerating JSON Payload...")
    # num_files = 3
    buffer_dir = 'output/buffer/content_json'
    json_files = [f for f in os.listdir(buffer_dir) if f.endswith('.json')]

    for json_file in json_files: 
        # print(style_obj)
        presentation_id, _ = os.path.splitext(json_file)
        file_path = os.path.join(buffer_dir, json_file)
        with open(file_path, 'r') as file:
            data = json.load(file)
        n_slides = len(data["slides"])
        if n_slides == 1:
            print(f"🟢 (1/2) Generating new template for JSON with ID: {presentation_id}")
            style_obj, footer_obj, new_data, date = generate_base_template()
        else:
            print(f"🟢 (1/2) Found existing presentation payload for JSON with ID: {presentation_id}")
            with open(f"output/{presentation_id}.json", 'r') as json_file:
                json_data = json.load(json_file)
                style_obj, footer_obj, new_data, date = fetch_base_template(json_data)

        new_slide = generate_random_slide(n_slides, data, style_obj, footer_obj, date, presentation_id)
        new_data["n_slides"] = n_slides
        new_data["slides"].append(new_slide)
        try:
            with open(f"output/{presentation_id}.json", 'w') as json_file:
                json.dump(new_data, json_file, indent=3)
            print(f"🟢 (2/2) JSON payload saved to output/{presentation_id}.json")
        except:
            print(f"🔴 ERROR: Could not create JSON payload")

        if os.path.exists('data/1234.json'):
            os.remove('data/1234.json')
            
        os.rename(file_path, "data/1234.json")
        
    
    # #Delete content JSON files
    # for json_file in json_files:
    #     os.remove(os.path.join(buffer_dir, json_file))
    

