from flask import render_template, Response, request, jsonify
import json
import boto3
import os
import logging



folder = json.load(open("./folder.json")) 

AWSclient = boto3.client( #s3 kkey id and access key
    's3',
    aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
    aws_session_token="FwoGZXIvYXdzEHIaDIUx69vedUWmArAxTyLFAaL2baIegNymiXHPnWDYopHe7m39740pErSi2l3Q3sSn8z3y/ivXZREtRGipjNtN42Z1hDI1nI+dksGiH7qH8IBt2uqAYV8zn88Tl1bP24abro/EkOiwbkl0Ly3CMrlUE8eg5nUCfehiamxHwHC9096P5EbeHbZEpQXuI1vrOo0HV3vyVEIaldTtkqUQZPu3rWw+wgWVMqdlykTCXnBaIYnhVZPgtWAg3nVqRVDlFkbDw2Fmz0bKFlR9JBtC2CnezMCVLQYHKLe45f4FMi2Jfxk6ntsm5Mj+Oz3kTJ71O/+r2Ep2mLp5Nk/nInmpilz+ey1QPtdOVVWmbkg=",

)  

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
    logging.warning('running upload func')
    logging.warning(os.getenv('ACCESS_KEY_ID'))
    logging.warning(os.getenv('SECRET_ACCESS_KEY'))
    filename = str(filename) #converts file to a string
    file = request.files['file'] # gets the data from file from post requests
    apikey = request.headers.get('api-key') # requests for the apikey
    logging.warning(apikey)
    if(apikey in folder):
        if(filename in folder[apikey]):
            #if user already have a file with the same name
            return Response(status=400)
        folder[apikey].append(filename)
        updatefolderFile(folder)
        updatetmp(file)
        AWSclient.upload_file('temp.txt', os.getenv('BUCKET'), filename)
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