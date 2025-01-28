from fastapi import FastAPI, HTTPException, Depends
import sqlite3

# Initialize FastAPI app
app = FastAPI()

# Database connection
DATABASE = "example.db"

# Create a table if it doesn't exist
def create_tables():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # cursor.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS items (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         name TEXT NOT NULL,
        #         description TEXT
        #     )
        #     """
        # )
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')

        # cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS categories (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         nom TEXT NOT NULL UNIQUE
        #     )
        # ''')

        # cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS posts (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         titre TEXT NOT NULL,
        #         contenu TEXT NOT NULL,
        #         utilisateur_id INTEGER,
        #         categorie_id INTEGER,
        #         FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id),
        #         FOREIGN KEY (categorie_id) REFERENCES categories (id)
        #     )
        # ''')

        # cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS commentaires (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         contenu TEXT NOT NULL,
        #         utilisateur_id INTEGER,
        #         post_id INTEGER,
        #         FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id),
        #         FOREIGN KEY (post_id) REFERENCES posts (id)
        #     )
        # ''')
        conn.commit()

# Dependency to get the database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()

# Pydantic model for request/response validation (optional but recommended)
# from pydantic import BaseModel

# class Item(BaseModel):
#     name: str
#     description: str | None = None

# class ItemResponse(Item):
#     id: int

from pydantic import BaseModel

class Utilisateur(BaseModel):
    id: int
    nom: str
    email: str

# class Categorie(BaseModel):
#     nom: str

# class Post(BaseModel):
#     titre: str
#     contenu: str
#     utilisateur_id: int
#     categorie_id: int

# class Commentaire(BaseModel):
#     contenu: str
#     utilisateur_id: int
#     post_id: int



# Create an item
@app.post("/utilisateur/", response_model=Utilisateur)
def create_utilisateur(utilisateur: Utilisateur, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO utilisateurs (nom, email) VALUES (?, ?)",
        (utilisateur.nom, utilisateur.email),
    )
    conn.commit()
    utilisateur_id = cursor.lastrowid
    return {**utilisateur.dict(), "id": utilisateur_id}

# Read all utilisateurs
@app.get("/utilisateurs/", response_model=list[Utilisateur])
def read_utilisateurs(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, email FROM utilisateurs")
    utilisateurs = cursor.fetchall()
    return [{"id": row[0], "nom": row[1], "email": row[2]} for row in utilisateurs]

# Read a single utilisateur by ID
@app.get("/utilisateur/{utilisateur_id}", response_model=Utilisateur)
def read_utilisateur(utilisateur_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, email FROM utilisateurs WHERE id = ?", (utilisateur_id,))
    utilisateur = cursor.fetchone()
    if utilisateur is None:
        raise HTTPException(status_code=404, detail="utilisateur not found")
    return {"id": utilisateur[0], "name": utilisateur[1], "email": utilisateur[2]}

# Update an utilisateur by ID
@app.put("/utilisateur/{utilisateur_id}", response_model=Utilisateur)
def update_item(utilisateur_id: int, utilisateur: Utilisateur, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE utilisateurs SET nom = ?, email = ? WHERE id = ?",
        (utilisateur.nom, utilisateur.email, utilisateur_id),
    )
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {**utilisateur.dict(), "id": utilisateur_id}

# Delete an item by ID
@app.delete("/utilisateurs/{utilisateur_id}")
def delete_item(utilisateur_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM utilisateurs WHERE id = ?", (utilisateur_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="utilisateur not found")
    return {"message": "utilisateur deleted"}

# Run the app
if __name__ == "__main__":
    create_tables()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)