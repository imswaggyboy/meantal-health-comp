from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests



url = "https://www.practo.com/navi-mumbai/psychiatrist/belapur"


Headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept-language': 'en-US, en;q=0.5'})


webpage = requests.get(url,headers=Headers)
# print(webpage)

soup = BeautifulSoup(webpage.content , 'html.parser')
# soup = soup.encode("utf-8")

doc_data = {"doc_name":[],"profile_link":[],"year_of_exp":[],"locality":[],\
            "consulting_fee":[],"patient_stories":[],"doc_recommmendation":[]}

# print(soup.encode("utf-8"))

#doctor name
doc_name =  soup.find_all('h2' , class_='doctor-name')

#extracting profile link
profile_link = soup.find_all('div', class_="info-section")

#year of experienc of the doctor
year_of_exp = soup.find_all('div',{'data-qa-id':"doctor_experience"})

#locality
locality = soup.find_all('span', {"data-qa-id":"practice_locality"})

#consulting fee
consult_fee = soup.find_all('span', {"data-qa-id":"consultation_fee"})

#patient stories
patient_stories = soup.find_all('span', {"data-qa-id":"total_feedback"})

#doctor recommendation
doc_recommendation = soup.find_all('span', {"data-qa-id":"doctor_recommendation"})

for i in range(len(doc_name)):

    #appending doctor name in the dictionary
    try:
        doc_data['doc_name'].append(doc_name[i].text)
    except:
        doc_data['doc_name'].append("")

    #appending doctor profile link
    try:
        doc_data['profile_link'].append(f"https://www.practo.com{profile_link[i].a['href']}")
    except:
        doc_data['profile_link'].append("")

    #appending year of experience
    try:
        doc_data['year_of_exp'].append(year_of_exp[i].div.get_text().split()[0])
    except:
        doc_data['year_of_exp'].append("")

    #appending locality
    try:
        doc_data['locality'].append(locality[i].text.strip(","))
    except:
        doc_data['locality'].append("")

    #appending consulting fee
    try:
        doc_data['consulting_fee'].append(consult_fee[i].text)
    except:
        doc_data['consulting_fee'].append(consult_fee[i].text)

    #appending pa`tient stories
    try:
        doc_data['patient_stories'].append(patient_stories[i].text.split()[0])
    except:
        doc_data['patient_stories'].append("")

    #appending doctor recommendation
    try:
        doc_data['doc_recommmendation'].append(doc_recommendation[i].text.strip(" "))
    except:
        doc_data['doc_recommmendation'].append("")

doc_data_pd = pd.DataFrame.from_dict(doc_data).head(5)



  
