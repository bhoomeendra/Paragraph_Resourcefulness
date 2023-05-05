import os
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from tqdm import tqdm
import pickle
import pdb

STOPWORD = set(stopwords.words('english'))
pt = PorterStemmer()

regx_sections = "(?i)section.\s*\d+\w?(\s*\(\d+\))?\s*(\(\w\))?"
regx_acts = r"(?i)\w+\sact(s)?[^\w]\s*(\d+)?"
regx_articles = r"(?i)Article\s+(\w+)"

def getPickel(path):

	if os.path.exists(path):
		with open(path,'rb') as data:
			return pickle.load(data)
	print(f"ERROR: File {path} Does not exits")
	return None

def putPickel(var,path):
    with open(path,'wb') as file:
        pickle.dump(var,file)
        print(f"Pickel Dumped in {path}")


def clean(s,stop_word = True):
    
    s = s.lower()
    
    # Removing Punctuation new line and tabs and extra spaces
    s = s.replace("\t",' ')
    s = s.replace('\.','')
    s = s.replace('.','')
    s = s.replace('/-','')
    s = s.replace(',','')
    s = s.replace('(',' ')
    s = s.replace(')',' ')
    s = s.replace('\n',' ')
    s = s.replace(';','')
    s = s.replace('-','')
    s = s.replace("'",'')
    s = s.replace('"','')
    s = s.replace('@','')
    s = s.replace('%','')
    s = s.replace(':','')
    s = s.replace('"','')
    s = s.replace('/',' ')
    s = s.replace('"','')
    s = s.replace('"','')
    s = s.replace('[',' ')
    s = s.replace(']',' ')
    s = s.replace('=',' ')
    s = re.sub(r'\\',' ',s)
    s = re.sub('\s\s+',' ',s)
    
    # Stemming the text
    word_count = 0
    if stop_word:
        s = re.sub(' +',' ',s)
        words = s.split(' ')
        output = ""
        for w in words:
            if w not in STOPWORD:
                output+= pt.stem(w) +' '
                word_count+=1
        if word_count >4:
            return output.strip()
        return ''
    return s

def preprocess_laws(reMatchobj):
    text = reMatchobj.group(0)
    text.replace(' ','')
    text = ''.join(filter(str.isalnum, text))
    return " "+text+" "


def replace_laws(text):
    """Making the section acts and articals into a single word"""
    text = re.sub(regx_sections,preprocess_laws,text)
    text = re.sub(regx_acts,preprocess_laws,text)
    text = re.sub(regx_articles,preprocess_laws,text)
    return text


def clear_paras(paras):
    """Cleanig the paragraphs"""
    text_paras = []
    for para in paras:
        x = replace_laws(para)
        x = clean(x)
        text_paras.append(x if len(x) else '<empty>')
    return text_paras

def clean_query_case():
    
    case_path = "../data/raw/Current_Cases/"
    files_name = os.listdir(case_path)
    
    for name in tqdm(files_name,desc='Query_Case_Cleaning'):
        try:
            text = open(case_path+name,'r').readlines()
            rname = name.split('.')[0]
            text_lines = clear_paras(text)
            file_txt = open(f'../data/Clean_Data/query/{rname}.txt','w')
            file_txt.writelines('\n'.join(text_lines).strip('\n'))
            file_txt.close()
            
        except:
            print(f"Exception: {name} is opened in rb")
            text = [str(para) for para in open(case_path+name,'rb').readlines()]
            rname = name.split('.')[0]
            text_lines = clear_paras(text)
            file_txt = open(f'../data/Clean_Data/query/{rname}.txt','w')
            file_txt.writelines('\n'.join(text_lines).strip('\n'))
            file_txt.close()

def clean_prior_cases():
    
    case_path = "../data/raw/Prior_Cases/"
    files_name = os.listdir(case_path)
    
    for name in tqdm(files_name,desc='Prior_Case_Cleaning'):
        text = open(case_path+name,'r').readlines()
        name = name.split('.')[0]
        text_lines = clear_paras(text)
        file_txt = open(f'../data/Clean_Data/prior/{name}.txt','w')
        file_txt.writelines('\n'.join(text_lines).strip('\n'))
        file_txt.close()

if __name__=='__main__':
    clean_query_case()
    print("Query_Done")
    clean_prior_cases() 
    print("Prior_Done")