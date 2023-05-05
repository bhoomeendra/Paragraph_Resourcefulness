import json 
import sys

def get_trec_format(path):
    file =  open(path,'r')
    out  = json.load(file)
    file.close()
    name_file = path.split('=')[1].split('.')[0]
    lines = []
    for key,val in out.items():
        for a in val:
            lines.append(key+" Q0 "+str(a[0])+" "+str(a[1])+' '+str(a[2])+" "+name_file+'\n')
    print(name_file)
    file = open('../data/query_results/'+name_file,'w')
    file.writelines(lines)
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
    file_path = f"../data/processed/rank_order={type[int(sys.argv[1])]}.json"# should come from yml
    get_trec_format(path=file_path)
    print("Convert to trec format")