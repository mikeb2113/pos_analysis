# We need a csv of text documents of the form: 
# Subject,?Star_Rating,Text,Word_Count,Length_Chars,Sentiment_Polarity
# ChatGPT,?5,𝐈 𝐚𝐦 𝐥𝐨𝐯𝐢𝐧𝐠 𝐢𝐭. 𝐈 𝐤𝐧𝐨𝐰𝐚 𝐥𝐨𝐭 𝐨𝐟 𝐭𝐡𝐢𝐧𝐠𝐬 𝐧𝐨𝐰 𝐞𝐚𝐬𝐲 𝐰𝐚𝐲. 𝐈 𝐝𝐨𝐧𝐭 𝐮𝐬𝐞 𝐠𝐨𝐨𝐠𝐥𝐞 𝐚𝐧𝐲 𝐦𝐨𝐫𝐞.,18,79,0,1.2026.076,0.0

# We should not yet require a subject. Rather, compare documents against each other to find what words will
# always be frequent. Then, when we can find relative frequencies, we can impute subjects

# Analyze the whole, then get more granular down the pipeline

from pathlib import Path
from pypdf import PdfReader
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import chardet
from chardet.universaldetector import UniversalDetector
from csir.pdf_extract import pdf_to_text

analyzer = SentimentIntensityAnalyzer()

def get_encoding_streaming(filename):
    detector = UniversalDetector()
    with open(filename, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done: 
                break
    detector.close()
    return detector.result['encoding']

def convert_to_utf8(filename,encoding):
    # 1. Detect the encoding
    with open(filename, 'rb') as f:
        raw_data = f.read()
    #    result = chardet.detect(raw_data)
    #    encoding = result['encoding']
    #    confidence = result['confidence']

    if encoding and encoding.lower() != 'utf-8':
        print(f"Converting {filename} from {encoding} to utf-8")
        # 2. Decode using detected encoding and write back as utf-8
        try:
            content = raw_data.decode(encoding)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")
    else:
        print(f"{filename} is already {encoding} or could not be determined.")

class csvable: #This iterates through each pdf and aquires stats
    class sentence: #This will be used to save the information that belongs to a sentence
        def __init__(self, text, word_count, length_chars, polarity, source,source_name,xmin,ymin,xmax,ymax,page,total_sentences):
             self.text = text
             self.word_count = word_count
             self.length_chars = length_chars
             self.polarity = polarity
             self.source = source
             self.source_name = source_name
             self.subject = None
             self.star_rating = -1
             self.xmin = xmin
             self.ymin = ymin
             self.xmax = xmax
             self.ymax = ymax
             self.page = page
             self.total_sentences = total_sentences


    def __init__(self, input_text,source,source_name):
        #This first section breaks the text down into sentences, giving each sentence a sentiment score
        #The goal will be that each text will have a library of sentences with pertinent information to use later

        #First, check the formatting. If it's a pdf, read as pdf
        #print("checking:")
        #print(input_text[-4:])
        if(input_text[-4:]==".pdf"):
            #print("Read as pdf!")
            pdf_reader = pdf_to_text(input_text)
            #pdf_reader = PdfReader(input_text)

        #Then, we'll initialize an array to save sentences to later!
        self.sentences = []
        self.source_name = source_name
        #for file in directory.iterdir():
            #if file.is_file():
                #path = "./pdfs/"+file.name
                #pdf_reader = PdfReader(path)
        content = {}
        builder = []

        text = ""
        #for idx,page in enumerate(pdf_reader):#looks for each page in a pdf
        #content[idx] = page#get the text
        #print("VALIDATING READER:")
        #print(pdf_reader)
        #print("ZERO:")
        #print(pdf_reader[0])#Sentence 0: [text,coords,page]
        #print("ONE:")
        #print(pdf_reader[1])#Sentence 1: [text,coords,page]
        #print(f"SOURCE: {source_name} TOTAL LENGTH: {len(pdf_reader)}")
        sentences = len(pdf_reader)
        if sentences<10000:
            #split = re.split(r'[.?!]',pdf_reader)#str(content[idx])) #save the text, split by sentence ending punctuation
            #builder.append(split) #save split text
            for i,sentence in enumerate(pdf_reader):
                builder.append(sentence)
            #for i in builder:
                        ##print(i)
                        ##print()
                #for i2 in i:
                            #i2 now holds each sentence
                            # So now make a requirements object for each sentence!
                char_length = len(sentence)-1
                #print(f"sentence: {sentence[0][0]}")
                length = len(sentence)
                sentiment = analyzer.polarity_scores(pdf_reader[0][i])["compound"]
                print(f"VALIDATING PDF_READER: {pdf_reader[1][i]}")
                print(f"INDEX COORDINATES {i}: {pdf_reader[1][i]}")
                print("Coordinates:")
                print(f"xmin: {pdf_reader[1][i][0]}")
                print(f"ymin: {pdf_reader[1][i][1]}")
                print(f"xmax: {pdf_reader[1][i][2]}")
                print(f"ymax: {pdf_reader[1][i][3]}")
                print(f"coords: {pdf_reader[1][0]}")
                print(f"page: {pdf_reader[2][i]}")
                print(f"Proposing coordinates: {pdf_reader[1][i]}")
                print(f"Proposing page: {pdf_reader[2][i]}")
                sentence_info = self.sentence(pdf_reader[0][i],length,char_length,sentiment,source,source_name,pdf_reader[1][i][0],pdf_reader[1][i][1],pdf_reader[1][i][2],pdf_reader[1][i][3],pdf_reader[2][i],sentences)
                self.sentences.append(sentence_info)
                #print(f"char_length: {char_length}") 
                #print(f"length: {length}")                                             
                #print(i2)
                #print()
                #re.sub(r' +', r' ',text)
                ##print(f"text: {i}")
                ##print(text)
             
        #self.requirements =  {
        #    "Subject": None,
        #    "Star_Rating": None,
        #    "Text": words,
        #    "Word_Count": word_count,
        #    "Length_Chars": char_count,
        #    "Sentiment_Polarity": analyzer.polarity_scores(words),
        #}

#test = csvable("pdfs/ClassOverlapping.pdf")
##print("Text: " + test.requirements[2])
##print("Word Count: " + test.requirements[3])
##print("Char Length: " + test.requirements[4])
##print("Sentiment Polarity: " + test.requirements[5])

        ##print(content)
        ##print()
        ##print(path)


#directory = Path('pdfs')
#for file in directory.iterdir():
#    if file.is_file():
#        #print(file.extract_text())