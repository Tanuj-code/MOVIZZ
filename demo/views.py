from django.shortcuts import render,redirect
import pandas as pd
import numpy as np
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.validators import validate_email
movies=pd.read_csv('imdb_top_1000.csv')
star={}
genre={}
rating={}
mapp={}
over={}
release={}
cert={}
run={}
tags={}
for i in movies.values:
    mapp[i[1]]=i[0]
    over[i[1]]=i[7]
    release[i[1]]=i[2]
    cert[i[1]]=i[3]
    run[i[1]]=i[4]
for i in movies.columns:
    if(i=='IMDB_Rating' or i=='Released_Year'  or i=='Meta_score' or i=='No_of_Votes' or i=='Gross'):
        continue
    movies[i]=movies[i].str.lower()


for i in movies.values:
    star[i[10]]=1
    star[i[11]]=1
    star[i[12]]=1
    star[i[13]]=1
    ss=str(i[10]).title()+ ", " + str(i[11]).title()+", "+str(i[12]).title()+", "+str(i[13]).title()
    for j in i[5].split(','):
        j=j.strip().title()
        genre[j]=1
        ss+=", "+str(j.title())
    rating[i[6]]=1
    tags[i[1].title()]=ss
star=list(star.keys())
genre=list(genre.keys())
rating=list(rating.keys())

molist=list(movies['Series_Title'])
chart=pd.DataFrame(index=movies['Series_Title'], columns=genre)
ind=chart.index
chart=dict(chart)
for i in range(0, 1000):
    stp=movies.values[i][5].split(',')
    for j in stp:
        j=j.strip()

        chart[j.title()][ind[i]]=1
chart=pd.DataFrame(chart)
chart.fillna(0, inplace=True)

from sklearn.metrics.pairwise import cosine_similarity
score=cosine_similarity(chart)
chart1=pd.DataFrame(index=movies['Series_Title'], columns=star)
chart3=pd.DataFrame(index=movies['Series_Title'], columns=genre)
chart1.fillna(0, inplace=True)
chart3.fillna(0, inplace=True)
chart1=dict(chart1)
chart3=dict(chart3)
for i in range(0, 1000):
    stp=[movies.values[i][10], movies.values[i][11], movies.values[i][12], movies.values[i][13]]
    for j in stp:
        chart1[j][ind[i]]=1
    stp=movies.values[i][5].split(',')
    for j in stp:
        aj=j.strip().title()
        chart3[aj][ind[i]]=1
chart1=pd.DataFrame(chart1)
chart3=pd.DataFrame(chart3)
score1=cosine_similarity(chart1)

a=movies.iloc[:, [1, 5]]
b=movies.iloc[:, [1, 6]]
b=b.sort_values('IMDB_Rating', ascending=False)
movcol=chart1.columns
movcol=list(movcol)

def recc(name):
    name=name.lower()
    lst=[]
    if name not in chart.index:
        return lst
    index=np.where(chart.index==name)[0][0]
    similar_items = sorted(list(enumerate(score[index])),key=lambda x:x[1],reverse=True)[1:51]
    for j in similar_items:
        if(j[1]==0):
            break
        lst.append(chart.index[j[0]])
    return lst

def rec1(name):
    name=name.lower()
    lst=[]
    if name not in chart1.index:
        return lst
    index=np.where(chart1.index==name)[0][0]
    similar_items = sorted(list(enumerate(score1[index])),key=lambda x:x[1],reverse=True)
    for j in similar_items:
        if(j[1]==0):
            break
        lst.append(chart1.index[j[0]])
    return lst

def mofindbyactor(xx):
    xx=xx.lower()    
    
    lst=[]
    fin=[]
    for i in xx.split(','):
        lst.append(i.strip())
    
    for k in lst:
        if(k not in chart1.columns):
            return fin
    newl=chart1[lst]
    
    for j in range(0, 1000):
        if(sum(newl.values[j])==len(lst)):            
            fin.append(newl.index[j])   
    return fin
def mofindbygenre(xx):
    xx=xx.lower()    
    
    lst=[]
    fin=[]
    for i in xx.split(','):
        lst.append(i.strip().title())
    
    for k in lst:
        if(k not in chart3.columns):
            return fin
    newl=chart3[lst]
    
    for j in range(0, 1000):
        if(sum(newl.values[j])==len(lst)):            
            fin.append(newl.index[j])   
    return fin
def home(request):
    return render(request, 'home.html')
def top(request):
    mapp2={}
    for i in movies.values:
        if(str(i[1]).title() in mapp):
            
        
            mapp2[str(i[1]).title()]=str(i[6])
    mapp2=sorted(mapp2.items(), key=lambda x:x[1], reverse=True)
    rat={}
    for x in mapp2:
        rat[x[0]]=mapp[x[0]]
        if(len(rat)==50):
            break
    newdict=[]
    for i in rat:
        li=[]
        li.append(i)
        li.append(rat[i])
        li.append(over[i])
        li.append(release[i])
        li.append(cert[i])
        li.append(run[i])
        newdict.append(li)
    return render(request, 'top.html', {"ratlist": newdict})
def contact(request):
    ear='''
    if(request.method=='POST'):
        name=request.POST['name']
        email=request.POST['email']
        ph=request.POST['ph']
        desc=request.POST['desc']
        if len(desc)>=150:
            desc=desc[0:150]
        if len(name)>=150:
            name=name[0:150]
        if len(email)>=150:
            email=email[0:150]
        if len(ph)>=150:
            ph=ph[0:150]
        try:
            u=User.objects.get(username=name)     
            q=u
            q.first_name=ph
            q.last_name=desc
            q.email=email
            q.save()
        except:
            user=User.objects.create_user(username=name, email=email, first_name=ph, last_name=desc)
            user.save()       
        return redirect('')
    else:
        return render(request, 'contact.html')
    '''
    if(request.method=='POST'):
        name=request.POST['name']
        email=request.POST['email']
        ph=request.POST['ph']
        desc=request.POST['desc']
        try:
            validate_email(email)
            send_mail(name, "[Name:"+" "+ name+"] "+"[Email:"+" "+ email+"] "+"[Phone:"+" "+ ph+"] "+"[Context:"+" "+ desc+"]", settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
            return redirect('')
        except:
            
            return redirect('contact')
        
        
    else:
        return render(request, 'contact.html')



        
   
    

    

def rec(request):
    val=request.POST["mov"]
    val=val.title()
    val2=rec1(val)
    val3=mofindbyactor(val)
    val4=mofindbygenre(val)
    temp=val
    val=recc(val)
    
    dct1=[]
    dct2=[]
    dct3=[]
    dct4=[]
    for i in val:
        aa=i.title()
        if(aa==temp):
            continue
        if(aa in mapp):
            ll=[]
            ll.append(aa)
            ll.append(mapp[aa])
            ll.append(tags[aa])
            dct1.append(ll)
    for i in val2:
        aa=i.title()
        if(aa==temp):
            continue
        if(aa in mapp):
            
            ll=[]
            ll.append(aa)
            ll.append(mapp[aa])
            ll.append(tags[aa])
            dct2.append(ll)
    for i in val4:
        aa=i.title()
        if(aa==temp):
            continue
        if(aa in mapp):
            ll=[]
            ll.append(aa)
            ll.append(mapp[aa])
            ll.append(tags[aa])
            dct3.append(ll)
    
    for i in val3:
            
            aa=i.title()
            if(aa==temp):

                continue
            if(aa in mapp):


                
                ll=[]
                ll.append(aa)
                ll.append(mapp[aa])
                ll.append(tags[aa])
                dct4.append(ll)    


    return render(request, 'home.html', {"l1": dct1, "l2":dct2, "l3":dct3, "l4":dct4})