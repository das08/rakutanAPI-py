from flask import Blueprint, jsonify
import modules.func as fn
from models import Rakutan, UserFav

app = Blueprint('api', __name__, url_prefix='/api')


# 指定した講義ID(kid)のらくたん情報を取得する
@app.route('/rakutan/<int:kid>', methods=['GET'])
def get_lecture_by_id(kid=None):
    res = fn.get_lecture_by_id(kid)
    if res.result == "success":
        return Rakutan.to_dict(res.rakutan)
    else:
        return res.result


# 指定した講義ID(kid)のらくたん情報を取得する
@app.route('/rakutan/search/<search_word>', methods=['GET'])
def get_lecture_by_search_word(search_word=None):
    search_word = search_word.strip().replace('％', '%')
    res = fn.get_lecture_by_search_word(search_word)
    if res.result == "success":
        tmp = []
        for rakutan in res.rakutanList:
            tmp.append(Rakutan.to_dict(rakutan))
        return {"searchResult": tmp, "searchCount": res.count}
    else:
        return res.result


# 指定したユーザー(uid)のお気に入りを取得する
@app.route('/users/fav/<uid>', methods=['GET'])
# kid: 講義ID
def get_users_favorite(uid=None):
    res = fn.get_user_favorite(uid)
    if res.result == "success":
        tmp = []
        for fav in res.favList:
            tmp.append(UserFav.to_dict(fav))
        return {"favList": tmp, "favCount": res.count}
    else:
        return res.result


# 指定したユーザー(uid)のお気に入りを作成する
@app.route('/users/fav', methods=['POST'])
# kid: 講義ID
def add_users_favorite():
    return jsonify()


# 指定したユーザー(uid)のお気に入りを削除する
@app.route('/users/fav/<uid>', methods=['DELETE'])
# kid: 講義ID
def delete_users_favorite(uid=None):
    return jsonify(uid)

# 指定したユーザー(uid)のお気に入りを取得する
@app.route('/omikuji/<omikujiType>', methods=['GET'])
# kid: 講義ID
def get_omikuji(omikujiType=None):
    res = fn.get_omikuji(omikujiType)
    if res.result == "success":
        return Rakutan.to_dict(res.rakutan)
    else:
        return res.result


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
