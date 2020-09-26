import random
from db import Database as DB
from models import Rakutan, UserFav
from modules.DotDict import DotDict
from modules.reserved import responseMessages as response


def unpack(result, count, queryResult):
    return result, count, queryResult


def get_lecture_by_id(lecID):
    """
    Find rakutan info from lecture ID
    :param lecID: (int) lecture ID
    :return: (dict) if success -> "result" would be "success" otherwise error message will be placed here.
    And if success -> "rakutan" will hold a Rakutan object.
    """
    db = DB()
    query = {'id': int(lecID)}
    # result, count, queryResult = db.find('rakutan', query)
    result, count, queryResult = unpack(**db.find('rakutan', query))

    res = DotDict({
        "result": None,
        "rakutan": None
    })

    if result == "success":
        if count == 0:
            res.result = response[1404].format(lecID)
        else:
            res.result = "success"
            res.rakutan = Rakutan.from_dict(queryResult[0])
    else:
        res.result = response[1001].format(lecID)

    return res


def get_lecture_by_search_word(search_word):
    """
    Find rakutan info from search word.
    :param search_word: (str) search word
    :return: (dict) if success -> "result" would be "success" otherwise error message will be placed here.
    And if success -> "rakrakutanListutan" will hold Rakutan objects list.
    """
    db = DB()

    # if search word has % in first letter, partial match search will be performed
    if search_word[0] == '%':
        query = {'lecturename': {'$regex': f'{search_word[1:]}', '$options': 'i'}}
    else:
        query = {'lecturename': {'$regex': f'^{search_word}', '$options': 'i'}}

    # result, count, queryResult = db.find('rakutan', query, projection={'_id': False})
    result, count, queryResult = unpack(**db.find('rakutan', query, projection={'_id': False}))

    res = DotDict({
        "result": None,
        "count": None,
        "rakutanList": None
    })

    if result == "success":
        if count == 0:
            res.result = response[2404].format(search_word)
        else:
            res.result = "success"
            res.count = count
            res.rakutanList = Rakutan.from_list(queryResult)
    else:
        res.result = response[2001].format(search_word)

    return res


def get_user_favorite(uid):
    """
    Get user's favorite.
    :param uid: (str) user's LINE UID
    :return: (dict) if success -> "result" would be "success" otherwise error message will be placed here.
    And if success -> "favList" will hold UserFav objects list.
    """
    db = DB()
    query = {'uid': uid}
    result, count, queryResult = unpack(**db.find('userfav', query))

    res = DotDict({
        "result": None,
        "count": None,
        "favList": None
    })

    if result == "success":
        if count == 0:
            res.result = response[3404].format(uid)
        else:
            res.result = "success"
            res.count = count
            res.favList = UserFav.from_list(queryResult)
    else:
        res.result = response[3001].format(uid)

    return res


def get_omikuji(omikujiType):
    """
    Get omikuji.
    :param omikujiType: (str) omikuji type. ["normal", "oni"]
    :return: (dict) if success -> "result" would be "success" otherwise error message will be placed here.
    And if success -> "rakutan" will hold a Rakutan object.
    """
    db = DB()

    res = DotDict({
        "result": None,
        "rakutan": None
    })

    if omikujiType == "oni":
        query = {'$and': [{'facultyname': '国際高等教育院'}, {'total_prev': {'$gt': 4}},
                          {'$expr': {'$lt': ['$accept_prev', {'$multiply': [0.31, '$total_prev']}]}}]}
    elif omikujiType == "normal":
        query = {'$and': [{'facultyname': '国際高等教育院'}, {'accept_prev': {'$gt': 15}},
                          {'$expr': {'$gt': ['$accept_prev', {'$multiply': [0.8, '$total_prev']}]}}]}
    else:
        res.result = response[4002].format(omikujiType)
        return res

    result, count, queryResult = unpack(**db.find('rakutan', query))

    if result == "success":
        if count == 0:
            res.result = response[4404].format(omikujiType)
        else:
            res.result = "success"
            res.rakutan = random.choice(Rakutan.from_list(queryResult))
    else:
        res.result = response[4001].format(omikujiType)

    return res


def get_kakomon_merge_list():
    pass


def add_user_favorite(uid, lecID, lectureName):
    """
    Add user's favorite.
    :param uid: (str) user's LINE UID
    :param lecID: (int) lecture ID
    :param lectureName: (str) lecture name
    :return: (dict) if success -> "result" would be "success" otherwise error message will be placed here.
    And if success -> "favList" will hold UserFav objects list.
    """
    db = DB()

    res = DotDict({
        "result": None,
        "successMsg": None
    })

    if db.exist('userfav', {'$and': [{'uid': uid}, {'lectureid': int(lecID)}]}):
        res.result = response[3405]
        return res

    query = {'uid': uid, 'lectureid': int(lecID), 'lecturename': lectureName}

    result = db.insert('userfav', query).result
    if result == "success":
        res.result = "success"
        res.successMsg = response[3406].format(uid, lectureName)
    else:
        res.result = response[3002].format(uid)

    return res


def delete_user_favorite(uid, lecID):
    """
    Delete user's favorite.
    :param uid: (str) user's LINE UID
    :param lecID: (int) lecture ID
    :return: (dict) if success -> "result" would be "success" otherwise error message will be placed here.
    And if success -> "favList" will hold UserFav objects list.
    """
    db = DB()

    res = DotDict({
        "result": None,
        "successMsg": None
    })

    if not db.exist('userfav', {'$and': [{'uid': uid}, {'lectureid': int(lecID)}]}):
        res.result = response[3408].format(lecID)
        return res

    query = {'$and': [{'uid': uid}, {'lectureid': int(lecID)}]}

    result = db.delete('userfav', query).result
    if result == "success":
        res.result = "success"
        res.successMsg = response[3407].format(uid, lecID)
    elif result == "fail":
        res.result = response[3409].format(lecID)
    else:
        res.result = response[3003].format(uid)

    return res


def add_users(uid):
    pass


def update_users(uid):
    pass
