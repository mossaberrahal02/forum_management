from sqlite3 import Connection

def create_user(conn: Connection, user):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO utilisateurs (name, email)
        VALUES (?, ?)
    ''', (user.name, user.email))
    conn.commit()
    return cursor.lastrowid

def get_user(conn: Connection, user_id: int):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM utilisateurs WHERE id = ?', (user_id,))
    return cursor.fetchone()

def update_user(conn: Connection, user_id: int, user):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE utilisateurs
        SET name = ?, email = ?
        WHERE id = ?
    ''', (user.name, user.email, user_id))
    conn.commit()

def delete_user(conn: Connection, user_id: int):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM utilisateurs WHERE id = ?', (user_id,))
    conn.commit()