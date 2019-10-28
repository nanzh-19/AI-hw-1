import json
import time
import os

def build_v_w_dict(filename):
    v_dict={}
    w_dict={}
    with open(filename,'r',encoding='gbk') as f:
        for line in f:
            line=line.split()
            voice=line[0]
            line.pop(0)
            v_dict[voice]=line
            for word in line:
                if word in w_dict.keys():
                    w_dict[word].append(voice)
                else:
                    w_dict[word]=[]
                    w_dict[word].append(voice)
    return v_dict,w_dict

def getdata(filename):
    lines=[]
    data=[]
    with open(filename,'r',encoding='gbk') as f:
        lines=[line for line in f]
    data=[json.loads(line) for line in lines]
    return data

def build_tree_from_str(theString,theTree,count):
    



def train_tree(inFile,theTree,outFile,count):
    data=getdata(inFile)
    for line in data:
        title=line['title']
        content=line['html']



filename='拼音汉字表.txt'
v_dict,w_dict=build_v_w_dict(filename)

freq_tree={}
count=0

for i in range(2,12):
    inFile ='2016-'+'%02d'%i+'.txt'
    outFile='train-'+'%02d'%i+'.json'
    freq_tree,count=def train_tree(inFile,freq_tree,outFile,count)

    




# 检验v_dict,w_dict
# filename='v_w_dict.json'
# with open(filename,'w') as f:
#     # json.dump(v_dict,f)
#     json.dump(w_dict,f)

# with open(filename) as f:
#     a=json.load(f)
# print(a)