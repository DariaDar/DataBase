from faculty import Faculty
from university import University
from universities import Universities
from faculties import Faculties
import os
import pickle

class Main:
    def run(self):
        data = Main.deserialize(self)
        if data[0] != None:
            universities = data[0]
        else:
            universities = Universities()
        if data[1] != None:
            faculties = data[1]
        else:
            faculties = Faculties
        if data[2] != None:
            uId = data[2]
        else:
            uId = 0
        if data[3] != None:
            facId = data[3]
        else:
            facId = 0;

        while 1:
            print(
                "\nДоступный функционал: \n1. Добавить университет \n2. Добавить факультет \n3. Удалить университет \n4. Удалить факультет "
                "\n5. Фильтрация (возраст декана < 50)\n6. Список университетов \n7. Список факультетов университета \n8. Список всех факультетов \n"
                "9. Модифицировать университет \n10. Модифицировать факультет \n11. Выход\n\n")

            num = input("Введите номер: ")

            if num.isdigit():
                if num == '1':
                    name = input("Введите название университета: ")
                    university = University(name, uId)
                    universities.add(university)
                    print("Университет успешно добавлен")
                    uId += 1
                elif num == '2':
                    nameUniver = input("Введите университет для факультета: ")
                    univ = universities.getUniverByName(nameUniver)
                    if univ != None:
                        name = input("Введите название факультета и возраст декана (__ __): ")
                        faculty = name.split(' ')
                        faculties.add(Faculty(faculty[0], faculty[1], facId, univ.uId, universities))
                        print("Факультет успешно добавлен")
                        facId += 1
                    #os.system("pause")
                elif num == '3':
                    name = input("Введите название университета: ")
                    univer = universities.getUniverByName(name)
                    faculList = faculties.getListUniverId(univer.uId)
                    faculties.deleteUniverFaculList(faculList)
                    universities.remove(univer)
                    print("Университет успешно удален.")
                elif num == '4':
                    name = input("Название университета и факультет, который хотите удалить: ")
                    words = name.split(' ')
                    univer = universities.getUniverByName(words[0])
                    faculty = faculties.getFacultyByName(words[1], univer.uId)
                    if faculty == None:
                        print("Факультет не найден")
                    else:
                        faculties.remove(faculty)
                        print("Факультет успешно удален.")
                elif num == '5':
                    list = universities.getUniverListDeanAge(faculties.getFacultiesListDeanAge())
                    i = 0;
                    for univer in list:
                        print("%i. %s" %(i + 1, univer.name))
                        i += 1
                elif num == '6':
                    universities.showList()
                elif num == '7':
                    name = input("Университет: ")
                    univer = universities.getUniverByName(name)
                    if univer != None:
                        list = faculties.getListUniverId(univer.uId)
                        for faculty in list:
                            print(faculty.__str__())
                elif num == '8':
                    faculties.showList()
                elif num == '9':
                    name = input("Старое и новое название университета (__ __): ")
                    oldNew = name.split(" ")
                    univer = universities.getUniverByName(oldNew[0])
                    if univer != None:
                        univer.edit(oldNew[1])
                        print("Изменения сохранены.")
                elif num == '10':
                    name = input("Введите университет и его факультет (__ __): ")
                    newname = input("Введите новое название факультета и возраст декана(__ __): ")
                    words = name.split(' ')
                    univer = universities.getUniverByName(words[0])
                    newWords = newname.split(" ")
                    faculty = faculties.getFacultyByName(words[1], univer.uId)
                    if faculty == None:
                        print("Факультет не найден")
                    else:
                        faculty.edit(newWords[0], newWords[1])
                        print("Изменения сохранены.")
                elif num == '11':
                    break
            else:
                print("Неправильный ввод!")

        Main.serialize(self, universities, faculties, uId, facId)

    @staticmethod
    def serialize(self, universities, faculties, uid, fid):
        data = [universities, faculties, uid, fid]
        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f)

    @staticmethod
    def deserialize(self):
        with open('data.pickle', 'rb') as f:
            data = pickle.load(f)
        return data



main = Main()
main.run()