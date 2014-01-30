from SimpleXMLRPCServer import *
import database
import datetime

database = database.Database()
database.connect()
database.prepare_database()

def add_appointment(params):
    global database
    params[3] = datetime.datetime.strptime(params[3], "%Y-%m-%d %H:%M")
    params[4] = datetime.datetime.strptime(params[4], "%Y-%m-%d %H:%M")
    with database.con:
        cur = database.con.cursor()
        cur.execute('INSERT INTO appointments (`name`, `content`, `type`, `start_date`, `end_date`) VALUES (?, ?, ?, ?, ?)', params)

def get_last_appointment():
    global database
    with database.con:
        cur = database.con.cursor()
        cur.execute('SELECT id FROM appointments ORDER BY id DESC LIMIT 1')
        return cur.fetchone()

def get_appointments(search = False):
    global database
    with database.con:
        cur = database.con.cursor()
        if search == False:
            cur.execute('SELECT * FROM appointments')
        else:
            cur.execute(search)
        return cur.fetchall()

def remove_appointment(id):
    global database
    with database.con:
        cur = database.con.cursor()
        cur.execute('DELETE FROM appointments WHERE id=?', [id])

def get_appointment(id):
    global database
    with database.con:
        cur = database.con.cursor()
        cur.execute('SELECT * FROM appointments WHERE id=? LIMIT 1', [id])
        return cur.fetchone()

def update_appointment(params):
    global database
    params[3] = datetime.datetime.strptime(params[3], "%Y-%m-%d %H:%M")
    params[4] = datetime.datetime.strptime(params[4], "%Y-%m-%d %H:%M")
    with database.con:
        cur = database.con.cursor()
        cur.execute('UPDATE appointments SET name=?, content=?, type=?, start_date=?, end_date=? WHERE id=?', params)

def ping():
    return "Pong"


server = SimpleXMLRPCServer(("localhost", 8002), allow_none=True)
server.register_function(add_appointment)
server.register_function(get_last_appointment)
server.register_function(get_appointments)
server.register_function(remove_appointment)
server.register_function(get_appointment)
server.register_function(update_appointment)
server.register_function(ping)
server.serve_forever()