import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# configs
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


# login route
@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing Email or Password", 401

    # check db for user/pass
    cursor = mysql.connection.cursor()
    result = cursor.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username)
    )

    # result returns an array of SQL rows
    # (result > 0) means the row exists
    if result > 0:
        user_row = cursor.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid Email or Password", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "Invalid Email or Password", 401

def createJWT():