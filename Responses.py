
from flask import jsonify

class Resp:

    @staticmethod
    def success(message, data={}):
        return jsonify({
            "success": True,
            "message": message,
            "data": data
        }), 200 
    
    @staticmethod
    def error(error_number, message, data={}):
        return jsonify({
            "success": False,
            "message": message,
            "data": {}
        }), error_number
    
    @staticmethod
    def session_error():
        return jsonify({
            "success": False,
            "message": "no session found, please login",
            "data": {}
        }), 500