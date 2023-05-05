import pickle
import re
import os
from tqdm import tqdm
import json
import sys
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math
"""
Run the file from the source folder level
"""
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

def paragraph_level_citation(qv,jm,type,use_para):
    """
    qv : query vector
    jm : judgment vector
    """
    simi = cosine_similarity(qv,jm).reshape(-1)# this is a vector
    simi[::-1].sort()
    if type == 'para_level_mean':
        return np.mean(simi)
    elif type == 'para_level_fix':
        return np.mean(simi[:3])
    elif type == 'para_level_per':
        return np.mean(simi[:max(1,int(len(simi)*use_para))])
    elif type == 'para_level_hybrid':
        return np.mean(simi[:max(1,min(int(len(simi)*0.06),3))])

def generate_ranked_list_citation(type,use_para):
    print(type)
    
    citation_query = getPickel('../data/processed/qcustom_citation_level.pkl')#'../data/processed/qlaw_judg_vec.pkl')#'../data/processed/qlaw_citation_level.pkl')#'../data/processed/query_ciation_level.pkl')
    judg_level = getPickel('../data/processed/pcustom_judg_vec.pkl')#'../data/processed/plaw_judg_vec.pkl')#"../data/processed/jud_level_case_vect.pkl")
    para_level = getPickel('../data/processed/pcustom_judg_matrix.pkl')#'../data/processed/plaw_judg_matrix.pkl')#"../data/processed/para_level_case_vect.pkl")
    vec_len = citation_query[list(citation_query.keys())[0]].shape[1]
    print(vec_len)
    query_results = {}
    count = 0
    if type == 'jud_level':
        for qkey,qval in tqdm(citation_query.items()):
            results = []       
            for jkey,jval in judg_level.items():
                results.append(( jkey, cosine_similarity(qval.reshape(-1,vec_len),jval.reshape(-1,vec_len))[0][0] ))
            results.sort(key=lambda x:x[1] , reverse= True)
            query_results[qkey] = [ (txt,idx,sim)  for idx,(txt,sim) in enumerate(results) ]
    else:
        for qkey,qval in tqdm(citation_query.items()):
            results = []
            if type == 'para_level_mean':
                for jkey,jval in para_level.items():
                    simi = paragraph_level_citation( qval.reshape(-1,vec_len),jval.reshape(-1,vec_len),type,use_para)
                    if math.isnan(simi):
                        simi = 0
                        print(f"Nan present: {count}",end=' ')
                        count+=1
                    # print(simi) 
                    results.append(( jkey, simi))
                results.sort(key=lambda x:x[1] , reverse= True)
                query_results[qkey] = [ (txt,idx,sim)  for idx,(txt,sim) in enumerate(results) ]
            
            elif type == 'para_level_fix':
                for jkey,jval in para_level.items():
                    simi = paragraph_level_citation( qval.reshape(-1,vec_len),jval.reshape(-1,vec_len),type,use_para)
                    if math.isnan(simi):
                        simi = 0
                        print(f"Nan present: {count}",end=' ')
                        count+=1
                    # print(simi) 
                    results.append(( jkey, simi))
                results.sort(key=lambda x:x[1] , reverse= True)
                query_results[qkey] = [ (txt,idx,sim)  for idx,(txt,sim) in enumerate(results) ]
                
            elif type == 'para_level_per':
                for jkey,jval in para_level.items():
                    simi = paragraph_level_citation( qval.reshape(-1,vec_len),jval.reshape(-1,vec_len),type,use_para)
                    if math.isnan(simi):
                        simi = 0
                        print(f"Nan present: {count}",end=' ')
                        count+=1
                    # print(simi)
                    results.append(( jkey, simi))
                results.sort(key=lambda x:x[1] , reverse= True)
                query_results[qkey] = [ (txt,idx,sim)  for idx,(txt,sim) in enumerate(results) ]

            elif type == 'para_level_hybrid':
                for jkey,jval in para_level.items():
                    simi = paragraph_level_citation( qval.reshape(-1,vec_len),jval.reshape(-1,vec_len),type,use_para)
                    if math.isnan(simi):
                        simi = 0
                        print(f"Nan present: {count}",end=' ')
                        count+=1
                    # print(simi)
                    results.append(( jkey, simi))
                results.sort(key=lambda x:x[1] , reverse= True)
                query_results[qkey] = [ (txt,idx,sim)  for idx,(txt,sim) in enumerate(results) ]

    file = open(f'../data/processed/rank_order={type}.json','w')
    json.dump(query_results,file)
    file.close()

if __name__=='__main__':
    type = {0:'jud_level' ,
            1: 'para_level_mean',
            2: 'para_level_fix',
            3: 'para_level_per',
            4: 'para_level_hybrid',
            5: 'thematic_mean',
            6: 'thematic_wieghted'
            }

    generate_ranked_list_citation(type[int(sys.argv[1])],float(sys.argv[2]))
    # generate_ranked_list_citation(type[int(sys.argv[1])],3)
    print("Done")
