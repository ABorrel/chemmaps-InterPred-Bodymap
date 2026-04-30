import psycopg2
from os import path

from django_server.db_config import load_postgresql_settings


class DBrequest:
    def __init__(self, verbose=1):
        self.dbconfig = path.abspath("./database.ini")
        self.conn = None
        self.verbose = verbose
        self.connect_kwargs = None
        self.schema = None

    def config(self, section="postgresql"):
        del section
        self.connect_kwargs, self.schema = load_postgresql_settings(self.dbconfig)
        self.params = dict(self.connect_kwargs)

    def connOpen(self):
        try:
            self.config()
            if self.verbose:
                print("Connecting to the PostgreSQL database...")
            if self.conn is not None:
                return
            self.conn = psycopg2.connect(**self.connect_kwargs)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn = None

    def connClose(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            if self.verbose == 1:
                print("Database connection closed.")

    def addElement(self, nameTable, lcoloumn, lval):
        self.connOpen()
        sqlCMD = "INSERT INTO %s(%s) VALUES(%s);" % (
            nameTable,
            ",".join(lcoloumn),
            ",".join(["'%s'" % (val,) for val in lval]),
        )
        if self.verbose == 1:
            print(sqlCMD)
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                cur.execute(sqlCMD)
                self.conn.commit()
                self.connClose()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                self.connClose()
        else:
            print("Open connection first")

    def extractColoumn(self, nameTable, coloumn, condition="", close_conn=True):
        """Fetch rows; set close_conn=False to reuse the same connection for the next query."""
        self.verbose = 0
        self.connOpen()
        sqlCMD = "SELECT %s FROM %s %s;" % (coloumn, nameTable, condition)
        if self.verbose == 1:
            print(sqlCMD)
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                cur.execute(sqlCMD)
                out = cur.fetchall()
                if self.verbose == 1:
                    print(out)
                return out
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                return "ERROR"
            finally:
                if close_conn:
                    self.connClose()
        else:
            print("Open connection first")
            if close_conn:
                self.connClose()
            return "ERROR"

    def getRow(self, table, condition):
        self.connOpen()
        sqlCMD = "SELECT * FROM %s WHERE %s;" % (table, condition)
        if self.verbose == 1:
            print(sqlCMD)
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                cur.execute(sqlCMD)
                out = cur.fetchall()
                if self.verbose == 1:
                    print(out)
                self.connClose()
                return out
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                self.connClose()
                return error
        else:
            self.connClose()
            print("Open connection first")

    def execCMD(self, cmdSQL):
        out = None
        if self.verbose == 1:
            print(cmdSQL)
        self.connOpen()
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                cur.execute(cmdSQL)
                out = cur.fetchall()
                if self.verbose == 1:
                    print(out)
            except (Exception, psycopg2.DatabaseError) as error:
                self.connClose()
                print(error)
                return "Error"
        else:
            print("Open connection first")
            return "Error"
        self.connClose()
        return out

    def updateElement(self, cmdSQL):
        if self.verbose == 1:
            print(cmdSQL)
        self.connOpen()
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                cur.execute(cmdSQL)
                self.conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                self.connClose()
                print(error)
                return "Error"
        else:
            print("Open connection first")
        self.connClose()
        return 0
