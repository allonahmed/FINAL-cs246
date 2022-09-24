from flask import render_template, Response
import json
import os


folder = json.load(open("./folder.json")) 

def home(): # home page
  return render_template('main.html')

#this makes a new user
def register(apikey): 
    apikey = str(apikey) #converts apikey to a string for error handling
    if(apikey not in folder): #if the key is not in api, which means it already exists inside of folder
        folder[apikey] = [] # create empty key with apikey name
        updatefolderFile(folder) # updates the user file so it saved when server resets
        return Response(status=200) # success status 
    else:
        return Response(status=403, response={ 'message': 'user already exist'}) # if the apikey found, in user, you do not need to register again.

def upload(filename):
    filename = str(filename) #converts file to a string
    file = request.files['file'] # gets the data from file from post requests
    apikey = request.headers.get('api-key') # requests for the apikey
    if(apikey in folder):
        if(filename in folder[apikey]):
            #if user already have a file with the same name
            return Response(status=400)
        folder[apikey].append(filename)
        updatefolderFile(folder)
        updatetmp(file)
        AWSclient.upload_file('temp.txt', BUCKET, filename)
        return Response(status=200)
    else:
        return Response(status=403)

#this returns list of file name
def files():
    apikey = request.headers.get('api-key')
    if(apikey in folder):
      return jsonify({"data":folder[apikey]})
        
    return Response(status=403)

#this returns file content
def getfile(filename):
    apikey = request.headers.get('api-key')
    if(apikey in folder):
        if(filename in folder[apikey]):
            returnfile = AWSclient.get_object(Bucket=BUCKET,Key=filename)
            return returnfile['Body'].read().decode("utf-8")
             
        return Response(status=404)
    print('apikey does not exist')
    return Response(status=403)

#this deletes files

def deletefile(filename):
    apikey = request.headers.get('api-key')
    if(apikey in folder):
        if(filename in folder[apikey]):
            AWSclient.delete_object(Bucket=BUCKET,Key=filename)
            folder[apikey].remove(filename)
            updatefolderFile(folder)
            return Response(status=200)
        return Response(status=403)
    return Response(status=403)
    

def remove(key):
    key = str(key)
    apikey = request.headers.get('api-key')
    if(str(apikey)!=key): return Response(status=403)
    if(key in folder):
        del folder[key]
        updatefolderFile(folder)
        return Response(status=200)
    return Response(status=403)

def delAllFiles(folder):
  folder.clear()
  updatefolderFile(folder)
  print(folder)


def updatefolderFile(folder):
  if os.path.exists('./folder.json'):
    with open('./folder.json', 'w') as f:
         json.dump(folder, f)

def updatetmp(file):
  with open('./temp.txt','w') as f:
    f.write(file.read().decode('utf-8'))



def printUsers():
    apikey = request.headers.get('api-key')
    if(apikey in folder):
      for i in folder:
        userList[i].append(folder)
      return Response(status=200)
    return Response(status=403)