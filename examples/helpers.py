import sqlite3


def get_access_token():
    '''gets the access token from the database'''
    CONN = sqlite3.connect('../DungeonBot/example_user.sqlite')
    # Create a Database cursor
    database = CONN.cursor()
    # Execute database search
    database.execute("SELECT * FROM account WHERE id = 'access_token'")
    #returns the access token
    # print(database.fetchone()[1])
    return database.fetchone()[1]