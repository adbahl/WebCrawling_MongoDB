#Course Staff.py: This files collect the Course and Staff details by crawling various webpages (Creating KnowledgeBase).
# Further the data is updated in MongoDB database.
#*******************************************************************************************

# Imports the required libraries
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client['Course_Staff']
data_col = db['data_col']

# First stage website
page_url = "https://webcms3.cse.unsw.edu.au/search"
uClient = uReq(page_url)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

# Saved Contact file
out_filename = "Course_Staff.csv"
headers = "Course Code,Semester,Course Name,Course Aliases, Main Course Staff  \n"
f = open(out_filename, "w")
f.write(headers)

# Variable assignment
container_s = page_soup.findAll("div", {"class": "table-responsive"})
containers = container_s[0]
table=containers.find('tbody')
rows = table.find_all('tr')
data = ''

# Looping and crawling websites to gather information and write to the file.
for row in rows:
    cols = row.find_all('td')
    data = data + cols[0].text+ ' , '
    data = data + cols[1].text+ ' , '
    data = data + cols[2].text.replace(',', '')+ ' , '
    data = data + cols[3].text.replace('\n', '').strip()+ ' , '
    #data = data + cols[4].findAll('a').text.replace('\n', ' ')+ ' , '

    '''
    if (len(cols[3].findAll('td') ==0):
        data = data + " " + ' , '
    else:
        data = data + cols[3].string+ ' , ' 
    data = data + cols[3].str + ' , '
        '''
    cd = cols[4].findAll('a')
    #print(cd)
    temp_data=''
    for i in  range(len(cd)):
        temp_data = temp_data + cd[i].text+ '; '
        
    data = data + temp_data + '\n'
    #print(data)
    f.write(data)
    tt1data = data.split(',')
    mydict ={"Course Code" : tt1data[0] ,"Semester" : tt1data[1] , "Course Name" : tt1data[2] , "Course Aliases" : tt1data[3] , "Main Course Staff " : tt1data[4] }
    data_col.insert_one(mydict)
    #print(tt1data[0], tt1data[1], tt1data[2], tt1data[3], tt1data[4])
    data =''
    #cols = [ele.text.strip() for ele in cols]
    #data.append([ele for ele in cols if ele]) 

f.close()

