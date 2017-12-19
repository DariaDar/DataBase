from MySQLdb import Error, connect
import sys
import json

file_path = r"C:\\1\\Studies\\DB\\Labs\\lab2\\"
paints_path = file_path + "painting.json"
artists_path = file_path + "artist.json"
visitors_path = file_path + "visitor.json"


class Object(object):
    pass


class Database:
    def __init__(self):
        self.con = None

    def connect(self):
        try:
            self.con = connect('localhost', 'daria', 'password', 'gallery')
        except Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)

    def close_connection(self):
        if self.con:
            self.con.close()

    def fill_tables(self):
        self.connect()

        with self.con:
            cur = self.con.cursor()
            cur.execute("DROP TABLE IF EXISTS visits")
            cur.execute("SET FOREIGN_KEY_CHECKS=0;")
            cur.execute("DELETE FROM artists;")
            cur.execute("ALTER TABLE artists AUTO_INCREMENT=1;")
            cur.execute("SET FOREIGN_KEY_CHECKS=1;")
            cur.execute("DELETE FROM paints;")
            cur.execute("ALTER TABLE paints AUTO_INCREMENT=1;")
            cur.execute("DELETE FROM visitors;")
            cur.execute("ALTER TABLE visitors AUTO_INCREMENT=1;")
            self.load_object()

            cur.execute("CREATE TABLE visits("
                        "visit_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                        "paint_id INT NOT NULL,"
                        "artist_id INT NOT NULL,"
                        "visitor_id INT NOT NULL,"
                        "FOREIGN KEY(paint_id) REFERENCES paints(paint_id),"
                        "FOREIGN KEY(artist_id) REFERENCES artists(artist_id),"
                        "FOREIGN KEY(visitor_id) REFERENCES visitors(visitor_id))")

        self.close_connection()

    def load_object(self):
        artist_data = open(artists_path, 'r')
        data = json.load(artist_data)
        for i in data['artists']['artist']:
            print(i)
            self.add_artist(i)
        artist_data.close()

        paint_data = open(paints_path, 'r')
        data = json.load(paint_data)
        for i in data['paints']['paint']:
            print(i)
            self.add_paint(i)
        paint_data.close()

        visitor_data = open(visitors_path, 'r')
        data = json.load(visitor_data)
        for i in data['visitors']['visitor']:
            print(i)
            self.add_visitor(i)
        visitor_data.close()

    def add_artist(self, data):
        cur = self.con.cursor()
        try:
            mysql = ("INSERT INTO artists(artist_name, birthdate, birthplace, biography) VALUES (%s, %s, %s, %s);")
            cur.execute(mysql, (data['artist_name'], data['birthdate'], data['birthplace'], data['biography']))
        except:
            print("EXCPTN")
        else:
            self.con.commit()

    def add_paint(self, data):
        cur = self.con.cursor()
        try:
            cur.execute("SELECT artist_id FROM `gallery`.`artists` WHERE artist_name=\"%s\"" % (data['artist']))
            artist = cur.fetchall()
            mysql = (
            "INSERT INTO paints(paint_name, style, creation_date, artist_id, technique) VALUES (%s, %s, %s, %s, %s);")
            cur.execute(mysql, (data['paint_name'], data['style'], int(data['date']), artist, data['technique']))
        except:
            print("EXCPTN")
        else:
            self.con.commit()

    def add_visitor(self, data):
        cur = self.con.cursor()
        try:
            mysql = ("INSERT INTO visitors(visitor_name, email, student) VALUES (%s, %s, %s);")
            if data['student'] == "true":
                student = True
            else:
                student = False
            cur.execute(mysql, (data['visitor_name'], data['email'], student))
        finally:
            self.con.commit()

    def read_all_entities(self):
        self.connect()

        with self.con:
            cur = self.con.cursor()
            objects = Object()
            cur.execute("SELECT artist_id, artist_name FROM artists")
            artists = cur.fetchall()
            objects.artists = artists
            cur.execute("SELECT paint_id, paint_name FROM paints")
            paints = cur.fetchall()
            objects.paints = paints
            cur.execute("SELECT visitor_id, visitor_name FROM visitors")
            visitors = cur.fetchall()
            objects.visitors = visitors

        self.close_connection()
        return objects

    def create_fact(self, artist_id, paint_id, visitor_id):
        self.connect()

        with self.con:
            cur = self.con.cursor()
            mysql = ("INSERT into visits(artist_id, paint_id, visitor_id) VALUES(%s, %s, %s)")
            cur.execute(mysql, (artist_id, paint_id, visitor_id))

        self.close_connection()

    def delete_fact(self, visit_id):
        self.connect()

        with self.con:
            cur = self.con.cursor()
            cur.execute("DELETE FROM visits WHERE visit_id=" + visit_id)

        self.close_connection()

    def update_fact(self, visit_id, artist_id, paint_id, visitor_id):
        self.connect()

        with self.con:
            cur = self.con.cursor()
            cur.execute("UPDATE visits SET artist_id=" + artist_id +
                        ", paint_id=" + paint_id +
                        ", visitor_id=" + visitor_id + " " +
                        "WHERE visit_id=" + visit_id)

        self.close_connection()

    def read_facts(self):
        self.connect()

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT visits.visit_id, artists.artist_name, paints.paint_name, visitors.visitor_name "
                        "FROM ((( visits "
                        "INNER JOIN artists ON visits.artist_id = artists.artist_id) "
                        "INNER JOIN paints ON visits.paint_id = paints.paint_id) "
                        "INNER JOIN visitors ON visits.visitor_id = visitors.visitor_id)")
            objects = cur.fetchall()

        self.close_connection()
        return objects

    def visitor_search(self, b_type):
        self.connect()

        with self.con:
            cur = self.con.cursor()
            if b_type == "true":
                student = True
            else:
                student = False
            cur.execute("SELECT * FROM visitors WHERE student=%s;" % student)
            objects = cur.fetchall()
        self.close_connection()
        return objects

    def get_technique(self):
        self.connect()

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT DISTINCT technique FROM paints;")
            objects = cur.fetchall()
        self.close_connection()
        return objects

    def get_tech_entities(self, tech):
        self.connect()

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM paints WHERE technique='" + tech + "'")
            objects = cur.fetchall()
        self.close_connection()
        return objects

    def boolean_search(self, table_name, command):
        self.connect()

        with self.con:
            cur = self.con.cursor()
            mysql = "SELECT * FROM " + table_name
            if command != "":
                mysql += " " + command
            cur.execute(mysql)

            objects = cur.fetchall()
        self.close_connection()
        return objects
