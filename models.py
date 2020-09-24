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
        self.credits: int = c
        self.accepted: list = a
        self.total: list = t
        self.url: str = u

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
