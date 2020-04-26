
# coding: utf-8

# In[28]:


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
path = r'C:\\Users\\pooja\\AnacondaProjects\\Chromedriver'
driver = webdriver.Chrome(executable_path = path)
driver.get('https://parivahan.gov.in/rcdlstatus/?pur_cd=101')


# In[29]:


dlno=input("Enter your Driving licence number:")
text_dl = driver.find_element_by_id('form_rcdl:tf_dlNO')
text_dl.send_keys(dlno)
dob=input("Enter your DOB(in dd-mm-yyyy format):")
text_dob = driver.find_element_by_id('form_rcdl:tf_dob_input')
text_dob.send_keys(dob)
text_dob.click()
captcha=input("Enter your Captcha:")
text_captcha=driver.find_element_by_id('form_rcdl:j_idt34:CaptchaID')
text_captcha.send_keys(captcha)
search_button = driver.find_element_by_id("form_rcdl:j_idt46")
search_button.click()
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "form_rcdl:j_idt118")))
txt=driver.find_elements_by_tag_name("td")
data=driver.find_elements_by_class_name("ui-column-title")

raw_data1=[]
raw_data2=[]
content=[]
for i in range(0,len(txt),1):
    if(txt[i].text!=""):
        raw_data1.append(txt[i].text)
for i in range(0,len(raw_data1)-3,1):
    content.append(raw_data1[i])
for i in data:
    content.append(i.text)
j=len(raw_data1)-3
for i in range(j,len(raw_data1),1):
    content.append(raw_data1[i])
dict={}
for i in range(0,len(content),2):
    content[i]=content[i].replace(":","")
    dict[content[i]]=content[i+1]
json=json.dumps(dict)
print("JSON object: ",json)

