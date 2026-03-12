from tkinter import Listbox
import customtkinter

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')

def login():
    print("TEST")

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

def on_open():
    root.update_idletasks()  # убедитесь, что окно создано и обновлено перед определением его размеров
    center_window(root, root.winfo_width(), root.winfo_height())

def update_users_list():
    users_listbox.delete(0, customtkinter.END)
    for user in users:
        users_listbox.insert(customtkinter.END, user)

def add_key():
    users = {}
    key = key_entry.get()
    if key:
        users[f"Пользователь {len(users) + 1}"] = key
        key_entry.delete(0, customtkinter.END)
        update_users_list()
        save_users_data()

#------------------------------------------------------UI----------------------------------------------
root = customtkinter.CTk()
root.geometry("800x550")

user_frame = customtkinter.CTkFrame(root)
user_frame.grid(row=0, column=0, padx=5, pady=5)

key_label = customtkinter.CTkLabel(user_frame, text="Приватный ключ:")
key_label.grid(row=0, column=0)

key_entry = customtkinter.CTkEntry(user_frame)
key_entry.grid(row=0, column=1)

add_button = customtkinter.CTkButton(user_frame, text="Добавить ключ", command=add_key)
add_button.grid(row=1, column=0, columnspan=2)

users_listbox = Listbox(user_frame, selectmode=customtkinter.MULTIPLE)
users_listbox.grid(row=2, column=0, columnspan=2)


# frame = customtkinter.CTkFrame(master=root)
# frame.pack(pady=20, padx=60, fill="both", expand=True)

# label = customtkinter.CTkLabel(master=frame, text="Account", font=("Roboto", 24))
# label.pack(pady=12, padx=10)

# entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="UserName")
# entry1.pack(pady=0, padx=0)

# bytton = customtkinter.CTkButton(master=frame, text="Go", command=login)
# bytton.pack(pady=0, padx=0)

root.bind("<Map>", lambda event: on_open())
root.mainloop()