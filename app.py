from flask import Flask, render_template,request
import pymongo
import urllib

mongo = pymongo.MongoClient('mongodb+srv://22_Omprakash:'+urllib.parse.quote("Opsr@2410")+'@invoice.wu80e.mongodb.net/Invoice?retryWrites=true&w=majority', tls=True, tlsAllowInvalidCertificates=True)
db = pymongo.database.Database(mongo, 'Resume_Project')
col = pymongo.collection.Collection(db, 'register')

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/register',methods=['POST','GET'])
def regiter():
    if request.method=='POST':
        detail=request.form
        name=detail['name']
        email=detail['email']
        username=detail['username']
        password=detail['password']
        gender=detail['gender']
        phone=detail['phone']
        dic={'name':name,'email':email,'uname':username,'password':password,'gender':gender,'phone':phone}
        
        s=set()
        x=col.find({},{"uname": 1})
        for i in x:
            print(i)
            s.add(i['uname'])
        if username  in s:
            msg='Username Already Exist !!!'
            return render_template('signup.html',msg=msg)
        else:
            msg1='Successfully Registered !!!'
            col.insert_one(dic)
            return render_template('signin.html',msg=msg1)

    
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        details=request.form
        uname=details['uname']
        password=details['password']
        dic={}
        x=col.find({},{"uname": 1,'password':1})
        for i in x:
            dic[i['uname']]=i['password']
        if uname in dic:
            if dic[uname]==password:
                return render_template('product.html')
            else:
                return render_template('signin.html',msg='Invalid Password')
        else:
            return render_template('signin.html',msg='Incorrect Username and Password')


if __name__=='__main__':
    app.run(debug=True)