from university import University
class Universities(object):

    def __init__(self):
        self.universities = []

    def add(self, univer):
        self.universities.append(univer)

    def remove(self, univer):
        self.universities.remove(univer)

    def getUniverByName(self, name):
        for univer in self.universities:
            if univer.name == name:
                return univer
            else:
                continue
        print("Университет не найден")
        return  None

    def showList(self):
        i = 0;
        for univer in self.universities:
            print("%i. %s" % (i + 1, univer.name))
            i += 1

    def getUniverListDeanAge(self, faculties):
        univers = []
        for univer in self.universities:
            for faculty in faculties:
                if univer.uId == faculty.univerId and not univers.__contains__(univer):
                    univers.append(univer)
        return univers

    def isExist(self, uid):
        for un in self.universities:
            if un.uId == uid:
                return True
            else:
                continue
        return False








