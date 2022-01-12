import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
sentence = "How  Friends Colony?"

relevtags=['Hobbies','HOBBIES','ExtraCurricularActivities','Activites','ACTIVITIES','Projects','PROJECTS',
           'WORK','Work','ACHIEVEMENTS','Achievements','SKILLS','Skills','Experience','EXPERIENCE',
           'Qualification','QUALIFICATION','Education','EDUCATION','EDUCATIONAL','Educational']

fo=open("Ujjwal Goyal-CV.txt",'r',encoding='utf-8')
text=fo.read()
fo.close()
fo=open("Ujjwal Goyal-CV.txt",'r',encoding='utf-8')
s=fo.readlines()
fo.close()
#print(text)
print(s)
#num = re.sub(r'[\n][\n]', "", text)
num2 = re.sub(r'[\n]', "", text)
print(num2)
slist=num2.split()
print(num2.split())


def extractmobile(s):
    m = re.search('[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', s)
    if m:
        print("hello")
        found = m.group(0)
        print(found)

# def extractcgpa(s):
#     m = re.findall('[0-9][.][0-9]', s)
#     if m:
#         print("hello")
#         found = m
#         print(found)

def extractemail(s):
    print("vsdf")
    m = re.findall('[ ][a-z|0-9]+[@][a-z]+[.][a-z]+[ ]', s)
    if m:
        print("hello")
        found = m
        print(found)

def extractperc(s):
    m = re.findall('[0-9][0-9][.][0-9][0-9]', s)
    if m:
        print("hello")
        found = m
        print(found)

def extractpersonalinfo(s):
    text=""
    for i in s:
        i=str(i).strip()
        #print(i)
        if i!="CAREER" and i!="Objective" and i!="Career" and i!="OBJECTIVE":
            text=text+str(i)+" "
        else:
            #print("gaya")
            break
    print(text)
    #print(ne_chunk(pos_tag(text.strip().split('.'))))

def extractobjective(s):
    global relevtags
    text=""
    for i in range(0,len(s)):
        temp=str(s[i]).strip()
        #print(i)

        if not temp.find("OBJECTIVE"):
            #print(temp)
            #print("found")
            for j in range(i+1,len(s)):
                if str(s[j]).strip() not in relevtags:
                    text=text+str(s[j]).strip()+" "
                else:
                    break
        else:

            continue
    print(text)
    #print(ne_chunk(pos_tag(text.strip().split('.'))))

def extracteducation(s):
    global relevtags
    text=""
    for i in range(0,len(s)):
        temp=str(s[i]).strip()
        #print(i)

        if not temp.find("EDUCATION") or not temp.find("EDUCATIONAL") or not temp.find("Education") or not temp.find("Educational") or not temp.find("QUALIFICATION"):
            #print(temp)
            #print("found")
            for j in range(i+1,len(s)):
                if str(s[j]).strip() not in relevtags:
                    text=text+str(s[j]).strip()+" "
                else:
                    break
        else:

            continue
    print(text)


def extractskills(s):
    global relevtags
    text=""
    for i in range(0,len(s)):
        temp=str(s[i]).strip()
        #print(i)

        if not temp.find("SKILLS") or not temp.find("Skills")  or not temp.find("Skill")  or not temp.find("skill"):
            #print(temp)
            #print("found")
            for j in range(i+1,len(s)):
                if str(s[j]).strip() not in relevtags:
                    text=text+str(s[j]).strip()+" "
                else:
                    break
        else:

            continue
    print(text)

def extractachievements(s):
    global relevtags
    text=""
    for i in range(0,len(s)):
        temp=str(s[i]).strip()
        #print(i)

        if not temp.find("Achievements") or not temp.find("ACHIEVEMENTS"):
            #print(temp)
            #print("found")
            for j in range(i+1,len(s)):
                if str(s[j]).strip() not in relevtags:
                    text=text+str(s[j]).strip()+" "
                else:
                    break
        else:

            continue
    print(text)

def extractprojects(s):
    global relevtags
    text=""
    for i in range(0,len(s)):
        temp=str(s[i]).strip()
        #print(i)

        if not temp.find("Projects") or not temp.find("PROJECTS"):
            #print(temp)
            #print("found")
            for j in range(i+1,len(s)):
                if str(s[j]).strip() not in relevtags:
                    text=text+str(s[j]).strip()+" "
                else:
                    break
        else:

            continue
    print(text)

def extracthobbies(s):
    global relevtags
    text=""
    for i in range(0,len(s)):
        temp=str(s[i]).strip()
        #print(i)

        if not temp.find("Activities") or not temp.find("ACTIVITIES"):
            #print(temp)
            #print("found")
            for j in range(i+1,len(s)):
                if str(s[j]).strip() not in relevtags:
                    text=text+str(s[j]).strip()+" "
                else:
                    break
        else:

            continue
    print(text)



extractmobile(text)
extractemail(num2)
extractperc(num2)
extractpersonalinfo(slist)
extractobjective(slist)
extracteducation(slist)
extractskills(slist)
extractachievements(slist)
extractprojects(slist)
extracthobbies(slist)