from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Highlight
from pypdf.generic import ArrayObject, FloatObject
import pymupdf
import os
from pathlib import Path

def highlight(file,page,x,y,dimensions):
    writer = PdfWriter()
    writer.add_page(page)
    
    if not os.path.exists(f"write_to/{file}.pdf"):
        print("No file!")
        input_file = f"pdfs/{file}.pdf"
        file = Path(f"write_to/{file}.pdf")
        file.parent.mkdir(exist_ok=True, parents=True)

        #rect = (50, 550, 200, 650)
        quad_points = [dimensions[0], dimensions[1], dimensions[2], dimensions[1], dimensions[0], dimensions[3], dimensions[2], dimensions[3]]

        # Add the highlight
        annotation = Highlight(
            rect=dimensions,
            quad_points=ArrayObject([FloatObject(quad_point) for quad_point in quad_points]),
        )
        writer.add_annotation(page_number=0, annotation=annotation)

    # Write the annotated file to disk
    writer.write(file)

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
    print(f"Text Blocks: {txtblocks}")
    print(f"Image blocks: {imgblocks}")
    print(f"Fonts: {len(docfonts)}")
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
                    print(entry['spans'][0])

#traverse_highlighting("CRISPR_paper")
traverse_text("CRISPR_paper")