import sys

sys.path.append('..')

from main import app
from flask_mysqldb import MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'umar'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'testing'

mysql = MySQL(app)


def getResource(table=None, field=None, join=None, where=None, group=None, order=None, limit=None):
    if table is None:
        return False
    else:
        query = "SELECT * FROM " + table
    if join is not None:
        for j in join:
            query += " JOIN " + j
    if where is not None:
        key, value = zip(*where.items())
        query += " WHERE " + " AND ".join(["{} = %s".format(k) for k in key])
    if field is not None:
        query = query.replace('*', ", ".join(field))
    if group is not None:
        query += " GROUP BY " + ", ".join(group)
    if order is not None:
        query += " ORDER BY " + ", ".join(order)
    if limit is not None:
        query += " LIMIT " + str(limit)
    cur = mysql.connection.cursor()
    try:
        if field is None:
          cur.execute(query)
        else:
          cur.execute(query, tuple(value))
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        cur.close()
        print("Error:", e)
        return False

def postResource(table=None, field=None):
    if table is None:
        return False
    else:
        query = "INSERT INTO " + table
        if field is not None:
            key, value = zip(*field.items())
            query += " (" + ", ".join(key) + ") VALUES (" + ", ".join(["%s" for k in key]) + ")"

        cur = mysql.connection.cursor()
        try:
            cur.execute(query, tuple(value))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            mysql.connection.rollback()
            cur.close()
            print("Error:", e)
            return False

def putResource(table=None, field=None, id=None):
    if table is None or id is None:
        return False
    else:
        query = "UPDATE {} SET ".format(table)
        if field is not None:
            key, value = zip(*field.items())
            query += ", ".join(["{} = %s".format(k) for k in key])
        query += " WHERE id = %s"
        value = list(value)
        value.append(id['id'])
        
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, tuple(value))
            mysql.connection.commit()
            print(cur.rowcount)
            cur.close()
            return True
        except Exception as e:
            mysql.connection.rollback()
            cur.close()
            print("Error:", e)
            return False

def deleteResource(table=None, where=None):
    if table is None:
        return False
    else:
        query = "DELETE FROM " + table
        if where is not None:
            key, value = zip(*where.items())
            query += " WHERE " + " AND ".join(["{} = %s".format(k) for k in key])

        cur = mysql.connection.cursor()
        try:
            cur.execute(query, tuple(value))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            mysql.connection.rollback()
            cur.close()
            print("Error:", e)
            return False