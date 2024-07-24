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




@app.route('/checking')
def checking():
    # if request.method == "POST":
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM rdc")
    data = cur.fetchall()
    cur.close()

    return render_template('checking.html', rdcData=data)


@app.route('/submit', methods = ['POST'])
def submit():
    if request.method == "POST":
        data = request.form

        arrOb = []
        ob = {
            'div': data.get('div'),
            'tech': "",
            'dep': "",
            'site': "",
            'month': data.get('MonthRow1'),
        }

        for i in range(1, 15):
            for dep, dv in data.items():
                if dep == "Number of Deployments{}".format(i):
                    ob['dep'] = dv
                    for site, sv in data.items():
                        if site == "Sites{}".format(i):
                            ob['site'] = sv
                            for tech, tv in data.items():
                                if tech == "Technology{}".format(i):
                                    ob['tech'] = tv
                                    break
            arrOb.append(ob)
            ob = {
                'div': data.get('div'),
                'tech': "",
                'dep': "",
                'site': "",
                'month': data.get('MonthRow1'),
            }

        filtered_data = [entry for entry in arrOb if entry['tech'] != '']

        cursor = mysql.connection.cursor()
        for i in filtered_data:
            div = i['div']
            tech = i['tech']
            dep = i['dep']
            site = i['site']
            month = i['month']
            
            cursor.execute(''' INSERT INTO rdc VALUES(null,NOW(),%s,%s,%s,%s,%s,YEAR(CURRENT_DATE()),"no",0,0) ''',(div,tech,dep,site,month))
        mysql.connection.commit()
        cursor.close()
        flash("Data Inserted Successfully")
        return redirect(url_for('Index'))
    
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        division = request.form['division']
        tech = request.form['tech']
        dep = request.form['dep']
        site = request.form['site']
        month = request.form['month']
        year = request.form['year']
        value = request.form['value']
        tpv = int(dep) * int(value)

        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO rdc VALUES(null,NOW(),%s,%s,%s,%s,%s,%s,"no",%s,%s) ''',(division,tech,dep,site,month,year,value,tpv))
        mysql.connection.commit()
        cursor.close()
        flash("Data Inserted Successfully")
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM rdc WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))

@app.route('/checking/accept/<string:id_data>', methods = ['GET'])
def accept(id_data):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE rdc SET `is_checked`='yes' WHERE id = %s",[id_data])
    flash("Record Has Been accepted Successfully")
    mysql.connection.commit()
    return redirect(url_for('checking'))

# @app.route('/checking/reject/<string:id_data>', methods = ['GET'])
# def accept(id_data):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM rdc WHERE id = %s",[id_data])
#     data = cur.fetchall()
#     division = data.get('division')
#     cur.execute(''' INSERT INTO rejected VALUES(null,NOW(),%s,%s,%s,%s,%s,"2024","no") ''',(division,tech,dep,site,month))
#     cur.close()

#     flash("Record Has Been accepted Successfully")
#     mysql.connection.commit()
#     return redirect(url_for('checking'))



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
        value = request.form['value']
        tpv = int(dep) * int(value)
        

        cur = mysql.connection.cursor()
        # cur.execute("""UPDATE rdc SET month=(%s)""", [month])
        # cur.execute("""UPDATE rdc SET month={}""".format(month))
        try:
            # cur.execute("UPDATE rdc SET dep=%s, site=%s WHERE id=%s", (dep,site,id_data))
            cur.execute("""UPDATE rdc SET division=%s,tech=%s, dep=%s, site=%s,month=%s, year=%s, is_checked=%s , value=%s, tpv=%s  
                    WHERE id=%s """, (division,tech,dep,site,month,year,is_checked,value,tpv,id_data))
            mysql.connection.commit()
        except:
            print("error")

        return redirect(url_for('Index'))



if __name__ == "__main__":
    app.run(host='localhost', port=5000,debug=True)
