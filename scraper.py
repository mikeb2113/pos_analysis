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
        def __init__(self, text, word_count, length_chars, polarity, source,source_name):
             self.text = text
             self.word_count = word_count
             self.length_chars = length_chars
             self.polarity = polarity
             self.source = source
             self.source_name = source_name
             self.subject = None
             self.star_rating = -1


    def __init__(self, input_text,source,source_name):
        #This first section breaks the text down into sentences, giving each sentence a sentiment score
        #The goal will be that each text will have a library of sentences with pertinent information to use later

        #First, check the formatting. If it's a pdf, read as pdf
        #print("checking:")
        #print(input_text[-4:])
        if(input_text[-4:]==".pdf"):
            #print("Read as pdf!")
            pdf_reader = PdfReader(input_text)
        #directory = Path('./pdfs')

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
        for idx,page in enumerate(pdf_reader.pages):#looks for each page in a pdf
            content[idx] = page.extract_text().replace("\n"," ") #get the text
            split = re.split(r'[.?!]',str(content[idx])) #save the text, split by sentence ending punctuation
            builder.append(split) #save split text
        for i in builder:
                    ##print(i)
                    ##print()
            for i2 in i:
                        #i2 now holds each sentence
                        # So now make a requirements object for each sentence!
                char_length = len(i2)-1
                length = len(i2.split(" "))-1
                sentiment = analyzer.polarity_scores(i2)["compound"]
                sentence_info = self.sentence(i2,length,char_length,sentiment,source,source_name)
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