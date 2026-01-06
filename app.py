import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # adapte si besoin

st.title("Gestionnaire de Dépenses de Voyage")

# -----------------------
# --- AJOUT UTILISATEUR --
# -----------------------
st.subheader("Ajouter un nouvel utilisateur / partenaire")
nouveau_nom = st.text_input("Nom de l'utilisateur")
if st.button("Créer utilisateur"):
    if not nouveau_nom:
        st.warning("Veuillez saisir un nom")
    else:
        try:
            payload = {"nom": nouveau_nom}
            r = requests.post(f"{API_URL}/utilisateurs/", json=payload)
            if r.status_code == 200:
                st.success(f"Utilisateur '{nouveau_nom}' ajouté avec succès !")
            else:
                st.error(f"Erreur API /utilisateurs : {r.status_code}")
                st.text(r.text)
        except requests.exceptions.RequestException as e:
            st.error("Impossible de joindre l'API /utilisateurs")
            st.text(str(e))

# -----------------------
# --- CHARGEMENT UTILISATEURS ----
# -----------------------
try:
    r_users = requests.get(f"{API_URL}/utilisateurs/")
    if r_users.status_code == 200:
        users = r_users.json()
    else:
        st.error(f"Erreur API /utilisateurs : {r_users.status_code}")
        st.text(r_users.text)
        users = []
except requests.exceptions.RequestException as e:
    st.error("Impossible de joindre l'API /utilisateurs")
    st.text(str(e))
    users = []

user_dict = {u["nom"]: u["id"] for u in users}

# -----------------------
# --- FORMULAIRE DEPENSE
# -----------------------
st.subheader("Ajouter une dépense")
description = st.text_input("Description (ex: Resto, Essence...)")
montant = st.number_input("Montant (€)", min_value=0.0, format="%.2f")

if user_dict:
    payeur_nom = st.selectbox("Qui a payé ?", list(user_dict.keys()))
    payeur_id = user_dict[payeur_nom]

    beneficiaires_nom = st.multiselect(
        "Pour qui ? (Bénéficiaires)", list(user_dict.keys())
    )
    beneficiaire_ids = [user_dict[n] for n in beneficiaires_nom]
else:
    st.info("Aucun utilisateur disponible")
    payeur_id = None
    beneficiaire_ids = []

if st.button("Ajouter la dépense"):
    if not description or montant <= 0 or not payeur_id or not beneficiaire_ids:
        st.warning("Veuillez remplir tous les champs correctement")
    else:
        try:
            payload = {
                "description": description,
                "montant": montant,
                "payeur_id": payeur_id,
                "beneficiaire_ids": beneficiaire_ids,
            }
            r = requests.post(f"{API_URL}/depenses/", json=payload)
            if r.status_code == 200:
                st.success(f"Dépense '{description}' ajoutée avec succès !")
            else:
                st.error(f"Erreur API /depenses : {r.status_code}")
                st.text(r.text)
        except requests.exceptions.RequestException as e:
            st.error("Impossible de joindre l'API /depenses")
            st.text(str(e))

# -----------------------
# --- AFFICHAGE SOLDES ---
# -----------------------
st.subheader("📊 Soldes Actuels")
try:
    r_soldes = requests.get(f"{API_URL}/soldes/")
    if r_soldes.status_code == 200:
        soldes_res = r_soldes.json()
        for s in soldes_res:
            st.write(f"{s['nom']}: Solde = {s['solde']} €")
    else:
        st.error(f"Erreur API /soldes : {r_soldes.status_code}")
        st.text(r_soldes.text)
except requests.exceptions.RequestException as e:
    st.error("Impossible de joindre l'API /soldes")
    st.text(str(e))

# -----------------------
# --- EXPORT EXCEL ------
# -----------------------
st.subheader("📑 Justificatif Excel")
if st.button("Télécharger Excel"):
    try:
        r = requests.get(f"{API_URL}/export-excel/")
        if r.status_code == 200:
            st.download_button(
                "Télécharger le fichier",
                r.content,
                file_name="Justificatif_Voyage.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.error(f"Erreur API /export-excel : {r.status_code}")
            st.text(r.text)
    except requests.exceptions.RequestException as e:
        st.error("Impossible de joindre l'API /export-excel")
        st.text(str(e))
