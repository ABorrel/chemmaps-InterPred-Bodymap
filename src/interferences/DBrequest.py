import psycopg2
from configparser import ConfigParser
from os import path

class DBrequest:
    def __init__(self, verbose=1):
        self.dbconfig = path.abspath("./database.ini")
        self.conn = None
        self.verbose = verbose


    def config(self, section='postgresql'):
        parser = ConfigParser()
        parser.read(self.dbconfig)
        dparams = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                dparams[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, self.dbconfig))

        self.params = dparams


    def connOpen(self):
        try:
            self.config()
            if self.verbose: print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(** self.params)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def connClose(self):
        if self.conn is not None:
            self.conn.close()
            if self.verbose == 1: print('Database connection closed.')


    def addElement(self, nameTable, lcoloumn, lval):
        self.connOpen()
        sqlCMD = "INSERT INTO %s(%s) VALUES(%s);"%(nameTable, ",".join(lcoloumn), ",".join(["\'%s\'"%(val) for val in lval]))
        if self.verbose == 1: print(sqlCMD)
        if self.conn != None:
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

    def extractColoumn(self, nameTable, coloumn, condition=""):
        self.connOpen()
        sqlCMD = "SELECT %s FROM %s %s;" % (coloumn, nameTable, condition)
        if self.verbose == 1: print(sqlCMD)
        if self.conn != None:
            try:
                cur = self.conn.cursor()
                cur.execute(sqlCMD)
                out = cur.fetchall()
                if self.verbose == 1: print(out)
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



    def getRow(self, table, condition):

        self.connOpen()
        sqlCMD = "SELECT * FROM %s WHERE %s;" % (table, condition)
        if self.verbose == 1: print(sqlCMD)
        if self.conn != None:
            try:
                cur = self.conn.cursor()
                cur.execute(sqlCMD)
                out = cur.fetchall()
                if self.verbose == 1: print(out)
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
        if self.verbose == 1: print(cmdSQL)
        self.connOpen()
        if self.conn != None:
            try:
                cur = self.conn.cursor()
                cur.execute(cmdSQL)
                #self.conn.commit()
                # print(cur)
                out = cur.fetchall()
                if self.verbose == 1: print(out)
            except (Exception, psycopg2.DatabaseError) as error:
                self.connClose()
                print(error)
                return "Error"
        else:
            print("Open connection first")
        self.connClose()
        return out

    def updateElement(self, cmdSQL):
        if self.verbose == 1: print(cmdSQL)
        self.connOpen()
        if self.conn != None:
            try:
                cur = self.conn.cursor()
                cur.execute(cmdSQL)
                self.conn.commit()
                # print(cur)
                #out = cur.fetchall()
                #if self.verbose == 1: print(out)
            except (Exception, psycopg2.DatabaseError) as error:
                self.connClose()
                print(error)
                return "Error"
        else:
            print("Open connection first")
        self.connClose()
        return 0



#cmd = 'select * from drugbank_chemicals  limit(10)'

#cmd = """INSERT INTO chemmaps_test(dbid, test) VALUES ('test3', 'test6')"""

#dbr = DBrequest()
#dbr.connOpen()
#dbr.addElement("chemmaps_test", ["dbid", "test"], ["tt2", "fff5"])
#out = dbr.extractColoumn("chemmap_1d2d_arr", "data_arr")
#dbr.execCMD(cmd)
#dbr.connClose()


#print(out[0][0][4])


