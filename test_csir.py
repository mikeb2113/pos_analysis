import pandas as pd
import re
#from collections import defaultdict
#from clean_data import paths
from pathlib import Path
import sys
from csir.document import Document
from csir.skeletons import Skeletons
from csir.pdf_extract import pdf_to_text,unstick_library_prefixes
import csir.skeletons
import json
from threading import Thread
from threading import Lock
import csv
input_file = "ClassOverlapping"
pdf_path = "pdfs/" + input_file + ".pdf"
pdf_transform = pdf_to_text(pdf_path)
#print(f"source -> {input_file} pdf: {pdf_transform}")
pdf = unstick_library_prefixes(pdf_to_text(pdf_path))

output_file2 = input_file + "_traversable.csv"#Output to the path as a CSV with connections present
y = Skeletons(pdf,output_file2)