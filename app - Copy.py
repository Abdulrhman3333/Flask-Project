from werkzeug.utils import redirect
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file, flash, make_response, Response 
import secrets,pypyodbc,dbutil
import datetime


####################################################################
####################################################################

def connect_to_db():
    MAX_ATTEMPTS = 3
    i = 1
    while True:
        try:
            DRIVER_NAME = 'SQL SERVER'
            SERVER_NAME = 'LAPTOP-T6NQ8T6P\SQLEXPRESS'
            DATABASE_NAME = 'aramco'
            # connection_string = r'Driver={ODBC Driver 17 for SQL Server};Server=\LAPTOP-T6NQ8T6P\SQLEXPRESS;Database=aramco;Truested_Connection=Yes;TrustServerCertificate=Yes'
            connection_string = f"""
            DRIVER={{{DRIVER_NAME}}};
            SERVER={SERVER_NAME};
            DATABASE={DATABASE_NAME};
            Trust_Connection=yes;
            """
            conn = pypyodbc.connect(connection_string)
            cur = conn.cursor()
            # cur.execute("SELECT * FROM abc")
            # print(conn)
            return cur
        except Exception as ex:
            print(f'Error connection to database in attempt {i}: {ex}')
            if i >= MAX_ATTEMPTS:
                raise Exception('Error connecting to database',ex)
            else:
                i += 1
####################################################################
####################################################################



app = Flask(__name__)
# secret = secrets.token_urlsafe (32)
secret = "abc"

app.secret_key = secret

# load the main page
@app.route('/')
def Index():
    cur = connect_to_db()
    cur.execute("SELECT * FROM rdc9")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', rdcData=data)
    # return render_template('powerBi.html', rdcData=data)

@app.route('/powerBi')
def powerBi():
    return render_template('powerBi.html')

# chacking page to accept and reject requests
@app.route('/checking')
def checking():
    cur = connect_to_db()
    cur.execute("SELECT * FROM rdc9") # rdc9 table which has all the inforamtion
    data = cur.fetchall() # get the data from database
    cur.close()
    return render_template('checking.html', rdcData=data) # rdcData will be sent to frontend


@app.route('/submit', methods = ['POST']) # this route is the only route coming from PDF, other routes related with the webiste itself
def submit():
    if request.method == "POST": 
        data = request.form
        arrOb = [] # store the in coming data as objects and store it in array as per row in pdf
        ob = {
            'div': data.get('div'), # division name
            'tech': "", # technology name
            'dep': "", # number of deployments
            'site': "" # site where take place
        }

        # for each row ( 15 rows ) get the exact value and combine it in one object
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
            arrOb.append(ob) # add the object to the array
            ob = { # clear the object to get new values
                'div': data.get('div'),
                'tech': "",
                'dep': "",
                'site': ""
            }

        filtered_data = [entry for entry in arrOb if entry['tech'] != ''] # remove all objects the have no dep number from the array

        cur = connect_to_db() # connect to db
        for i in filtered_data:
            division = i['div']
            tech = i['tech']
            dep = i['dep']
            site = i['site']
            month = datetime.datetime.now().month
            year = datetime.datetime.now().year
            current_date = datetime.datetime.now()
            cur.execute('INSERT INTO aramco.dbo.rdc9 (date,division,tech,dep,site,month,year,is_checked,value,tpv) VALUES(?,?,?,?,?,?,?,?,?,?)',
            (current_date,division,tech,dep,site,month,year,'no',0,0)) 
        cur.commit()    
        cur.close()
        flash("Data Inserted Successfully")
        return redirect(url_for('Index'))
    
@app.route('/insert', methods = ['POST']) # this insert which come from the website 
def insert():
    if request.method == "POST":
        current_date = datetime.datetime.now()
        division = request.form['division']
        tech = request.form['tech']
        dep = request.form['dep']
        site = request.form['site']
        month = request.form['month']
        year = request.form['year']
        value = request.form['value']   
        tpv = int(dep) * int(value)
        cur = connect_to_db()
        cur.execute('INSERT INTO aramco.dbo.rdc9 (date,division,tech,dep,site,month,year,is_checked,value,tpv) VALUES(?,?,?,?,?,?,?,?,?,?)',
                    (current_date,division,tech,dep,site,month,year,'no',value,tpv)) 
        cur.commit()
        cur.close()
        flash("Data Inserted Successfully")
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = connect_to_db()
    cur.execute("DELETE FROM rdc9 WHERE id=?", (id_data,))
    cur.commit()
    cur.close()
    return redirect(url_for('Index'))

@app.route('/checking/accept/<string:id_data>', methods = ['GET'])
def accept(id_data):
    cur = connect_to_db()
    cur.execute("UPDATE rdc9 SET `is_checked`='yes' WHERE id = ?",[id_data])
    cur.commit()
    cur.close()
    flash("Record Has Been accepted Successfully")
    return redirect(url_for('checking'))

# @app.route('/checking/reject/<string:id_data>', methods = ['GET'])
# def reject(id_data):
#     cur = connect_to_db()
#     cur.execute("SELECT * FROM rdc9 WHERE id = ?",[id_data])
#     data = cur.fetchone()
#     id = data[0]
#     date = data[1]
#     division = data[2]
#     tech = data[3]
#     dep = data[4]
#     site = data[5]
#     month = data[6]
#     year = data[7]
#     is_checked = data[8]
#     value = data[9]
#     tpv = data[10]
#     cur.execute(''' INSERT INTO rejected1 VALUES(?,?,?,?,?,?,?,?,?,?,?) ''',(id,date,division,tech,dep,site,month,year,is_checked,value,tpv))
#     cur.execute("DELETE FROM rdc9 WHERE id = ?",(id,))
#     cur.execute("DELETE FROM rdc9 WHERE id =39")
#     cur.close()

#     flash("Record Has Been accepted Successfully")
#     # mysql.connection.commit()
#     return redirect(url_for('checking'))


# @app.route('/checking/rejected/', methods = ['GET'])
# def rejected():
#     cur = connect_to_db()
#     cur.execute("SELECT * FROM rejected1")
#     data = cur.fetchall()
#     cur.close()

#     return render_template('rejected.html', rdcData=data)

# @app.route('/checking/retrieve/<string:id_data>', methods = ['GET'])
# def retrieve(id_data):
#     cur = connect_to_db()

@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
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

        cur = connect_to_db()
        try:
            cur.execute("""UPDATE aramco.dbo.rdc9 SET division=?,tech=?, dep=?, site=?,month=?, year=?, is_checked=? , value=?, tpv=?  
                    WHERE id=? """, (division,tech,dep,site,month,year,is_checked,value,tpv,id_data))
            cur.commit()
            cur.close()
            flash("Data Updated Successfully")
        except:
            print("error")

        return redirect(url_for('Index'))



if __name__ == "__main__":
    app.run(host='localhost', port=5000,debug=True)
