a={'1':'2','3':'4'}
a=sorted(a.items(),key=lambda d:d[1],reverse=True)
print(a)