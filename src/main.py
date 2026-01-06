import io

from fastapi import FastAPI, Depends, HTTPException, Response  # Ajout de Response ici
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List
import pandas as pd
from fastapi.responses import FileResponse

# Imports de vos fichiers locaux
from src import models
from src import schemas
from src.database import SessionLocal, engine

app = FastAPI(title="Application de Voyage - Gestion des Dépenses")


# Création d'une fonction pour gérer la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- ROUTES POUR LES UTILISATEURS ---


@app.post("/utilisateurs/", response_model=schemas.Utilisateur)
def creer_utilisateur(user: schemas.UtilisateurCreate, db: Session = Depends(get_db)):
    db_user = models.Utilisateur(nom=user.nom)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/utilisateurs/", response_model=List[schemas.Utilisateur])
def lister_utilisateurs(db: Session = Depends(get_db)):
    return db.query(models.Utilisateur).all()


# --- ROUTES POUR LES DÉPENSES ---


@app.post("/depenses/")
def ajouter_depense(depense: schemas.DepenseCreate, db: Session = Depends(get_db)):
    # 1. Vérifier si le payeur existe
    payeur = (
        db.query(models.Utilisateur)
        .filter(models.Utilisateur.id == depense.payeur_id)
        .first()
    )
    if not payeur:
        raise HTTPException(status_code=404, detail="Payeur non trouvé")

    # 2. Création de la dépense principale
    nouvelle_depense = models.Depense(
        description=depense.description,
        montant=depense.montant,
        payeur_id=depense.payeur_id,
    )
    db.add(nouvelle_depense)
    db.flush()  # Récupère l'ID sans valider définitivement

    # 3. Calcul et création des répartitions
    nb_beneficiaires = len(depense.beneficiaire_ids)
    if nb_beneficiaires == 0:
        raise HTTPException(
            status_code=400, detail="Il doit y avoir au moins un bénéficiaire"
        )

    part_individuelle = depense.montant / nb_beneficiaires

    for b_id in depense.beneficiaire_ids:
        repartition = models.Repartition(
            depense_id=nouvelle_depense.id, beneficiaire_id=b_id, part=part_individuelle
        )
        db.add(repartition)

    db.commit()
    return {
        "status": "success",
        "message": f"Dépense '{depense.description}' enregistrée",
    }


# --- CALCUL DES SOLDES ---


@app.get("/soldes/")
def calculer_soldes(db: Session = Depends(get_db)):
    utilisateurs = db.query(models.Utilisateur).all()
    bilan = []

    for u in utilisateurs:
        # Somme de ce qu'il a payé (Crédit)
        total_paye = (
            db.query(func.sum(models.Depense.montant))
            .filter(models.Depense.payeur_id == u.id)
            .scalar()
            or 0
        )

        # Somme de ce qu'il doit (Débit)
        total_du = (
            db.query(func.sum(models.Repartition.part))
            .filter(models.Repartition.beneficiaire_id == u.id)
            .scalar()
            or 0
        )

        bilan.append(
            {
                "id": u.id,
                "nom": u.nom,
                "total_payé": total_paye,
                "total_dû": total_du,
                "solde": round(total_paye - total_du, 2),
            }
        )

    return bilan


# --- EXPORT EXCEL ---


@app.get("/export-excel/")
def export_excel(db: Session = Depends(get_db)):
    try:
        # On retire d.date car la colonne n'existe pas dans votre table
        query = text(
            """
            SELECT 
                d.description as objet, 
                d.montant as montant_total, 
                u_payeur.nom as payeur, 
                r.part as part_individuelle, 
                u_benef.nom as beneficiaire
            FROM depenses d
            JOIN utilisateurs u_payeur ON d.payeur_id = u_payeur.id
            JOIN repartitions r ON d.id = r.depense_id
            JOIN utilisateurs u_benef ON r.beneficiaire_id = u_benef.id
        """
        )

        with engine.connect() as connection:
            df = pd.read_sql(query, connection)

        # Si le DataFrame est vide, on crée une structure par défaut
        if df.empty:
            df = pd.DataFrame(
                columns=[
                    "objet",
                    "montant_total",
                    "payeur",
                    "part_individuelle",
                    "beneficiaire",
                ]
            )

        # Création du fichier Excel en mémoire
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Dépenses")

        output.seek(0)

        headers = {
            "Content-Disposition": 'attachment; filename="Justificatif_Voyage.xlsx"'
        }
        return Response(
            content=output.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers,
        )

    except Exception as e:
        print(f"Erreur lors de l'export : {e}")
        raise HTTPException(status_code=500, detail=str(e))
