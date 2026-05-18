from flask import Flask, render_template, jsonify, redirect, url_for
import storage
from tester.runner import run_all_tests

app = Flask(__name__)

@app.route("/")
def index():
    """Redirection par defaut vers le tableau de bord."""
    return redirect(url_for("dashboard"))

@app.route("/run")
def run_tests():
    """
    Declenche l'execution de la suite de tests, 
    enregistre le resultat en base de donnees et retourne la synthese JSON.
    """
    try:
        run_summary = run_all_tests()
        storage.save_run(run_summary)
        return jsonify({
            "status": "success",
            "message": "Run de tests execute et enregistre avec succes.",
            "data": run_summary
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Echec de l'execution du run : {str(e)}"
        }), 500

@app.route("/dashboard")
def dashboard():
    """Affiche le tableau de bord avec l'historique complet des runs."""
    runs_history = storage.list_runs()
    return render_template("dashboard.html", runs=runs_history)

@app.route("/health")
def health_check():
    """
    [BONUS] Point de terminaison de controle de sante (Healthcheck).
    Verifie la connectivite operationnelle avec la base de donnees.
    """
    try:
        # Tentative de lecture simple sur la base de donnees
        storage.list_runs()
        return jsonify({
            "status": "UP",
            "database_connected": True,
            "monitored_api": "Frankfurter API"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "DOWN",
            "database_connected": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    # Execution locale sur le port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
