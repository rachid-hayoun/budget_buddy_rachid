import customtkinter
import mysql.connector
import tkinter as tk

class Transac:

    def __init__(self, log_instance, prenom_utilisateur):
        self.log_instance = log_instance
        self.root = log_instance.root
        self.font = log_instance.font
        self.prenom_utilisateur = prenom_utilisateur
        self.db = log_instance.db
        self.cursor = self.db.cursor()
        self.table_frame = None

    def home(self):
        for widget in self.root.winfo_children():
            widget.place_forget()
        self.show_home_page()

    def show_home_page(self):
        self.home_frame = customtkinter.CTkFrame(self.root, width=650, height=325)
        self.home_frame.place(x=25, y=105)

        self.frame_user = customtkinter.CTkFrame(self.root, width=310, height=60)
        self.frame_user.place(x=25, y=20)

        label_user = customtkinter.CTkLabel(
            self.frame_user,
            text=f"Bonjour, {self.prenom_utilisateur} !",
            font=self.font
        )
        label_user.place(relx=0.5, rely=0.5, anchor="center")

        frame_solde = customtkinter.CTkFrame(self.root, width=310, height=60)
        frame_solde.place(relx=1, x=-25, y=20, anchor="ne")

        self.display_balance(frame_solde)
        self.display_transactions(self.home_frame, filter_type="Tous")

    def display_balance(self, frame_solde):
        try:
            self.cursor.execute("SELECT SUM(montant) FROM transaction")
            result = self.cursor.fetchone()
            solde = result[0] if result[0] is not None else 0

            label_solde = customtkinter.CTkLabel(
                frame_solde,
                text=f"Votre solde : {solde:.2f} €",
                font=self.font
            )
            label_solde.place(relx=0.5, rely=0.5, anchor="center")

        except mysql.connector.Error as err:
            print(f"Erreur lors de l'exécution de la requête : {err}")

    def display_transactions(self, frame, filter_type="Tous"):
        if self.table_frame:
            self.table_frame.destroy()

        try:
            if filter_type == "Montant Débit":
                self.cursor.execute("SELECT Reference, Description, Date, Type, Categorie, Montant FROM transaction WHERE Montant >= 0")
            elif filter_type == "Montant Crédit":
                self.cursor.execute("SELECT Reference, Description, Date, Type, Categorie, Montant FROM transaction WHERE Montant < 0")
            else:
                self.cursor.execute("SELECT Reference, Description, Date, Type, Categorie, Montant FROM transaction")

            transactions = self.cursor.fetchall()

            combobox = customtkinter.CTkComboBox(
                frame,
                values=["Tous", "Montant Débit", "Montant Crédit"],
                command=lambda choice: self.display_transactions(frame, filter_type=choice)
            )
            combobox.set(filter_type)
            combobox.place(relx=0.05, rely=0.05)

            self.table_frame = customtkinter.CTkScrollableFrame(frame)
            self.table_frame.place(relx=0.05, rely=0.12, relwidth=0.9, relheight=0.68)

            headers = ["Référence", "Description", "Date", "Type", "Catégorie", "Montant"]

            for col, header in enumerate(headers):
                label = customtkinter.CTkLabel(self.table_frame, text=header, font=("Poppins", 12, "bold"))
                label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

            for row, transaction in enumerate(transactions, start=1):
                for col, value in enumerate(transaction):
                    if col == 5:
                        color = "green" if value >= 0 else "red"
                        label = customtkinter.CTkLabel(
                            self.table_frame,
                            text=f"{value:.2f} €",
                            font=("Poppins", 12),
                            text_color=color
                        )
                    else:
                        label = customtkinter.CTkLabel(
                            self.table_frame,
                            text=str(value),
                            font=("Poppins", 12)
                        )
                    label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            for col in range(len(headers)):
                self.table_frame.grid_columnconfigure(col, weight=1)

            back_button = customtkinter.CTkButton(
                frame,
                text="Déconnexion",
                command=self.show_login_page
            )
            back_button.place(relx=0.5, rely=0.90, anchor="center")  # 15px plus bas

        except mysql.connector.Error as err:
            print(f"Erreur lors de l'exécution de la requête : {err}")

    def show_login_page(self):
        self.home_frame.place_forget()
        self.log_instance.show_login_page()
