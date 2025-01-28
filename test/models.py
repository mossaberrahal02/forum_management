from pydantic import BaseModel
import sqlite3

# Modèles Pydantic pour la validation des données
class UtilisateurCreate(BaseModel):
    nom: str
    email: str

class UtilisateurResponse(UtilisateurCreate):
    id: int

class CategorieCreate(BaseModel):
    nom: str

class CategorieResponse(CategorieCreate):
    id: int

class PostCreate(BaseModel):
    titre: str
    contenu: str
    utilisateur_id: int
    categorie_id: int

class PostResponse(PostCreate):
    id: int

class CommentaireCreate(BaseModel):
    contenu: str
    utilisateur_id: int
    post_id: int

class CommentaireResponse(CommentaireCreate):
    id: int

def create_tables(conn: sqlite3.Connection):
    cursor = conn.cursor()
    print("creating utilisateurs table .....  ")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')

    print("creating categories table .....  ")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL UNIQUE
        )
    ''')

    print("creating posts table .....  ")
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

    print("creating commentaire table .....  ")
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

def get_db():
    conn = sqlite3.connect("forum.db")
    try:
        print("from get_db()  yield conn")
        yield conn
    finally:
        print("from get_db() conn.close()")
        conn.close()