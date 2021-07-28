import requests
def get():
  print(requests.get("https://Scratch-Profile-Comments.sid72020123.repl.co/?username=Ankit_Anmol&limit=5").json())