from sqlite3 import Connection

def create_tables(conn: Connection):
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            contenu TEXT NOT NULL,
            utilisateur_id INTEGER,
            categorie_id INTEGER,
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id),
            FOREIGN KEY (categorie_id) REFERENCES categories (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commentaires (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenu TEXT NOT NULL,
            utilisateur_id INTEGER,
            post_id INTEGER,
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id),
            FOREIGN KEY (post_id) REFERENCES posts (id)
        )
    ''')
    
    conn.commit()