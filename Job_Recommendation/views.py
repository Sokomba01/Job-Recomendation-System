from django.shortcuts import render, HttpResponse, redirect
from Job_Recommendation.models import *
#from  Job_Recommendation.models import UserResumes
from django.contrib.auth.models import User
from django.contrib import messages
from Job_Recommendation.forms import *
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.mail import  EmailMessage
from django.shortcuts import get_object_or_404
import os
import re
from django.shortcuts import get_object_or_404
import zipfile
import PyPDF2
from django.shortcuts import render
import pythoncom
pythoncom.CoInitialize()
import comtypes.client
from .forms import UploadFileForm
from .models import UserResumes
from Job_Recommendation_System.settings import MEDIA_ROOT
from docxtpl import DocxTemplate
from nltk.corpus import stopwords
import numpy as np
import numpy.linalg as LA
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from fuzzywuzzy import process
from datetime import date
# Create your views here.




def index(request):
    return render(request,"Recommendation/index.html")
def studentpage(request):
    return render(request,"Recommendation/studentpage.html")
def about_us(request):
    return render(request,"Recommendation/about_us.html")
def recruiterpage(request):
    return render(request,"Recommendation/recruiterpage.html")
def blog_details(request):
    data = Job_Dataset.objects.all()
    # data=[up2.JobTitle,up2.Company,up2.Location,up2.PostDate,up2.ExtractDate,up2.Summary,up2.Salary,up2.JobUrl]
    for up2 in data:
      tall={'JobTitle':up2.JobTitle}
      print(tall)
    respp= render(request,"Recommendation/blog_details.html",{'data1':tall})
    return respp
def Signup(request):
    return render(request,"Recommendation/Signup.html")
def Contact_us(request):
    return render(request,"Recommendation/Contact_us.html")
def signup(request):
    if request.method=="POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        role_select = request.POST['role_select']
        password = request.POST['password']
        again_password = request.POST['again_password']
        phone_number= request.POST['phone_number']
        myuser = EmployeeForm(request.POST)
        if myuser.is_valid():
            print("user saved....!!!!")
            myuser.save()
        if User.objects.filter(username=username):
            messages.warning(request, 'This email is already taken: Try another Email')
            print("already Exists....!!!!")
            return render(request, 'Recommendation/Signup.html', {'form': EmployeeForm()})
            #return redirect('Signup')
        if (password != again_password):
            messages.error(request, " Passwords do not match")
            print("Unmatched password")
            return render(request, 'Recommendation/Signup.html', {'form': EmployeeForm()})
        if len(username) < 14:
            messages.error(request, " Your user name must be under 10 characters")
            return render(request, 'Recommendation/Signup.html', {'form': EmployeeForm()})
            #return redirect('index')
        if len(first_name) < 3:
            messages.error(request, " Your First name must be under 3 characters")
            return render(request, 'Recommendation/Signup.html', {'form': EmployeeForm()})
            #return redirect('index')
        if len(last_name) < 3:
            messages.error(request, " Your Last name must be under 3 characters")
            return render(request, 'Recommendation/Signup.html', {'form': EmployeeForm()})
            #return redirect('index')
        if len(password) < 6:
            messages.error(request, " Your password must be under 6 characters")
            return render(request, 'Recommendation/Signup.html', {'form': EmployeeForm()})
            #return redirect('index')

        else:
            if role_select == "student":
                myuser1 = User.objects.create_user(username, first_name, password)
                myuser1.save()
                my_admin_group = Group.objects.get_or_create(name='Student')
                my_admin_group[0].user_set.add(myuser1)
                messages.success(request, "Your Account has been successfully created")
                return HttpResponseRedirect('/Login')
            else:
                myuser1 = User.objects.create_user(username, first_name, password)
                myuser1.save()
                my_admin_group = Group.objects.get_or_create(name='Recruiter')
                my_admin_group[0].user_set.add(myuser1)
                messages.success(request, "Your Account has been successfully created")
                return HttpResponseRedirect('/Login')

    return render(request, 'Recommendation/index.html')
def is_recruiter(user):
    return user.groups.filter(name='Recruiter').exists()
def is_student(user):
    return user.groups.filter(name='Student').exists()
def afterlogin(request):
    if is_recruiter(request.user):
        return redirect('recruiterpage')
    elif is_student(request.user):
        return redirect('studentpage')
    else:
        return render(request,'Recommendation/index.html')
    return HttpResponse("Talha")
@login_required(login_url='/Login')
@user_passes_test(is_student)
@login_required(login_url='/Login')
@user_passes_test(is_student)
def studentpage(request):
    return render(request,"Recommendation/studentpage.html")
@login_required(login_url='/Login')
@user_passes_test(is_recruiter)
def recruiterpage(request):
    return render(request,"Recommendation/recruiterpage.html")
def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully Logout")
    return redirect('index')
@login_required(login_url='/Login')
@user_passes_test(is_student)
def resumeupload(request):
    return render(request,"Recommendation/resumeupload.html")
try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'

relevtags=['Hobbies','HOBBIES','ExtraCurricularActivities','Activites','ACTIVITIES','Projects','PROJECTS','WORK','Work',
           'ACHIEVEMENTS','Achievements','SKILLS','Skills','Skill','Experience','EXPERIENCE','Qualification','QUALIFICATION','Education',
           'EDUCATION','EDUCATIONAL','Educational']
def get_docx_text(path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    wdFormatPDF = 17
    word=comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open('word/document.xml')
    doc.SaveAs(FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()
    # document = zipfile.ZipFile(path)
    # xml_content = document.read('word/document.xml')
    # document.close()
    # tree = XML(xml_content)

    # paragraphs = []
    # for paragraph in tree.getiterator(PARA):
    #     texts = [node.text
    #              for node in paragraph.getiterator(TEXT)
    #              if node.text]
    #     if texts:
    #         paragraphs.append(''.join(texts))
    #
    # return '\n\n'.join(paragraphs)


def convertpdf(name):
    #print("hiiii")
    pdfobj=open("UploadedResumes/"+str(name), 'rb')
    pdfreader=PyPDF2.PdfFileReader(pdfobj)
    #print(pdfreader.numPages)
    x = name[0:len(name)-3]
    desturl =str(x)+"txt"
    fob = open("UploadedResumes/"+desturl, "w", encoding="utf-8")
    for page in pdfreader.pages:
        s = page.extractText()
        #print(s)
        lines=s.split("\n")
        #print(lines)
        for line in lines:
            fob.write((line + "\n"))

    fob.close()
    pdfobj.close()


def handle_uploaded_file(file, name, content):
    fo = open("UploadedResumes/" + str(name), "wb+")
    for chunk in file.chunks():
        fo.write(chunk)
    fo.close()
    if content.endswith("pdf"):
        convertpdf(name)
    if content.endswith=='document':

        text = get_docx_text("UploadedResumes/",name)
        # text = os.linesep.join([s for s in text.splitlines() if s])
        # s=str(name)
        # fo = open('UploadedResumes/'+s[:s.rfind('.')]+".txt", "w",encoding="utf-8")
        # fo.write(text)
        # fo.close()


def resumeupload(request):
    if request.method=="POST":
        uploadform=UploadFileForm(request.POST, request.FILES)
        if uploadform.is_valid():
            #print("its in normal")
            file = request.FILES['file']
            print(file.name)
            print(file.content_type)
            handle_uploaded_file(file, file.name, file.content_type)
            x = file.name[0:len(file.name) - 3]
            desturl = str(x) + "txt"
            fo = open("UploadedResumes/" + desturl, "r", encoding="utf-8")
            text = fo.read()
            fo.close()
            fo = open("UploadedResumes/" + desturl, "r", encoding="utf-8")
            s = fo.readlines()
            fo.close()
            # print(text)
            #print(s)
            # num = re.sub(r'[\n][\n]', "", text)
            num2 = re.sub(r'[\n]', "", text)
            slist = num2.split()
            mobno=extractmobile(text)
            email=extractemail(num2)
            perc=extractperc(num2)
            # pinfo=extractpersonalinfo(slist)
            # obj=extractobjective(slist)
            edu=extracteducation(slist)
            skill=extractskills(slist)
            achieve=extractachievements(slist)
            projects=extractprojects(slist)
            hobb=extracthobbies(slist)
            skill = str(skill)
            email = str(email)
            user=UserResumes(mobile=mobno,email=email,skill=skill, companylocation="Lahore", experience="3")
            user.save()
            for i in UserResumes.objects.all():
                print(i.mobile)
            #return redirect('getrecommend')
            return render(request, "Recommendation/Recommendation.html")
            # return render(request, 'Recommendation/success.html', {'mobno':mobno,'email':email,'skills':skill,'achieve':achieve,'hobbies':hobb})
        else:
            print("default form created")
            form=UploadFileForm()
    return render(request,'Recommendation/resumeupload.html',{'fileform':form})


def extractmobile(s):
    m = re.search('[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', s)
    if m:
        #print("hello")
        found = m.group(0)
        return found



def extractemail(s):
    #print("vsdf")
    m = re.findall('[ ][a-z|0-9]+[@][a-z]+[.][a-z]+[ ]', s)
    if m:
        #print("hello")
        found = m
        return found[0]

def extractperc(s):
    m = re.findall('[0-9][0-9][.][0-9][0-9]', s)
    if m:
        #print("hello")
        found = m
        return found

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
    return text
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
    return text
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
    return text


def extractskills(s):
    global relevtags
    text=""
    for i in range(0,len(s)):
        temp=str(s[i]).strip()
        #print(i)

        if not temp.find("SKILLS") or not temp.find("Skills") or not temp.find("Skill") or not temp.find("skill"):
            #print(temp)
            #print("found")
            for j in range(i+1,len(s)):
                if str(s[j]).strip() not in relevtags:
                    text=text+str(s[j]).strip()+" "
                else:
                    break
        else:

            continue
    return text

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
    return text

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
    return text

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
    return text
@login_required(login_url='/Login')
@user_passes_test(is_student)
def resumepage(request):
    return render(request,"Recommendation/createresume.html")
def createresume(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        objective = request.POST['objective']
        address = request.POST['address']
        experience = request.POST['experience']
        mobile = request.POST['mobile']
        companylocation = request.POST['companylocation']
        skill = request.POST['skill']
        description = request.POST['description']
        degreename1 = request.POST['degreename1']
        degreename2 = request.POST['degreename2']
        collegename = request.POST['collegename']
        universityname = request.POST['universityname']
        marks = request.POST['marks']
        cgpas = request.POST['cgpas']
        contact = UserResumes(email=email, objective=objective,mobile=mobile,address=address,experience=experience,skill=skill,
                            companylocation=companylocation,firstname=firstname,lastname=lastname,description=description,
                              degreename1=degreename1,degreename2=degreename2,collegename=collegename,universityname=universityname
                              ,marks=marks,cgpas=cgpas)
        contact.save()
        username = request.user
        print(username)
        resume=template.objects.last()
        res=resume.select
        if res=="Designtemp1":
            return redirect("downloadDesigntemp1")
        elif res=="Designtemp2":
            return redirect("downloadDesigntemp2")
        elif res=="Designtemp3":
            return redirect("downloadDesigntemp3")
        elif res=="SimpleResume":
            #return redirect("downloadSimpleResume")
            return render(request, "Recommendation/Recommendation.html")
        else:
            return redirect("downloadResumeViking")
    return redirect('index')
def downloadDesigntemp1(request):
    downloadresume=UserResumes.objects.all()
    return render(request,"Recommendation/downloadDesigntemp1.html",{'downloadresume':downloadresume})
def downloadDesigntemp2(request):
    downloadresume=UserResumes.objects.all()
    return render(request,"Recommendation/downloadDesigntemp2.html",{'downloadresume':downloadresume})
def downloadDesigntemp3(request):
    downloadresume=UserResumes.objects.all()
    return render(request,"Recommendation/downloadDesigntemp3.html",{'downloadresume':downloadresume})
def downloadResumeViking(request):
    downloadresume=UserResumes.objects.all()
    return render(request,"Recommendation/downloadResumeViking.html",{'downloadresume':downloadresume})
def downloadSimpleResume(request):
    downloadresume=UserResumes.objects.all()
    return render(request,"Recommendation/downloadSimpleResume.html",{'downloadresume':downloadresume})

def getresumedesign1(request,id):
        # movie = get_object_or_404(UserResumes, id=id)
        # creator = movie.user.username
        # if request.method == "POST" and request.user.username == creator:
        up1 = UserResumes.objects.get(id=id)
        base_url = MEDIA_ROOT + '/talha/'
        asset_url = base_url + 'Designtemp1.docx'   
        tpl = DocxTemplate(asset_url)
        context = {'firstname':up1.firstname,'lastname':up1.lastname,'mobile': up1.mobile, 'email': up1.email,
                   'objective':up1.objective,'skill':up1.skill,'address':up1.address,'experience':up1.experience,
                   'companylocation':up1.companylocation,'description':up1.description,'degreename1':up1.degreename1,
                   'degreename2': up1.degreename2, 'collegename': up1.collegename,'universityname': up1.universityname,
                   'marks':up1.marks,'cgpas':up1.cgpas}
        tpl.render(context)
        # tpl.save(base_url + 'temps.docx')
        from io import BytesIO
        f = BytesIO()
        # f = StringIO()
        tpl.save(f)
        length = f.tell()
        f.seek(0)
        # f.cloce()
        response = HttpResponse(f.getvalue(),content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename='
        response['Content-Length'] = length
        return response
        return render(request,'Recommendation/downoadDesigntemp1.html',{'creator':creator})
def getresumedesign2(request,id):
    up1 = UserResumes.objects.get(id=id)
    base_url = MEDIA_ROOT + '/talha/'
    asset_url = base_url + 'Designtemp2.docx'
    tpl = DocxTemplate(asset_url)
    context = {'firstname':up1.firstname,'lastname':up1.lastname,'mobile': up1.mobile, 'email': up1.email,
               'objective':up1.objective,'skill':up1.skill,'address':up1.address,'experience':up1.experience,
               'companylocation':up1.companylocation,'description':up1.description,'degreename1':up1.degreename1,
               'degreename2': up1.degreename2, 'collegename': up1.collegename,'universityname': up1.universityname,
               'marks':up1.marks,'cgpas':up1.cgpas}
    tpl.render(context)
    # tpl.save(base_url + 'temps.docx')
    from io import BytesIO
    f = BytesIO()
    # f = StringIO()
    tpl.save(f)
    length = f.tell()
    f.seek(0)
    # f.cloce()
    response = HttpResponse(f.getvalue(),content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename='
    response['Content-Length'] = length
    return response
def getresumedesign3(request,id):
    up1 = UserResumes.objects.get(id=id)
    base_url = MEDIA_ROOT + '/talha/'
    asset_url = base_url + 'Designtemp3.docx'
    tpl = DocxTemplate(asset_url)
    context = {'firstname':up1.firstname,'lastname':up1.lastname,'mobile': up1.mobile, 'email': up1.email,
               'objective':up1.objective,'skill':up1.skill,'address':up1.address,'experience':up1.experience,
               'companylocation':up1.companylocation,'description':up1.description,'degreename1':up1.degreename1,
               'degreename2': up1.degreename2, 'collegename': up1.collegename,'universityname': up1.universityname,
               'marks':up1.marks,'cgpas':up1.cgpas}
    tpl.render(context)
    # tpl.save(base_url + 'temps.docx')
    from io import BytesIO
    f = BytesIO()
    # f = StringIO()
    tpl.save(f)
    length = f.tell()
    f.seek(0)
    # f.cloce()
    response = HttpResponse(f.getvalue(),content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename='
    response['Content-Length'] = length
    return response
def getresumeviking(request,id):
    up1 = UserResumes.objects.get(id=id)
    base_url = MEDIA_ROOT + '/talha/'
    asset_url = base_url + 'Resume Viking.docx'
    tpl = DocxTemplate(asset_url)
    context = {'firstname':up1.firstname,'lastname':up1.lastname,'mobile': up1.mobile, 'email': up1.email,
               'objective':up1.objective,'skill':up1.skill,'address':up1.address,'experience':up1.experience,
               'companylocation':up1.companylocation,'description':up1.description,'degreename1':up1.degreename1,
               'degreename2': up1.degreename2, 'collegename': up1.collegename,'universityname': up1.universityname,
               'marks':up1.marks,'cgpas':up1.cgpas}
    tpl.render(context)
    # tpl.save(base_url + 'temps.docx')
    from io import BytesIO
    f = BytesIO()
    # f = StringIO()
    tpl.save(f)
    length = f.tell()
    f.seek(0)
    # f.cloce()
    response = HttpResponse(f.getvalue(),content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename='
    response['Content-Length'] = length
    return response
def getsimpleresume(request,id):
    up1 = UserResumes.objects.get(id=id)
    base_url = MEDIA_ROOT + '/talha/'
    asset_url = base_url + 'Simpleresume.docx'
    tpl = DocxTemplate(asset_url)
    context = {'firstname':up1.firstname,'lastname':up1.lastname,'mobile': up1.mobile, 'email': up1.email,
               'objective':up1.objective,'skill':up1.skill,'address':up1.address,'experience':up1.experience,
               'companylocation':up1.companylocation,'description':up1.description,'degreename1':up1.degreename1,
               'degreename2': up1.degreename2, 'collegename': up1.collegename,'universityname': up1.universityname,
               'marks':up1.marks,'cgpas':up1.cgpas}
    tpl.render(context)
    # tpl.save(base_url + 'temps.docx')
    from io import BytesIO
    f = BytesIO()
    # f = StringIO()
    tpl.save(f)
    length = f.tell()
    f.seek(0)
    # f.cloce()
    response = HttpResponse(f.getvalue(),content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename='
    response['Content-Length'] = length
    return response

@login_required(login_url='/Login')
@user_passes_test(is_recruiter)
def publishjob(request):
    return render(request,"Recommendation/publishjob.html")
def publishjobs(request):
        if request.method == "POST":
            JobTitles = request.POST['JobTitles']
            Companys = request.POST['Companys']
            Locations = request.POST['Locations']
            PostDates = request.POST['PostDates']
            ExpiredDate = request.POST['ExpiredDate']
            Summarys = request.POST['Summarys']
            Salarys = request.POST['Salarys']
            experienceRequired = request.POST['experienceRequired']
            contacts = Job_Dataset(JobTitle=JobTitles, Company=Companys, Location=Locations, PostDate=PostDates, ExtractDate=ExpiredDate,
                                Summary=Summarys,Salary=Salarys, experienceRequired=experienceRequired)
            contacts.save()
            skill = UserResumes.objects.filter(skill__icontains=JobTitles)
            description = UserResumes.objects.filter(description__icontains=JobTitles)
            allUsers = skill.union(description)
            emailList = []
            for i in allUsers:
                if(i.companylocation==Locations):
                    userE = int(i.experience)
                    rE = int(experienceRequired)
                    if(userE >= rE):
                        emailList.append(i.email)
            print(emailList)
            email = EmailMessage(
                'Job Matched',
                'Following job'+ JobTitles + 'is matched with your skill',
                'noreply@semycolon.com',
                emailList,
            )
            email.send()
        return redirect('recruiterpage')
def chosentemp(request):
    if request.method=="POST":
        select=request.POST['select']
        cv = template(select=select)
        cv.save()
        if select=="Designtemp1":
          return redirect('Designtemp1')
        elif select=="Designtemp2":
          return redirect('Designtemp2')
        elif select=="Designtemp3":
          return redirect('Designtemp3')
        elif select == "ResumeViking":
          return redirect('ResumeViking')
        elif select == "SimpleResume":
          return redirect('SimpleResume')
    return redirect('index')
def getrecommend(request):
    pros=UserResumes.objects.all()
    return render(request,"Recommendation/getrecommend.html",{'pros':pros})
def choosetemp(request):
    return render(request,"Recommendation/choosetemp.html")
def Designtemp1(request):
    email = request.user.username
    return render(request,"Recommendation/Designtemp1.html", {"email": email})
def Designtemp2(request):
    email = request.user.username
    return render(request,"Recommendation/Designtemp2.html", {"email": email})
def Designtemp3(request):
    email = request.user.username
    return render(request,"Recommendation/Designtemp3.html", {"email": email})
def ResumeViking(request):
    email = request.user.username
    return render(request,"Recommendation/ResumeViking.html", {"email": email})
def SimpleResume(request):
    email = request.user.username
    return render(request,"Recommendation/SimpleResume.html", {"email": email})
def Recommendation(request):
    return render(request,"Recommendation/Recommendation.html")
def tfidfs(request,id):
    # ds = pd.read_csv(r"C:\Users\ittefaq\PyCharm Community Edition 2019.2.1\Job_Recommendation_System\media\talha\recs.csv")
    up1 = UserResumes.objects.get(id=id)
    ds=Job_Dataset.objects.all()
    j1=[]
    for j in ds:
     j1.append(j.JobTitle)
     # print(j1)
    # print(j1)
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, max_df=2, stop_words='english')
    tfidf_matrix = tf.fit_transform(ds[j1])
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    # print(j1)
    results = {}

    for idx, row in ds.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], ds['JobTitle'][i]) for i in similar_indices]

        results[row['JobTitle']] = similar_items

    # def item(skill):
    #     return ds.loc[ds['JobTitle'] == skill]['JobTitle'].tolist()[0]
    # def item1(sk):
    #     return ds.loc[ds['JobTitle'] == sk]['Location'].tolist()[0])
    # Just reads the results out of the dictionary.
    def recommend(item_skill, num):
        # print("Recommending " + str(num) + " products similar to " + item(item_skill)+"...")
        strOptions = ["Python/Django Developer", "Python Developer", "Web Developer", "Project Manager",
                      "Front End Web Developer - Internship / Part Time", "Python Analyst",
                      "Android App Developer", "Java Developer", "Software Engineer", "Django Developer",
                      "Software Analyzer","Full Stack PHP/JS Developer","C# Net Developer",
                      "Software Developer - Internee","Back end Developer","Requirement Analyst",
                      "Flutter Developer","Manager Admissions"]
        high = process.extractOne(item_skill, strOptions)
        talha = high[0]
        global recs
        recs = results[talha][:num]
    recommend(item_skill=up1.skill, num=5)
    return render(request, "Recommendation/Recommendation.html",{'data':recs})

def CfRecommender(request):
    #jobs = []
    print("function is executed")
    matched = []
    skills = []
    collectedJobs = []
    correctJobs = []
    username = request.user
    lastRecord = UserResumes.objects.last()
    email = lastRecord.email
    jobs = Job_Dataset.objects.all()
    records = UserResumes.objects.filter(email = email)
    print(records.count())
    for record in records:
        skills.append(record.skill)
    for skil in skills:
        collectedJobs = Job_Dataset.objects.filter(JobTitle__icontains=skil)
    for i, j in zip(collectedJobs, records):
        jE = int(i.experienceRequired)
        uE = int(j.experience)
        if uE >=jE:
            if i.ExtractDate > date.today():
                correctJobs.append(i)
    for job in jobs:
        nskillJob = len(job.JobTitle)
        count = 0
        for skil in skills:
            #collectedJobs.append(Job_Dataset.objects.filter(JobTitle__icontains=skil))
            if skil in job.JobTitle:
                count = count+1
                userE = record.experience
                userE = int(userE)
                jobE = job.experienceRequired
                jobE = int(jobE)
                if userE >= jobE:
                    matched.append(job)
                        #{
                        #    'name': job.JobTitle,
                         #   'ptc': count/nskillJob*100,
                          #  'location': job.Location,
                           # 'Salary': job.Salary,
                            #'url': job.JobUrl,
                            #'Experience': job.experienceRequired
                        #}
                    #)
    allJobs = correctJobs + matched
    matchedFriends = []
    currentUser = UserResumes.objects.get(email = username)
    users = UserResumes.objects.all()
    for rec in records:
        skills.append(rec.skill)
    for user in users:
        nskill = len(user.skill)
        count = 0
        for skil in skills:
            if skil in user.skill:
                count = count+1
                if user in matchedFriends:
                    print("alread exists")
                else:
                    matchedFriends.append(user)
    return render(request, "Recommendation/Recommendation.html", {"matched": allJobs, "matchedFriend": matchedFriends})
