import requests
import subprocess

OLLAMA_URL = "http://localhost:11434"
MODELE = "phi3:mini"

def ollama_est_lance():
    try:
        reponse = requests.get(OLLAMA_URL, timeout=3)
        return reponse.status_code == 200
    except:
        return False

def telecharger_modele_si_besoin():
    try:
        reponse = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        modeles_dispo = [m["name"] for m in reponse.json().get("models", [])]
        if not any(MODELE in m for m in modeles_dispo):
            subprocess.run(["ollama", "pull", MODELE], check=True)
    except Exception as e:
        print(f"Erreur modele : {e}")

def ameliorer_note(texte_brut):
    prompt = f"""Tu es un assistant qui transforme des prises de notes brutes en fiches de révision claires et utiles.

À partir du texte ci-dessous, génère une fiche structurée avec :
- Un titre court qui résume le sujet
- Une section "Ce qu'il faut retenir" avec les points clés en tirets
- Une section "Exemples" si des exemples sont pertinents (sinon omets-la)
- Une section "À ne pas confondre" ou "Attention" si il y a des pièges ou nuances importantes (sinon omets-la)

Règles :
- Utilise des tirets pour chaque point, pas de paragraphes
- Sois précis et concis, garde uniquement ce qui est utile
- Écris de façon naturelle, comme si un bon élève avait réécrit ses notes
- Ne rajoute rien qui ne vient pas des notes originales

Notes originales :
{texte_brut}

Fiche :"""

    try:
        reponse = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODELE,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        data = reponse.json()
        return data.get("response", "").strip()
    except requests.exceptions.ConnectionError:
        return "Ollama n'est pas lance. Lance Ollama et reessaie."
    except requests.exceptions.Timeout:
        return "L'IA a mis trop de temps a repondre. Reessaie dans un moment."
    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}"
