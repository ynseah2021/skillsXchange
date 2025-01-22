from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        '''
        Error handler for exceptions from requests
        '''
        return jsonify({"message": "Internal server error",
                        "success": False,
                        "content": str(e)}), 500

    @app.errorhandler(404)
    def not_found_error(e):
        '''
        Error returned when no transactions can be found or retrieved
        '''
        return jsonify({"message": "Resource not found", 
                        "success": False,
                        "content": str(e.description)}), 404 
    
    @app.errorhandler(400)
    def bad_request_error(e):
        '''
        Error returned when bad request, missing or invalid data
        '''
        return jsonify({"message": "Bad request, missing or invalid data", 
                        "success": False,
                        "content": str(e.description)}), 404 
    
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        app.logger.error(f"Database error: {error}")
        return jsonify({'error': 'Database operation failed'}), 500