
from flask import jsonify

class Resp:

    @staticmethod
    def success(message):
        return jsonify({
            "success": True,
            "message": message
        }), 200 
    
    @staticmethod
    def error(error_number, message):
        return jsonify({
            "success": False,
            "message": message,
        }), error_number