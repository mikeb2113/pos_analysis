from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Highlight
from pypdf.generic import ArrayObject, FloatObject
import pymupdf
import os
from pathlib import Path
from fpdf import FPDF

def highlight(file,page,x,y,dimensions):
    writer = PdfWriter()
    #writer.add_page(page)
    
    if not os.path.exists(f"write_to/{file}.pdf"):
        print("No file!")
        input_file = f"pdfs/{file}.pdf"
        file = Path(f"write_to/{file}.pdf")
        file.parent.mkdir(exist_ok=True, parents=True)
        #print(f"xmin: {dimensions[0]}")
        #print(f"ymin: {dimensions[1]}")
        #print(f"xmax: {dimensions[2]}")
        #print(f"ymax: {dimensions[3]}")
        #print(f"page: {page}")

        #rect = (50, 550, 200, 650)
        quad_points = [dimensions[0], dimensions[1], dimensions[2], dimensions[1], dimensions[0], dimensions[3], dimensions[2], dimensions[3]]

        # Add the highlight
        annotation = Highlight(
            rect=dimensions,
            quad_points=ArrayObject([FloatObject(quad_point) for quad_point in quad_points]),
        )
        writer.add_annotation(page_number=page, annotation=annotation)

    # Write the annotated file to disk
    writer.write(file)

def ensure_file_exists(input_file,output_file):
    #print(f"input file: {input_file} output file: {output_file}")
    if not os.path.exists(output_file):
        doc=pymupdf.open(input_file)
        doc.save(output_file)
        #file.ez_save(file)

def return_quad(dimensions):
    quads = f"Quad(Point({dimensions[0]}, {dimensions[1]}), Point({dimensions[2]}, {dimensions[1]}), Point({dimensions[0]}, {dimensions[3]}), Point({dimensions[2]}, {dimensions[3]}))"
    return quads


def highlight_by_text(sentence,file):
    input_word = sentence[5]
    dimensions = [sentence[0],sentence[1],sentence[2],sentence[3]]
    page = sentence[4]#input_word,page,input_doc,output_doc
    input_word = input_word.replace(".","")
    words = input_word.split(",")
    #print("words:")
    for word in words:
        print(word)
    #print(f"xmin: {dimensions[0]}")
    #print(f"ymin: {dimensions[1]}")
    #print(f"xmax: {dimensions[2]}")
    #print(f"ymax: {dimensions[3]}")
    #print(f"page: {page}")
    quad = pymupdf.Quad(
        (dimensions[0], dimensions[1]),  # Upper Left
        (dimensions[2], dimensions[1]),  # Upper Right
        (dimensions[0], dimensions[3]),  # Lower Left
        (dimensions[2], dimensions[3])   # Lower Right
    )
    #print("quad:")
    #print(quad)
    input_doc = "./pdfs/" + file + ".pdf"
    output_doc = "./write_to/" + file + ".pdf"
    ensure_file_exists(input_doc,output_doc)

    doc=pymupdf.open(output_doc)


    # load desired page (0-based page number)
    page = doc[page]
    #print(f"page: {page}")


    # search for "whale", results in a list of rectangles

    page.add_highlight_annot(quad)

    if doc.can_save_incrementally():
            #print("saving incrementally...")
            doc.saveIncr()
    #else:
            #print("cannot save incrementally...")
            #break
            #doc.save(output_doc)
        #doc.saveIncr(output_doc)

def get_stats(file):
    doc = pymupdf.open(f"pdfs/{file}.pdf")
    txtblocks = 0
    imgblocks = 0
    docfonts = []
    for page in doc:
        t = page.get_text("dict")
        for b in t['blocks']:
            if(b['type']==0):
                txtblocks+=1
            elif(b['type']==1):
                imgblocks+=1
        pagefonts = page.get_fonts()
        for f in pagefonts:
            if(f[3] not in tuple(docfonts)):
                docfonts.append(f[3])
    #print(f"Text Blocks: {txtblocks}")
    #print(f"Image blocks: {imgblocks}")
    #print(f"Fonts: {len(docfonts)}")
    for ft in docfonts:
        print(ft)
    doc.close()

def traverse_text(file):
    doc = pymupdf.open(f"pdfs/{file}.pdf")
    txtblocks = 0
    imgblocks = 0
    docfonts = []
    minskip = 186
    for page in doc:
        t = page.get_text("dict")
        for b in t['blocks']:
            if(b['type']==0):
                for entry in b['lines']:
                    print(entry['spans'][0]['text'])
                    print(page.number)
                    print(f"xmin: {entry['spans'][0]['bbox'][0]}")
                    print(f"ymin: {entry['spans'][0]['bbox'][1]}")
                    print(f"xmax: {entry['spans'][0]['bbox'][2]}")
                    print(f"ymax: {entry['spans'][0]['bbox'][3]}")

def traverse_highlighting(file):
    doc = pymupdf.open(f"pdfs/{file}.pdf")
    txtblocks = 0
    imgblocks = 0
    docfonts = []
    minskip = 186
    for page in doc:
        t = page.get_text("dict")
        for b in t['blocks']:
            if(b['type']==0):
                for entry in b['lines']:
                    dimensions = entry['spans'][0]['bbox']
                    reader = PdfReader(f"pdfs/{file}.pdf")
                    page = reader.pages[0]
                    highlight(file,page,1,1,dimensions)
                    #print(entry['spans'][0])

#traverse_highlighting("CRISPR_paper")
#traverse_text("CRISPR_paper")