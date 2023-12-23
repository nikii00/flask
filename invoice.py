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


@app.route("/invoice", methods=["GET"])
def get_customers():
    data = data_fetch("""select * from invoices""")
    return make_response(jsonify(data), 200)


@app.route("/invoice/<int:id>", methods=["GET"])
def get_customer_by_id(id):
    data = data_fetch("""SELECT * FROM invoices where invoice_number = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/invoice", methods=["POST"])
def add_customerr():
    cur = mysql.connection.cursor()
    info = request.get_json()
    job_id = info["job_id"]
    date = info["invoice_date"]
    cost = info["total_cost"]
    details = info["other_details"]
    cur.execute(
        """ INSERT INTO invoices (job_id, invoice_date,total_cost,other_details) VALUE (%s, %s, %s, %s)""",
        (job_id,date,cost,details),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Invoice added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/invoice/<int:id>", methods=["PUT"])
def update_cutomer(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    job_id = info["job_id"]
    date = info["invoice_date"]
    cost = info["total_cost"]
    details = info["other_details"]
    cur.execute(
        """ UPDATE invoices SET job_id = %s, invoice_date = %s,total_cost = %s,other_details = %s WHERE invoice_number = %s """,
        (job_id,date,cost,details, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Invoice updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/invoice/<int:id>", methods=["DELETE"])
def delete_cutomer(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM invoices where invoice_number = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Invoice deleted successfully", "rows_affected": rows_affected}
        ), 
        200,
    )

@app.route("/invoice/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)

@app.route("/invoice/search", methods=["GET"])
def search_invoice():
    # Get search parameters from the query string
    job_id = request.args.get('job_id')

    # Build the SQL query dynamically based on the provided parameters
    query = "SELECT * FROM invoices WHERE 1=1"
    if job_id:
        query += f" AND job_id = {job_id}"

    data = data_fetch(query)
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)