# import streamlit as st
# import requests

# # Base URL of the FastAPI backend
# BASE_URL = "http://0.0.0.0:8000"

# st.set_page_config(page_title="Gestion des utilisateurs d'un forum", layout="wide")

# # Navigation Sidebar
# st.sidebar.title("Navigation")
# menu = st.sidebar.radio("Go to", ["Home", "Create Post", "Manage Categories", "Users"])

# # Utility function to fetch data from the backend
# def fetch_data(endpoint):
#     try:
#         response = requests.get(f"{BASE_URL}{endpoint}")
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching data: {e}")
#         return []

# # Utility function to post data to the backend
# def post_data(endpoint, payload):
#     try:
#         response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error posting data: {e}")
#         return None
# # Home Page
# if menu == "Home":
#     st.title("Welcome to the Forum!")

#     # Fetch all posts
#     posts = fetch_data("/posts/")

#     # Fetch available users for comment submission
#     users = fetch_data("/utilisateurs/")
#     user_options = {user['id']: user['nom'] for user in users}  # Creating a dictionary for easy access
#     user_dict = {user['id']: user['nom'] for user in users}  # A mapping from user_id to user name
    
#     if posts:
#         for post in posts:
#             with st.expander(post['titre']):
#                 # Title of the post
#                 st.subheader(post['titre'])
#                 # Content of the post
#                 st.write(post['contenu'])
                
#                 # Display post's meta information with the user's name instead of user_id
#                 post_user_name = user_dict.get(post['utilisateur_id'], "Unknown User")
#                 post_category = post['categorie_id']  # Assuming you have category information in posts
#                 st.caption(f"poste par {post_user_name} dans le Categorie {post_category}")
                
#                 # Add a delete post button
#                 delete_post_button = st.button("Delete Post", key=f"delete_{post['id']}")
                
#                 if delete_post_button:
#                     response = requests.delete(f"{BASE_URL}/posts/{post['id']}")
                    
#                     if response.status_code == 200:
#                         st.success("Post deleted successfully!")
#                         # Refresh the post list after deletion
#                         posts = fetch_data("/posts/")
#                     else:
#                         st.error("Failed to delete the post. Make sure the ID is correct.")
                
#                 # Add a new comment section
#                 selected_user_id = st.selectbox(
#                     "Select User to Submit Comment", 
#                     options=list(user_options.keys()), 
#                     format_func=lambda x: user_options[x], 
#                     key=f"select_user_{post['id']}"  # Unique key for each selectbox
#                 )
#                 new_comment = st.text_input(f"Add a comment for post {post['id']}", key=f"comment_{post['id']}")
                
#                 if st.button("Submit Comment", key=f"submit_{post['id']}"):
#                     if new_comment:
#                         payload = {"contenu": new_comment, "utilisateur_id": selected_user_id, "post_id": post['id']}
#                         post_data("/commentaires/", payload)
#                         st.success("Comment added successfully!")
#                     else:
#                         st.error("Comment cannot be empty.")

#             # Fetch and display comments for the post outside of the post's expander
#             comments = fetch_data(f"/commentaires/?post_id={post['id']}")
#             with st.expander(f"View Comments for Post {post['id']}"):
#                 if comments:
#                     st.write("### Comments")
#                     for comment in comments:
#                         user_name = user_dict.get(comment['utilisateur_id'], "Unknown")
#                         # Displaying the comment with user name before and after the comment text
#                         st.markdown(f"**{user_name}**: {comment['contenu']} (**{user_name}**)")  # This is the new format
#                 else:
#                     st.write("No comments yet. Be the first to comment!")
#     else:
#         st.write("No posts available yet. Please check back later.")

# # Create Post Page
# elif menu == "Create Post":
#     st.title("Create a New Post")
#     title = st.text_input("Post Title")
#     content = st.text_area("Post Content")
    
#     # Fetch available users
#     users = fetch_data("/utilisateurs/")
#     user_options = {user['id']: user['nom'] for user in users}  # Creating a dictionary for easy access
    
#     # Select user from the available list
#     user_id = st.selectbox("Select User", options=list(user_options.keys()), format_func=lambda x: user_options[x])
    
#     # Fetch available categories
#     categories = fetch_data("/categories/")
#     category_options = {category['id']: category['nom'] for category in categories}  # Creating a dictionary for easy access
    
#     # Select category from the available list
#     category_id = st.selectbox("Select Category", options=list(category_options.keys()), format_func=lambda x: category_options[x])

#     if st.button("Submit Post"):
#         if title and content:
#             payload = {
#                 "titre": title,
#                 "contenu": content,
#                 "utilisateur_id": user_id,
#                 "categorie_id": category_id
#             }
#             post_data("/posts/", payload)
#             st.success("Post created successfully!")
#         else:
#             st.error("Title and Content cannot be empty.")



# # Manage Categories Page
# elif menu == "Manage Categories":
#     st.title("Categories Management")
    
#     # Fetch and display existing categories with their IDs
#     categories = fetch_data("/categories/")

#     st.write("### Existing Categories")
#     for category in categories:
#         st.write(f"**ID:** {category['id']} - **Category Name:** {category['nom']}")

#     # Section to create a new category
#     st.subheader("Add a New Category")
#     new_category = st.text_input("New Category Name")

#     if st.button("Add Category"):
#         if new_category:
#             payload = {"nom": new_category}
#             post_data("/categories/", payload)
#             st.success("Category added successfully!")
#             # Optionally refresh the category list
#             categories = fetch_data("/categories/")
#         else:
#             st.error("Category name cannot be empty.")

#     # Section to delete a category by ID
#     st.subheader("Delete Category")
#     category_id_to_delete = st.number_input("Enter Category ID to Delete", min_value=1, step=1)

#     if st.button("Delete Category"):
#         if category_id_to_delete:
#             response = requests.delete(f"{BASE_URL}/categories/{category_id_to_delete}")
            
#             if response.status_code == 200:
#                 st.success("Category deleted successfully!")
#                 # Optionally refresh the category list
#                 categories = fetch_data("/categories/")
#             else:
#                 st.error("Failed to delete category. Make sure the ID is correct.")
#         else:
#             st.error("Please enter a valid category ID.")




# # Users Page
# elif menu == "Users":
#     st.title("User Management")
    
#     # Fetch and display existing users with their IDs
#     users = fetch_data("/utilisateurs/")

#     st.write("### Existing Users")
#     for user in users:
#         st.write(f"**ID:** {user['id']} - **Name:** {user['nom']} - **Email:** {user['email']}")

#     # Section to create a new user
#     st.subheader("Create New User")
#     new_user_name = st.text_input("New User Name")
#     new_user_email = st.text_input("New User Email")

#     if st.button("Add User"):
#         if new_user_name and new_user_email:
#             payload = {"nom": new_user_name, "email": new_user_email}
#             post_data("/utilisateurs/", payload)
#             st.success("User added successfully!")
#             # Optionally refresh the user list
#             users = fetch_data("/utilisateurs/")
#         else:
#             st.error("Name and Email cannot be empty.")

#     # Section to delete a user by ID
#     st.subheader("Delete User")
#     user_id_to_delete = st.number_input("Enter User ID to Delete", min_value=1, step=1)

#     if st.button("Delete User"):
#         if user_id_to_delete:
#             response = requests.delete(f"{BASE_URL}/utilisateurs/{user_id_to_delete}")
            
#             if response.status_code == 200:
#                 st.success("User deleted successfully!")
#                 # Optionally refresh the user list
#                 users = fetch_data("/utilisateurs/")
#             else:
#                 st.error("Failed to delete user. Make sure the ID is correct.")
#         else:
#             st.error("Please enter a valid user ID.")



# # Clear Database Button
# if st.button("Clear All Data"):
#     response = requests.delete(f"{BASE_URL}/clear_all")
    
#     if response.status_code == 200:
#         st.success("All data has been cleared from the database!")
#     else:
#         st.error("Failed to clear data.")





import streamlit as st
import requests

BASE_URL = "http://0.0.0.0:8000"

st.set_page_config(page_title="Gestion des utilisateurs d'un forum", layout="wide")

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Aller à", ["Accueil", "Créer un Post", "Gérer les Catégories", "Utilisateurs"])

def recuperer_donnees(endpoint):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return []

def envoyer_donnees(endpoint, payload):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'envoi des données : {e}")
        return None

if menu == "Accueil":
    st.title("Bienvenue sur le Forum !")

    posts = recuperer_donnees("/posts/")
    utilisateurs = recuperer_donnees("/utilisateurs/")
    options_utilisateur = {utilisateur['id']: utilisateur['nom'] for utilisateur in utilisateurs}
    dictionnaire_utilisateurs = {utilisateur['id']: utilisateur['nom'] for utilisateur in utilisateurs}
    
    if posts:
        for post in posts:
            with st.expander(post['titre']):
                st.subheader(post['titre'])
                st.write(post['contenu'])
                
                nom_utilisateur_post = dictionnaire_utilisateurs.get(post['utilisateur_id'], "Utilisateur inconnu")
                categorie_post = post['categorie_id']
                st.caption(f"Posté par {nom_utilisateur_post}")
                
                bouton_supprimer_post = st.button("Supprimer le Post", key=f"delete_{post['id']}")
                
                if bouton_supprimer_post:
                    response = requests.delete(f"{BASE_URL}/posts/{post['id']}")
                    
                    if response.status_code == 200:
                        st.success("Post supprimé avec succès !")
                        posts = recuperer_donnees("/posts/")
                    else:
                        st.error("Échec de la suppression du post. Assurez-vous que l'ID est correct.")
                
                id_utilisateur_select = st.selectbox(
                    "Sélectionner un utilisateur pour soumettre un commentaire", 
                    options=list(options_utilisateur.keys()), 
                    format_func=lambda x: options_utilisateur[x], 
                    key=f"select_user_{post['id']}"
                )
                nouveau_commentaire = st.text_input(f"Ajouter un commentaire pour le post {post['id']}", key=f"comment_{post['id']}")
                
                if st.button("Soumettre le commentaire", key=f"submit_{post['id']}"):
                    if nouveau_commentaire:
                        payload = {"contenu": nouveau_commentaire, "utilisateur_id": id_utilisateur_select, "post_id": post['id']}
                        envoyer_donnees("/commentaires/", payload)
                        st.success("Commentaire ajouté avec succès !")
                    else:
                        st.error("Le commentaire ne peut pas être vide.")

            commentaires = recuperer_donnees(f"/commentaires/?post_id={post['id']}")
            with st.expander(f"Voir les commentaires pour le post {post['id']}"):
                if commentaires:
                    st.write("### Commentaires")
                    for commentaire in commentaires:
                        nom_utilisateur = dictionnaire_utilisateurs.get(commentaire['utilisateur_id'], "Inconnu")
                        st.markdown(f"**{nom_utilisateur}**: {commentaire['contenu']} ")  
                else:
                    st.write("Aucun commentaire pour l'instant. Soyez le premier à commenter !")
    else:
        st.write("Aucun post disponible pour le moment. Veuillez revenir plus tard.")

elif menu == "Créer un Post":
    st.title("Créer un nouveau post")
    titre = st.text_input("Titre du post")
    contenu = st.text_area("Contenu du post")
    
    utilisateurs = recuperer_donnees("/utilisateurs/")
    options_utilisateur = {utilisateur['id']: utilisateur['nom'] for utilisateur in utilisateurs}
    
    id_utilisateur = st.selectbox("Sélectionner un utilisateur", options=list(options_utilisateur.keys()), format_func=lambda x: options_utilisateur[x])
    
    categories = recuperer_donnees("/categories/")
    options_categorie = {categorie['id']: categorie['nom'] for categorie in categories}
    
    id_categorie = st.selectbox("Sélectionner une catégorie", options=list(options_categorie.keys()), format_func=lambda x: options_categorie[x])

    if st.button("Soumettre le post"):
        if titre and contenu:
            payload = {
                "titre": titre,
                "contenu": contenu,
                "utilisateur_id": id_utilisateur,
                "categorie_id": id_categorie
            }
            envoyer_donnees("/posts/", payload)
            st.success("Post créé avec succès !")
        else:
            st.error("Le titre et le contenu ne peuvent pas être vides.")

elif menu == "Gérer les Catégories":
    st.title("Gestion des Catégories")
    
    categories = recuperer_donnees("/categories/")

    st.write("### Catégories existantes")
    for categorie in categories:
        st.write(f"**ID :** {categorie['id']} - **Nom de la catégorie :** {categorie['nom']}")

    st.subheader("Ajouter une nouvelle catégorie")
    nouvelle_categorie = st.text_input("Nom de la nouvelle catégorie")

    if st.button("Ajouter la catégorie"):
        if nouvelle_categorie:
            payload = {"nom": nouvelle_categorie}
            envoyer_donnees("/categories/", payload)
            st.success("Catégorie ajoutée avec succès !")
            categories = recuperer_donnees("/categories/")
        else:
            st.error("Le nom de la catégorie ne peut pas être vide.")

    st.subheader("Supprimer une catégorie")
    id_categorie_a_supprimer = st.number_input("Entrez l'ID de la catégorie à supprimer", min_value=1, step=1)

    if st.button("Supprimer la catégorie"):
        if id_categorie_a_supprimer:
            response = requests.delete(f"{BASE_URL}/categories/{id_categorie_a_supprimer}")
            
            if response.status_code == 200:
                st.success("Catégorie supprimée avec succès !")
                categories = recuperer_donnees("/categories/")
            else:
                st.error("Échec de la suppression de la catégorie. Assurez-vous que l'ID est correct.")
        else:
            st.error("Veuillez entrer un ID de catégorie valide.")

elif menu == "Utilisateurs":
    st.title("Gestion des Utilisateurs")
    
    utilisateurs = recuperer_donnees("/utilisateurs/")

    st.write("### Utilisateurs existants")
    for utilisateur in utilisateurs:
        st.write(f"**ID :** {utilisateur['id']} - **Nom :** {utilisateur['nom']} - **Email :** {utilisateur['email']}")

    st.subheader("Créer un nouvel utilisateur")
    nouveau_nom_utilisateur = st.text_input("Nom du nouvel utilisateur")
    nouvel_email_utilisateur = st.text_input("Email du nouvel utilisateur")

    if st.button("Ajouter un utilisateur"):
        if nouveau_nom_utilisateur and nouvel_email_utilisateur:
            payload = {"nom": nouveau_nom_utilisateur, "email": nouvel_email_utilisateur}
            envoyer_donnees("/utilisateurs/", payload)
            st.success("Utilisateur ajouté avec succès !")
            utilisateurs = recuperer_donnees("/utilisateurs/")
        else:
            st.error("Le nom et l'email ne peuvent pas être vides.")

    st.subheader("Supprimer un utilisateur")
    id_utilisateur_a_supprimer = st.number_input("Entrez l'ID de l'utilisateur à supprimer", min_value=1, step=1)

    if st.button("Supprimer l'utilisateur"):
        if id_utilisateur_a_supprimer:
            response = requests.delete(f"{BASE_URL}/utilisateurs/{id_utilisateur_a_supprimer}")
            
            if response.status_code == 200:
                st.success("Utilisateur supprimé avec succès !")
                utilisateurs = recuperer_donnees("/utilisateurs/")
            else:
                st.error("Échec de la suppression de l'utilisateur. Assurez-vous que l'ID est correct.")
        else:
            st.error("Veuillez entrer un ID d'utilisateur valide.")

if st.button("Effacer toutes les données"):
    response = requests.delete(f"{BASE_URL}/clear_all")
    
    if response.status_code == 200:
        st.success("Toutes les données ont été effacées de la base de données !")
    else:
        st.error("Échec de l'effacement des données.")
