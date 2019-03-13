import os

import vertica_python


def connect_to_db():
    conn_info = {'host': '192.168.154.129',
                 'port': 5433,
                 'user': 'dbadmin',
                 'password': 'password',
                 'database': 'VMart',
                 'ssl': False,
                 'connection_timeout': 5}

    connection = vertica_python.connect(**conn_info)
    return connection


def insert(connection, filename):
    cur = connection.cursor()
    with open(filename, "rb") as fs:
        my_file = fs.read().decode('utf-8')
        cur.copy("COPY big_data_system_design FROM STDIN parser fjsonparser()", my_file)
        connection.commit()


def select(connection):
    cur = connection.cursor()
    cur.execute("SELECT MAPTOSTRING(__raw__) FROM big_data_system_design")
    for row in cur.iterate():
        dict = dict(row)

    connection.close()


def main():
    conn = connect_to_db()
    # for json file:
    path = os.getcwd()
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)) and 'partij-' in i:
            insert(conn, i)
    select(conn)


if __name__ == '__main__':
    main()
