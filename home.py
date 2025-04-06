import customtkinter
import mysql.connector
from tkinter import messagebox
import re
import hashlib
from transac import Transac

class Db():
    def __init__(self):
        try:
            self.db = mysql.connector.connect(host="localhost", user="root", password="rachidsql", database="banquebis")
            self.cursor = self.db.cursor()
            print("Connexion BDD : ✅")
        except mysql.connector.Error as err:
            print(f"Connexion BDD : ❌ - {err}")

class Log(Db):
    def __init__(self):
        super().__init__()
        self.font = ("Verdana", 23, "bold")
        self.root = None 
        self.screen()

    def screen(self):
        self.root = customtkinter.CTk()
        self.root.title("Ma Banque")
        self.root.geometry("700x450")
        self.root.configure(fg_color="black")
        customtkinter.set_default_color_theme("blue")
        self.frame()
        self.label()
        self.entry()
        self.submit()

    def frame(self):
        self.main_frame = customtkinter.CTkFrame(self.root, width=650, height=70)
        self.main_frame.place(x=25, y=15)
        self.inscription = customtkinter.CTkFrame(self.root, width=315, height=325)
        self.inscription.place(x=25, y=105)
        self.connexion = customtkinter.CTkFrame(self.root, width=315, height=325)
        self.connexion.place(x=360, y=105)

    def label(self):
        self.titre = customtkinter.CTkLabel(self.main_frame, text="Bienvenue chez vous !", font=self.font)
        self.titre.place(relx=0.5, rely=0.5, anchor="center")
        self.inscription_label = customtkinter.CTkLabel(self.inscription, text="Inscription", font=self.font)
        self.inscription_label.place(relx=0.5, rely=0.05, anchor="n")
        self.connexion_label = customtkinter.CTkLabel(self.connexion, text="Connexion", font=self.font)
        self.connexion_label.place(relx=0.5, rely=0.05, anchor="n")

    def entry(self):
        self.nom = customtkinter.CTkEntry(self.inscription, placeholder_text="Nom", width=220, height=35, )
        self.nom.place(relx=0.5, rely=0.2, anchor="n")
        self.prenom = customtkinter.CTkEntry(self.inscription, placeholder_text="Prénom", width=220, height=35)
        self.prenom.place(relx=0.5, rely=0.35, anchor="n")
        self.mail = customtkinter.CTkEntry(self.inscription, placeholder_text="Mail", width=220, height=35)
        self.mail.place(relx=0.5, rely=0.5, anchor="n")
        self.mdp = customtkinter.CTkEntry(self.inscription, placeholder_text="Créer un mot de passe", width=220, height=35, show="*")
        self.mdp.place(relx=0.5, rely=0.65, anchor="n")
        self.mail_connexion = customtkinter.CTkEntry(self.connexion, placeholder_text="Entrez votre Mail", width=220, height=35)
        self.mail_connexion.place(relx=0.5, rely=0.25, anchor="n")
        self.mdp_connexion = customtkinter.CTkEntry(self.connexion, placeholder_text="Entrez votre mot de passe", width=220, height=35, show="*")
        self.mdp_connexion.place(relx=0.5, rely=0.5, anchor="n")

    def submit(self):
        self.inscription_submit = customtkinter.CTkButton(self.inscription, text="M'inscrire", fg_color="green", width=150, height=30, font=("Verdana", 17, "bold"),command=self.insert_info)
        self.inscription_submit.place(relx=0.25, rely=0.825)
        self.connexion_submit = customtkinter.CTkButton(self.connexion, text="Valider", fg_color="green", width=150, height=30, font=("Verdana", 17, "bold"),command=self.verify_login)
        self.connexion_submit.place(relx=0.25, rely=0.825)

    def insert_info(self):
        nom = self.nom.get()
        prenom = self.prenom.get()
        mail = self.mail.get()
        mdp = self.mdp.get()

        if not self.validate_password(mdp):
            return

        hashed_password = hashlib.sha256(mdp.encode()).hexdigest()

        try:
            self.cursor.execute(
                "INSERT INTO user (Nom, Prenom, Email, Mot_De_Passe) VALUES (%s, %s, %s, %s)",(nom, prenom, mail, hashed_password))
            self.db.commit()
            messagebox.showinfo("Succès", "Inscription réussie !")
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur lors de l'insertion dans la base de données : {err}")

    def show_login_page(self):
        for widget in self.root.winfo_children():
            widget.place_forget()
        
        self.frame()
        self.label()
        self.entry()
        self.submit()

    def verify_login(self):
        mail = self.mail_connexion.get() 
        mdp = self.mdp_connexion.get()    

        try:
            if not mdp:
                messagebox.showerror("Erreur", "Le champ mot de passe est vide.")
                return
            hashed_password = hashlib.sha256(mdp.encode()).hexdigest()

            self.cursor.execute(
                "SELECT Prenom FROM user WHERE Email = %s AND Mot_De_Passe = %s", 
                (mail, hashed_password))
            result = self.cursor.fetchone()

            if result:
                prenom_utilisateur = result[0] 
                transac = Transac(self, prenom_utilisateur) 
                transac.home()
            else:
                messagebox.showerror("Erreur", "Email ou mot de passe incorrect")
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur lors de la vérification : {err}")

    def validate_password(self, password):
        if len(password) < 10:
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 10 caractères.")
            return False
        if not re.search(r"[a-z]", password):
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins une minuscule.")
            return False
        if not re.search(r"[A-Z]", password):
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins une majuscule.")
            return False
        if not re.search(r"[0-9]", password):
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins un chiffre.")
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins un caractère spécial.")
            return False
        return True

