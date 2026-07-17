
from flask import Flask, jsonify, request, render_template, send_from_directory
import os
from Responses import Resp

app = Flask(__name__)




class API:
    def __init__(self):
        pass
    
    
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/data', methods=["GET"])
    def data():
        files = os.listdir('database')
        return jsonify({
            "files": files
        })
    
    @app.route('/download/<filename>')
    def download(filename):
        files = os.listdir('database')
        if filename in files:
            return send_from_directory(
                "database",
                filename,
                as_attachment=True
            )
        
        return Resp.error(404, f"'{filename}' doesnt exist !")


    @app.route('/delete', methods=["POST"])
    def delete():
        data = request.get_json()
        filename = data['file']

        os.remove(os.path.join('database', filename))

        return Resp.success('file has been deleted successfully !')

    @app.route('/upload', methods=['POST'])
    def upload():
        files = os.listdir('database')
        print(request.files)
        file = request.files['file']
        
        if file.filename in files:
            return Resp.error(409, f"'{file.filename}' already exists !")

        try:
            file.save(os.path.join('database',file.filename))
        except:
            return Resp.error(404, "please choose a file !")
        
        return Resp.success('file has been uploaded successfully !')
        
        
        
    ##############################################################################
                              ## CODE EDITOR ##
    ###############################################################################
        
    @app.route('/editor')
    def editor():
        return render_template('editor.html')
    
    
    
    def run(self):
        app.run(debug=True)