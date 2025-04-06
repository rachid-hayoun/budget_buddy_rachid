import customtkinter as ctk

class MyApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Fenêtre avec Zone de Texte")
        self.root.geometry("500x400")

        # Créer une zone de texte
        self.textbox = ctk.CTkTextbox(self.root, width=400, height=200)
        self.textbox.place(x=50, y=50)  # Placer la zone de texte à une position spécifique

        # Créer un bouton pour récupérer le texte de la zone de texte
        self.button = ctk.CTkButton(self.root, text="Afficher le texte", command=self.show_text)
        self.button.place(x=200, y=300)

        self.root.mainloop()

    def show_text(self):
        # Récupérer le texte dans la zone de texte
        text = self.textbox.get("1.0", "end-1c")  # "1.0" signifie commencer à la ligne 1, colonne 0
        print("Texte dans la zone :")
        print(text)

# Lancer l'application
app = MyApp()
