
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file, flash, make_response, Response 
import secrets,pypyodbc,dbutil
app = Flask(__name__)
#app.secret_key "your_secret_key" # Replace with a secure secret key
secret = secrets.token_urlsafe (32)
# app.secret_key = secret
#app.jinja_env.auto_reload = True

#app.config['TEMPLATES_AUTO_RELOAD'] = True # Reload templates when they are changed #app.config['SEND_FILE_MAX_AGE_DEFAULT'] 60 # Cache control max age in seconds 




@app.route("/home", methods=["GET"])
def home():
    connect_to_db()
    stage_id = 1
    remarks = "test"
    username = "testuser"
    current_user = "testuser"
    print("heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    # log_id = dbutil.insert_log(stage_id, "Returned", "Submited", remarks, username) 
    return render_template("home.html", current_user=current_user)

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
            cursor = conn.cursor()
            a = cursor.execute("SELECT * FROM abc")
            print(a.fetchall())

            return conn
        except Exception as ex:
            print(f'Error connection to database in attempt {i}: {ex}')
            if i >= MAX_ATTEMPTS:
                raise Exception('Error connecting to database',ex)
            else:
                i += 1

if __name__ == "__main__":
    app.run(debug=True)

