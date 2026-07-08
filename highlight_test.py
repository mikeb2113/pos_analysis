from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Highlight
from pypdf.generic import ArrayObject, FloatObject
import pymupdf

def highlight(file):
    reader = PdfReader(f"pdfs/{file}.pdf")
    page = reader.pages[0]
    writer = PdfWriter()
    writer.add_page(page)

    rect = (50, 550, 200, 650)
    quad_points = [rect[0], rect[1], rect[2], rect[1], rect[0], rect[3], rect[2], rect[3]]

    # Add the highlight
    annotation = Highlight(
        rect=rect,
        quad_points=ArrayObject([FloatObject(quad_point) for quad_point in quad_points]),
    )
    writer.add_annotation(page_number=0, annotation=annotation)

    # Write the annotated file to disk
    writer.write("ClassOverlapping.pdf")

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

traverse_text("ClassOverlapping")