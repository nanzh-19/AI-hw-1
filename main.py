import json

def importFreqTree(filename):
    with open(filename,'r') as f:
        lines=[line for line in f]
    data=[json.loads(line) for line in lines]
    all_word=data[0]
    single_tree=data[1]
    freq_tree=data[2]
    return (all_word,single_tree,freq_tree)

def vv2ww(voice1,voice2,lamda):
    ww={}
    vv=voice1+voice2
    if voice1 in freq_tree.keys():
        Tree1=freq_tree[voice1]
    else:
        print('error:illegal voice input'+voice1)
    for word1 in Tree1.keys():
        Tree2=Tree1[word1]
        if vv in Tree2:
            Tree3=Tree2[vv]
            freq=Tree2['Freq_of_word']
            for wordword in Tree3:
                if Tree3[wordword]>freq_limit:
                    ww[wordword]=Tree3[wordword]/freq*lamda+(1-lamda)*freq/all_word['all_word']
    if ww is None:
        w1=single_tree[voice1]
        return(w1)
    return(ww)

def wv2ww(w1,voice1,voice2,lamda):
    w2={}
    if voice2 not in freq_tree:
        print('error:illegal voice input'+voice2)
    Tree1=freq_tree[voice1]
    Tree2=Tree1[w1]
    vv=voice1+voice2
    if vv in Tree2:
        Tree3=Tree2[vv]
    freq=Tree2['Freq_of_word']
    for wordword in Tree3:
        temp_w2=wordword[-1]
        if Tree3[wordword]>freq_limit:
            w2[temp_w2]=Tree3[wordword]/freq*lamda+(1-lamda)*freq/all_word['all_word']
    return(w2)



def pinyin2hanzi(yijuhua,lamda,item_limit):
    hanzi=[]
    if len(yijuhua)==1:
        if yijuhua[0] in single_tree.keys():
            return(single_tree[yijuhua[0]])
        else:
            print('error:illegal voice input'+yijuhua[0])
            return([[yijuhua[0],0]])
    i=0
    while i<len(yijuhua)-1:
        voice1=yijuhua[i]
        voice2=yijuhua[i+1]
        if i==0:
            temp=vv2ww(voice1,voice2,lamda)
            temp_tuple=sorted(temp.items(),key=lambda d:d[1],reverse=True)
            ii=0
            while len(hanzi)<min(item_limit,len(temp_tuple)):
                hanzi.append([temp_tuple[ii][0],temp_tuple[ii][1]])
                ii=ii+1
            i=i+1
            continue            
        all_w1={}
        for item in hanzi:
            w1=item[0][-1]
            if w1 not in all_w1:
                all_w1[w1]={item[0]:item[1]}
            else:
                tt=all_w1[w1]
                tt[item[0]]=item[1]
        temp_dict={}
        for w1 in all_w1:
            temp=wv2ww(w1,voice1,voice2,lamda)
            tt=all_w1[w1]
            for old in tt:
                for new in temp:
                    temp_dict[old+new]=tt[old]*temp[new]
        temp_tuple=sorted(temp_dict.items(),key=lambda d:d[1],reverse=True)
        hanzi=[]
        ii=0
        while len(hanzi)<min(item_limit,len(temp_tuple)):
            hanzi.append([temp_tuple[ii][0],temp_tuple[ii][1]])
            ii=ii+1
        i=i+1
    if hanzi:
        return(hanzi)

freq_limit=400

all_word,single_tree,freq_tree=importFreqTree('Freq_Tree.json')
input_filename='input.txt'
with open(input_filename,'r') as f:
    pin_yin=[line for line in f]
f=open('output.txt','w')
f.close()
f=open('output.txt','a')
for yijuhua in pin_yin:
    lamda=0.5
    item_limit=100
    yijuhua=yijuhua.split()
    out=pinyin2hanzi(yijuhua,lamda,item_limit)
    output=out[0][0]
    print(output)
    f.write(output+'\n')
f.close()
print('Transformation is complished')
