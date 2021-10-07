from flask import Flask,Response,session
from flask import render_template,jsonify
from flask import request,redirect,url_for
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import binascii
import base64
import os
from tinydb import TinyDB, Query, where
from cryptography.fernet import Fernet
password = b"password"

db = TinyDB('secret_file.json')
KEY_GLOBAL=''
def set_key(db,salt,hashval):
    table=db.table('key')
    print (hashval)
    table.insert({"secret":salt.hex(),"hash":hashval.hex()})
    return
def generate_key(db,password,salt=None):
    set_db=False
    if(not salt):
        salt=os.urandom(16)
        print("salt init=",salt)
        set_db=True
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
    hash_value=binascii.hexlify(password.encode())
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    if(set_db):
        set_key(db,salt,hash_value)
    print("generating password")
    return key

def load_key(db,password):
    global KEY_GLOBAL
    if(not KEY_GLOBAL):
        table=db.table('key')
        result=table.all()
        if(result):
            salt=bytes.fromhex(result[0]["secret"])
            print("salt loaded=",salt)
            hashval=result[0]["hash"]
            if(hashval!=binascii.hexlify(password.encode()).hex()):
                print("password mis match",hashval,binascii.hexlify(password.encode()).hex())
                return False
            KEY_GLOBAL=generate_key(db,password,salt)
            print("password found",KEY_GLOBAL)
        else:
            KEY_GLOBAL=generate_key(db,password)
    return True
def decryptrows(arraydict):
    result=[]
    for x in arraydict:
        temp={}
        temp["cred_name"]=decryptval(x["cred_name"])
        temp["cred_secret"]=decryptval(x["cred_secret"])
        temp["domain"]=x["domain"]
        result.append(temp) 
    return result

app = Flask(__name__,
            static_url_path='', 
            template_folder='templates/')

def decryptval(input):
    f=Fernet(KEY_GLOBAL)
    return f.decrypt(input.encode()).decode()

@app.route('/')
def hello():
    session["login"]=False
    return render_template("index.html")


@app.route('/load_file')
def load_file():
    print ("sdfsdf")
    return "blah blah"
@app.route('/logout')
def logout():
    KEY_GLOBAL=''
    session["login"]=False
    return redirect(url_for('hello'))
@app.route('/addcreds', methods=['GET','POST'])
def store_data():
    try:
        if(session["login"]== True):
            if (request.method=="POST"):
                username=request.form['username']
                password=request.form['password']
                domain=request.form['domain']
                f=Fernet(KEY_GLOBAL)
                search= Query()
                dbresult=db.search(search.domain==domain)
                for x in dbresult:
                    if(decryptval(x["cred_name"])==username):
                        return Response("cred already exist", status=400, mimetype='text/html')
                db.insert({'cred_name':f.encrypt(username.encode()).decode(),'cred_secret':f.encrypt(password.encode()).decode(),'domain':domain})
            return jsonify(decryptrows( db.all()))
        else:
            return Response("Not Allowed", status=400, mimetype='text/html')
    except:
        return redirect(url_for('logout'))
@app.route('/login', methods=['POST','GET'])
def login():
    if(request.method=="POST"):
        password=request.form['password']
        if(load_key(db,password)==True):
            session["login"]=True
            return render_template("login.html")
        else:
            session["login"]=False
            return Response("wrong password", status=400, mimetype='text/html')
    elif(request.method=="GET" and session["login"]== True):
        return render_template("login.html")
    return Response("Not Allowed", status=400, mimetype='text/html')


@app.route('/delete', methods=['GET','POST'])
def delete():
    try:
        f=Fernet(KEY_GLOBAL)
        if(session["login"]==True and request.method=="POST"):
            domainform=request.form["domain"]
            name=request.form["name"]
            search= Query()
            dbresult=db.search(search.domain==domainform)
            for x in dbresult:
                if(decryptval(x["cred_name"])==name):
                    dbresult=db.remove((where('domain')==domainform) and (where('cred_name')==x["cred_name"]))
            print(dbresult)
            dbresult=db.search(search.domain==domainform)
            return jsonify(decryptrows(dbresult))
        else:
            return redirect(url_for('logout'))
    except ValueError:
        return redirect(url_for('logout'))
@app.route('/getlist', methods=['GET','POST'])
def get_list():
    try:
        if(session["login"]==True):
            domain=request.args.get('searchdomain')
            search= Query()
            if(domain=="all"):
                dbresult=db.all()
            else:
                dbresult=db.search(search.domain==domain)
            return jsonify(decryptrows(dbresult))
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('logout'))
@app.route('/postnotes', methods=['GET','POST'])
def store_note():
    try:
        if(session["login"]== True):
            if (request.method=="POST"):
                title=request.form['note_title']
                note=request.form['note_text']
                f=Fernet(KEY_GLOBAL)
                search= Query()
                dbresult=db.search(search.domain==title)
                for x in dbresult:
                    if(decryptval(x["domain"])==title):
                        return Response("title already exist", status=400, mimetype='text/html')
                db.insert({'cred_name':f.encrypt(title.encode()).decode(),'cred_secret':f.encrypt(note.encode()).decode(),'domain':title})
            return jsonify(decryptrows(db.all()))
        else:
            return Response("Not Allowed", status=400, mimetype='text/html')
    except:
        return redirect(url_for('logout'))
if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'the random string'   
    app.run(host ='0.0.0.0', port = os.environ['PORT'],debug=True)