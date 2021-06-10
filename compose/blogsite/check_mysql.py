import sys
from MySQLdb import connect
from MySQLdb._exceptions import MySQLError

try:
    connect(
        host='mysql',
        port=3306,
        user='root',
        passwd='root',
        db='blogsite',
    )
except MySQLError:
    sys.exit(1)
sys.exit(0)
