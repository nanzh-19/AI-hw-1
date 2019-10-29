import json
line=[]
data=[]
with open('Freq_Tree.json','r',encoding='utf-8') as f:
    lines=[line for line in f]
    data=[json.loads(line) for line in lines]
    print(data)