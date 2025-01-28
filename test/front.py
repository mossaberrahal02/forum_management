import streamlit as st
import requests

# API URL for FastAPI
API_URL = "http://0.0.0.0:8000"

# Function to handle API requests with error handling
def api_request(method, endpoint, **kwargs):
    try:
        url = f"{API_URL}{endpoint}"
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        st.error(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        st.error(f"Error occurred: {err}")
    return None

# USER CRUD FUNCTIONS
def get_utilisateurs():
    return api_request("GET", "/utilisateurs/")

def create_utilisateur(nom, email):
    return api_request("POST", "/utilisateurs/", json={"nom": nom, "email": email})

def update_utilisateur(utilisateur_id, nom, email):
    return api_request("PUT", f"/utilisateurs/{utilisateur_id}", json={"nom": nom, "email": email})

def delete_utilisateur(utilisateur_id):
    return api_request("DELETE", f"/utilisateurs/{utilisateur_id}")

# CATEGORY CRUD FUNCTIONS
def get_categories():
    return api_request("GET", "/categories/")

def create_categorie(nom):
    return api_request("POST", "/categories/", json={"nom": nom})

def update_categorie(categorie_id, nom):
    return api_request("PUT", f"/categories/{categorie_id}", json={"nom": nom})

def delete_categorie(categorie_id):
    return api_request("DELETE", f"/categories/{categorie_id}")

# POST CRUD FUNCTIONS
def get_posts():
    return api_request("GET", "/posts/")

def create_post(titre, contenu, utilisateur_id, categorie_id):
    return api_request("POST", "/posts/", json={"titre": titre, "contenu": contenu, "utilisateur_id": utilisateur_id, "categorie_id": categorie_id})

def update_post(post_id, titre, contenu, utilisateur_id, categorie_id):
    return api_request("PUT", f"/posts/{post_id}", json={"titre": titre, "contenu": contenu, "utilisateur_id": utilisateur_id, "categorie_id": categorie_id})

def delete_post(post_id):
    return api_request("DELETE", f"/posts/{post_id}")

# COMMENT CRUD FUNCTIONS
def get_commentaires():
    return api_request("GET", "/commentaires/")

def create_commentaire(contenu, utilisateur_id, post_id):
    return api_request("POST", "/commentaires/", json={"contenu": contenu, "utilisateur_id": utilisateur_id, "post_id": post_id})

def update_commentaire(commentaire_id, contenu, utilisateur_id, post_id):
    return api_request("PUT", f"/commentaires/{commentaire_id}", json={"contenu": contenu, "utilisateur_id": utilisateur_id, "post_id": post_id})

def delete_commentaire(commentaire_id):
    return api_request("DELETE", f"/commentaires/{commentaire_id}")

# Streamlit Layout

# Header
st.title("Forum Management System")
# --- USERS MANAGEMENT ---
st.header("Manage Users")

# List Users
st.subheader("List Users")
utilisateurs = get_utilisateurs()
if utilisateurs:
    for utilisateur in utilisateurs:
        st.write(f"ID: {utilisateur['id']}, Nom: {utilisateur['nom']}, Email: {utilisateur['email']}")

# Create User
st.subheader("Create User")
nom = st.text_input("Name")
email = st.text_input("Email")
if st.button("Create User"):
    result = create_utilisateur(nom, email)
    if result:
        st.success(f"User created: {result['nom']} ({result['email']})")
    else:
        st.error("Error creating user.")

# Update User
st.subheader("Update User")
utilisateur_id_update = st.number_input("User ID", min_value=1, key="update_user_id")
nom_update = st.text_input("New Name")
email_update = st.text_input("New Email")
if st.button("Update User"):
    result = update_utilisateur(utilisateur_id_update, nom_update, email_update)
    if result:
        st.success(f"User updated: {result['nom']} ({result['email']})")
    else:
        st.error("Error updating user.")

# Delete User
st.subheader("Delete User")
utilisateur_id_delete = st.number_input("User ID to Delete", min_value=1, key="delete_user_id")
if st.button("Delete User"):
    result = delete_utilisateur(utilisateur_id_delete)
    if result:
        st.success(f"User deleted successfully!")
    else:
        st.error("Error deleting user.")

# --- CATEGORIES MANAGEMENT ---
st.header("Manage Categories")

# List Categories
st.subheader("List Categories")
categories = get_categories()
if categories:
    for categorie in categories:
        st.write(f"ID: {categorie['id']}, Name: {categorie['nom']}")

# Create Category
st.subheader("Create Category")
categorie_nom = st.text_input("Category Name")
if st.button("Create Category"):
    result = create_categorie(categorie_nom)
    if result:
        st.success(f"Category created: {result['nom']}")
    else:
        st.error("Error creating category.")

# Update Category
st.subheader("Update Category")
categorie_id_update = st.number_input("Category ID", min_value=1, key="update_category_id")
categorie_nom_update = st.text_input("New Category Name")
if st.button("Update Category"):
    result = update_categorie(categorie_id_update, categorie_nom_update)
    if result:
        st.success(f"Category updated: {result['nom']}")
    else:
        st.error("Error updating category.")

# Delete Category
st.subheader("Delete Category")
categorie_id_delete = st.number_input("Category ID to Delete", min_value=1, key="delete_category_id")
if st.button("Delete Category"):
    result = delete_categorie(categorie_id_delete)
    if result:
        st.success(f"Category deleted successfully!")
    else:
        st.error("Error deleting category.")

# --- POSTS MANAGEMENT ---
st.header("Manage Posts")

# List Posts
st.subheader("List Posts")
posts = get_posts()
if posts:
    for post in posts:
        st.write(f"ID: {post['id']}, Title: {post['titre']}, Content: {post['contenu']}")

# Create Post
st.subheader("Create Post")
post_titre = st.text_input("Post Title")
post_contenu = st.text_area("Post Content")
post_utilisateur_id = st.number_input("User ID", min_value=1, key="create_post_user_id")
post_categorie_id = st.number_input("Category ID", min_value=1, key="create_post_category_id")
if st.button("Create Post"):
    result = create_post(post_titre, post_contenu, post_utilisateur_id, post_categorie_id)
    if result:
        st.success(f"Post created: {result['titre']}")
    else:
        st.error("Error creating post.")

# Update Post
st.subheader("Update Post")
post_id_update = st.number_input("Post ID", min_value=1, key="update_post_id")
post_titre_update = st.text_input("New Post Title")
post_contenu_update = st.text_area("New Post Content")
post_utilisateur_id_update = st.number_input("User ID", min_value=1, key="update_post_user_id")
post_categorie_id_update = st.number_input("Category ID", min_value=1, key="update_post_category_id")
if st.button("Update Post"):
    result = update_post(post_id_update, post_titre_update, post_contenu_update, post_utilisateur_id_update, post_categorie_id_update)
    if result:
        st.success(f"Post updated: {result['titre']}")
    else:
        st.error("Error updating post.")

# Delete Post
st.subheader("Delete Post")
post_id_delete = st.number_input("Post ID to Delete", min_value=1, key="delete_post_id")
if st.button("Delete Post"):
    result = delete_post(post_id_delete)
    if result:
        st.success(f"Post deleted successfully!")
    else:
        st.error("Error deleting post.")

# --- COMMENTS MANAGEMENT ---
st.header("Manage Comments")

# List Comments
st.subheader("List Comments")
commentaires = get_commentaires()
if commentaires:
    for commentaire in commentaires:
        st.write(f"ID: {commentaire['id']}, Content: {commentaire['contenu']}")

# Create Comment
st.subheader("Create Comment")
commentaire_contenu = st.text_area("Comment Content")
commentaire_utilisateur_id = st.number_input("User ID", min_value=1, key="create_comment_user_id")
commentaire_post_id = st.number_input("Post ID", min_value=1, key="create_comment_post_id")
if st.button("Create Comment"):
    result = create_commentaire(commentaire_contenu, commentaire_utilisateur_id, commentaire_post_id)
    if result:
        st.success(f"Comment created: {result['contenu']}")
    else:
        st.error("Error creating comment.")

# Update Comment
st.subheader("Update Comment")
commentaire_id_update = st.number_input("Comment ID", min_value=1, key="update_comment_id")
commentaire_contenu_update = st.text_area("New Comment Content")
commentaire_utilisateur_id_update = st.number_input("User ID", min_value=1, key="update_comment_user_id")
commentaire_post_id_update = st.number_input("Post ID", min_value=1, key="update_comment_post_id")
if st.button("Update Comment"):
    result = update_commentaire(commentaire_id_update, commentaire_contenu_update, commentaire_utilisateur_id_update, commentaire_post_id_update)
    if result:
        st.success(f"Comment updated: {result['contenu']}")
    else:
        st.error("Error updating comment.")

# Delete Comment
st.subheader("Delete Comment")
commentaire_id_delete = st.number_input("Comment ID to Delete", min_value=1, key="delete_comment_id")
if st.button("Delete Comment"):
    result = delete_commentaire(commentaire_id_delete)
    if result:
        st.success(f"Comment deleted successfully!")
    else:
        st.error("Error deleting comment.")
