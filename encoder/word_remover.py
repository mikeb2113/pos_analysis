from pathlib import Path
import PyPDF2
import html
import pdfplumber
import re
import unicodedata
from .libs import DET,PREP,CONJ,COMP,MOD,AUX,PREFIX_WHITELIST
from pathlib import Path
import fitz  # PyMuPDF
import pymupdf


LIB_WORDS = DET | PREP | CONJ | COMP | MOD | AUX

#def traverse_text(file):
#    doc = pymupdf.open(f"pdfs/{file}.pdf")
#    txtblocks = 0
#    imgblocks = 0
#    docfonts = []
#    minskip = 186
#    for page in doc:
#        t = page.get_text("dict")
#        for b in t['blocks']:
#            if(b['type']==0):
#                for entry in b['lines']:
#                    print(entry['spans'][0]['text'])
#                    print(f"xmin: {entry['spans'][0]['bbox'][0]}")
#                    print(f"ymin: {entry['spans'][0]['bbox'][1]}")
#                    print(f"xmax: {entry['spans'][0]['bbox'][2]}")
#                    print(f"ymax: {entry['spans'][0]['bbox'][3]}")

def pdf_to_text(path: str) -> str:
    """Extract raw text from a PDF as one big string."""
    path = Path(path)
    text_chunks = []
    decoded = [],[],[]
    doc = pymupdf.open(path)
    for page in doc:
        t = page.get_text("dict")
        for b in t['blocks']:
            if(b['type']==0):
                for entry in b['lines']:
                    page_text = entry['spans'][0]['text']
                    xmin = entry['spans'][0]['bbox'][0]
                    ymin = entry['spans'][0]['bbox'][1]
                    xmax = entry['spans'][0]['bbox'][2]
                    ymax = entry['spans'][0]['bbox'][3]
                    pdf_coordinates_bbox = [xmin,ymin,xmax,ymax]
                    #print(f"text: {page_text}")
                    #print(f"xmin: {xmin}")
                    #print(f"ymin: {ymin}")
                    #print(f"xmax: {xmax}")
                    #print(f"ymax: {ymax}")
                    #print(f"Page number: {page.number}")
                    decoded[0].append(page_text)#(clean_text(page_text))
                    decoded[1].append(pdf_coordinates_bbox)
                    decoded[2].append(page.number)
                    #text_chunks.append(decoded)
    #for page_num, page in enumerate(doc):
    #    page_text = page.get_text("text") or ""

        # Keep page markers if desired
        # text_chunks.append(
        #     f"\n\n=== PAGE {page_num + 1} ===\n\n{page_text}"
        # )

    doc.close()
    #print('TESTING:')
    #for chunk in text_chunks:
    #    print(f"text: {chunk[0]}")
    #    print(f"coorindates: {chunk[1]}")

    #return "\n".join(text_chunks)
    #print("validating:")
    #print("text: ")
    #print(decoded[0])
    #print("Coordinates:")
    #print(decoded[1])
    #print("pages:")
    #print(decoded[2])
    return decoded

def unstick_library_prefixes(
    text: str,
    min_lib_len: int = 1,   # skip tiny libs like "a", "in", "to"
) -> str:
    """
    Try to fix glued cases like 'theking' -> 'the king',
    using per-prefix whitelists of valid words.

    Logic:
      - At the start of a letter-run, check if it begins with any library word
        of length >= min_lib_len that has a whitelist.
      - Extract the full word (letters only).
      - If full word == lib word: leave as-is.
      - Else if full word is in that prefix's whitelist: leave as-is.
      - Else: split into 'lib' + ' ' + 'tail'.
    """

    # Only consider library words we actually have whitelists for,
    # and that meet the length requirement
    safe_libs = [
        w for w in LIB_WORDS
        if len(w) >= min_lib_len and w in PREFIX_WHITELIST
    ]

    # Try longer library words first
    lib_sorted = sorted(safe_libs, key=len, reverse=True)

    out = []
    i = 0
    n = len(text)

    def is_alpha(ch: str) -> bool:
        return ch.isalpha()

    while i < n:
        ch = text[i]

        if not is_alpha(ch):
            out.append(ch)
            i += 1
            continue

        prev = text[i-1] if i > 0 else " "

        # Only consider at the *start* of a word-like run
        if not is_alpha(prev):
            lowered_slice = text[i:].lower()
            matched = False

            for w in lib_sorted:
                wl = len(w)
                if wl <= len(lowered_slice) and lowered_slice.startswith(w):
                    # Found a library prefix at word start
                    j = i + wl

                    # Consume the full word: lib + tail letters
                    k = j
                    while k < n and is_alpha(text[k]):
                        k += 1

                    full_word = text[i:k]
                    full_lower = full_word.lower()

                    whitelist = PREFIX_WHITELIST.get(w, set())

                    if full_lower == w:
                        # Just the lib word itself, e.g. "the "
                        out.append(full_word)
                        i = k
                        matched = True
                        break

                    if full_lower in whitelist:
                        # Legit word like "theorem", "overall", etc. -> don't split
                        out.append(full_word)
                        i = k
                        matched = True
                        break

                    # Otherwise treat as glued and split: "<lib><tail>" -> "<lib> <tail>"
                    lib_part = text[i:i+wl]
                    tail_part = text[i+wl:k]
                    out.append(lib_part)
                    out.append(" ")
                    out.append(tail_part)
                    i = k
                    matched = True
                    break

            if matched:
                continue

        # Default: just copy the character
        out.append(ch)
        i += 1

    return "".join(out)

# def extract_pdf_text(path: str) -> str:
#     path = Path(path)
#     text_chunks = []

#     with pdfplumber.open(path) as pdf:
#         for page in pdf.pages:
#             # layout=True tries to respect glyph positions
#             page_text = page.extract_text(layout=True) or ""
#             text_chunks.append(page_text)

#     raw = "\n".join(text_chunks)
#     return clean_text(raw)

def clean_text(text: str) -> str:
    # Decode HTML entities like &quot;
    text = html.unescape(text)

    # Normalize unicode (fancy quotes, compatibility forms)
    text = unicodedata.normalize("NFKC", text)

    # Normalize weird whitespace: turn all whitespace into single spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()
"""
&quot;Along the shore the cloud waves break,
The twin suas sink behind the lake.
The shadows lengthen
In Carcosa.
"""

# --- Example Usage ---
if __name__ == "__main__":
    # 1. Define your blocklist (keep them lowercase for case-insensitive matching)
    forbidden_words = [
    "a","an","that","the","these","this","those","at","by","for","from","in","into","of", 
    "on","onto","over","to","under","with",
    "and","but","or",
    "that","which","who","whom","can","could","may","might","must","shall","should","will","would",
    "am","are","be","been","being","did","do","does","had","has","have","is","was","were",
    "a","an","certain","one","some","somebody","someone","something","somewhere",
    "all","any","each","every","whatever","whichever","whoever",
    "never","no","nobody","none","noone","nothing","nowhere","no-one"
    ]