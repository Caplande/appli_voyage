// --- Afficher la section sélectionnée ---
function showSection(sectionId) {
    document.querySelectorAll('.menuSection').forEach(s => s.style.display = 'none');
    document.getElementById(sectionId).style.display = 'block';
}

// --- Charger les voyages et définir le voyage par défaut ---
async function loadVoyages() {
    const resp = await fetch("/voyages/derniers_voyages");
    const data = await resp.json();
    const voyages = data.voyages;
    const defaultId = data.voyage_defaut_id;

    const selectMembre = document.getElementById("voyageSelectMembre");
    const selectDepense = document.getElementById("voyageSelectDepense");

    [selectMembre, selectDepense].forEach(sel => {
        sel.innerHTML = ""; // vider la liste
        voyages.forEach(v => {
            const opt = document.createElement("option");
            opt.value = v.id;
            opt.textContent = `${v.nom} (${v.date_debut} → ${v.date_fin})`;
            sel.appendChild(opt);
        });
        if(defaultId) sel.value = defaultId; // pré-sélection du voyage par défaut
    });
}

// --- Créer voyage ---
document.getElementById("voyageForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const nom = document.getElementById("voyageNom").value;
    const commentaire = document.getElementById("voyageCommentaire").value; // ⚡ ajouté
    const date_debut = document.getElementById("voyageDebut").value;
    const date_fin = document.getElementById("voyageFin").value;

    // const resp = await fetch("/voyages/", {
    //     method: "POST",
    //     headers: {"Content-Type": "application/json"},
    //     body: JSON.stringify({ nom, commentaire, date_debut, date_fin }) // ⚡ inclure commentaire
    // });

    //********************* Temp *************************
    const resp = await fetch("/voyages/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        nom: "Voyage Test",
        commentaire: "Optionnel",
        date_debut: "2026-01-08",
        date_fin: "2026-01-08"
    })
    });

    // ***************************************************

    const data = await resp.json();
    document.getElementById("voyageResult").textContent =
        `Voyage créé : ${data.nom} (id=${data.id}) - ${data.commentaire || ""}`;

    loadVoyages(); // mettre à jour la liste des voyages
});

// --- Ajouter membre ---
document.getElementById("ajouterMembreBtn").addEventListener("click", async () => {
    const voyage_id = document.getElementById("voyageSelectMembre").value;
    const prenom = document.getElementById("prenom").value;
    const nom = document.getElementById("nom").value;
    const email = document.getElementById("email").value;
    const mobile = document.getElementById("mobile").value;

    const resp = await fetch(`/voyages/${voyage_id}/membres`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({prenom, nom, email, mobile})
    });
    const data = await resp.json();
    document.getElementById("membreResult").textContent = `Membre ajouté : ${data.prenom} ${data.nom} (id=${data.id})`;
});

// --- Ajouter dépense ---
document.getElementById("ajouterDepenseBtn").addEventListener("click", async () => {
    const voyage_id = document.getElementById("voyageSelectDepense").value;
    const description = document.getElementById("desc").value;
    const montant = parseFloat(document.getElementById("montant").value);
    const payeur_id = parseInt(document.getElementById("payeurId").value);

    const resp = await fetch(`/voyages/${voyage_id}/depenses`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({description, montant, payeur_id, voyage_id})
    });
    const data = await resp.json();
    document.getElementById("depenseResult").textContent = `Dépense ajoutée : ${data.description} (${data.montant} €)`;
});

// --- Charger les voyages au démarrage ---
loadVoyages();
