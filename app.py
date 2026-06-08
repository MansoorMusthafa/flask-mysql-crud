from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", "4000"))
}

def get_conn():
    return mysql.connector.connect(**db_config)

@app.route("/")
def index():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close(); conn.close()
    return render_template("index.html", users=users)

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO users(name,email,phone) VALUES(%s,%s,%s)",
                    (request.form["name"], request.form["email"], request.form["phone"]))
        conn.commit()
        cur.close(); conn.close()
        return redirect(url_for("index"))
    return render_template("add_user.html")

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    if request.method == "POST":
        cur2 = conn.cursor()
        cur2.execute("UPDATE users SET name=%s,email=%s,phone=%s WHERE id=%s",
                     (request.form["name"], request.form["email"], request.form["phone"], id))
        conn.commit()
        cur2.close()
        conn.close()
        return redirect(url_for("index"))
    cur.execute("SELECT * FROM users WHERE id=%s", (id,))
    user = cur.fetchone()
    cur.close(); conn.close()
    return render_template("edit_user.html", user=user)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id,))
    conn.commit()
    cur.close(); conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
