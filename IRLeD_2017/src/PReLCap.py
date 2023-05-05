from nltk.corpus import stopwords
import nltk
from tqdm import tqdm
import sys
def process(file):
    try:
        raw=open(file).read()
        words= raw.split()
        porter = nltk.PorterStemmer()
        stemmed_tokens = [porter.stem(t) for t in words]
        stop_words = set(stopwords.words('english'))
        voc = [w for w in stemmed_tokens if not w in stop_words]
        return set(voc)
    except:
        raw= str(open(file,'rb').read())
        words= raw.split()
        porter = nltk.PorterStemmer()
        stemmed_tokens = [porter.stem(t) for t in words]
        stop_words = set(stopwords.words('english'))
        voc = [w for w in stemmed_tokens if not w in stop_words]
        return set(voc)


def jaccard_similarity(list1,list2):
    intersec = len(list1 & list2) 
    union = len(list1) + len(list2) - intersec 
    return float(intersec / union)

def findfile(a,name):    
    for i in tqdm(range(1,2001),desc='One Loop'):
        num = str(i).zfill(4)
        path = '../data/raw/Prior_Cases/prior_case_'+ num +'.txt'
        b=process(path)
        f1.write(case_name+'  '+ 'prior_case_'+ num + ' PReLCap ')
        f1.write(str(jaccard_similarity(a,b)))
        f1.write('\n')

if __name__ == '__main__':

    all_case_set = dict()

    f1=open('../data/processed/PReLCap/j_fullscore.txt','w+')
    
    for j in tqdm(range(1,201),desc='Query_Prep'):
        name = str(j).zfill(4)
        path='../data/raw/Current_Cases/current_case_'+name+'.txt'
        case_name = 'current_case_'+name+' Q0 '
        all_case_set[case_name]= process(path)

    for j in tqdm(range(1,2001),desc='Case_Prep'):
        name = str(j).zfill(4)
        path='../data/raw/Prior_Cases/prior_case_'+name+'.txt'
        case_name = 'prior_case_'+ name
        all_case_set[case_name] = process(path)
    
   for i in tqdm(range(1,201),desc='ranking'):
        query_name = 'current_case_'+str(i).zfill(4)+' Q0 '
        for j in range(1,2001):
            prior_name = 'prior_case_'+str(j).zfill(4)+' '
            score = jaccard_similarity(all_case_set[query_name],all_case_set[prior_name])
            f1.write(query_name+prior_name+score+' PReLCap\n')
    f1.close()    
