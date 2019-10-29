import json
import time
import os

def build_v_w_dict(filename):
    v_dict={}
    w_dict={}
    with open(filename,'r') as f:
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
    return (v_dict,w_dict)

def getdata(filename):
    lines=[]
    data=[]
    with open(filename,'r',encoding='utf-8') as f:
        lines=[line for line in f]
        data=[json.loads(line) for line in lines]
    return data

def build_tree_from_str(theString,theTree,count):
    N=len(theString)
    i=0
    count=0
    while i<(N-1):
        word1=theString[i]
        word2=theString[i+1]
        if word2 not in w_dict.keys():
            i=i+1
            continue
        if word1 not in w_dict.keys():
            i=i+1
            continue
        voice1=w_dict[word1]
        voice2=w_dict[word2]
        for voice1_i in voice1:
            if voice1_i in theTree.keys():
                son1=theTree[voice1_i]
            else:
                theTree[voice1_i]={}
                son1=theTree[voice1_i]
            if word1 in son1.keys():
                son2=son1[word1]
                son2['Freq_of_word']=son2['Freq_of_word']+1
            else:
                son1[word1]={}
                son2=son1[word1]
                son2['Freq_of_word']=1
            #处理句子最后一个字
            if i==(N-2):
                if word2 in son1.keys():
                    son2=son1[word2]
                    son2['Freq_of_word']=son2['Freq_of_word']+1
                else:
                    son1[word2]={}
                    son2=son1[word2]
                    son2['Freq_of_word']=1
            for voice2_i in voice2:
                vv=voice1_i+voice2_i
                if vv in son2.keys():
                    son3=son2[vv]
                else:
                    son2[vv]={}
                    son3=son2[vv]
                ww=word1+word2
                if ww in son3.keys():
                    son3[ww]=son3[ww]+1
                else:
                    son3[ww]=1
        i=i+1
    return (theTree,count)

def train_tree(inFile,theTree,outFile,count):
    data=getdata(inFile)
    for line in data:
        title=line['title']
        content=line['html']
        theTree,count=build_tree_from_str(title,theTree,count)
        theTree,count=build_tree_from_str(content,theTree,count)
    with open(outFile,'w') as f:
        json.dump(theTree,f)
    return (theTree,count)


filename='拼音汉字表.txt'
v_dict,w_dict=build_v_w_dict(filename)

freq_tree={}
count=0


for i in range(2,12):
    inFile ='2016-'+'%02d'%i+'.txt'
    outFile='train-'+'%02d'%i+'.json'
    start=time.time()
    number=0
    freq_tree,count=train_tree(inFile,freq_tree,outFile,count)
    time1=time.time()-start
    number=number+1
    print(str(number),time1)
    if time1>3600:
        break
    if i > 2:
        del_i = i-2
        del_f = open('train-'+'%02d'%del_i+'.json','w')
    
singleTree={}
for voice in freq_tree:
    freq=1
    Tree1=freq_tree[voice]
    for word in Tree1:
        Tree2=Tree1[word]
        if Tree2['Freq_of_word']>freq:
            freq=Tree2['Freq_of_word']
            theWord=word
    singleTree[voice]=theWord

tf = open('Freq_Tree.json','w')#清空Freq_Tree
tf.close()

with open('Freq_Tree.json','a') as f:
    json.dump({'all_word':count},f)
    f.write('\n')
    json.dump(singleTree,f)
    f.write('\n')
    json.dump(freq_tree,f)
    f.write('\n')
    f.close()

print('training is over')



# 检验v_dict,w_dict
# filename='v_w_dict.json'
# with open(filename,'w') as f:
#     # json.dump(v_dict,f)
#     json.dump(w_dict,f)

# with open(filename) as f:
#     a=json.load(f)
# print(a)