from faculty import Faculty

class Faculties:
    def __init__(self):
        self.faculties = []

    def add(self, faculty):
        self.faculties.append(faculty)

    def remove(self, faculty):
        self.faculties.remove(faculty)

    def getFacultyByName(self, name, uid):
        for faculty in self.faculties:
            if faculty.name == name and faculty.univerId == uid:
                return faculty
            else:
                continue
        return None

    def getFacultiesListDeanAge(self):
        deanList = []
        for faculty in self.faculties:
            if faculty.deanAge <= '50':
                deanList.append(faculty)
        return deanList

    def getListUniverId(self, uid):
        list = []
        for faculty in self.faculties:
            if faculty.univerId == uid:
                list.append(faculty)
        return list

    def deleteUniverFaculList(self, faculList):
        for fac in faculList:
            self.faculties.remove(fac)

    def showList(self):
        for fac in self.faculties:
            print (fac.name)