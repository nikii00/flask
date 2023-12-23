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


@app.route("/items", methods=["GET"])
def get_customers():
    data = data_fetch("""select * from invoice_line_items""")
    return make_response(jsonify(data), 200)


@app.route("/items/<int:id>", methods=["GET"])
def get_customer_by_id(id):
    data = data_fetch("""SELECT * FROM invoice_line_items where invoice_number = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/items", methods=["POST"])
def add_customerr():
    cur = mysql.connection.cursor()
    info = request.get_json()
    order_id = info["order_item_id"]
    task = info["task_name"]
    quantity = info["quantity"]
    cost = info["cost"]
    details = info["other_details"]
    cur.execute(
        """ INSERT INTO invoice_line_items (order_item_id, task_name,quantity,cost,other_details) VALUE (%s, %s, %s, %s, %s)""",
        (order_id, task,quantity,cost,details),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Customer added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/items/<int:id>", methods=["PUT"])
def update_cutomer(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    order_id = info["order_item_id"]
    task = info["task_name"]
    quantity = info["quantity"]
    cost = info["cost"]
    details = info["other_details"]
    cur.execute(
        """ UPDATE invoice_line_items SET order_item_id = %s, task_name = %s,quantity = %s,cost = %s,other_details = %s WHERE invoice_number = %s """,
        (order_id, task,quantity,cost,details, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Customer updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/items/<int:id>", methods=["DELETE"])
def delete_cutomer(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM invoice_line_items where invoice_number = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Customer deleted successfully", "rows_affected": rows_affected}
        ), 
        200,
    )

@app.route("/items/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)

if __name__ == "__main__":
    app.run(debug=True)
