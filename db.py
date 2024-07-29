import secrets,pypyodbc,dbutil

def connect_to_db():
    MAX_ATTEMPTS = 3
    i = 1
    while True:
        try:
            DRIVER_NAME = 'SQL SERVER'
            SERVER_NAME = 'LAPTOP-T6NQ8T6P\SQLEXPRESS'
            DATABASE_NAME = 'aramco'
            connection_string = f"""
            DRIVER={{{DRIVER_NAME}}};
            SERVER={SERVER_NAME};
            DATABASE={DATABASE_NAME};
            Trust_Connection=yes;
            """
            conn = pypyodbc.connect(connection_string)
            cur = conn.cursor()
            return cur
        except Exception as ex:
            print(f'Error connection to database in attempt {i}: {ex}')
            if i >= MAX_ATTEMPTS:
                raise Exception('Error connecting to database',ex)
            else:
                i += 1