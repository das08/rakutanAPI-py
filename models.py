class Rakutan:
    lecID = None
    facultyName = None
    lectureName = None
    groups = None
    credits = None
    accepted = []
    total = []
    url = None

    def __init__(self, lecID, fN, lN, g, c, a, t, u):
        self.lecID: int = lecID
        self.facultyName: str = fN
        self.lectureName: str = lN
        self.groups: str = g
        self.credits: str = c
        self.accepted: list = a
        self.total: list = t
        self.url: str = u

    @classmethod
    def from_dict(cls, dbRakutanDict: dict):
        return Rakutan(
            lecID=dbRakutanDict['lecID'],
            fN=dbRakutanDict['facultyName'],
            lN=dbRakutanDict['lectureName'],
            g=dbRakutanDict['groups'],
            c=dbRakutanDict['credits'],
            a=dbRakutanDict['accepted'],
            t=dbRakutanDict['total'],
            u=dbRakutanDict['url']
        )

    @classmethod
    def from_list(cls, dbRakutanList: list):
        rakutanList = []
        for rakutan in dbRakutanList:
            rakutanList.append(cls.from_dict(rakutan))
        return rakutanList

    def to_dict(self):
        return {
            'lecID': self.lecID,
            'facultyName': self.facultyName,
            'lectureName': self.lectureName,
            'groups': self.groups,
            'credits': self.credits,
            'accepted': self.accepted,
            'total': self.total,
            'url': self.url
        }


class UserFav:
    uid = None
    lecID = None

    def __init__(self, uid, lecID):
        self.uid: str = uid
        self.lecID: int = lecID

    @classmethod
    def from_dict(cls, dbUserFavDict: dict):
        return UserFav(
            uid=dbUserFavDict['uid'],
            lecID=dbUserFavDict['lecID']
        )

    @classmethod
    def from_list(cls, dbUserFavList: list):
        userFavList = []
        for fav in dbUserFavList:
            userFavList.append(cls.from_dict(fav))
        return userFavList

    def to_dict(self):
        return {
            'uid': self.uid,
            'lecID': self.lecID
        }


class Kakomon:
    uid = None
    lecID = None
    url = None
    sendTime = None

    def __init__(self, uid, lecID, u, sT):
        self.uid: str = uid
        self.lecID: int = lecID
        self.url: str = u
        self.sendTime: str = sT

    @classmethod
    def from_dict(cls, dbKakomonDict: dict):
        return Kakomon(
            uid=dbKakomonDict['uid'],
            lecID=dbKakomonDict['lecID'],
            u=dbKakomonDict['url'],
            sT=dbKakomonDict['sendTime']
        )

    @classmethod
    def from_list(cls, dbKakomonList: list):
        kakomonList = []
        for kakomon in dbKakomonList:
            kakomonList.append(cls.from_dict(kakomon))
        return kakomonList

    def to_dict(self):
        return {
            'uid': self.uid,
            'lecID': self.lecID,
            'url': self.url,
            'sendTime': self.sendTime
        }