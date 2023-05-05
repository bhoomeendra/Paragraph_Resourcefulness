from sklearn.feature_extraction.text import TfidfVectorizer
from glob import glob 
from tqdm import tqdm
import pickle

def putPickel(var,path):
    with open(path,'wb') as file:
        pickle.dump(var,file)
        print(f"Pickel Dumped in {path}")


qc_path = '../data/Clean_Data/query/*'
pc_path = '../data/Clean_Data/prior/*'
tfidf_model = TfidfVectorizer(min_df=2,max_df=0.9,ngram_range=(1,2))



all_docs = []
for path in tqdm(glob(qc_path),desc="Query_Case_Loading"):
    all_docs.append(' '.join(open(path).readlines()).strip())
for path in tqdm(glob(pc_path),desc="Prior_Case_Loading"):
    all_docs.append(' '.join(open(path).readlines()).strip())
clean_all =  [x.replace('\n','') for x in all_docs]

print("Training Tf-Idf Model Please wait for some time :)")

tfidf_model.fit(clean_all)

print("TF-Idf Model trained of vocublary size",len(tfidf_model.vocabulary_))


pc_judg_vec = dict()
for path in tqdm(glob(pc_path),desc="Prior_Case_Vectorization_at_Document_level"):# Using whole judgment
    name = path.split('/')[-1].split('.')[0]
    pc_judg_vec[name] = tfidf_model.transform([' '.join(open(path).readlines()).strip()])

pc_judg_matrix = dict()
for path in tqdm(glob(pc_path),desc="Prior_Case_Vectorization_at_Paragraph_level"): # Paragraph based search space 
    name = path.split('/')[-1].split('.')[0]
    out = open(path).readlines()
    pc_judg_matrix[name] = tfidf_model.transform( out if len(out) else ['empty'])

qc_para_matrix = dict()
for path in tqdm(glob(qc_path),desc="Query_Case_Vectorization_at_Paragraph_level"): # Paragraph based search space 
    name = path.split('/')[-1].split('.')[0]
    out = open(path).readlines()
    qc_para_matrix[name] = tfidf_model.transform( out if len(out) else ['empty'])


qc_citation_level = dict()
for path in tqdm(glob(qc_path),desc="Quer_Case_Vectorization_with_citation_paragraphs"):
    name = path.split('/')[-1].split('.')[0]
    citation_lines = []
    out = open(path).readlines()
    for line in out:
        if line.find('?citation?') > -1:
            citation_lines.append(line)

    if len(citation_lines) == 0:
        print("No citations found")
        citation_lines.extend(out)
    qc_citation_level[name] = tfidf_model.transform(citation_lines)

putPickel(qc_para_matrix,'../data/processed/qcustom_para_matrix.pkl')
putPickel(pc_judg_vec,'../data/processed/pcustom_judg_vec.pkl')
putPickel(qc_citation_level,'../data/processed/qcustom_citation_level.pkl')
putPickel(pc_judg_matrix,'../data/processed/pcustom_judg_matrix.pkl')