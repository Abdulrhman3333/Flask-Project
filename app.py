from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'aramco'

mysql = MySQL(app)


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM rdc")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', rdcData=data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        # division = request.form['division']
        # tech = request.form['tech']
        # dep = request.form['dep']
        # site = request.form['site']
        # month = request.form['month']
        # year = request.form['year']

        id_data = request.get_json()['id']
        # date = request.get_json()['date']
        division = request.get_json()['division']
        tech = request.get_json()['tech']
        dep = request.get_json()['dep']
        site = request.get_json()['site']
        month = request.get_json()['month']
        year = request.get_json()['year']
        is_checked = request.get_json()['is_checked']
        cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO rdc (date, division, tech,dep, site, month, year, is_checked) VALUES (NOW(), '%s', '%s', '%s', '%s', '%s', '%s','no')", (division, tech, dep, site, month, year))
        # cur.execute(''' INSERT INTO rdc VALUES(%s,%s) ''',(division,tech))
        cur.execute(''' INSERT INTO rdc VALUES(%s,NOW(),%s,%s,%s,%s,%s,%s,"no") ''',(id_data,division,tech,dep,site,month,year))

        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM rdc WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        # print("Header info: ", request.headers['Content-Type'])
        flash("Data Updated Successfully")
        # id_data = request.get_json()['id']
        # # date = request.get_json()['date']
        # division = request.get_json()['division']
        # tech = request.get_json()['tech']
        # dep = request.get_json()['dep']
        # site = request.get_json()['site']
        # month = request.get_json()['month']
        # year = request.get_json()['year']
        # is_checked = request.get_json()['is_checked']
        # ===============================================================
        id_data  = request.form['id']
        date = request.form['date']
        division = request.form['division']
        tech = request.form['tech']
        dep = request.form['dep']
        site = request.form['site']
        month = request.form['month']
        year = request.form['year']
        is_checked = request.form['is_checked']
        

        cur = mysql.connection.cursor()
        # cur.execute("""UPDATE rdc SET month=(%s)""", [month])
        # cur.execute("""UPDATE rdc SET month={}""".format(month))
        try:
            # cur.execute("UPDATE rdc SET dep=%s, site=%s WHERE id=%s", (dep,site,id_data))
            cur.execute("""UPDATE rdc SET division=%s,tech=%s, dep=%s, site=%s,month=%s, year=%s, is_checked=%s 
                    WHERE id=%s """, (division,tech,dep,site,month,year,is_checked,id_data))
            mysql.connection.commit()
        except:
            print("eroooorrrrr rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")

        return redirect(url_for('Index'))



if __name__ == "__main__":
    app.run(host='localhost', port=5000,debug=True)
