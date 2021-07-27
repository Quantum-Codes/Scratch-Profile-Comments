import requests
from bs4 import BeautifulSoup
import json
import re
import os

os.system('clear')
URL = "https://scratch.mit.edu/site-api/comments/user/Ankit_Anmol/?page=1"
page = requests.get(URL)
API = []
soup = BeautifulSoup(page.content, "html.parser")
#print(soup)
result = soup.find_all("li", class_="top-level-reply")
#print(result[6])
#exit()

def get_replies(count):
  replies = result[count].find("ul", class_="replies")
  if replies.text == "":
    print("No content!")
  user = replies.find_all("div", class_="info")
  #print(user)
  all_replies = []
  for i in range(0, len(user)):
	  username = user[i].find("div", class_="name")
	  username = username.find("a").text
	  content = user[i].find("div", class_="content").text
	  username = username.strip().replace("\n","")
	  content = content.strip().replace("\n","")
	  search = re.search("data-comment-id=", str(result[i]))
	  index = search.span()[1]
	  data = str(result[i])[index + 1:]
	  i = 0
	  id = ""
	  while data[i] != '"':
		  id += data[i]
		  i += 1
	  id = int(id)
	  search = re.search("title=", str(result[i]))
	  #print(search)
	  index = search.span()[1]
	  #print(index)
	  data = str(result[i])[index + 1:]
	  #print(data)
	  i = 0
	  comment_time = ""
	  while data[i] != '"':
	    comment_time += data[i]
	    i += 1
        
	  reply = {"id":id, "username" : username, "comment" : 	content.replace("                   ",""), "timestamp" : comment_time}
	  all_replies.append(reply)
  return all_replies
#print(get_replies())  

'''
search = re.search("title=", str(result[0]))
print(search)
index = search.span()[1]
#print(index)
data = str(result[0])[index + 1:]
#print(data)
i = 0
comment_time = ""
while data[i] != '"':
	comment_time += data[i]
	i += 1

print(id)
'''
for i in range(0, len(result)):
  user = result[i].find("div", class_="comment")
  replies = get_replies(i)
  user = user.find("div", class_="info")
  user = user.find("div", class_="name")
  user = user.find("a")
  user = user.text
  
  content = result[i].find("div", class_="comment")
  content = content.find("div", class_="info")
  content = content.find("div", class_="content")
  content = content.text.strip()
  
  search = re.search("data-comment-id=", str(result[i]))
  #print(search)
  index = search.span()[1]
  #print(index)
  data = str(result[i])[index + 1:]
  #print(data)
  i = 0
  id = ""
  while data[i] != '"':
    id += data[i]
    i += 1
  id = int(id)
  #print(id)
  
  search = re.search("title=", str(result[i]))
  #print(search)
  index = search.span()[1]
  #print(index)
  data = str(result[i])[index + 1:]
  #print(data)
  i = 0
  comment_time = ""
  while data[i] != '"':
    comment_time += data[i]
    i += 1
  if len(replies) == 0:
    parent = False
  else:
    parent = True
  comment = {
	    "Username": user,
	    "Content": content,
	    "Time": comment_time,
	    "ID": id,
	    "IsParent": parent,
	    "Replies": replies,
	    "CommentID": id
  }
  comment = json.dumps(comment)
  comment = json.loads(comment)
  #print(comment)
  API.append(comment)

print(API)