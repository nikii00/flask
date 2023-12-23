from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "customer"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/task", methods=["GET"])
def get_customers():
    data = data_fetch("""select * from standard_tasks""")
    return make_response(jsonify(data), 200)


@app.route("/task/<int:id>", methods=["GET"])
def get_customer_by_id(id):
    data = data_fetch("""SELECT * FROM standard_tasks where task_id = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/task", methods=["POST"])
def add_customerr():
    cur = mysql.connection.cursor()
    info = request.get_json()
    name = info["task_name"]
    price = info["task_price"]
    details = info["task_description"]
    cur.execute(
        """ INSERT INTO standard_tasks (task_name, task_price,task_description) VALUE (%s,%s, %s)""",
        (name,price,details),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Task added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/task/<int:id>", methods=["PUT"])
def update_cutomer(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    info = request.get_json()
    name = info["task_name"]
    price = info["task_price"]
    details = info["task_description"]
    cur.execute(
        """ UPDATE standard_tasks SET task_name = %s, task_price = %s,task_description = %s WHERE task_id = %s """,
        (name,price,details, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Task updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/task/<int:id>", methods=["DELETE"])
def delete_cutomer(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM standard_tasks where task_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Task deleted successfully", "rows_affected": rows_affected}
        ), 
        200,
    )

@app.route("/task/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)

if __name__ == "__main__":
    app.run(debug=True)
