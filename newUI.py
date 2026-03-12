import tkinter as tk
import json
import customtkinter

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')

class UserManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("zKSync Combine")

        self.users = {}
        self.selected_actions = []
        self.selected_users = []

        self.user_frame = customtkinter.CTkFrame(self.root)
        self.user_frame.grid(row=0, column=0, padx=5, pady=5)

        self.key_label = customtkinter.CTkLabel(self.user_frame, text="Приватный ключ:")
        self.key_label.grid(row=0, column=0, padx=10, pady=10)

        self.key_entry = customtkinter.CTkEntry(self.user_frame)
        self.key_entry.grid(row=0, column=1, padx=10, pady=10)

        self.add_button = customtkinter.CTkButton(self.user_frame, text="Добавить ключ", command=self.add_key)
        self.add_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.users_listbox = tk.Listbox(self.user_frame, selectmode=customtkinter.MULTIPLE, background='grey')
        self.users_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.show_key_button = customtkinter.CTkButton(self.user_frame, text="Показать ключ", command=self.show_selected_key)
        self.show_key_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.key_display = customtkinter.CTkLabel(self.user_frame, text="", wraplength=300)
        self.key_display.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.bridge_frame = customtkinter.CTkFrame(self.root)
        self.bridge_frame.grid(row=0, column=1, padx=10, pady=10)

        self.bridge_amount_label = customtkinter.CTkLabel(self.bridge_frame, text="Количество Stable coin для бриджа через Orbiter:")
        self.bridge_amount_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.bridge_amount_entry = customtkinter.CTkEntry(self.bridge_frame)
        self.bridge_amount_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.arbitrum_button = customtkinter.CTkButton(self.bridge_frame, text="USDT", command=lambda: self.button_clicked("BRIDGE USDT"))
        self.arbitrum_button.grid(row=3, column=0, padx=10, pady=10)

        self.arbitrum_button = customtkinter.CTkButton(self.bridge_frame, text="USDC", state="disabled")
        self.arbitrum_button.grid(row=3, column=1, padx=10, pady=10)

        self.from_network_label = customtkinter.CTkLabel(self.bridge_frame, text="Выберите из какой сети перевести:")
        self.from_network_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.arbitrum_button = customtkinter.CTkButton(self.bridge_frame, text="Arbitrum", command=lambda: self.button_clicked("From Arbitrum"))
        self.arbitrum_button.grid(row=5, column=0, padx=10, pady=10)

        self.optimism_button = customtkinter.CTkButton(self.bridge_frame, text="Optimism", state="disabled")
        self.optimism_button.grid(row=5, column=1, padx=10, pady=10)

        self.to_network_label = customtkinter.CTkLabel(self.bridge_frame, text="Выберите в какую сеть перевести:")
        self.to_network_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.zksync_button = customtkinter.CTkButton(self.bridge_frame, text="zkSync", command=lambda: self.button_clicked("To zkSync"))
        self.zksync_button.grid(row=7, column=0, padx=10, pady=10)

        self.linea_button = customtkinter.CTkButton(self.bridge_frame, text="Linea", state="disabled")
        self.linea_button.grid(row=7, column=1, padx=10, pady=10)

        self.start_frame = customtkinter.CTkFrame(self.root)
        self.start_frame.grid(row=0, column=2, padx=50, pady=50)

        self.selection_label = customtkinter.CTkLabel(self.start_frame, text=f"Вы выбрали действия: {self.selected_actions}", wraplength=100)
        self.selection_label.pack(padx=10, pady=10, fill="both", expand=True)

        self.users_select_label = customtkinter.CTkLabel(self.start_frame, text=f"От юзеров: {self.selected_users}", wraplength=100)
        self.users_select_label.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.start_button = customtkinter.CTkButton(self.start_frame, text="Начать", command=self.do_orbiter)
        self.start_button.pack(padx=10, pady=10, fill="both", expand=True)

        self.load_users_data() 

    def update_selection_label(self):
        selected_text = "Вы выбрали действия: "
        if self.selected_actions:
            selected_text += ", ".join(self.selected_actions)
        else:
            selected_text += "ничего не выбрано"
        self.selection_label.configure(text=selected_text)
    
    def button_clicked(self, button_text):
        if button_text not in self.selected_actions:
            self.selected_actions.append(button_text)
        else:
            self.selected_actions.remove(button_text)
        self.update_selection_label()
        self.user_selector() 
        self.update_users_select_label()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

    def on_open(self):
        root.update_idletasks()  # убедитесь, что окно создано и обновлено перед определением его размеров
        self.center_window(root, root.winfo_width(), root.winfo_height())

    def add_key(self):
        key = self.key_entry.get()
        if key:
            self.users[f"Пользователь {len(self.users) + 1}"] = key
            self.key_entry.delete(0, tk.END)
            self.update_users_list()
            self.save_users_data()

    def show_selected_key(self):
        selected_indices = self.users_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            selected_user = self.users_listbox.get(index)
            key = self.users[selected_user]
            self.key_display.configure(text=f"Приватный ключ для {selected_user}: {key}")
            self.key_entry.delete(0, tk.END)

    def update_users_list(self):
        self.users_listbox.delete(0, tk.END)
        for user in self.users:
            self.users_listbox.insert(tk.END, user)

    def user_selector(self):
        selected_indices = self.users_listbox.curselection()
        selected_users = [self.users_listbox.get(i) for i in selected_indices]
    
        for user in selected_users:
            if user not in self.selected_users:
                self.selected_users.append(user)

    def update_users_select_label(self):
        selected_users_text = "От юзеров: "
        if self.selected_users:
            selected_users_text += ", ".join(self.selected_users)
        else:
            selected_users_text += "нет выбранных пользователей"
        self.users_select_label.configure(text=selected_users_text)

    def do_orbiter(self):
        selected_indices = self.users_listbox.curselection()
        if selected_indices:
            selected_users = [self.users_listbox.get(i) for i in selected_indices]
            keys = [self.users[user] for user in selected_users]
            bridge_amount = self.bridge_amount_entry.get()
            print(f"Выбранные пользователи: {selected_users}")
            print(f"Приватные ключи: {keys}")
            print(f"Количество USDT для бриджа: {bridge_amount}")

    def save_users_data(self):
        with open("users_data.json", "w") as file:
            json.dump(self.users, file)

    def load_users_data(self):
        try:
            with open("users_data.json", "r") as file:
                self.users = json.load(file)
                self.update_users_list()  # Обновление списка после успешной загрузки
        except FileNotFoundError:
            pass

    def on_closing(self):
        self.save_users_data()
        self.root.destroy()

root = customtkinter.CTk()
app = UserManagementApp(root)
root.bind("<Map>", lambda event: app.on_open())
root.mainloop()
