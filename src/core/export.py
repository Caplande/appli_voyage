import pandas as pd
from sqlalchemy.orm import Session


@app.get("/export-excel")
def export_from_db(db: Session = Depends(get_db)):
    # Requête SQL pour récupérer toutes les données jointes
    query = """
    SELECT d.description, d.montant, u.nom as payeur, r.part, ub.nom as beneficiaire
    FROM depenses d
    JOIN utilisateurs u ON d.payeur_id = u.id
    JOIN repartitions r ON r.depense_id = d.id
    JOIN utilisateurs ub ON r.beneficiaire_id = ub.id
    """

    df = pd.read_sql(query, engine)
    df.to_excel("justificatif_complet.xlsx", index=False)

    return FileResponse("justificatif_complet.xlsx")
