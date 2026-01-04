import tkinter as tk
from tkinter import ttk, font, scrolledtext
import sys
import os

# Ensure we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.database import MaterialDatabase
from src.nlp_engine import NLPEngine
from src.recommender import Recommender

class MaterialChatbotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Material Selection Assistant - Pro")
        master.geometry("1000x700")
        
        # Initialize Backend
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, 'data', 'materials.json')
        
        try:
            self.db = MaterialDatabase(data_path)
            self.nlp = NLPEngine()
            self.recommender = Recommender(self.db)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to initialize backend: {e}")
            master.destroy()
            return

        self._configure_styles()
        self._setup_layout()
        self._populate_material_list()
        self._display_welcome()

    def _configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colors
        self.bg_color = "#f0f2f5"
        self.sidebar_color = "#2c3e50"
        self.accent_color = "#27ae60"
        self.text_color = "#333333"
        
        # Configure Frames
        self.style.configure('Main.TFrame', background=self.bg_color)
        self.style.configure('Sidebar.TFrame', background=self.sidebar_color)
        
        # Configure Labels
        self.style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), foreground=self.sidebar_color, background=self.bg_color)
        self.style.configure('SidebarHeader.TLabel', font=('Segoe UI', 12, 'bold'), foreground="white", background=self.sidebar_color)
        
        # Configure Buttons
        self.style.configure('Action.TButton', font=('Segoe UI', 10, 'bold'), background=self.accent_color, foreground="white")
        self.style.map('Action.TButton', background=[('active', '#219150')])

    def _setup_layout(self):
        # Main Container (Split View)
        main_pane = tk.PanedWindow(self.master, orient=tk.HORIZONTAL, bg=self.bg_color, sashwidth=4)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # --- Left Panel: Chat Interface ---
        left_frame = ttk.Frame(main_pane, style='Main.TFrame')
        main_pane.add(left_frame, minsize=500)
        
        # Chat Header
        ttk.Label(left_frame, text="Chat Assistant", style='Header.TLabel').pack(pady=10,padx=10, anchor='w')
        
        # Chat Area
        self.chat_area = scrolledtext.ScrolledText(
            left_frame, 
            state='disabled', 
            wrap='word', 
            font=('Segoe UI', 10),
            bg="white",
            relief="flat",
            padx=10, pady=10
        )
        self.chat_area.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)
        
        self._setup_chat_tags()

        # Input Area
        input_container = ttk.Frame(left_frame, style='Main.TFrame')
        input_container.pack(fill=tk.X, padx=10, pady=10)
        
        self.user_input = ttk.Entry(input_container, font=('Segoe UI', 11))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", self.process_input)
        
        send_btn = ttk.Button(input_container, text="Send", style='Action.TButton', command=self.process_input)
        send_btn.pack(side=tk.RIGHT)

        # --- Right Panel: Material Library/Inspector ---
        right_frame = ttk.Frame(main_pane, style='Sidebar.TFrame')
        main_pane.add(right_frame, minsize=300)
        
        ttk.Label(right_frame, text="Material Library", style='SidebarHeader.TLabel').pack(pady=10, padx=10, anchor='w')
        
        # List of Materials
        list_frame = ttk.Frame(right_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))
        
        self.mat_listbox = tk.Listbox(
            list_frame, 
            bg="#34495e", 
            fg="white", 
            font=('Segoe UI', 10), 
            selectbackground=self.accent_color,
            relief="flat",
            borderwidth=0
        )
        self.mat_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.mat_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.mat_listbox.config(yscrollcommand=scrollbar.set)
        
        self.mat_listbox.bind('<<ListboxSelect>>', self.on_material_select)
        
        # Details Panel (Bottom Right)
        details_frame = ttk.Frame(right_frame, style='Sidebar.TFrame')
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(details_frame, text="Quick Details:", style='SidebarHeader.TLabel').pack(anchor='w')
        
        self.details_text = tk.Text(
            details_frame, 
            height=15, 
            bg="#34495e", 
            fg="#ecf0f1", 
            font=('Segoe UI', 9),
            relief="flat",
            wrap="word",
            padx=5, pady=5
        )
        self.details_text.pack(fill=tk.BOTH, expand=True, pady=5)
        # self.details_text.config(state='disabled') # Keep editable for copy-paste or read-only

    def _setup_chat_tags(self):
        self.chat_area.tag_config("user", foreground="#2980b9", justify="right") # Blue, Right aligned
        self.chat_area.tag_config("bot", foreground="#333333", justify="left")
        self.chat_area.tag_config("title", font=('Segoe UI', 11, 'bold'), foreground="#2c3e50")
        self.chat_area.tag_config("highlight", background="#d4efdf", foreground="#145a32") # Green match
        self.chat_area.tag_config("error", foreground="#c0392b")

    def _populate_material_list(self):
        self.materials = self.db.get_all_materials()
        self.mat_listbox.delete(0, tk.END)
        for mat in self.materials:
            self.mat_listbox.insert(tk.END, mat['name'])

    def on_material_select(self, event):
        selection = self.mat_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        mat_name = self.mat_listbox.get(index)
        mat = self.db.get_material_by_name(mat_name)
        
        if mat:
            self.show_material_details(mat)

    def show_material_details(self, mat):
        self.details_text.config(state='normal')
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, f"{mat['name']}\n", "bold")
        self.details_text.insert(tk.END, f"Type: {mat['type']}\n\n")
        self.details_text.insert(tk.END, "Properties:\n")
        for k, v in mat['properties'].items():
            self.details_text.insert(tk.END, f"- {k}: {v}\n")
        self.details_text.insert(tk.END, f"\nDesc: {mat['description']}\n")
        self.details_text.config(state='disabled')

    def _append_message(self, sender, message, tag):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"\n{sender}: {message}\n", tag)
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def process_input(self, event=None):
        query = self.user_input.get().strip()
        if not query:
            return
        
        self.user_input.delete(0, tk.END)
        self._append_message("You", query, "user")
        
        constraints = self.nlp.process_query(query)
        if not constraints:
            self._append_message("Bot", "I couldn't identify specific properties. Try 'strong', 'light', 'cheap'.", "error")
            return
        
        # Feedback on detection
        self.chat_area.configure(state='normal')
        det_str = ", ".join([f"{k}={v}" for k,v in constraints.items()])
        self.chat_area.insert(tk.END, f"   [Searching for: {det_str}]\n", "bot")
        self.chat_area.configure(state='disabled')

        results = self.recommender.recommend(constraints)
        
        if results:
            top = results[0]
            mat = top['material']
            
            # Select in Sidebar
            self._select_material_in_list(mat['name'])
            
            # Show in Chat
            self.chat_area.configure(state='normal')
            self.chat_area.insert(tk.END, "\nBot: I recommend ", "bot")
            self.chat_area.insert(tk.END, mat['name'] + "\n", "title")
            
            self.chat_area.insert(tk.END, "     Why?\n", "bot")
            for reason in top['reasons']:
                self.chat_area.insert(tk.END, f"     • {reason}\n", "bot")
            
            self.chat_area.insert(tk.END, "\n", "bot")
            self.chat_area.configure(state='disabled')
            self.chat_area.see(tk.END)
        else:
            self._append_message("Bot", "No perfect match found.", "error")

    def _select_material_in_list(self, name):
        # Find index
        idx = -1
        for i, m_name in enumerate(self.mat_listbox.get(0, tk.END)):
            if m_name == name:
                idx = i
                break
        
        if idx != -1:
            self.mat_listbox.selection_clear(0, tk.END)
            self.mat_listbox.selection_set(idx)
            self.mat_listbox.see(idx)
            # Trigger detail view
            self.on_material_select(None)

    def _display_welcome(self):
        self._append_message("Bot", "Welcome! I can help you select materials.\nType requirements like 'lightweight, strong' in the box below.\nOr browse the library on the right.", "bot")

def main():
    root = tk.Tk()
    # Optional: Set icon if available, skipped for now
    app = MaterialChatbotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
