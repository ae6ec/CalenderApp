from flask import *
import pyrebase
from app import app

FIREBASE_CONFIG={
    "apiKey": "AIzaSyBtaWPLnzjuH-Xuo-U293wGIHGMLZqq4xM",
    "authDomain": "test-kk-c1456.firebaseapp.com",
    "databaseURL": "https://test-kk-c1456.firebaseio.com",
    "projectId": "test-kk-c1456",
    "storageBucket": "test-kk-c1456.appspot.com",
    "messagingSenderId": "1018971320822",
    "appId": "1:1018971320822:web:db5ff1eac24fb41ad2d7d7"
  }

firebase=pyrebase.initialize_app(FIREBASE_CONFIG)

@app.route('/',methods=['GET','POST'])
def basereturn():
    return "<h1>TEST Working</h1>"
    
@app.route('/api/<service>/',methods=['GET','POST'])
def api(service):
    if request.method == 'GET':
        return {"success":0,"msg":"Only POST Method Supported"}
    else:
        data=request.get_json()
        try:
            if(service=="gettoken"):
                email=data['email']
                password=data['pass']
                user=firebase.auth().sign_in_with_email_and_password(email,password)
                return {"success":1,"msg":"Token Valid For 1 hour","token":user['idToken']}        
                        
            elif(service=="registerAcc"):
                auth=firebase.auth()
                email=data['email']
                password=data['pass']
                auth.create_user_with_email_and_password(email,password)
                user=auth.sign_in_with_email_and_password(email,password)
                auth.send_email_verification(user['idToken'])
                # if(auth.get_account_info(user['idToken'])['users'][0]['emailVerified']==True):
                return {"success":1,"msg":"Email verification sent"}

            elif(service=='forgotAcc'):          
                email=data['email']
                firebase.auth().send_password_reset_email(email)
                return {"success":1,"msg":"Password reset email Sent"}

            elif(service=="makeSlotAvail"):
                name=data['name']
                day=data['day']
                email=data['email']
                password=data['pass']
                auth=firebase.auth()
                user=auth.sign_in_with_email_and_password(email,password)
                db=firebase.database()
                db_data={name:{day:{}}}
                for i in data['slots']:
                    db_data[name][day][i]=str(i)
                print(db_data)
                db.child("Calender").set(db_data, user['idToken'])
                return {"success":1,"msg":"Slots Added"}
	# "email" : "0kkmodi0@gmail.com",
	# "pass": "testtesttest",
            elif(service=="getSlotInfo"):
                email=data['email']
                password=data['pass']
                auth=firebase.auth()
                user=auth.sign_in_with_email_and_password(email,password)
                slotName=data['slotName']
                day=data['day']
                db=firebase.database()
                slotData=db.child("Calender").child(slotName).child(day).get()
                freeSlotData=[]
                for i in slotData.each():
                    if(i.val()==str(i.key())):
                        freeSlotData.append(i.val())
                print(freeSlotData)        
                return {"success":1,"msg":"Avilable Slots Info","FreeSlot":freeSlotData}

            elif(service=="bookSlot"):
                slotName=data['slotName']
                slot=data['slot']
                name=data['name']
                day=data['day']
                email=data['email']
                password=data['pass']
                auth=firebase.auth()
                user=auth.sign_in_with_email_and_password(email,password)
                db=firebase.database()
                db.child("Calender").child(slotName).child(day).update({slot:name})
                return {"success":1,"msg":"Slot Booking Successful"}
        except:
            return {"success":0,"msg":"Format or Data incorrect"}
