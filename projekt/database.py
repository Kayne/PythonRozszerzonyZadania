#encoding: utf-8
import sqlite3
import sys


class Database:
    """
    Obsługa bazy danych

    Atrybuty:
        con     holder na połączenie z bazą danych
    """
    con = ""

    def connect(self):
        """
        Łączenie się z bazą danych
        """
        try:
            self.con = sqlite3.connect('db/db.sqlite')
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def disconnect(self):
        """
        Rozłączenie z bazą danych
        """
        self.con.close()

    def prepare_database(self):
        """
        Utworzenie bazy danych jeśli nie istniała wcześniej
        """
        with self.con:
            cur = self.con.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, file TEXT UNIQUE)')

    def clear_database(self):
        """
        Czyścy bazę danych - niszcząc tabelę
        """
        with self.con:
            cur = self.con.cursor()
            cur.execute('DROP TABLE images')
        self.prepare_database()

    def add_image(self, image):
        """
        Dodanie grafiki do tabeli
        """
        with self.con:
            cur = self.con.cursor()
            try:
                cur.execute('INSERT INTO images (`file`) VALUES (?)', [image])
            except sqlite3.IntegrityError:
                pass

    def get_images(self):
        """
        Zwraca wszystkie obrazki z tabeli
        """
        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT * FROM images ORDER BY id ASC')
            return cur.fetchall()

    def get_image(self, id):
        """
        Zwraca pojedynczy obrazek
        """
        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT * FROM images WHERE id=? LIMIT 1', [id])
            return cur.fetchone()

    def remove_image(self, id):
        """
        Usuwa wskazany obrazek z tabeli
        """
        with self.con:
            cur = self.con.cursor()
            cur.execute('DELETE FROM images WHERE id=?', [id])

    def count_images(self):
        """
        Zlicza ile obrazków jest w tabeli
        """
        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT count(id) FROM images')
            return cur.fetchone()

    def get_images_in_range(self, min=0, max=250):
        """
        Zwraca obrazki z podanego zakresu
        """
        if min < 0:
            min = 0
        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT * FROM images ORDER BY id LIMIT ? OFFSET ?', [max, min])
            return cur.fetchall()
