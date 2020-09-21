from flask import Blueprint, jsonify


app = Blueprint('api', __name__, url_prefix='/api')


@app.route('/rakutan', methods=['GET'])
def list_user():
    return "hi"


@app.route('/rakutan/<int:kid>', methods=['GET'])
# kid: 講義ID
def get_user(kid=None):
    return jsonify(kid)


@app.errorhandler(404)
def error_handler(error):
    return jsonify({'error': {
        'code': error.description['code'],
        'message': error.description['message']
    }}), error.code
