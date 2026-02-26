import customtkinter as ctk
import threading
import os
import ia

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

FICHIER_NOTE = os.path.join(os.path.dirname(__file__), "note.txt")

COULEUR_FOND       = "#2B2B2B"
COULEUR_TITRE      = "#1E1E1E"
COULEUR_TEXTE      = "#F5F5DC"
COULEUR_BOUTON     = "#F0C040"
COULEUR_BTN_HOVER  = "#E0A800"
COULEUR_BTN_FERMER = "#FF5F5F"


class StickyNote(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("")
        self.geometry("340x420")
        self.resizable(True, True)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color=COULEUR_FOND)
        self.attributes("-alpha", 0.96)

        self._drag_x = 0
        self._drag_y = 0

        self._construire_interface()
        self._charger_note()
        self._verifier_ollama_en_arriere_plan()

        self.protocol("WM_DELETE_WINDOW", self._fermer)

    def _construire_interface(self):
        self.barre = ctk.CTkFrame(self, fg_color=COULEUR_TITRE, height=36, corner_radius=0)
        self.barre.pack(fill="x")
        self.barre.pack_propagate(False)

        self.label_titre = ctk.CTkLabel(
            self.barre,
            text="  📝  Sticky Note IA",
            text_color=COULEUR_TEXTE,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        self.label_titre.pack(side="left", padx=8, fill="x", expand=True)

        self.btn_fermer = ctk.CTkButton(
            self.barre,
            text="✕",
            width=32,
            height=28,
            fg_color="transparent",
            hover_color=COULEUR_BTN_FERMER,
            text_color=COULEUR_TEXTE,
            font=ctk.CTkFont(size=13),
            command=self._fermer,
            corner_radius=0
        )
        self.btn_fermer.pack(side="right", padx=2)

        for widget in [self.barre, self.label_titre]:
            widget.bind("<ButtonPress-1>", self._debut_drag)
            widget.bind("<B1-Motion>", self._pendant_drag)

        self.zone_texte = ctk.CTkTextbox(
            self,
            fg_color="#333333",
            text_color=COULEUR_TEXTE,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            corner_radius=8,
            border_width=0,
            wrap="word"
        )
        self.zone_texte.pack(fill="both", expand=True, padx=12, pady=(10, 6))

        self.zone_texte.insert("1.0", "Écris ta note ici...")
        self.zone_texte.bind("<FocusIn>", self._effacer_placeholder)
        self._placeholder_actif = True

        self.frame_bas = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_bas.pack(fill="x", padx=12, pady=(0, 12))

        self.label_statut = ctk.CTkLabel(
            self.frame_bas,
            text="",
            text_color="#AAAAAA",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self.label_statut.pack(side="left", fill="x", expand=True)

        self.btn_fiche = ctk.CTkButton(
            self.frame_bas,
            text="📋  Fiche IA",
            fg_color=COULEUR_BOUTON,
            hover_color=COULEUR_BTN_HOVER,
            text_color="#1A1A1A",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            height=34,
            width=120,
            command=self._lancer_ia
        )
        self.btn_fiche.pack(side="right")

    def _debut_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _pendant_drag(self, event):
        delta_x = event.x - self._drag_x
        delta_y = event.y - self._drag_y
        nouveau_x = self.winfo_x() + delta_x
        nouveau_y = self.winfo_y() + delta_y
        self.geometry(f"+{nouveau_x}+{nouveau_y}")

    def _effacer_placeholder(self, event):
        if self._placeholder_actif:
            self.zone_texte.delete("1.0", "end")
            self._placeholder_actif = False

    def _get_texte(self):
        texte = self.zone_texte.get("1.0", "end-1c").strip()
        if texte == "Écris ta note ici...":
            return ""
        return texte

    def _verifier_ollama_en_arriere_plan(self):
        def verif():
            if not ia.ollama_est_lance():
                self.label_statut.configure(text="⚠️ Ollama non détecté", text_color="#FF8C00")
            else:
                ia.telecharger_modele_si_besoin()
                self.label_statut.configure(text="✅ IA prête", text_color="#6BCB77")

        threading.Thread(target=verif, daemon=True).start()

    def _lancer_ia(self):
        texte = self._get_texte()

        if not texte:
            self.label_statut.configure(text="Écris quelque chose d'abord !", text_color="#FF8C00")
            return

        if not ia.ollama_est_lance():
            self.label_statut.configure(text="Lance Ollama d'abord → ollama.com", text_color="#FF5F5F")
            return

        self.btn_fiche.configure(state="disabled", text="⏳  En cours...")
        self.label_statut.configure(text="L'IA améliore ta note...", text_color="#AAAAAA")

        def tache_ia():
            resultat = ia.ameliorer_note(texte)
            self.after(0, lambda: self._afficher_resultat(resultat))

        threading.Thread(target=tache_ia, daemon=True).start()

    def _afficher_resultat(self, texte_ameliore):
        self.zone_texte.delete("1.0", "end")
        self.zone_texte.insert("1.0", texte_ameliore)
        self._placeholder_actif = False

        self.btn_fiche.configure(state="normal", text="📋  Fiche IA")
        self.label_statut.configure(text="✨ Note améliorée !", text_color="#6BCB77")

        self._sauvegarder_note()

    def _sauvegarder_note(self):
        texte = self._get_texte()
        try:
            with open(FICHIER_NOTE, "w", encoding="utf-8") as f:
                f.write(texte)
        except Exception as e:
            print(f"Impossible de sauvegarder : {e}")

    def _charger_note(self):
        if os.path.exists(FICHIER_NOTE):
            try:
                with open(FICHIER_NOTE, "r", encoding="utf-8") as f:
                    contenu = f.read().strip()
                if contenu:
                    self.zone_texte.delete("1.0", "end")
                    self.zone_texte.insert("1.0", contenu)
                    self._placeholder_actif = False
            except Exception as e:
                print(f"Impossible de charger la note : {e}")

    def _fermer(self):
        self._sauvegarder_note()
        self.destroy()


if __name__ == "__main__":
    app = StickyNote()
    app.mainloop()
