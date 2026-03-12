import tkinter as tk
import json

class UserManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление приватными ключами")

        self.users = {}

        self.user_frame = tk.Frame(self.root)
        self.user_frame.grid(row=0, column=0, padx=5, pady=5)

        self.key_label = tk.Label(self.user_frame, text="Приватный ключ:")
        self.key_label.grid(row=0, column=0)

        self.key_entry = tk.Entry(self.user_frame)
        self.key_entry.grid(row=0, column=1)

        self.add_button = tk.Button(self.user_frame, text="Добавить ключ", command=self.add_key)
        self.add_button.grid(row=1, column=0, columnspan=2)

        self.users_listbox = tk.Listbox(self.user_frame, selectmode=tk.MULTIPLE)
        self.users_listbox.grid(row=2, column=0, columnspan=2)

        self.show_key_button = tk.Button(self.user_frame, text="Показать ключ", command=self.show_selected_key)
        self.show_key_button.grid(row=3, column=0, columnspan=2)

        self.key_display = tk.Label(self.user_frame, text="", wraplength=300)
        self.key_display.grid(row=5, column=0, columnspan=2)

        self.bridge_frame = tk.Frame(self.root)
        self.bridge_frame.grid(row=0, column=1, padx=5, pady=5)

        self.bridge_amount_label = tk.Label(self.bridge_frame, text="Количество Stable coin для бриджа через Orbiter:")
        self.bridge_amount_label.grid(row=0, column=0, columnspan=2)

        self.bridge_amount_entry = tk.Entry(self.bridge_frame)
        self.bridge_amount_entry.grid(row=1, column=0, columnspan=2)

        self.arbitrum_button = tk.Button(self.bridge_frame, text="USDT", command=self.select_arbitrum, relief=tk.RAISED)
        self.arbitrum_button.grid(row=3, column=0)

        self.arbitrum_button = tk.Button(self.bridge_frame, text="USDC", command=self.select_arbitrum, relief=tk.RAISED)
        self.arbitrum_button.grid(row=3, column=1)

        self.from_network_label = tk.Label(self.bridge_frame, text="Выберите из какой сети перевести:")
        self.from_network_label.grid(row=4, column=0, columnspan=2)

        self.arbitrum_button = tk.Button(self.bridge_frame, text="Arbitrum", command=self.select_arbitrum, relief=tk.RAISED)
        self.arbitrum_button.grid(row=5, column=0)

        self.optimism_button = tk.Button(self.bridge_frame, text="Optimism", command=self.select_optimism, relief=tk.RAISED)
        self.optimism_button.grid(row=5, column=1)

        self.to_network_label = tk.Label(self.bridge_frame, text="Выберите в какую сеть перевести:")
        self.to_network_label.grid(row=6, column=0, columnspan=2)

        self.zksync_button = tk.Button(self.bridge_frame, text="zkSync", command=self.select_zksync, relief=tk.RAISED)
        self.zksync_button.grid(row=7, column=0)

        self.linea_button = tk.Button(self.bridge_frame, text="Linea", command=self.select_linea, relief=tk.RAISED)
        self.linea_button.grid(row=7, column=1)

        self.start_frame = tk.Frame(self.root)
        self.start_frame.grid(row=0, column=2, padx=5, pady=5)

        self.start_button = tk.Button(self.start_frame, text="Начать", command=self.do_orbiter)
        self.start_button.pack()

        self.load_users_data()

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
            self.key_display.config(text=f"Приватный ключ для {selected_user}: {key}")
            self.key_entry.delete(0, tk.END)

    def update_users_list(self):
        self.users_listbox.delete(0, tk.END)
        for user in self.users:
            self.users_listbox.insert(tk.END, user)

    def do_orbiter(self):
        selected_indices = self.users_listbox.curselection()
        if selected_indices:
            selected_users = [self.users_listbox.get(i) for i in selected_indices]
            keys = [self.users[user] for user in selected_users]
            bridge_amount = self.bridge_amount_entry.get()
            from_network = self.get_selected_network(self.arbitrum_button, self.optimism_button)
            to_network = self.get_selected_network(self.zksync_button, self.linea_button)
            print(f"Выбранные пользователи: {selected_users}")
            print(f"Приватные ключи: {keys}")
            print(f"Количество USDT для бриджа: {bridge_amount}")
            print(f"Из сети: {from_network}")
            print(f"В сеть: {to_network}")

    def select_arbitrum(self):
        self.arbitrum_button.config(relief=tk.SUNKEN)
        self.optimism_button.config(relief=tk.RAISED)

    def select_optimism(self):
        self.arbitrum_button.config(relief=tk.RAISED)
        self.optimism_button.config(relief=tk.SUNKEN)

    def select_zksync(self):
        self.zksync_button.config(relief=tk.SUNKEN)
        self.linea_button.config(relief=tk.RAISED)

    def select_linea(self):
        self.zksync_button.config(relief=tk.RAISED)
        self.linea_button.config(relief=tk.SUNKEN)

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

    def get_selected_network(self, button1, button2):
        if button1.cget("relief") == tk.SUNKEN:
            return button1["text"]
        elif button2.cget("relief") == tk.SUNKEN:
            return button2["text"]
        else:
            return ""

root = tk.Tk()
app = UserManagementApp(root)
root.mainloop()
