
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import sqlite3
import os
import shutil

DB_FILE = "materiaux.db"

def connect_db():
    return sqlite3.connect(DB_FILE)

class MELECApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MELEC Software")
        self.create_widgets()
        self.load_materiaux()
        self.load_chantiers()

    def create_widgets(self):
        # Frame matériaux
        frame_mat = ttk.LabelFrame(self.root, text="Matériaux")
        frame_mat.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.materiaux_listbox = tk.Listbox(frame_mat, width=50)
        self.materiaux_listbox.pack(padx=5, pady=5)

        btn_ajouter_mat = ttk.Button(frame_mat, text="Ajouter Matériau", command=self.ajouter_materiau)
        btn_ajouter_mat.pack(padx=5, pady=5)

        btn_modifier_mat = ttk.Button(frame_mat, text="Modifier Matériau", command=self.modifier_materiau)
        btn_modifier_mat.pack(padx=5, pady=5)

        btn_supprimer_mat = ttk.Button(frame_mat, text="Supprimer Matériau", command=self.supprimer_materiau)
        btn_supprimer_mat.pack(padx=5, pady=5)

        # Frame chantiers
        frame_chantier = ttk.LabelFrame(self.root, text="Chantiers")
        frame_chantier.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.chantiers_listbox = tk.Listbox(frame_chantier, width=50)
        self.chantiers_listbox.pack(padx=5, pady=5)

        btn_ajouter_chantier = ttk.Button(frame_chantier, text="Créer Chantier", command=self.ajouter_chantier)
        btn_ajouter_chantier.pack(padx=5, pady=5)

        btn_associer = ttk.Button(frame_chantier, text="Associer Matériau", command=self.associer_materiau)
        btn_associer.pack(padx=5, pady=5)

        btn_ajouter_plan = ttk.Button(frame_chantier, text="Associer Plan", command=self.associer_plan)
        btn_ajouter_plan.pack(padx=5, pady=5)

        btn_voir_mat = ttk.Button(frame_chantier, text="Voir Matériaux", command=self.voir_materiaux_chantier)
        btn_voir_mat.pack(padx=5, pady=5)

    def load_materiaux(self):
        self.materiaux_listbox.delete(0, tk.END)
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT id, nom, reference, quantite FROM materiaux")
        for row in c.fetchall():
            self.materiaux_listbox.insert(tk.END, f"{row[0]} - {row[1]} (Réf: {row[2]}, Qté: {row[3]})")
        conn.close()

    def load_chantiers(self):
        self.chantiers_listbox.delete(0, tk.END)
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT id, nom FROM chantiers")
        for row in c.fetchall():
            self.chantiers_listbox.insert(tk.END, f"{row[0]} - {row[1]}")
        conn.close()

    def ajouter_materiau(self):
        nom = simpledialog.askstring("Nom", "Nom du matériau:")
        ref = simpledialog.askstring("Référence", "Code de référence:")
        qte = simpledialog.askinteger("Quantité", "Quantité:")
        desc = simpledialog.askstring("Description", "Description:")
        if nom and ref and qte is not None and qte >= 0:
            conn = connect_db()
            c = conn.cursor()
            c.execute("INSERT INTO materiaux (nom, reference, quantite, description) VALUES (?, ?, ?, ?)",
                      (nom, ref, qte, desc))
            conn.commit()
            conn.close()
            self.load_materiaux()
            messagebox.showinfo("Succès", "Matériau ajouté.")

    def modifier_materiau(self):

        mat_sel = self.materiaux_listbox.get(tk.ACTIVE)
        if mat_sel:
            mat_id = mat_sel.split(" - ")[0]
            conn = connect_db()
            c = conn.cursor()
            c.execute("SELECT nom, reference, quantite, description FROM materiaux WHERE id=?", (mat_id,))
            mat = c.fetchone()
            conn.close()

            if mat:
                new_nom = simpledialog.askstring("Nom", "Nouveau nom:", initialvalue=mat[0])
                new_ref = simpledialog.askstring("Référence", "Nouveau code de référence:", initialvalue=mat[1])
                new_qte = simpledialog.askinteger("Quantité", "Nouvelle quantité:", initialvalue=mat[2])
                new_desc = simpledialog.askstring("Description", "Nouvelle description:", initialvalue=mat[3])

                if new_nom and new_ref and new_qte is not None and new_qte >= 0:
                    conn = connect_db()
                    c = conn.cursor()
                    c.execute("UPDATE materiaux SET nom=?, reference=?, quantite=?, description=? WHERE id=?",
                              (new_nom, new_ref, new_qte, new_desc, mat_id))
                    conn.commit()
                    conn.close()
                    self.load_materiaux()
                    messagebox.showinfo("Succès", "Matériau modifié.")
                else:
                    messagebox.showwarning("Erreur", "Valeurs invalides.")
            else:
                messagebox.showwarning("Erreur", "Matériau introuvable.")
        else:
            messagebox.showwarning("Erreur", "Sélectionnez un matériau.")
        mat_sel = self.materiaux_listbox.get(tk.ACTIVE)
        if mat_sel:
            mat_id = mat_sel.split(" - ")[0]
            new_nom = simpledialog.askstring("Nouveau nom", "Nouveau nom:")
            new_ref = simpledialog.askstring("Nouvelle référence", "Nouveau code de référence:")
            new_qte = simpledialog.askinteger("Nouvelle quantité", "Nouvelle quantité:")
            new_desc = simpledialog.askstring("Nouvelle description", "Nouvelle description:")
            if new_nom and new_ref and new_qte is not None and new_qte >= 0:
                conn = connect_db()
                c = conn.cursor()
                c.execute("UPDATE materiaux SET nom=?, reference=?, quantite=?, description=? WHERE id=?",
                          (new_nom, new_ref, new_qte, new_desc, mat_id))
                conn.commit()
                conn.close()
                self.load_materiaux()
                messagebox.showinfo("Succès", "Matériau modifié.")
        else:
            messagebox.showwarning("Erreur", "Sélectionnez un matériau.")

    def supprimer_materiau(self):
        mat_sel = self.materiaux_listbox.get(tk.ACTIVE)
        if mat_sel:
            mat_id = mat_sel.split(" - ")[0]
            confirm = messagebox.askyesno("Confirmer", "Supprimer ce matériau ?")
            if confirm:
                conn = connect_db()
                c = conn.cursor()
                c.execute("DELETE FROM materiaux WHERE id=?", (mat_id,))
                conn.commit()
                conn.close()
                self.load_materiaux()
                messagebox.showinfo("Succès", "Matériau supprimé.")
        else:
            messagebox.showwarning("Erreur", "Sélectionnez un matériau.")

    # Les fonctions pour chantiers (inchangées pour le moment)

    def ajouter_chantier(self):
        nom = simpledialog.askstring("Nom", "Nom du chantier:")
        desc = simpledialog.askstring("Description", "Description:")
        if nom:
            conn = connect_db()
            c = conn.cursor()
            c.execute("INSERT INTO chantiers (nom, description) VALUES (?, ?)", (nom, desc))
            conn.commit()
            conn.close()
            self.load_chantiers()
            messagebox.showinfo("Succès", "Chantier créé.")

    def associer_materiau(self):
        chantier_sel = self.chantiers_listbox.get(tk.ACTIVE)
        mat_sel = self.materiaux_listbox.get(tk.ACTIVE)
        if chantier_sel and mat_sel:
            chantier_id = chantier_sel.split(" - ")[0]
            mat_id = mat_sel.split(" - ")[0]
            conn = connect_db()
            c = conn.cursor()
            c.execute("INSERT INTO chantier_materiaux (chantier_id, materiau_id) VALUES (?, ?)", (chantier_id, mat_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Matériau associé au chantier.")
        else:
            messagebox.showwarning("Erreur", "Sélectionnez un chantier et un matériau.")

    def associer_plan(self):
        chantier_sel = self.chantiers_listbox.get(tk.ACTIVE)
        if chantier_sel:
            chantier_id = chantier_sel.split(" - ")[0]
            filepath = filedialog.askopenfilename(title="Choisir un plan")
            if filepath:
                dest = os.path.join("plans", os.path.basename(filepath))
                shutil.copy(filepath, dest)
                conn = connect_db()
                c = conn.cursor()
                c.execute("UPDATE chantiers SET plan_path = ? WHERE id = ?", (dest, chantier_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Succès", "Plan associé au chantier.")
        else:
            messagebox.showwarning("Erreur", "Sélectionnez un chantier.")

    def voir_materiaux_chantier(self):
        chantier_sel = self.chantiers_listbox.get(tk.ACTIVE)
        if chantier_sel:
            chantier_id = chantier_sel.split(" - ")[0]
            conn = connect_db()
            c = conn.cursor()
            c.execute("""
            SELECT m.nom, m.reference, m.quantite FROM materiaux m
            JOIN chantier_materiaux cm ON m.id = cm.materiau_id
            WHERE cm.chantier_id = ?""", (chantier_id,))
            rows = c.fetchall()
            conn.close()
            if rows:
                materiaux = "\n".join([f"{r[0]} (Réf: {r[1]}, Qté: {r[2]})" for r in rows])
                messagebox.showinfo("Matériaux du chantier", materiaux)
            else:
                messagebox.showinfo("Matériaux du chantier", "Aucun matériau associé.")
        else:
            messagebox.showwarning("Erreur", "Sélectionnez un chantier.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MELECApp(root)
    root.mainloop()
