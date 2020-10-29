from dataclasses import dataclass


@dataclass
class Rakutan:
    lecID: int
    facultyName: str
    lectureName: str
    groups: str
    credits: str
    accepted: list
    total: list
    url: str

    @classmethod
    def from_dict(cls, dbRakutanDict: dict):
        return Rakutan(
            lecID=dbRakutanDict['lecID'],
            facultyName=dbRakutanDict['facultyName'],
            lectureName=dbRakutanDict['lectureName'],
            groups=dbRakutanDict['groups'],
            credits=dbRakutanDict['credits'],
            accepted=dbRakutanDict['accepted'],
            total=dbRakutanDict['total'],
            url=dbRakutanDict['url']
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


@dataclass
class UserFav:
    uid: str
    lecID: int

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


@dataclass
class Kakomon:
    uid: str
    lecID: int
    url: str
    sendTime: str

    @classmethod
    def from_dict(cls, dbKakomonDict: dict):
        return Kakomon(
            uid=dbKakomonDict['uid'],
            lecID=dbKakomonDict['lecID'],
            url=dbKakomonDict['url'],
            sendTime=dbKakomonDict['sendTime']
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
