import tkinter as tk
from tkinter import ttk, messagebox
import requests
import webbrowser
from ttkbootstrap import Style

def get_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code != 200:
        messagebox.showerror("Error", f"Unable to fetch repositories for user {username}")
        return []
    return response.json()

def display_repositories(event=None):
    username = username_entry.get()
    if not username:
        messagebox.showwarning("Warning", "Please enter a GitHub username")
        return
    
    repos = get_repositories(username)
    
    for i in tree.get_children():
        tree.delete(i)
    
    for repo in repos:
        tree.insert('', 'end', values=(
            repo['name'],
            repo['description'] or 'No description',
            repo['stargazers_count'],
            repo['forks_count']
        ))

def open_repo(event):
    item = tree.selection()[0]
    repo_name = tree.item(item, 'values')[0]
    username = username_entry.get()
    url = f"https://github.com/{username}/{repo_name}"
    webbrowser.open_new(url)

# Create the main window with ttkbootstrap
root = tk.Tk()
style = Style(theme='flatly')
root.title("GitHub Repository Viewer")
root.geometry("1000x600")

# Create main frame
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Create and pack the title label
title_label = ttk.Label(main_frame, text="GitHub Repository Viewer", font=('Helvetica', 24, 'bold'))
title_label.pack(pady=(0, 20))

# Create and pack the input frame
input_frame = ttk.Frame(main_frame)
input_frame.pack(fill=tk.X, pady=(0, 20))

ttk.Label(input_frame, text="Enter GitHub username:", font=('Helvetica', 12)).pack(side=tk.LEFT, padx=(0, 10))
username_entry = ttk.Entry(input_frame, width=30, font=('Helvetica', 12))
username_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
username_entry.bind('<Return>', display_repositories)

search_button = ttk.Button(input_frame, text="Search", command=display_repositories, style='primary.TButton')
search_button.pack(side=tk.LEFT)

# Create and pack the treeview
tree_frame = ttk.Frame(main_frame)
tree_frame.pack(expand=True, fill=tk.BOTH)

tree = ttk.Treeview(tree_frame, columns=('Name', 'Description', 'Stars', 'Forks'), show='headings', style='primary.Treeview')
tree.heading('Name', text='Name')
tree.heading('Description', text='Description')
tree.heading('Stars', text='Stars')
tree.heading('Forks', text='Forks')

tree.column('Name', width=200)
tree.column('Description', width=500)
tree.column('Stars', width=100)
tree.column('Forks', width=100)

tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
tree.bind('<Double-1>', open_repo)

# Add scrollbar to the treeview
scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Status bar
status_var = tk.StringVar()
status_bar = ttk.Label(main_frame, textvariable=status_var, font=('Helvetica', 10))
status_bar.pack(pady=(10, 0))

root.mainloop()