import psycopg2

from os import path

from django_server.db_config import load_postgresql_settings


class DB:
    def __init__(self, verbose=0):
        self.dbconfig = path.abspath("./database.ini")
        self.conn = None
        self.verbose = verbose
        self.connect_kwargs = None
        self.schema = None

    def config(self, section="postgresql"):
        del section  # retained for callers; always use postgresql section file layout
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

    def addElementCMD(self, sqlCMD):
        if self.verbose == 1:
            print(sqlCMD)
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                cur.execute(sqlCMD)
                self.conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        else:
            print("Open connection first")

    def extractColoumn(self, nameTable, column, condition=""):
        self.verbose = 0
        self.connOpen()
        sqlCMD = "SELECT %s FROM %s %s" % (column, nameTable, condition)
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
                return "ERROR"
        else:
            print("Open connection first")
            self.connClose()
            return "ERROR"

    def getColnames(self, nameTable):
        self.config()
        schema = self.schema or "public"
        self.connOpen()
        if self.conn is None:
            print("Open connection first")
            return []
        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                SELECT column_name FROM information_schema.columns
                WHERE table_name = %s AND table_schema = %s
                ORDER BY ordinal_position
                """,
                (nameTable, schema),
            )
            out = cur.fetchall()
            if self.verbose == 1:
                print(out)
            return out
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return []
        finally:
            self.connClose()

    def getTable(self, nameTable):
        self.connOpen()
        sqlCMD = "SELECT * FROM %s;" % (nameTable,)
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
                return []
            finally:
                self.connClose()
        else:
            self.connClose()
            print("Open connection first")
            return []

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
                return out
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                return error
            finally:
                self.connClose()
        else:
            self.connClose()
            print("Open connection first")
            return None

    def execCMD(self, cmdSQL):
        out = None
        if self.verbose == 1:
            print(cmdSQL)
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                cur.execute(cmdSQL)
                out = cur.fetchall()
                if self.verbose == 1:
                    print(out)
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error", error)
                return "Error"
        else:
            print("Open connection first")
            return "Error"
        return out

    def updateElement(self, cmdSQL):
        if self.verbose == 1:
            print(cmdSQL)
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                cur.execute(cmdSQL)
                self.conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                return "Error"
        else:
            print("Open connection first")
        return 0
