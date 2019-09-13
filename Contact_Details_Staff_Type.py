#Contact_Details_Staff.py: This files collect the contact details of staff member from multiple web location (Creating KnowledgeBase).
# This code also multiple logic to detect the staff member type "Staff or tutor"
# Further the data is updated in MongoDB database.
#Created By : Arvind Bahl
#*******************************************************************************************

# Imports the required libraries
from bs4 import BeautifulSoup as soup
import csv
from urllib.request import urlopen as uReq
from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client['ContactDetails_StaffType']
data_col = db['data_col']


# First stage website
page_url = "https://webcms3.cse.unsw.edu.au/search"
uClient = uReq(page_url)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

# Saved Contact file
out_filename = "Contact_Details_Staff_Type.csv"
headers = "Name, Staff Type  \n"

#f = open(out_filename, "w")
#f.write(headers)

# Variable assignment
container_s = page_soup.findAll("div", {"class": "table-responsive"})
containers = container_s[0]
table=containers.find('tbody')
rows = table.find_all('tr')
data = {}

# Looping and crawling different websites to gather information
for row in rows:
    cols =row.findAll('a', href=True)
 
    temp_data=''
    for i in  range(1, len(cols)):
        if cols[i].text in data:
            pass
        else:
            page_url1 = "https://webcms3.cse.unsw.edu.au"+ cols[i]["href"]
            uClient1 = uReq(page_url1)
            page_soup1 = soup(uClient1.read(), "html.parser")
            uClient1.close()
            container_s1 = page_soup1.findAll("div", {"class": "table-responsive"})
            emaild = cols[i]["href"].replace("/users/", "") + "@unsw.edu.au"
            if (len(container_s1) == 1):
                a_temp=container_s1[0].find_all("td")
                data[cols[i].text]= [emaild , a_temp[3].text, a_temp[1].text, "Staff"]
            else:

                data[cols[i].text]= [emaild , 'N/A', 'N/A', "Tutor"]
        
        
#Writing to the output file.
with open(out_filename, 'w') as csv_file:
    #csv_file.write(headers)
    writer = csv.writer(csv_file)
    writer.writerow(["Name", "Email ID", "Phone Number", "Office Location", "Staff Type"])
    for key, value in data.items():
       writer.writerow([key, value[0], value[1], value[2], value[3]])
       mydict={"Name": key, "Email ID": value[0], "Phone Number": value[1], "Office Location": value[2], "Staff Type": value[3]}
       data_col.insert_one(mydict)
       


