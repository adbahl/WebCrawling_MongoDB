#Contact_Details.py: This files collect the contact details of University staff members from webpages (Creating KnowledgeBase).
# and stores it in MongoDB database.
#Created By : Arvind Bahl
#*******************************************************************************************


# Imports the required libraries
from bs4 import BeautifulSoup as soup
import csv
from urllib.request import urlopen as uReq
from pymongo import MongoClient

# Create a database for saving Contact details.
client = MongoClient('localhost:27017')
db = client['ContactDetails']
contact_col = db['contact_col']

# First stage website
page_url = "https://webcms3.cse.unsw.edu.au/search"
uClient = uReq(page_url)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()


# Saved Contact file
out_filename = "Contact_Details.csv"
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
    #data = data + cols[0].text+ ' , '
    #data = data + cols[1].text+ ' , '
    #data = data + cols[2].text.replace(',', '')+ ' , '
    #data = data + cols[3].text.replace('\n', '').strip()+ ' , '
    #data = data + cols[4].findAll('a').text.replace('\n', ' ')+ ' , '

    '''
    if (len(cols[3].findAll('td') ==0):
        data = data + " " + ' , '
    else:
        data = data + cols[3].string+ ' , ' 
    data = data + cols[3].str + ' , '
        '''
    #cd = cols[4].findAll('a')
 
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
                #data[cols[i].text]= emaild + "," + a_temp[1].text + "," + a_temp[3].text
                data[cols[i].text]= [emaild , a_temp[3].text, a_temp[1].text]
                #print(a_temp[3].text)
            else:
                #data[cols[i].text]= emaild + "," + "N/A" + "," + "N/A"
                data[cols[i].text]= [emaild , 'N/A', 'N/A']
        
        
    #data = data + temp_data + '\n'

#Writing to the output file.
with open(out_filename, 'w') as csv_file:
    #csv_file.write(headers)
    writer = csv.writer(csv_file)
    writer.writerow(["Name", "Email ID", "Phone Number", "Office Location"])
    for key, value in data.items():
       writer.writerow([key, value[0], value[1], value[2]])
       mydict = {"Name": key, "Email Id": value[0], "Phone Number" : value[1], "Office Location": value[2]}
       contact_col.insert_one(mydict)
       
#f.write(data)
#data =''
    #cols = [ele.text.strip() for ele in cols]
    #data.append([ele for ele in cols if ele]) 

#f.close()

