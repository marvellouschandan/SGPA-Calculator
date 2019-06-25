from django.shortcuts import render
import getpass
import requests
from bs4 import BeautifulSoup

# Create your views here.
from django.http import HttpResponse
import os, sys

cwd=os.getcwd()
cwd+="/template"
sys.path.insert(0, cwd)


def home(request):
    return render(request, 'home.html')



def calculate_sgpa(request):
    UID = request.POST["uname"]
    PSW = request.POST["psw"]
    payload={"username":UID,"password":PSW}
    req=requests.post("https://academics.gndec.ac.in/",data=payload)
    cookies=req.cookies
    values={"final_exam_result_with_grades":"in"}
    rpost = requests.post("https://academics.gndec.ac.in", cookies=cookies, data=values)
    soup=BeautifulSoup(rpost.content,'html.parser')
    
   
    # +===================================================================================
    # Clearing HTML tags and making list of contents

    td_tags = list(soup.find_all('td'))
    #print(td_tags)
    candidate_name = td_tags[0].get_text()
    td_tags = td_tags[5:-32]  # Clearing the extra data
    
    subject_list = []
    temp_list = []
    count = 1
    for item in td_tags:
        if item.get_text()!='' and item.get_text()!=' ':
            temp_list.append(item.get_text())
        else:
    	    temp_list.append('0')
        if count == 13:
            count=1
            subject_list.append(temp_list)
            temp_list=[]
        else:
            count+=1
    
    #print(subject_list)

    # +============================================================================
    # Calculating the SGPA

    fail_flag=0  # To check if a student failed in a subject or not
    
    total_credit=0
    credit_grade_sum=0
    
    for subject in subject_list:
        if int(subject[-2]) >= 4:  # Grade >=4
            credit_grade_sum += int(subject[11])*int(subject[12])
            total_credit += int(subject[12])
        else:
            fail_flag=1

    try:
        sgpa=credit_grade_sum/total_credit
    except:
        print("Error: Credit Being Zero")

    # +============================================================================
    # Creating HTML table for displaying on Result.HTML

    headers=["Semester","Subject Code","M code","Subject Title","Theory / Practical","Result Type","Internal Obtained Marks", "Internal Max. Marks", "External Obtained Marks", "External Max. Marks", "Grade Letter", "Grade Point", "Credits"]
    
    table_string="<table>\n"

    for header in headers:
        table_string+="<th>{}</th>\n".format(header)

    for subject in subject_list:
        table_string+="<tr>\n"
        for item in subject:
            table_string += "<td>{}</td>\n".format(item)
        table_string+="</tr>\n"

    table_string+="</table>"

    # +============================================================================
    # Responding to the request
    
    if fail_flag!=1:
        return render(request, 'result.html', {"sgpa":"{:0.2f}".format(sgpa), "percent":"{:0.2f}".format(sgpa*9.5), "name":candidate_name, "table":table_string})
    else:
        return render(request, 'error.html', {"name":candidate_name, "table":table_string})

