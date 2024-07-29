from werkzeug.utils import redirect
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file, flash, make_response, Response 
import secrets,pypyodbc,dbutil
import datetime
from db import connect_to_db


##########################################
# things need to be done:
# change the db is_checked to status, and on the code
#
#
##########################################



app = Flask(__name__)
# secret = secrets.token_urlsafe (32)
secret = "abc"

app.secret_key = secret

#############################################################
# main page to show only the approved status
@app.route('/')
def Index():
    cur = connect_to_db()
    cur.execute("SELECT * FROM rdc9 WHERE is_checked =?",('APPROVED',))
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', rdcData=data)

# insert from the website manually
@app.route('/insert', methods = ['POST']) # this insert which come from the website 
def insert():
    if request.method == "POST":
        current_date = datetime.datetime.now()
        division = request.form['division']
        tech = request.form['tech']
        dep = request.form['dep']
        site = request.form['site']
        month = datetime.datetime.now().strftime("%B")
        year = datetime.datetime.now().year
        value = request.form['value']   
        tpv = int(dep) * int(value)
        cur = connect_to_db()
        cur.execute('INSERT INTO rdc9 (date,division,tech,dep,site,month,year,is_checked,value,tpv) VALUES(?,?,?,?,?,?,?,?,?,?)',
                    (current_date,division,tech,dep,site,month,year,'APPROVED',value,tpv)) 
        cur.commit()
        cur.close()
        flash("Data Inserted Successfully")
        return redirect(url_for('Index'))
    
# update from main page
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
            cur.execute("""UPDATE rdc9 SET division=?,tech=?, dep=?, site=?,month=?, year=?, is_checked=? , value=?, tpv=?  
                    WHERE id=? """, (division,tech,dep,site,month,year,is_checked,value,tpv,id_data))
            cur.commit()
            cur.close()
            flash("Data Updated Successfully")
        except:
            print("error")

        return redirect(url_for('Index'))

# delete from main page and will transfer it to rejected page, it will be as rejected
@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = connect_to_db()
    cur.execute("UPDATE rdc9 SET is_checked='REJECTED' WHERE id = ?",[id_data])
    cur.commit()
    cur.close()
    return redirect(url_for('Index'))
# main page to show only the approved status
#############################################################


#############################################################
# intermediate route to accept and reject requests
@app.route('/intermediate')
def intermediate():
    cur = connect_to_db()
    cur.execute("SELECT * FROM rdc9 WHERE is_checked =?",('WAITING',)) # rdc9 table which has all the inforamtion
    data = cur.fetchall() # get the data from database
    cur.commit()
    cur.close()
    return render_template('intermediate.html', rdcData=data) # rdcData will be sent to frontend

@app.route('/intermediate/accept/<string:id_data>', methods = ['GET'])
def accept(id_data):
    cur = connect_to_db()
    cur.execute("UPDATE rdc9 SET is_checked='APPROVED' WHERE id = ?",[id_data])
    cur.commit()
    cur.close()
    flash("Record Has Been accepted Successfully")
    return redirect(url_for('intermediate'))

@app.route('/intermediate/reject/<string:id_data>', methods = ['GET'])
def reject(id_data):
    cur = connect_to_db()
    cur.execute("UPDATE rdc9 SET is_checked='REJECTED' WHERE id = ?",[id_data])
    cur.commit()
    cur.close()
    flash("Record Has Been rejected Successfully")
    # mysql.connection.commit()
    return redirect(url_for('intermediate'))
# intermediate route to accept and reject requests
#############################################################

    
#############################################################
# rejected route
@app.route('/rejected/', methods = ['GET'])
def rejected():
    cur = connect_to_db()
    cur.execute("SELECT * FROM rdc9 WHERE is_checked =?",('REJECTED',))
    data = cur.fetchall()
    cur.close()
    return render_template('rejected.html', rdcData=data)

@app.route('/rejected/restore/<string:id_data>', methods = ['GET'])
def restore(id_data):
    cur = connect_to_db()
    cur.execute("UPDATE rdc9 SET is_checked='APPROVED' WHERE id = ?",[id_data])
    cur.commit()
    cur.close()
    flash("Record Has Been rejected Successfully")
    return redirect(url_for('rejected'))

@app.route('/rejected/remove/<string:id_data>', methods = ['GET'])
def remove(id_data):
    cur = connect_to_db()
    cur.execute("DELETE FROM rdc9 WHERE id = ?",[id_data])
    cur.commit()
    cur.close()
    flash("Record Has Been rejected Successfully")
    return redirect(url_for('rejected'))

@app.route('/rejected/removeall', methods = ['GET'])
def removeall():
    cur = connect_to_db()
    cur.execute("DELETE FROM rdc9 WHERE is_checked = ?",('REJECTED',))
    cur.commit()
    cur.close()
    flash("All Records have Been removed forever Successfully")
    return redirect(url_for('rejected'))

# rejected route
#############################################################







##################################################
# insert from pdf
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
            month = datetime.datetime.now().strftime("%B")
            year = datetime.datetime.now().year
            current_date = datetime.datetime.now()
            cur.execute('INSERT INTO rdc9 (date,division,tech,dep,site,month,year,is_checked,value,tpv) VALUES(?,?,?,?,?,?,?,?,?,?)',
            (current_date,division,tech,dep,site,month,year,'WAITING',0,0)) 
        cur.commit()    
        cur.close()
        flash("Data Inserted Successfully")
        return redirect(url_for('Index'))
# insert from pdf
###############################################

##################################
# power bi page
@app.route('/powerBi')
def powerBi():
    return render_template('powerBi.html')
# power bi page
##################################


if __name__ == "__main__":
    app.run(host='localhost', port=5000,debug=True)
