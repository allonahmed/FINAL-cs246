import requests, json

url = 'https://finalprojectCS265.allonahmed2.repl.co'

key = 'allon'

file = {'file':open('temp.txt','r')}

filename = "assignment2"

#registers user using the key
register = requests.get(url+"/register/{}".format(key))
if(register.status_code==200):
  print('Welcome new User!')
else:
  print('It seems you are already a member. Start adding files to the server!')

#uploads the file using the filename and file url to aws
upload = requests.post(url+"/upload/{}".format(filename), files = file, headers={'api-key': key})
if upload.status_code==200:
  print("We have successfully added your file to the server!")
elif upload.status_code==400:
  print('You already have a file with the same name in the server! ERROR 400')
elif upload.status_code==403:
  print("You're key cannot be found in the server. ERROR 403")

#prints all the files that have been added to user's server
filelist = requests.get('https://finalprojectCS265.allonahmed2.repl.co/files', headers={'api-key': key})

print("list of files: ", json.loads(filelist.content)["data"])

#returns the file contents that was saved on ASW

getFile = requests.get(url+'/files/{}'.format(filename), headers = {'api-key': key})
if getFile.status_code==200:
  print("{} :".format(filename), getFile.content.decode('utf-8'))
elif getFile.status_code==404:
  print('filename is not in the server. ERROR 404')
elif getFile.status_code==403:
  print('your key is invalid. ERROR 403')

# delete a file

df = requests.get(url+"/delete/{}".format(filename), headers={'api-key': key})
if df.status_code==200:
  print("YOu have successfully deleted file {}".format(filename))
elif df.status_code==403:
  print("We could not find the file with that name in your folder. ERROR 403")

filelist = requests.get('https://finalprojectCS265.allonahmed2.repl.co/files', headers={'api-key': key})

print("list of files after deletion: ", json.loads(filelist.content)["data"])

# #unregister user from server

rm = requests.get(url+"/removeuser/{}".format(key), headers={"api-key": key})
if rm.status_code==200:
  print("{} was successfully deregisted from our service".format(key))
else:
  print("User does not exist in server! ERROR 403")



