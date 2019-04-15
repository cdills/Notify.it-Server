"Watches Reddit submission stream and notifies based on user criteria"

import sys
import sqlite3
from multiprocessing import Process

from flask import Flask, g, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
masterList = []
database = "./users.db"   #Will create if noexist

class userprefs(): #Define empty string for argument objects. Not sure if required.
    sub = ""
    query = ""
    udid = ""


class CreateMonitor(Resource): #Updates DB with arguments from POST. Returns posted arguments
    def post(self):
        try:
            global args
            global p1
            # Parse the arguments
            parser = reqparse.RequestParser()

            parser.add_argument('sub', type=str, help='subreddit to search')
            parser.add_argument('query', type=str, help='text to search for')
            parser.add_argument('udid', type=str, help='unique device ID')
            args = parser.parse_args()

            newUser = userprefs()
            newUser.sub = args['sub']
            newUser.query = args['query']
            newUser.udid = args['udid']
            masterList.append(newUser)

            with sqlite3.connect(database) as con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO users (id,sub,query,udid) VALUES (Null, \"{newUser.sub}\", \"{newUser.query}\", \"{newUser.udid}\") ") """WHERE NOT EXISTS (SELECT * FROM users WHERE sub = \"{newUser.sub}\" AND query = \"{newUser.query}\" AND udid = \"{newUser.udid}\")")
                con.commit()

            return {'sub': args['sub'], 'query': args['query'], 'udid': args['udid']}

        except Exception as e:
            return {'error': str(e)}

class ClearSearch(Resource): #Removes entry from DB for matching user ID from POST. Returns user ID
    def post(self):
        try:
            global args
            global p1
            # Parse the arguments
            parser = reqparse.RequestParser()

            parser.add_argument('udid', type=str, help='unique device ID')
            args = parser.parse_args()

            newUser = userprefs()

            newUser.udid = args['udid']


            with sqlite3.connect(database) as con:
                cur = con.cursor()
                cur.execute(f"DELETE FROM users WHERE udid = \"{newUser.udid}\"") #Will delete ALL matching entries.
                con.commit()

            return {'udid': args['udid']}

        except Exception as e:
            return {'error': str(e)}

api.add_resource(ClearSearch, '/ClearSearch') #Adds the functions to the specified URL for API
api.add_resource(CreateMonitor, '/CreateMonitor') #Adds the functions to the specified URL for API

def create_connection(db_file): #Creates DB connection, returns connection object
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return None

def create_table(conn, create_table_sql): #Creates table with specified query and connection object.
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)

###def main():
#    p1 = Process(app.run(debug=True))
 #   p1.start()"""


def main():


    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        sub text NOT NULL,
                                        query text,
                                        UDID text
                                    ); """


    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create user table
        create_table(conn, sql_create_user_table)

    else:
        print("Error! cannot create the database connection.")

    app.run(host='0.0.0.0', port = 5500) #Starts the API listening on localhost:5000


#for item in masterList:
 #   sub = item.sub
  #  query = item.query


# gui()

if __name__ == "__main__":
    sys.exit(main())
