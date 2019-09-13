import psycopg2
from configparser import ConfigParser

def main():    
    connect()


def connect():
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()              
        cur.execute('select * from chemmap_3d_arr  limit(10)')         
        line = cur.fetchone()

        print(line[0])
        print(line[1])
        print(line[2])
        print(line[3][2])
        #or you can access array data as:
        array = line[3]
        data= array[2]
        print(data)
       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def config(filename='database.ini', section='postgresql'):
     parser = ConfigParser()
     parser.read(filename)
     db = {}
     if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]]=param[1]
     else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

     return db

if __name__=="__main__":
    main()