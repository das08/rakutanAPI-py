from flask import Blueprint, jsonify

app = Blueprint('api', __name__, url_prefix='/api')


# 指定した講義ID(kid)のらくたん情報を取得する
@app.route('/rakutan/<int:kid>', methods=['GET'])
def get_lecture_by_id(kid=None):
    return jsonify(kid)


# 指定した講義ID(kid)のらくたん情報を取得する
@app.route('/rakutan/search/<search_word>', methods=['GET'])
def get_lecture_by_search_word(search_word=None):
    search_word = search_word.strip().replace('％', '%')
    return jsonify(search_word)


# 指定したユーザー(uid)の情報を取得する
@app.route('/users/<uid>', methods=['GET'])
# kid: 講義ID
def get_users(uid=None):
    return jsonify(uid)


# 指定したユーザー(uid)の情報を作成する
@app.route('/users', methods=['POST'])
# kid: 講義ID
def add_users():
    return jsonify()


# 指定したユーザー(uid)の情報を更新する
@app.route('/users/<uid>', methods=['PUT'])
# kid: 講義ID
def update_users(uid=None):
    return jsonify(uid)


# 指定した講義ID(kid)の過去問リンクを許可待ちリストに追加する
@app.route('/kakomon', methods=['POST'])
# kid: 講義ID
def add_kakomon():
    return jsonify()


# 指定した講義ID(kid)の過去問リンクを許可待ちリストから削除する
@app.route('/kakomon/<kid>', methods=['DELETE'])
# kid: 講義ID
def delete_kakomon(kid=None):
    return jsonify(kid)


@app.errorhandler(404)
def error_handler(error):
    return jsonify({'error': {
        'code': error.description['code'],
        'message': error.description['message']
    }}), error.code
