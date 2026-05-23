from config_prompt import SYSTEM_PROMPT, API_URL
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Connexion MongoDB
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["atelier_macs"]
collection = db["reparations"]

# ---- ROUTES API ----

# Créer un nouveau dossier
@app.route("/dossiers", methods=["POST"])
def creer_dossier():
    data = request.json
    data["date_creation"] = datetime.now().isoformat()
    data["statut"] = "Réceptionnée"
    data["historique"] = [{
        "date": datetime.now().isoformat(),
        "statut": "Réceptionnée",
        "commentaire": "Dossier créé"
    }]
    result = collection.insert_one(data)
    return jsonify({"id": str(result.inserted_id), "message": "Dossier créé"}), 201

# Récupérer tous les dossiers
@app.route("/dossiers", methods=["GET"])
def lister_dossiers():
    statut = request.args.get("statut")
    filtre = {"statut": statut} if statut else {}
    dossiers = list(collection.find(filtre, {"_id": 0}))
    return jsonify(dossiers)

# Récupérer un dossier par numéro
@app.route("/dossiers/<numero>", methods=["GET"])
def get_dossier(numero):
    dossier = collection.find_one({"_id": numero}, {"_id": 0})
    if not dossier:
        return jsonify({"erreur": "Dossier introuvable"}), 404
    return jsonify(dossier)

# Mettre à jour un dossier
@app.route("/dossiers/<numero>", methods=["PATCH"])
def modifier_dossier(numero):
    data = request.json
    # Ajouter à l'historique si le statut change
    if "statut" in data:
        nouvelle_entree = {
            "date": datetime.now().isoformat(),
            "statut": data["statut"],
            "commentaire": data.get("commentaire", "Mise à jour")
        }
        collection.update_one(
            {"_id": numero},
            {"$push": {"historique": nouvelle_entree}}
        )
    collection.update_one({"_id": numero}, {"$set": data})
    return jsonify({"message": "Dossier mis à jour"})

# Obtenir les alertes (retards et urgences)
@app.route("/alertes", methods=["GET"])
def get_alertes():
    alertes = []
    today = datetime.now().isoformat()[:10]
    # Dossiers en retard
    en_retard = list(collection.find({
        "conditions_prise_en_charge.date_limite_souhaitee": {"$lt": today},
        "statut": {"$nin": ["Livrée", "Clôturée", "Abandonnée"]}
    }, {"_id": 1, "client.nom": 1, "statut": 1,
        "conditions_prise_en_charge.date_limite_souhaitee": 1}))
    for d in en_retard:
        alertes.append({
            "type": "retard",
            "dossier": d["_id"],
            "client": d.get("client", {}).get("nom", ""),
            "message": f"Date limite dépassée"
        })
    # Dossiers prêts non récupérés
    prets = list(collection.find(
        {"statut": "Terminée — Prête à livrer"},
        {"_id": 1, "client.nom": 1}
    ))
    for d in prets:
        alertes.append({
            "type": "pret_non_retire",
            "dossier": d["_id"],
            "client": d.get("client", {}).get("nom", ""),
            "message": "Machine prête, client non prévenu ou machine non récupérée"
        })
    return jsonify(alertes)

# Tableau de bord
@app.route("/tableau-de-bord", methods=["GET"])
def tableau_de_bord():
    pipeline = [{"$group": {"_id": "$statut", "count": {"$sum": 1}}}]
    stats = list(collection.aggregate(pipeline))
    total = collection.count_documents({})
    return jsonify({"total": total, "par_statut": stats})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
if __name__ == "__main__":
    # Route pour récupérer le prompt système (utilisée par Google AI Studio)
@app.route("/config", methods=["GET"])
def get_config():
    return jsonify({
        "system_prompt": SYSTEM_PROMPT,
        "api_url": API_URL,
        "version": "1.0"
    })
