import tornado.ioloop
import tornado.web
from tornado.options import define, options
import Settings
import platform
from datetime import datetime as dt
import gviz_api
import MySQLdb as mydb
import os

CONF={}
CONF['host'] = '127.0.0.1' #'remote-mysql'
CONF['port'] = int('33060')
CONF['user'] = 'root' #'os.environ['MYSQL_USER']
CONF['passwd'] =  'poto' #= os.environ['MYSQL_PASS']

schema = {"topic": ("string", "Topic"), "times": ("number", "Times")}
#data = [{"topic": "work", "times": 1}, {"topic": "sleep", "times": 2}]

define("port", default=8080, help="run on the given port", type=int)

def init_table():
    con = mydb.connect(**CONF)
    cur = con.cursor()
    try:
        cur.execute('create database demo')
        con.commit()
    except:
        pass
    con.select_db('demo')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS topics (name varchar(100) unique, ntimes integer default 0)')
    try:
        cur.execute("insert into topics values('python', 0)")
        cur.execute("insert into topics values('idl', 0)")
        cur.execute("insert into topics values('fortran', 0)")
        cur.execute("insert into topics values('c++', 0)")
        cur.execute("insert into topics values('go', 0)")
    except:
        pass
    cur.execute('CREATE TABLE IF NOT EXISTS records (name varchar(100), time datetime)')
    con.commit()
    con.close()

def add_topic(topic, new=False):
    con = mydb.connect(**CONF)
    con.select_db('demo')
    cur = con.cursor()
    if new:
        try:
            cur.execute("insert into topics values('{}', 0)".format(topic))
        except:
            pass
    cur.execute("insert into records values ('{topic}', '{time}')".format(topic=topic, time=dt.now().strftime('%Y-%m-%d %H:%M:%S')))
    cur.execute("UPDATE topics SET ntimes = ntimes + 1  WHERE name = '{topic}'".format(topic=topic))
    con.commit()
    con.close()

def get_data():
    con = mydb.connect(**CONF)
    con.select_db('demo')
    cur = con.cursor()
    cur.execute("select * from topics")
    data = cur.fetchall()
    con.commit()
    con.close()
    return data
    

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html", hostname=platform.node())

class GetDataHandler(tornado.web.RequestHandler):
    def get(self):
        data_table = gviz_api.DataTable(schema)
        all_data = get_data()
        data=[]
        for line in all_data:
            data.append({"topic": line[0], "times": line[1]})
        data_table.LoadData(data)
        self.write(data_table.ToJSon(columns_order=("topic", "times")))

class AddDataHandler(tornado.web.RequestHandler):
    def get(self):
        topic = self.get_argument("flavor",None)
        topictxt = self.get_argument("flavortxt",None)
        if topic is not None:
            add_topic(topic)
        if topictxt is not '':
            add_topic(topictxt.lower(), new=True)
        self.redirect('/')
        #self.render("main.html", hostname=platform.node())
        

class Application(tornado.web.Application):
    """
    The tornado application  class
    """

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/getdata", GetDataHandler),
            (r"/add", AddDataHandler),
            ]
        settings = {
            "template_path": Settings.TEMPLATE_PATH,
            "static_path": Settings.STATIC_PATH,
            "debug": Settings.DEBUG,
        }
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    """
    The main function
    """
    init_table()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
