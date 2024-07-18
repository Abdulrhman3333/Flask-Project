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
        div = request.form['div']
        tech = request.form['tech']
        dep = request.form['dep']
        site = request.form['site']
        month = request.form['month']
        year = request.form['year']
        cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO rdc (date, div, tech,dep, site, month, year, is_checked) VALUES (NOW(), '%s', '%s', '%s', '%s', '%s', '%s','no')", (div, tech, dep, site, month, year))
        # cur.execute(''' INSERT INTO rdc VALUES(%s,%s) ''',(div,tech))
        cur.execute(''' INSERT INTO rdc VALUES(Null,NOW(),%s,%s,%s,%s,%s,%s,"no") ''',(div,tech,dep,site,month,year))

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
        id_data = request.form['id']
        date = request.form['date']
        div = request.form['div']
        tech = request.form['tech']
        dep = request.form['dep']
        month = request.form['month']
        year = request.form['year']
        is_checked = request.form['is_checked']
        hfjkshdkjfh

        cur = mysql.connection.cursor()
        cur.execute('''UPDATE rdc SET div=%s
                    WHERE id=%s ''', (div,id_data))
        # cur.execute('''UPDATE rdc SET date=%s, div=%s,tech=%s, dep=%s, site=%s,month=%s, year=%s, is_checked=%s 
        #             WHERE id=%s ''', (date,div,tech,dep,site,month,year,is_checked,id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))




if __name__ == "__main__":
    app.run(host='localhost', port=5000,debug=True)
