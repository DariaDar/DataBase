class Faculty(object):
    def __init__(self, name, deanAge, faculId, univerId, universities):
        if not universities.isExist(univerId):
            raise Exception("\nID университета не найдено.")
        self.name = name
        self.deanAge = deanAge
        self.faculId = faculId
        self.univerId = univerId

    def edit(self, name, deanAge):
        self.name = name
        self.deanAge = deanAge


    def __str__(self):
        return "%s, dean age: %s" % (self.name, self.deanAge)

