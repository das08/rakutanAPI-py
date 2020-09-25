from db import Database as DB
from models import Rakutan
from modules.reserved import responseMessages as response


def get_lecture_by_id(kid):
    """
    Find rakutan info from lecture ID
    :param kid: (int) kougi ID(lecture ID)
    :return: (dict) if success -> "result" would be "success" otherwise error message will be placed here.
    And if success -> "rakutan" will hold a Rakutan object.
    """
    db = DB()
    query = {'id': int(kid)}
    result, count, queryResult = db.find('rakutan', query)

    res = {
        "result": None,
        "rakutan": None
    }

    if result == "success":
        if count == 0:
            res.result = response[1404].format(kid)
        else:
            res.result = "success"
            res.rakutan = Rakutan.from_dict(queryResult[0])
    else:
        res.result = response[1001].format(kid)

    return res


def get_lecture_by_search_word(search_word):
    """
    Find rakutan info from search word.
    :param search_word: (str) search word
    :return: (dict) if success -> "result" would be "success" otherwise error message will be placed here.
    And if success -> "rakutan" will hold a Rakutan object.
    """
    db = DB()

    # if search word has % in first letter, partial match search will be performed
    if search_word[0] == '%':
        query = {'lecturename': {'$regex': f'{search_word[1:]}', '$options': 'i'}}
    else:
        query = {'lecturename': {'$regex': f'^{search_word}', '$options': 'i'}}

    result, count, queryResult = db.find('rakutan', query, projection={'_id': False})

    res = {
        "result": None,
        "rakutanList": None
    }

    if result == "success":
        if count == 0:
            res.result = response[2404].format(search_word)
        else:
            res.result = "success"
            res.rakutanList = Rakutan.from_list(queryResult)
    else:
        res.result = response[2001].format(search_word)

    return res
