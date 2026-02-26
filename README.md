# 📝 Sticky Note IA

Une petite application de prise de notes qui flotte toujours au-dessus de tes fenêtres, avec un bouton qui envoie ta note à une IA locale pour en faire une fiche de révision propre.

---

## Ce que ça fait

- Une sticky note toujours visible sur ton écran, déplaçable
- Tu écris tes notes en vrac
- Tu cliques sur **📋 Fiche IA** et l'IA te génère une fiche structurée avec les points clés, des exemples, et les pièges à éviter
- Ta note est sauvegardée automatiquement à la fermeture

---

## Installation

### 1. Prérequis

- [Python](https://www.python.org/downloads/) — coche bien **"Add Python to PATH"** pendant l'installation
- [Ollama](https://ollama.com/download) — l'outil qui fait tourner l'IA en local

### 2. Lancer l'installation

Double-clique sur `install.bat` — il installe les librairies Python et télécharge le modèle IA automatiquement (~2 Go, une seule fois).

### 3. Lancer l'app

```
python main.py
```

---

## Stack

- Python
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) pour l'interface
- [Ollama](https://ollama.com) + phi3:mini pour l'IA locale
