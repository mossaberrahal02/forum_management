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
