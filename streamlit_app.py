import streamlit as st
import requests
from datetime import date

API_URL = "http://127.0.0.1:8000"  # adapte si besoin

st.title("🧳 Démarrage du voyage")

# Pour mémoriser le voyage créé pendant la session
if "voyage_id" not in st.session_state:
    st.session_state.voyage_id = None

# --- Création du voyage ---
if st.session_state.voyage_id is None:

    nom_voyage = st.text_input("Nom du voyage")
    commentaire_voyage = st.text_area("Commentaire (facultatif)")
    date_debut = st.date_input("Date de début", value=date.today())
    date_fin = st.date_input("Date de fin", value=date.today())

    participants_txt = st.text_area("Participants (un par ligne, ex: Prénom Nom)")
    participants = [p.strip() for p in participants_txt.splitlines() if p.strip()]

    if st.button("Créer le voyage"):
        if not nom_voyage or not participants:
            st.warning("Nom du voyage et participants obligatoires")
        else:
            payload = {
                "nom": nom_voyage,
                "commentaire": commentaire_voyage,
                "date_debut": date_debut.isoformat(),
                "date_fin": date_fin.isoformat(),
                "participants": participants,
            }
            try:
                r = requests.post(f"{API_URL}/voyages/", json=payload)
                if r.status_code == 200:
                    st.session_state.voyage_id = r.json()["voyage_id"]
                    st.success("Voyage créé !")
                    st.rerun()  # recharge la page pour passer à l'étape suivante
                else:
                    st.error("Erreur création voyage")
                    st.text(r.text)
            except requests.exceptions.RequestException as e:
                st.error("Impossible de joindre l'API /voyages")
                st.text(str(e))

    # ⛔ bloque l’accès au reste de l’appli tant que le voyage n’est pas créé
    st.stop()

# --- Après création du voyage ---
st.success(f"Voyage sélectionné : {nom_voyage} ({date_debut} → {date_fin})")
