from fastapi import FastAPI, HTTPException, Depends
from models import (
    UtilisateurCreate, UtilisateurResponse,
    CategorieCreate, CategorieResponse,
    PostCreate, PostResponse,
    CommentaireCreate, CommentaireResponse,
    create_tables, get_db
)
import sqlite3

app = FastAPI()

# Créer les tables au démarrage de l'application
@app.on_event("startup")
def startup():
    with sqlite3.connect("forum.db") as conn:
        create_tables(conn)

#---------------------------------------------
# Endpoints pour Utilisateurs
@app.get("/utilisateurs/", response_model=list[UtilisateurResponse])
def list_utilisateurs(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, email FROM utilisateurs")
    utilisateurs = cursor.fetchall()
    return [{"id": u[0], "nom": u[1], "email": u[2]} for u in utilisateurs]

@app.get("/utilisateurs/by-name/{nom}", response_model=list[UtilisateurResponse])
def list_utilisateurs_by_name(nom: str, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, email FROM utilisateurs WHERE nom LIKE ?", (f"%{nom}%",))
    utilisateurs = cursor.fetchall()
    if not utilisateurs:
        raise HTTPException(status_code=404, detail="Aucun utilisateur correspondant trouvé")
    return [{"id": u[0], "nom": u[1], "email": u[2]} for u in utilisateurs]

@app.post("/utilisateurs/", response_model=UtilisateurResponse)
def create_utilisateur(utilisateur: UtilisateurCreate, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO utilisateurs (nom, email) VALUES (?, ?)",
        (utilisateur.nom, utilisateur.email),
    )
    conn.commit()
    utilisateur_id = cursor.lastrowid
    return {**utilisateur.dict(), "id": utilisateur_id}

@app.get("/utilisateurs/{utilisateur_id}", response_model=UtilisateurResponse)
def read_utilisateur(utilisateur_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, email FROM utilisateurs WHERE id = ?", (utilisateur_id,))
    utilisateur = cursor.fetchone()
    if utilisateur is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"id": utilisateur[0], "nom": utilisateur[1], "email": utilisateur[2]}

@app.put("/utilisateurs/{utilisateur_id}", response_model=UtilisateurResponse)
def update_utilisateur(utilisateur_id: int, utilisateur: UtilisateurCreate, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE utilisateurs SET nom = ?, email = ? WHERE id = ?",
        (utilisateur.nom, utilisateur.email, utilisateur_id)
    )
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {**utilisateur.dict(), "id": utilisateur_id}

@app.delete("/utilisateurs/{utilisateur_id}")
def delete_utilisateur(utilisateur_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM utilisateurs WHERE id = ?", (utilisateur_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"message": "Utilisateur supprimé avec succès"}
#---------------------------------------------





#---------------------------------------------

# Endpoints pour Catégories
@app.get("/categories/", response_model=list[CategorieResponse])
def list_categories(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM categories")
    categories = cursor.fetchall()
    return [{"id": c[0], "nom": c[1]} for c in categories]

@app.post("/categories/", response_model=CategorieResponse)
def create_categorie(categorie: CategorieCreate, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO categories (nom) VALUES (?)",
        (categorie.nom,),
    )
    conn.commit()
    categorie_id = cursor.lastrowid
    return {**categorie.dict(), "id": categorie_id}

@app.get("/categories/{categorie_id}", response_model=CategorieResponse)
def read_categorie(categorie_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM categories WHERE id = ?", (categorie_id,))
    categorie = cursor.fetchone()
    if categorie is None:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    return {"id": categorie[0], "nom": categorie[1]}


@app.put("/categories/{categorie_id}", response_model=CategorieResponse)
def update_categorie(categorie_id: int, categorie: CategorieCreate, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE categories SET nom = ? WHERE id = ?",
        (categorie.nom, categorie_id)
    )
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    return {**categorie.dict(), "id": categorie_id}

@app.delete("/categories/{categorie_id}")
def delete_categorie(categorie_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id = ?", (categorie_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    return {"message": "Catégorie supprimée avec succès"}
#---------------------------------------------















#---------------------------------------------

# Endpoints pour Posts
@app.get("/posts/", response_model=list[PostResponse])
def list_posts(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, titre, contenu, utilisateur_id, categorie_id FROM posts")
    posts = cursor.fetchall()
    return [
        {"id": p[0], "titre": p[1], "contenu": p[2], "utilisateur_id": p[3], "categorie_id": p[4]}
        for p in posts
    ]

@app.get("/posts/by-title/{titre}", response_model=list[PostResponse])
def list_posts_by_title(titre: str, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, titre, contenu, utilisateur_id, categorie_id FROM posts WHERE titre LIKE ?", (f"%{titre}%",))
    posts = cursor.fetchall()
    if not posts:
        raise HTTPException(status_code=404, detail="Aucun post correspondant trouvé")
    return [
        {"id": p[0], "titre": p[1], "contenu": p[2], "utilisateur_id": p[3], "categorie_id": p[4]}
        for p in posts
    ]

@app.post("/posts/", response_model=PostResponse)
def create_post(post: PostCreate, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO posts (titre, contenu, utilisateur_id, categorie_id) VALUES (?, ?, ?, ?)",
        (post.titre, post.contenu, post.utilisateur_id, post.categorie_id),
    )
    conn.commit()
    post_id = cursor.lastrowid
    return {**post.dict(), "id": post_id}

@app.get("/posts/{post_id}", response_model=PostResponse)
def read_post(post_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, titre, contenu, utilisateur_id, categorie_id FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=404, detail="Post non trouvé")
    return {"id": post[0], "titre": post[1], "contenu": post[2], "utilisateur_id": post[3], "categorie_id": post[4]}

@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostCreate, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE posts SET titre = ?, contenu = ?, utilisateur_id = ?, categorie_id = ? WHERE id = ?",
        (post.titre, post.contenu, post.utilisateur_id, post.categorie_id, post_id)
    )
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Post non trouvé")
    return {**post.dict(), "id": post_id}

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Post non trouvé")
    return {"message": "Post supprimé avec succès"}



#---------------------------------------------
















#---------------------------------------------

# Endpoints pour Commentaires
@app.get("/commentaires/", response_model=list[CommentaireResponse])
def list_commentaires(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, contenu, utilisateur_id, post_id FROM commentaires")
    commentaires = cursor.fetchall()
    return [
        {"id": c[0], "contenu": c[1], "utilisateur_id": c[2], "post_id": c[3]}
        for c in commentaires
    ]


@app.post("/commentaires/", response_model=CommentaireResponse)
def create_commentaire(commentaire: CommentaireCreate, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO commentaires (contenu, utilisateur_id, post_id) VALUES (?, ?, ?)",
        (commentaire.contenu, commentaire.utilisateur_id, commentaire.post_id),
    )
    conn.commit()
    commentaire_id = cursor.lastrowid
    return {**commentaire.dict(), "id": commentaire_id}

@app.get("/commentaires/{commentaire_id}", response_model=CommentaireResponse)
def read_commentaire(commentaire_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, contenu, utilisateur_id, post_id FROM commentaires WHERE id = ?", (commentaire_id,))
    commentaire = cursor.fetchone()
    if commentaire is None:
        raise HTTPException(status_code=404, detail="Commentaire non trouvé")
    return {"id": commentaire[0], "contenu": commentaire[1], "utilisateur_id": commentaire[2], "post_id": commentaire[3]}

@app.put("/commentaires/{commentaire_id}", response_model=CommentaireResponse)
def update_commentaire(commentaire_id: int, commentaire: CommentaireCreate, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE commentaires SET contenu = ?, utilisateur_id = ?, post_id = ? WHERE id = ?",
        (commentaire.contenu, commentaire.utilisateur_id, commentaire.post_id, commentaire_id)
    )
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Commentaire non trouvé")
    return {**commentaire.dict(), "id": commentaire_id}

@app.delete("/commentaires/{commentaire_id}")
def delete_commentaire(commentaire_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM commentaires WHERE id = ?", (commentaire_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Commentaire non trouvé")
    return {"message": "Commentaire supprimé avec succès"}

#---------------------------------------------


# Démarrer l'application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)