
from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, abort, session
import os
from Responses import Resp
import re

from database import *
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
users = Users("database.json", "database")

app.secret_key = 'difouhgdfiughsihoahsdoashdaohd12381263728346238742873' 


class API:
    def __init__(self):
        pass
    


    @app.route('/home/')
    @app.route('/home')
    @app.route('/')
    def home():
        if session.get("user_id"):
            return render_template('index.html')
        return redirect('/register')

    @app.route('/data', methods=["GET"])
    @app.route('/data/', methods=["GET"])
    def data():
        files = None
        user_id = session.get('user_id')
        if user_id:
            files = users.get_user(user_id).file_dir
            user = users.get_user(user_id)
            return jsonify({
                "files": files,
                "username": user.username,
                "message": "files have been loaded successfully !"
            })
        
        return Resp.session_error()
    
    @app.route('/download/<filename>')
    @app.route('/download/<filename>/')
    def download(filename):
        user_id = session.get('user_id')
        if user_id:
            files = users.get_user(user_id).file_dir
            if filename in files:
                return send_from_directory(
                    f"database\\{user_id}",
                    filename,
                    as_attachment=True
                )
            
            return Resp.error(404, f"'{filename}' doesnt exist !")
        return Resp.error(500, "please login")


    @app.route('/home/delete', methods=["POST"])
    @app.route('/home/delete/', methods=["POST"])
    def delete():
        user_id = session.get('user_id')
        if user_id:
            data = request.get_json()
            filename = data['file']

            os.remove(os.path.join(f'database\\{user_id}', filename))
            return Resp.success('file has been deleted successfully !')
        
        return Resp.session_error()

    @app.route('/home/upload', methods=['POST'])
    def upload():
        user_id = session.get('user_id')
        if user_id:
            files = users.get_user(user_id).file_dir
            # print(request.files)
            file = request.files['file']
            
            if file.filename in files:
                return Resp.error(409, f"'{file.filename}' already exists !")

            try:
                file.save(os.path.join(f'database\\{user_id}',file.filename))
            except:
                return Resp.error(404, "please choose a file !")
            
            return Resp.success('file has been uploaded successfully !')
        
        return Resp.session_error()
        
    
    @app.route('/home/create')
    @app.route('/home/create/', methods=["POST"])
    def create():
        user_id = session.get('user_id')
        if user_id:
            data = request.get_json()
            files = users.get_user(user_id).file_dir
            filename = data['filename']

            # return Resp.success('file has been created !') 
            if filename in files:
                return Resp.error(409, f"'{filename}' already exists !")
            try:
                result, msg = File.is_valid_filename(filename)
                if not result:
                    return Resp.error(400, msg)

                with open(f"database\\{user_id}\\{filename}", 'w', encoding="utf-8") as file:
                    file.write("")

                return Resp.success('file has been created !') 

            except Exception as e:
                print(e)
                return Resp.error(500, f"unexcepted error: {e}")
            
        return Resp.session_error()

    
    ###############################################################################
                              ## ACCOUNTS HANDLER ##
    ###############################################################################




    @app.route('/register')
    @app.route('/register/', methods=["POST", "GET"])
    def register():
        user_id = session.get('user_id')
        if not user_id:
            return render_template("signup.html")
        return redirect("/home")
    

    @app.route('/logout')
    @app.route('/logout/', methods=["POST"])
    def logout():
        user_id = session.get('user_id')
        if user_id:
            del session['user_id']
            return Resp.success('loged out successfully !')
        return Resp.session_error()            



    @app.route('/login')
    @app.route('/login/', methods=['POST'])
    def login():
        user_id = session.get('user_id')
        if not user_id:
            data = request.get_json()
            username = data['username']
            password = data['password']

            if not Users.is_valid_username(username):
                print("Invalid Username")
                return Resp.error(401, "Invalid Username")
            if not Users.is_valid_password(password):
                print("Invalid Password")
                return Resp.error(401, "Invalid Password")
            if not users.is_user_exists(username):
                return Resp.error(401, "Username doesnt exist")
            
            user = users.get_user_by_username(username)
            user_password = user.password
            
            if not check_password_hash(user_password, password):
                print('Password is Wrong')
                return Resp.error(401, 'Password is Wrong')
            
            print(user.username, 'has been loged in')
            session['user_id'] = user.id
            return Resp.success("loged in successfully !")
            
        return Resp.session_error()
            



    @app.route('/signup')
    @app.route('/signup/', methods=["POST"])
    def signup():
        user_id = session.get('user_id')
        if not user_id:
            data = request.get_json()
            username = data['username']
            password = data['password']
            repassword = data['repassword']

            if not Users.is_valid_username(username):
                print("Invalid Username")
                return Resp.error(401, "Invalid Username")
            if not Users.is_valid_password(password):
                print("Invalid Password")
                return Resp.error(401, "Invalid Password")
            if not (password == repassword):
                print("Password and Re-Password must be the same")
                return Resp.error(401, "Password and Re-Password must be the same")
            if users.is_user_exists(username):
                print("Username is already taken")
                return Resp.error(401, "Username is already taken")
            
            hashed_password = generate_password_hash(password)
            user = users.add_user(username, hashed_password, 20)
            
            print(user.username, "has been signed up")

            session['user_id'] = user.id
            return Resp.success(f"signed up successfully !")
    

        
    ###############################################################################
                              ## CODE EDITOR ##
    ###############################################################################
        
    
    @app.route('/editor/<filename>')
    @app.route('/editor/<filename>/')
    def editor(filename=None):
        user_id = session.get('user_id')
        if user_id:
            content = ""
            try:
                with open(f"database\\{user_id}\\{filename}", "r", encoding="utf-8") as file:
                    content = file.read()
            except Exception as e:
                print(f"ERROR: {e}")

            return render_template('editor.html', content=content, filename=filename)
        return Resp.session_error()


    @app.route('/editor/edit', methods=['POST'])
    @app.route('/editor/edit/', methods=['POST'])
    def editor_save():
        user_id = session.get('user_id')
        if user_id:
            data = request.get_json()
            cmd = data['cmd']
            filename = data['filename']

            if cmd == "save-content":
                content = data['content']
                with open(f"database\\{user_id}\\{filename}", "w", encoding="utf-8") as file:
                    file.write(content)
                
                
                return Resp.success('file has been saved successfully !')
            
            if cmd == "change-name":
                new_name = data['new_name']
                os.rename(f"database\\{user_id}\\{filename}", f"database\\{user_id}\\{new_name}")            
                return Resp.success("file's name has been changed successfully !")
        return Resp.session_error()

    
    
    def run(self):
        app.run(
            debug=True,
            exclude_patterns = ["database\\*"]
        )