
import sqlite3
import os

def connect_db():
    conn = sqlite3.connect('materiaux.db')
    return conn

def ajouter_materiau():
    nom = input("Nom du matériau: ")
    description = input("Description: ")
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO materiaux (nom, description) VALUES (?, ?)", (nom, description))
    conn.commit()
    conn.close()
    print("Matériau ajouté.")

def lister_materiaux():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM materiaux")
    rows = c.fetchall()
    conn.close()
    for r in rows:
        print(f"ID: {r[0]} | Nom: {r[1]} | Description: {r[2]}")

def creer_chantier():
    nom = input("Nom du chantier: ")
    description = input("Description: ")
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO chantiers (nom, description) VALUES (?, ?)", (nom, description))
    conn.commit()
    conn.close()
    print("Chantier créé.")

def associer_materiaux():
    chantier_id = input("ID du chantier: ")
    lister_materiaux()
    materiau_id = input("ID du matériau à associer: ")
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO chantier_materiaux (chantier_id, materiau_id) VALUES (?, ?)", (chantier_id, materiau_id))
    conn.commit()
    conn.close()
    print("Matériau associé au chantier.")

def lister_materiaux_chantier():
    chantier_id = input("ID du chantier: ")
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
    SELECT m.nom, m.description FROM materiaux m
    JOIN chantier_materiaux cm ON m.id = cm.materiau_id
    WHERE cm.chantier_id = ?""", (chantier_id,))
    rows = c.fetchall()
    conn.close()
    print("Matériaux du chantier:")
    for r in rows:
        print(f"Nom: {r[0]} | Description: {r[1]}")

def associer_plan():
    chantier_id = input("ID du chantier: ")
    plan_path = input("Chemin du fichier de plan: ")
    if not os.path.exists(plan_path):
        print("Fichier introuvable.")
        return
    dest = os.path.join("plans", os.path.basename(plan_path))
    os.rename(plan_path, dest)
    conn = connect_db()
    c = conn.cursor()
    c.execute("UPDATE chantiers SET plan_path = ? WHERE id = ?", (dest, chantier_id))
    conn.commit()
    conn.close()
    print("Plan associé au chantier.")

def menu():
    while True:
        print("""
1. Ajouter un matériau
2. Lister les matériaux
3. Créer un chantier
4. Associer un matériau à un chantier
5. Lister les matériaux d'un chantier
6. Associer un fichier de plan à un chantier
7. Quitter""")
        choix = input("Choix: ")
        if choix == "1":
            ajouter_materiau()
        elif choix == "2":
            lister_materiaux()
        elif choix == "3":
            creer_chantier()
        elif choix == "4":
            associer_materiaux()
        elif choix == "5":
            lister_materiaux_chantier()
        elif choix == "6":
            associer_plan()
        elif choix == "7":
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    menu()
