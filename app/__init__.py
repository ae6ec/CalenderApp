# import pyrebase
from flask import *
app=Flask(__name__)
from app import routes
app.secret_key="N5XW633INBUCCQTJM5JWKY3SMV2ESQLNKN2XEZI"
# config={
#     apiKey: "AIzaSyBtaWPLnzjuH-Xuo-U293wGIHGMLZqq4xM",
#     authDomain: "test-kk-c1456.firebaseapp.com",
#     databaseURL: "https://test-kk-c1456.firebaseio.com",
#     projectId: "test-kk-c1456",
#     storageBucket: "test-kk-c1456.appspot.com",
#     messagingSenderId: "1018971320822",
#     appId: "1:1018971320822:web:db5ff1eac24fb41ad2d7d7"
#   }

# firebase=pyrebase.initialize_app(config)
# auth=firebase.auth()


# email='0kkmodi0@gmail.com'
# @app.route('/api/registerAcc/',methods=['GET','POST'])
    