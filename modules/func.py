import datetime
import random
import re

from db import Database as DB
from models import Rakutan, UserFav, Kakomon
from modules.DotDict import DotDict
from modules.reserved import responseMessages as response


def get_lecture_by_id(lecID):
    """
    Find rakutan info from lecture ID
    :param lecID: (int) lecture ID
    :return: (dict) if success -> "result" would be "success" otherwise error message will be placed here.
    And if success -> "rakutan" will hold a Rakutan object.
    """
    db = DB()
    query = {'lecID': int(lecID)}
    result, count, queryResult = [*db.find('rakutan2020', query).values()]

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
    And if success -> "rakutanList" will hold Rakutan objects list.
    """
    db = DB()

    # if search word has % in first letter, partial match search will be performed
    if search_word[0] == '%':
        query = {'lectureName': {'$regex': f'{search_word[1:]}', '$options': 'i'}}
    else:
        query = {'lectureName': {'$regex': f'^{search_word}', '$options': 'i'}}

    # result, count, queryResult = db.find('rakutan', query, projection={'_id': False})
    result, count, queryResult = [*db.find('rakutan2020', query, projection={'_id': False}).values()]

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
    result, count, queryResult = [*db.find('userfav', query).values()]

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
        query = {'$and': [{'facultyName': '国際高等教育院'}, {'total.0': {'$gt': 4}},
                          {'$expr': {'$lt': [{'$arrayElemAt': ['$accepted', 0]},
                                             {'$multiply': [0.31, {'$arrayElemAt': ['$total', 0]}]}]}}]}
    elif omikujiType == "normal":
        query = {'$and': [{'facultyName': '国際高等教育院'}, {'accepted.0': {'$gt': 15}},
                          {'$expr': {'$gt': [{'$arrayElemAt': ['$accepted', 0]},
                                             {'$multiply': [0.8, {'$arrayElemAt': ['$total', 0]}]}]}}]}
    else:
        res.result = response[4002].format(omikujiType)
        return res

    result, count, queryResult = [*db.find('rakutan2020', query).values()]

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
    """
    Get provided kakomon list.
    :return: (dict) if success -> "result" would be "success" otherwise error message will be placed here.
    And if success -> "kakomonList" will hold Kakomon objects list.
    """
    db = DB()
    query = {'lecID': {'$ne': ''}}
    result, count, queryResult = [*db.find('urlmerge', query).values()]

    res = DotDict({
        "result": None,
        "count": None,
        "kakomonList": None
    })

    if result == "success":
        if count == 0:
            res.result = response[5404]
        else:
            res.result = "success"
            res.count = count
            res.kakomonList = Kakomon.from_list(queryResult)
    else:
        res.result = response[5001].format(uid)

    return res


def add_user_favorite(uid, lecID):
    """
    Add user's favorite.
    :param uid: (str) user's LINE UID
    :param lecID: (int) lecture ID
    :return: (dict) if success -> "result" would be "success" otherwise error message will be placed here.
    And if success -> "successMsg" will hold succcess message string.
    """
    db = DB()

    res = DotDict({
        "result": None,
        "successMsg": None
    })

    if db.exist('userfav', {'$and': [{'uid': uid}, {'lecID': int(lecID)}]}):
        res.result = response[3405]
        return res

    query = {'uid': uid, 'lecID': int(lecID)}

    result = db.insert('userfav', query).result
    if result == "success":
        res.result = "success"
        res.successMsg = response[3406].format(uid, lecID)
    else:
        res.result = response[3002].format(uid)

    return res


def delete_user_favorite(uid, lecID):
    """
    Delete user's favorite.
    :param uid: (str) user's LINE UID
    :param lecID: (int) lecture ID
    :return: (dict) if success -> "result" would be "success" otherwise error message will be placed here.
    And if success -> "successMsg" will hold succcess message string.
    """
    db = DB()

    res = DotDict({
        "result": None,
        "successMsg": None
    })

    if not db.exist('userfav', {'$and': [{'uid': uid}, {'lecID': int(lecID)}]}):
        res.result = response[3408].format(lecID)
        return res

    query = {'$and': [{'uid': uid}, {'lecID': int(lecID)}]}

    result = db.delete('userfav', query).result
    if result == "success":
        res.result = "success"
        res.successMsg = response[3407].format(uid, lecID)
    elif result == "fail":
        res.result = response[3409].format(lecID)
    else:
        res.result = response[3003].format(uid)

    return res


def add_kakomon_url(uid, lecID, url):
    """
    Add kakomon url to merge list.
    :param uid: (str) user's LINE UID
    :param lecID: (int) lecture ID
    :param url: (str) URL
    :return: (dict) if success -> "result" would be "success" otherwise error message will be placed here.
    And if success -> "successMsg" will hold succcess message string.
    """
    db = DB()

    res = DotDict({
        "result": None,
        "successMsg": None
    })

    if not re.match("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", url):
        res.result = response[5003].format(lecID)
        return res

    dates = str(datetime.datetime.now()).replace('.', '/')
    query = {'lecID': int(lecID), 'url': url, 'uid': uid, 'sendTime': dates}

    result = db.insert('urlmerge', query).result
    if result == "success":
        res.result = "success"
        res.successMsg = response[5405].format(lecID)
    else:
        res.result = response[5002].format(uid)

    return res


def delete_kakomon_url(lecID, url):
    """
    Delete kakomon url from merge list.
    :param lecID: (int) lecture ID
    :param url: (str) url
    :return: (dict) if success -> "result" would be "success" otherwise error message will be placed here.
    And if success -> "successMsg" will hold succcess message string.
    """
    db = DB()

    res = DotDict({
        "result": None,
        "successMsg": None
    })

    # TODO: work on existence check
    if not db.exist('urlmerge', {'$and': [{'uid': uid}, {'lecID': int(lecID)}]}):
        res.result = response[3408].format(lecID)
        return res

    query = {'$and': [{'lecID': int(lecID)}, {'url': url}]}

    result = db.delete('urlmerge', query).result
    if result == "success":
        res.result = "success"
        res.successMsg = response[5406].format(lecID, url)
    elif result == "fail":
        res.result = response[5407].format(lecID, url)
    else:
        res.result = response[5004]

    return res


def add_users(uid):
    pass


def update_users(uid):
    pass
