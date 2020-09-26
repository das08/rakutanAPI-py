from flask import Blueprint, jsonify, request
import modules.func as fn
from models import Rakutan, UserFav

app = Blueprint('api', __name__, url_prefix='/api')


# 指定した講義ID(lecID)のらくたん情報を取得する
@app.route('/rakutan/<int:lecID>', methods=['GET'])
def get_lecture_by_id(lecID=None):
    res = fn.get_lecture_by_id(lecID)
    if res.result == "success":
        return Rakutan.to_dict(res.rakutan)
    else:
        return res.result


# 指定した講義ID(lecID)のらくたん情報を取得する
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
def add_users_favorite():
    uid = request.json.get('uid')
    lecID = request.json.get('lecID')
    lectureName = request.json.get('lectureName')

    res = fn.add_user_favorite(uid, lecID, lectureName)
    if res.result == "success":
        return res.successMsg
    else:
        return res.result


# 指定したユーザー(uid)のお気に入りを削除する
@app.route('/users/fav/<uid>', methods=['DELETE'])
def delete_users_favorite(uid=None):
    return jsonify(uid)


# 指定したユーザー(uid)のお気に入りを取得する
@app.route('/omikuji/<omikujiType>', methods=['GET'])
def get_omikuji(omikujiType=None):
    res = fn.get_omikuji(omikujiType)
    if res.result == "success":
        return Rakutan.to_dict(res.rakutan)
    else:
        return res.result


# 指定した講義ID(lecID)の過去問リンクを許可待ちリストに追加する
@app.route('/kakomon', methods=['POST'])
def add_kakomon():
    return jsonify()


# 指定した講義ID(lecID)の過去問リンクを許可待ちリストから削除する
@app.route('/kakomon/<lecID>', methods=['DELETE'])
def delete_kakomon(lecID=None):
    return jsonify(lecID)


@app.errorhandler(404)
def error_handler(error):
    return jsonify({'error': {
        'code': error.description['code'],
        'message': error.description['message']
    }}), error.code
