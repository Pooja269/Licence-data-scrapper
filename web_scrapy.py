
# coding: utf-8

# In[45]:


import csv
import urllib
from bs4 import BeautifulSoup
import psycopg2
import sys
import matplotlib.pyplot as plt
url='https://docs.google.com/spreadsheets/d/12UrT3MddhdXuFbCLmZfz92W6PQCzeg1YQErdFeK_4UY/edit#gid=0'
data=urllib.request.urlopen(url)
reader=data.read()
val="YES"
conn=""
cursor=""
def get_info():
    name=input("Enter your name:")
    email=input("Enter your email address:")
    return name,email
def store_data(name,email,gender,degree,university):
    try:
        
        query = """INSERT INTO person_info (name,email_add,gender,degree,university) VALUES (%s,%s,%s,%s,%s)"""
        result = cursor.execute(query,(str(name),str(email),str(gender),str(degree),str(university)))
        conn.commit()
        print("Data has been stored into database successfully")
    except(Exception, psycopg2.Error) as error :
        if(conn): 
            print("Error occurred while storing data into database")
    

def get_profile(name,email):
    soup = BeautifulSoup(reader,'html.parser')
    try:
        #to get values from CSV file using beautifulsoup library by parsing  HTML tags
        gender=soup.find('td',text=name).find_next_sibling('td',text=email).find_next_sibling('td')
        gen=gender.get_text()
        other_info=gender.find_next_siblings('td')
        degree=other_info[0].get_text()
        university=other_info[1].get_text()
        print("Gender:",gen,"\nHighest Degree earned:",degree,"\nUniversity:",university)
        store_data(name,email,gen,degree,university) #to store data into DB
    except (Exception,AttributeError) as error:
        print("match not found")

def build_pie_chart():
        count_query="""SELECT count(degree) from person_info where degree='MS'"""
        cursor.execute(count_query)
        deg_ms=cursor.fetchone()
        count_query="""SELECT count(degree) from person_info where degree!='MS'"""
        cursor.execute(count_query)
        deg_other=cursor.fetchone()
        conn.commit()
        ms=deg_ms[0]
        other=deg_other[0]
        labels = 'MS','other degrees'
        sizes = [ms,other]  
        colors = ['gold','orange']
        explode = (0,0)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%',shadow=True, startangle=90)
        plt.axis('equal')
        plt.show()
        
try:
    conn = psycopg2.connect(user="postgres",password="admin",host="127.0.0.1",port="5432",database="postgres")
    cursor = conn.cursor()
    while (val=='YES'):
        name,email=get_info() 
        get_profile(name,email) #to get name and email address from user
        val=input("Do you want to continue get information for next data(YES/NO)?")
        build_pie_chart()
        
except:
    print("Some error has occurred")
    
finally:
    if(conn):
        cursor.close()
        conn.close()
        print("Database connection is closed")   

