import requests
from bs4 import BeautifulSoup
import re


def get_comments(username, site_page=1):
    # Retrieve comments from API. "f" is used before the beginning of the string to make Python substitute the values. If you provide a value of 1 (or no value) for the second argument, it's equivalent to opening someone's Scratch profile with SA disabled; the first page of comments loads. If you pass a value of 2, it's the equivalent to loading the page, using a browser extension to return an empty response for the first page of comments, and then loading the second page of comments. Since this doesn't need authentication, you don't provide your password.
    URL = f"https://scratch.mit.edu/site-api/comments/user/{username}/?page={site_page}"
    # Send an HTTP request to retrieve a page of comments, as explained above.
    page = requests.get(URL)
    # Initialize an empty array with name "API"
    API = []
    # Start the HTML parser on the data.
    soup = BeautifulSoup(page.content, "html.parser")
    # Retrieve each comment thread. An individual thread looks like this:
    # 
    # <li class="top-level-reply">
    #     <div id="comments-1" class="comment " data-comment-id="1">
    #         <div class="actions-wrap">
    #         </div>
    #         <a href="/users/username" id="comment-user" data-comment-user="username"><img class="avatar" src="//cdn2.scratch.mit.edu/get_image/user/1_60x60.png" width="45" height="45"/></a>
    #         <div class="info">
    #             <div class="name">
    #             <a href="/users/username">username</a>
    #         </div>
    #         <div class="content">
    #             Some characters are HTML entity encoded like this &amp; this. This is an apostrophe. &#39;
    #         </div>
    #         <div>
    #             <span class="time" title="2000-01-01T01:01:01Z">January 1, 2022</span>
    #             <a class="reply" style="display: none;" data-comment-id="1" data-parent-thread="1" data-commentee-id="1" data-control="modal-login">
    #                 <span>Reply</span>
    #             </a>
    #         </div>
    #         <div data-content="reply-form"></div>
    #     </div>
    # </div>
    # There's more after this, but it's not in here. However, you get the point.
    result = soup.find_all("li", class_="top-level-reply")
    # Finds everything with a "top-level-reply" class. In other words, every thread.
    if len(result) == 0:
      return {"error":"page doesn't exist"}
    # Detects 404 pages

    def get_replies(count):
        '''
        Retrieve replies to comment thread.
        '''
        # Extract reply list
        replies = result[count].find("ul", class_="replies")
        if replies.text == "":
            # Detect empty reply chain
            return None
        else:
            # Get DOM node containing user data for comment
            user = replies.find_all("div", class_="info")
            # print(user)
            # Initialize array with name "all_replies"
            all_replies = []
            # Iterate through reply list and extract username
            for i in range(0, len(user)):
                # Get username section. Probably does it like this to save memory.
                username = user[i].find("div", class_="name")
                # Redefine username as the actual username element
                username = username.find("a").text
                # Get post content
                content = user[i].find("div", class_="content").text
                # Trim username newlines
                username = username.strip().replace("\n", "")
                # Trim post content newlines
                content = content.strip().replace("\n", "")
                # Get comment IDs
                search = re.search("data-comment-id=", str(result[i]))
                # Get post position in reply list
                index = search.span()[1]
                data = str(result[i])[index + 1:]
                i = 0
                id = ""
                while data[i] != '"':
                    id += data[i]
                    i += 1
                id = int(id)
                # Get post numbers (I think)
                search = re.search("title=", str(result[i]))
                index = search.span()[1]
                data = str(result[i])[index + 1:]
                i = 0
                comment_time = ""
                while data[i] != '"':
                    comment_time += data[i]
                    i += 1
                    # Create final comment body
                reply = {"id": id, "username": username, "comment": content.replace("                   ", ""),
                         "timestamp": comment_time}
                all_replies.append(reply)
            return all_replies

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
        index = search.span()[1]
        data = str(result[i])[index + 1:]
        i = 0
        id = ""
        while data[i] != '"':
            id += data[i]
            i += 1
        id = int(id)

        search = re.search("title=", str(result[i]))
        index = search.span()[1]
        data = str(result[i])[index + 1:]
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
            "IsParent": parent,
            "Replies": replies,
            "CommentID": id
        }
        API.append(comment)
    return API
