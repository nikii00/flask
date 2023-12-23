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


@app.route("/job", methods=["GET"])
def get_customers():
    data = data_fetch("""select * from jobs""")
    return make_response(jsonify(data), 200)


@app.route("/job/<int:id>", methods=["GET"])
def get_customer_by_id(id):
    data = data_fetch("""SELECT * FROM jobs where job_id = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/job", methods=["POST"])
def add_customerr():
    cur = mysql.connection.cursor()
    info = request.get_json()
    customer_id = info["customer_id"]
    start = info["date_job_started"]
    complete = info["date_job_completed"]
    details = info["other_details"]
    cur.execute(
        """ INSERT INTO jobs (customer_id, date_job_started,date_job_completed,other_details) VALUE (%s, %s, %s, %s)""",
        (customer_id,start,complete,details),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Job added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/job/<int:id>", methods=["PUT"])
def update_cutomer(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    customer_id = info["customer_id"]
    start = info["date_job_started"]
    complete = info["date_job_completed"]
    details = info["other_details"]
    cur.execute(
        """ UPDATE jobs SET customer_id = %s, date_job_started = %s,date_job_completed = %s,other_details = %s WHERE job_id = %s """,
        (customer_id,start,complete,details, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Job updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/job/<int:id>", methods=["DELETE"])
def delete_cutomer(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM jobs where job_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Job deleted successfully", "rows_affected": rows_affected}
        ), 
        200,
    )

@app.route("/job/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)

if __name__ == "__main__":
    app.run(debug=True)