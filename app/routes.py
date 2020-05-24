from flask import *
import pyrebase
from app import app
import requests
import json
import datetime
import random
uuid=int(1)
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
def index():
    return render_template('login.html')


@app.route('/recovery',methods=['GET','POST'])
def recovery():
    if request.method == "GET":
            return render_template('recovery.html') 
    else:
        try:
            firebase.auth().send_password_reset_email(request.form['email'])
            return render_template('login.html') 
        except:
            return render_template('500.html')


@app.route('/logout',methods=['GET','POST'])
def logout():
    if request.method == "GET":
            return render_template('login.html') 
    else:
        try:
            session.pop(request.cookies.get('uuid'), None)
            return render_template('login.html')            
        except:
            return render_template('500.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
            return render_template('login.html') 
    else:
        try:
            email=request.form['email']
            password=request.form['pass']
            # print('data done')
            user=firebase.auth().sign_in_with_email_and_password(email,password)
            r=random.randint(1111,9999)
            session.clear()
            session[str(r)]=user
            db=firebase.database()
            db.child("Calender").child(user['email'])
            # print('auth done'+user['email'])
            # print('sess starting')
            # session[user['']]=user
            # print('sess done')
            # slots=[{'slot':'1','name':'1'}]
            # date='2020-20-20'
            # print('starting done')
            # print(redirect(url_for("dashboard")))
            resp = make_response(redirect(url_for("dashboard")))
            # print('redirect done')
            resp.set_cookie('uuid', str(r))
            print(r)
            return resp
        except:
            return "<h3>Failed</h3>"
            # return render_template('500.html')
@app.route('/formMakeAvil',methods=['GET','POST'])
def formMakeAvil():
    if request.method == "GET":
            return render_template('formMakeAvil.html') 
    else:
        try:
            if(request.cookies.get('uuid') in session):
                # print("in sess")
                day=request.form['day']
                slot=request.form['slot']
                user=session.get(request.cookies.get('uuid'))
                print(day)
                print(slot)
                print(user)
                print(user['email'])
                db=firebase.database()
                slot={slot:slot}
                db.child("Calender").child(user['email']).chid(day)
                db.child("Calender").child(user['email']).child(day).update(slot)
                return redirect(url_for("dashboard"))
            else:
                #TODO: make error page for login again 
                return  "<h3>Format or Data Incorrect</h3>"
        except:
            return render_template('500.html')

@app.route('/formGetAvil',methods=['GET','POST'])
def formGetAvil():
    if request.method == "GET":
            return render_template('formGetAvil.html') 
    else:
        try:
            if(request.cookies.get('uuid') in session):
                # print("in sess")
                day=request.form['day']
                slotName=request.form['slotName']
                user=session[request.cookies.get('uuid')]
                #TODO ::REMOVE TEST AND USE REAL DATA
                response=requests.get(f'https://test-kk-c1456.firebaseio.com/Calender/{slotName}/{day}.json')
                # response=response.json()
                print(response)
                # if()
                data={}
                for i in response:
                    if(i.key()==i.val()):
                        data['O']=str(i.key())
                # make page how data and redirect back to dashboarad TODO 
                return render_template("freeSlot.html",slots=data)
            else:
                #TODO: make error page for login again 
                return  "<h3>no Schedule available or Format or Data Incorrect</h3>"
        except:
            return render_template('500.html')


@app.route('/bookGetAvil',methods=['GET','POST'])
def bookGetAvil():
    if request.method == "GET":
            return render_template('bookGetAvil.html') 
    else:
        try:
            if(request.cookies.get('uuid') in session):
                day=request.form['day']
                slotName=request.form['slotName']
                slot=request.form['slot']
                user=session[request.cookies.get('uuid')]
                db=firebase.database()
                db.child("Calender").child(slotName).child(day).update({slot:user["email"]})
            else:
                #TODO: make error page for login again 
                return  "<h3>That Schedule isn't available or  Data Incorrect</h3>"
        except:
            return render_template('500.html')


@app.route('/signUp',methods=['GET','POST'])
def signUp():
    if request.method == "GET":
            return render_template('signUp.html') 
    else:
        try:
            auth=firebase.auth()
            print(request.form)
            email=request.form['email']
            password=request.form['pass']
            auth.create_user_with_email_and_password(email,password)
            user=auth.sign_in_with_email_and_password(email,password)
            auth.send_email_verification(user['idToken'])
            return render_template('login.html')            
        except:
            return render_template('500.html')

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    try:
        if(request.cookies.get('uuid') in session):
            print("in sess")
            x = datetime.datetime.now()
            dateAPI=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
            dateRes=x.strftime("%d %b %Y")
            print(request.cookies.get('uuid'))
            user=session.get(request.cookies.get('uuid'))
            print(dateAPI)
            #TODO ::REMOVE TEST AND USE REAL DATA
            try:
                response=requests.get('https://test-kk-c1456.firebaseio.com/Calender/Test%20Data/2020-05-23.json')
                # response=request.get(f'https://test-kk-c1456.firebaseio.com/Calender/{user["email"]}/{dateAPI}.json')
                # response=response.json()
                # print(response.json())
                # for i in response:
                #     print(i+":"+response[i])
                # print(response)    
                slots=[{'slot':'1','name':'1'},{'slot':'2','name':'Vergil'},{'slot':'3','name':'tarun'}]
                return render_template('dashboard.html',date=dateRes,slots=slots)
            except:
                print("SAD")
                return render_template('dashboard.html',date=dateRes,slots={})
        else:
            #TODO: make error page for login again 
            return  "<h3>login again</h3>"
    except:
        return render_template('500.html')  


# THE BELOW ARE FOR RESTFUL API




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
                # name=data['name']
                day=data['day']
                email=data['email']
                password=data['pass']
                auth=firebase.auth()
                user=auth.sign_in_with_email_and_password(email,password)
                db=firebase.database()
                db_data={email:{day:{}}}
                for i in data['slots']:
                    db_data[name][day][i]=str(i)
                # print(db_data)
                db.child("Calender").set(db_data, user['idToken'])
                return {"success":1,"msg":"Slots Added"}
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
                # name=data['name']
                day=data['day']
                email=data['email']
                password=data['pass']
                auth=firebase.auth()
                user=auth.sign_in_with_email_and_password(email,password)
                db=firebase.database()
                db.child("Calender").child(slotName).child(day).update({slot:email})
                return {"success":1,"msg":"Slot Booking Successful"}
        except:
            return {"success":0,"msg":"Format or Data incorrect"}
