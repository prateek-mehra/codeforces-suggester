from flask import Flask
from flask import render_template
from flask import request,redirect,url_for
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method=="POST":
        name=request.form["username"]
        return redirect(url_for("user",usr=name))
    else:
        return render_template('login.html')


        

@app.route('/<usr>')
def user(usr):
    if usr is None:
        return "ERROR"
    import matplotlib.pyplot as plt
    from pprint import pprint
    import requests,random
    from collections import defaultdict
    
    verdicts=defaultdict(list)
    page="https://codeforces.com/api/user.status?handle="+usr
    page+="&from=1&count=450"
    open=requests.get(page).json()
    res=open["result"]
    nm=[]
    problems=[]
    probset=[]
    tagset=[]
    tagle=[]
    strong_topics=[]

    strength={'2-sat':0,'chinese remainder theorem':0,'greedy':0,'binary search':0,'brute force':0,'combinatorics':0,'constructive algorithms':0,'data structures':0,'dfs and similar':0,'bitmasks':0,'*special':0
         ,'divide and conquer':0,'dp':0,'dsu':0,'fft':0,'expression parsing':0,'flows':0,'games':0,'geometry':0,'graph matchings':0,'implementation':0,'hashing':0,'graphs':0,'interactive':0,'math':0,'matrices':0,'meet-in-the-middle':0,'number theory':0, 'probabilities':0,'schedules':0,'shortest paths':0,'sortings':0,'string suffix structures':0,'strings':0,'ternary search':0,'trees':0,'two pointers':0}
    
    total={'2-sat':0,'chinese remainder theorem':0,'greedy':0,'binary search':0,'brute force':0,'combinatorics':0,'constructive algorithms':0,'data structures':0,'dfs and similar':0,'bitmasks':0,'*special':0
         ,'divide and conquer':0,'dp':0,'dsu':0,'fft':0,'expression parsing':0,'flows':0,'games':0,'geometry':0,'graph matchings':0,'implementation':0,'hashing':0,'graphs':0,'interactive':0,'math':0,'matrices':0,'meet-in-the-middle':0,'number theory':0, 'probabilities':0,'schedules':0,'shortest paths':0,'sortings':0,'string suffix structures':0,'strings':0,'ternary search':0,'trees':0,'two pointers':0}
    
    final={'2-sat':0,'chinese remainder theorem':0,'greedy':0,'binary search':0,'brute force':0,'combinatorics':0,'constructive algorithms':0,'data structures':0,'dfs and similar':0,'bitmasks':0,'*special':0
         ,'divide and conquer':0,'dp':0,'dsu':0,'fft':0,'expression parsing':0,'flows':0,'games':0,'geometry':0,'graph matchings':0,'implementation':0,'hashing':0,'graphs':0,'interactive':0,'math':0,'matrices':0,'meet-in-the-middle':0,'number theory':0, 'probabilities':0,'schedules':0,'shortest paths':0,'sortings':0,'string suffix structures':0,'strings':0,'ternary search':0,'trees':0,'two pointers':0}
    
    for item in res:
        problems.append(item["problem"]["name"])
        verdicts[item["problem"]["name"]].append(item["verdict"])
        nm.append(item["problem"]["tags"])
        
    for i in range(len(nm)):
        for j in range(len(nm[i])):
            tagle.append(nm[i][j])
    
    for i in range(len(problems)-1):
        if(problems[i]!=problems[i+1]):
            probset.append(problems[i])
            tagset.append(nm[i])
    
    for i in range(len(probset)):
        if(len(verdicts[probset[i]])==1 and verdicts[probset[i]][0]=="OK"):
            for j in range(len(tagset[i])):
                strength[tagset[i][j]]+=1
    
    for i in range(len(probset)):
        for j in range(len(tagset[i])):
            total[tagset[i][j]]+=1

    for i in total:
        if(total[i]>0):
            final[i]=strength[i]/total[i]

    #for i in final:
    #    print(i,final[i])


    sort_strength = sorted(final.items(), key=lambda x: x[1], reverse=True)
    ctr2=0
    strongest=[]
    for i in sort_strength:
        ctr2+=1
        if(ctr2<=10):
            strong_topics.append(i[0])
        if(ctr2<=5):
            strongest.append(i[0])
    #print("Your strong topics are:")

    #for i in range(len(strong_topics)):
    #    print(strong_topics[i])
    weak=strong_topics.copy()
    weak.reverse()
    links=[]
    sample="http://codeforces.com/problemset?tags="
    ctr=0
    for i in range(len(weak)):
        if ctr<5:
            ctr+=1
            links.append(weak[i])
    improve=links.copy()
    linknew=[]
    for i in range(len(links)):
        linknew.append(links[i].replace(" ","%20"))
        #print(linknew[i])

    stronglinks=[]
    weaklinks=linknew.copy()
    for i in range(len(strongest)):
        stronglinks.append(sample+strongest[i].replace(" ","%20"))
        #print(stronglinks[i])

    for i in range(len(weaklinks)):
        weaklinks[i]=sample+weaklinks[i]
        #print(weaklinks[i])

      
    page2="https://codeforces.com/api/user.info?handles="
    page2+=usr
    res2=requests.get(page2).json()["result"]
    rank=res2[0]["rating"]
    ctr=0
    probid=[] 
    indices=[]  
    for i in range(len(linknew)):
        if ctr<5:
            ctr+=1
            page3="https://codeforces.com/api/problemset.problems?tags="
            page3+=linknew[i]    
            res3=requests.get(page3).json()["result"]
            
            for i in res3["problems"]:
                if "rating" in i:
                    if i["rating"]>=rank and i["rating"]-rank<=200:
                        probid.append(i["contestId"])
                        indices.append(i["index"])  

                    if rank>=3500:
                        if rank-i["rating"]<=200:
                            probid.append(i["contestId"])
                            indices.append(i["index"])
    finallinks=[]
    sample2="https://codeforces.com/problemset/problem"                  
    for i in range(25):
        a=random.randrange(1,len(probid))
        finallinks.append(sample2+"/"+str(probid[a])+"/"+str(indices[a]))



 
    return render_template('suggester.html',Myname=usr,topics=strongest,links=finallinks,improve=improve,stronglinks=stronglinks,weaklinks=weaklinks)
    
if __name__=="__main__":
    name=None
    app.run(debug=True) 