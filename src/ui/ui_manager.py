import tkinter as tk
from tkinter import ttk
from app_manager import AppManager


class CustomerFurnitureApp:
    def __init__(self, root, session):
        self.session = session
        self.am = AppManager(self.session)

        self.root = root
        self.root.title("Furniture data manager")

        # Application size in pixels
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()- 80
        self.root.geometry("%dx%d+0+0" % (width, height))

        # Grid layout (2 columns, 3 rows)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)

        self.sidebar_frame = tk.Frame(self.root)
        self.sidebar_frame.grid(column=0, row=0, rowspan=3, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(0, weight=0)
        self.sidebar_frame.grid_rowconfigure(1, weight=1)
        self.sidebar_frame.grid_rowconfigure(2, weight=0)

        self.data_frame = tk.Frame(self.root)
        self.data_frame.grid(column=1, row=0, rowspan=2, sticky="nsew")
        self.input_frame = tk.Frame(self.root)
        self.input_frame.grid(column=1, row=2, sticky="nsew")
        self.input_frame.grid_columnconfigure((0,1,2), weight=1)

        FONT_SIZE = 18
        
        # ---------------------
        # SIDEBAR FRAME
        # ---------------------

        self.search_entry = EntryWithPlaceholder(self.sidebar_frame, placeholder="Search Customer", font_size=14, foreground="grey")
        self.search_entry.grid(column=0, row=0, padx=5, pady= 15)
        self.customer_listbox = tk.Listbox(self.sidebar_frame, bg="#CCCCCC", borderwidth=0, highlightthickness=0)
        self.customer_listbox.grid(column=0, row=1, padx=5, sticky="nsew")
        self.add_customer_frame = tk.Frame(self.sidebar_frame)
        self.add_customer_frame.grid(column=0, row=2, padx=5, pady=15, sticky="nsew")
        self.name_label = tk.Label(self.add_customer_frame, text="Name", font=FONT_SIZE)
        self.name_label.grid(column=0, row=0, sticky="ew")
        self.name_entry = tk.Entry(self.add_customer_frame, font=FONT_SIZE)
        self.name_entry.grid(column=1, row=0, padx=10, sticky="ew")
        self.surname_label = tk.Label(self.add_customer_frame, text="Surname", font=FONT_SIZE)
        self.surname_label.grid(column=0, row=1, pady=10, sticky="ew")
        self.surname_entry = tk.Entry(self.add_customer_frame, font=FONT_SIZE)
        self.surname_entry.grid(column=1, row=1, padx=10, sticky="ew")
        self.save_customer_button = tk.Button(self.add_customer_frame, text="Add customer", font=FONT_SIZE, state=tk.DISABLED)
        self.save_customer_button.grid(column=0, row=3, columnspan=2, padx=10, sticky="ew")
        self.rename_button = tk.Button(self.add_customer_frame, text="Rename", font=FONT_SIZE, state=tk.DISABLED)
        self.rename_button.grid(column=0, row=4, columnspan=2, padx=10, pady=(10, 0), sticky="ew")
        self.customer_menu = tk.Menu(self.root, tearoff=False)
        self.customer_menu.add_command(label="Rename", command=lambda: self.am.prepare_customer_rename_ui(self.name_entry, self.surname_entry, self.save_customer_button, self.rename_button))
        self.customer_menu.add_command(label="Delete", command=lambda: self.am.confirm_customer_deletion(self.customer_listbox, self.full_name_label, self.project_combobox, self.tree, self.total_price_label))
        
        
        # ---------------------
        # DATA FRAME
        # ---------------------

        columns = ("family", "description", "sernumber", "amount", "price", "url")
        self.tree = ttk.Treeview(self.data_frame, columns=columns, show='headings')
        self.tree.heading("family", text="Family")
        self.tree.column("family", width=30)
        self.tree.heading("description", text="Description")
        self.tree.column("description", width=300)
        self.tree.heading("sernumber", text="Serial number")
        self.tree.column("sernumber", width=50)
        self.tree.heading("amount", text="Amount")
        self.tree.column("amount", width=10)
        self.tree.heading("price", text="Price")
        self.tree.column("price", width=30)
        self.tree.heading("url", text="URL")
        self.tree.column("url", width=350)

        self.tree.pack(expand=True, fill="both")

        self.tree_menu = tk.Menu(self.root, tearoff=False)
        self.tree_menu.add_command(label="Delete", command="delete")

        # ---------------------
        # CUSTOM FURNITURE FRAME
        # ---------------------

        self.custom_furniture_frame = tk.Frame(self.input_frame, bg="light grey")
        self.custom_furniture_frame.grid(column=0, row=0, sticky="nsew")
        self.custom_furniture_frame.grid_columnconfigure((0,1), weight=1)
        self.custom_furniture_frame.grid_rowconfigure((0,1,2,3),weight= 1)
        self.custom_furniture_label = tk.Label(self.custom_furniture_frame, text="Custom furniture", font=FONT_SIZE, bg="light grey")
        self.custom_furniture_label.grid(column=0, row=0, columnspan=2, padx=10, pady=10)
        self.custom_furname_label = tk.Label(self.custom_furniture_frame, text="Furniture name", font=FONT_SIZE, bg="light grey")
        self.custom_furname_label.grid(column=0, row=1, padx=10)
        self.custom_furname_entry = tk.Entry(self.custom_furniture_frame, font=FONT_SIZE)
        self.custom_furname_entry.grid(column=1, row=1, padx=(0, 10), pady=10)
        self.custom_furdescription_label = tk.Label(self.custom_furniture_frame, text="Product description", font=FONT_SIZE, bg="light grey")
        self.custom_furdescription_label.grid(column=0, row=2, padx=10)
        self.custom_furdescription_entry = tk.Entry(self.custom_furniture_frame, font=FONT_SIZE)
        self.custom_furdescription_entry.grid(column=1, row=2, padx=(0, 10), pady=10)
        self.custom_furamout_label = tk.Label(self.custom_furniture_frame, text="Product amount", font=FONT_SIZE, bg="light grey")
        self.custom_furamout_label.grid(column=0, row=3, padx=10)
        self.custom_furamount_spinbox = tk.Spinbox(self.custom_furniture_frame, font=FONT_SIZE, from_=1, to=float('inf'))
        self.custom_furamount_spinbox.grid(column=1, row=3, padx=(0, 10), pady=10)
        self.product_price_label = tk.Label(self.custom_furniture_frame, text="Price", font=FONT_SIZE, bg="light grey")
        self.product_price_label.grid(column=0, row=4, padx=10)
        self.product_price_entry = tk.Entry(self.custom_furniture_frame, font=FONT_SIZE)
        self.product_price_entry.grid(column=1, row=4, padx=(0, 10), pady=10)
        self.custom_furniture_button = tk.Button(self.custom_furniture_frame, text="Add Furniture", font=FONT_SIZE, state=tk.DISABLED)
        self.custom_furniture_button.grid(column=0, row=5, columnspan=2, padx=10, pady=(0,10), sticky="ew")
        
        # ---------------------
        # SCRAPE FRAME
        # ---------------------

        self.scrape_frame = tk.Frame(self.input_frame)
        self.scrape_frame.grid(column=1, row=0, sticky="nsew")
        self.scrape_frame.grid_columnconfigure((0,1), weight=1)
        self.scrape_frame.grid_rowconfigure((0,1,2,3,4),weight= 1)
        self.scrape_label = tk.Label(self.scrape_frame, text= "Scrape Furniture Data", font=FONT_SIZE)
        self.scrape_label.grid(column= 0, row=0, columnspan=2, padx=10, pady=10)
        self.browser_options = ["Mozilla Firefox", "Google Chrome"]
        self.stores = ["Ikea", "Lesnina"]
        self.combo_var_browser = tk.StringVar()
        self.combo_var_store = tk.StringVar()
        self.browser_label = tk.Label(self.scrape_frame, text="Select browser", font=FONT_SIZE)
        self.browser_label.grid(column=0, row=1, padx=10)
        self.browser_combobox = ttk.Combobox(self.scrape_frame, textvariable=self.combo_var_browser, values= self.browser_options, state='readonly')
        self.browser_combobox.set(self.browser_options[0])
        self.browser_combobox.grid(column=1, row=1, padx=(0, 10), pady=10)
        self.browser_combobox.configure(font=FONT_SIZE)
        self.store_label = tk.Label(self.scrape_frame, text="Select store", font=FONT_SIZE)
        self.store_label.grid(column=0, row=2, padx=10)
        self.store_combobox = ttk.Combobox(self.scrape_frame, textvariable=self.combo_var_store, values=self.stores, state='readonly')
        self.store_combobox.grid(column=1, row=2, padx=(0, 10), pady=10)
        self.store_combobox.configure(font=FONT_SIZE)
        self.article_number_label = tk.Label(self.scrape_frame, text="Article ID", font=FONT_SIZE)
        self.article_number_label.grid(column=0, row=3, padx=10)
        self.article_id_entry = tk.Entry(self.scrape_frame, font=FONT_SIZE)
        self.article_id_entry.grid(column=1, row=3, padx=(0, 10), pady=10)
        self.article_count_label = tk.Label(self.scrape_frame, text="Number of articles", font=FONT_SIZE)
        self.article_count_label.grid(column=0, row=4, padx=10)
        self.article_count_spinbox = tk.Spinbox(self.scrape_frame, from_=1, to=float('inf'), font=FONT_SIZE)
        self.article_count_spinbox.grid(column=1, row=4, padx=(0, 10), pady=10)
        self.article_listbox = tk.Listbox(self.scrape_frame ,borderwidth=1, relief="solid")
        self.article_listbox.grid(column=2, row=1, rowspan=4, padx=(0,10))

        self.add_button = tk.Button(self.scrape_frame, text="Add", font=FONT_SIZE, state=tk.DISABLED)
        self.add_button.grid(column=0, row=5, padx=20, pady=10, sticky="ew")
        self.scrape_button = tk.Button(self.scrape_frame, text="Scrape", font=FONT_SIZE)
        self.scrape_button.grid(column=1, row=5, padx=20, pady=10, sticky="ew")
        self.listbox_menu = tk.Menu(root, tearoff=False)
        self.listbox_menu.add_command(label="Delete", command=lambda: self.am.delete_selected_item(self.article_listbox))
        self.listbox_menu.add_separator()
        self.listbox_menu.add_command(label="Clear all", command=lambda: self.am.clear_listbox(self.article_listbox))

        # ---------------------
        # INFORMATION FRAME
        # ---------------------

        self.information_frame = tk.Frame(self.input_frame, width=500, bg="light grey")
        self.information_frame.grid(column=2, row=0, sticky="nsew")
        self.information_frame.grid_propagate(False)
        self.information_frame.grid_columnconfigure((0,1), weight=1)
        self.information_frame.grid_rowconfigure((0,1,2,3),weight= 1)
        self.full_name_label = tk.Label(self.information_frame, text="Customer not selected", font=FONT_SIZE, bg="light grey")
        self.full_name_label.grid(column=0, row=0)
        self.create_project_label = tk.Label(self.information_frame, text="Create New Project", font=FONT_SIZE, bg="light grey")
        self.create_project_label.grid(column=0, row=1, pady=10)
        self.create_project_entry = tk.Entry(self.information_frame, font=FONT_SIZE)
        self.create_project_entry.grid(column=1, row=1, padx=10)
        self.create_project_button = tk.Button(self.information_frame, text="Create Project", font=FONT_SIZE, state=tk.DISABLED)
        self.create_project_button.grid(column=2, row=1, padx=10, pady=10, sticky="ew")
        self.select_project_label = tk.Label(self.information_frame, text="Select Project", font=FONT_SIZE, bg="light grey")
        self.select_project_label.grid(column=0, row=2, padx=10)
        self.combo_var_project = tk.StringVar()
        self.project_combobox = ttk.Combobox(self.information_frame, textvariable=self.combo_var_project, state='readonly')
        self.project_combobox.grid(column=1, row=2, padx=(0, 10), pady=10)
        self.project_combobox.configure(font=FONT_SIZE)
        self.delete_project_button = tk.Button(self.information_frame, text="Delete Project", font=FONT_SIZE)
        self.delete_project_button.grid(column=2, row=2, padx=10, pady=10, sticky="ew")
        self.total_price_label = tk.Label(self.information_frame, text="Furniture price: ", font=FONT_SIZE, bg="light grey")
        self.total_price_label.grid(column=0, row=3, columnspan=2, padx=10)

        # ---------------------
        # Binding functions to UI elements
        # ---------------------

        self.search_entry.bind("<KeyRelease>", lambda x, self=self: self.am.update_search_results(self.search_entry.get(), self.customer_listbox))
        self.am.refresh_listbox(self.customer_listbox)
        self.save_customer_button.bind("<Button-1>", lambda x: self.am.add_customer_ui(self.save_customer_button, self.rename_button, self.name_entry.get(), self.surname_entry.get(), self.name_entry, self.surname_entry, self.customer_listbox))
        self.rename_button.bind("<Button-1>", lambda x: self.am.rename_customer_ui(self.rename_button, self.save_customer_button, self.name_entry.get(), self.surname_entry.get(), self.name_entry, self.surname_entry, self.customer_listbox))
        self.customer_listbox.bind("<<ListboxSelect>>", lambda event: self.am.on_customer_selected(event, self.full_name_label, self.project_combobox, self.tree, self.total_price_label))
        self.customer_listbox.bind("<Button-3>", lambda event: self.am.on_click_customer_menu(event, self.customer_listbox, self.customer_menu, self.full_name_label, self.project_combobox, self.tree, self.total_price_label))
        self.create_project_button.bind("<Button-1>", lambda x: self.am.create_project_ui(self.create_project_entry.get(), self.create_project_entry, self.project_combobox, self.tree, self.create_project_button, self.total_price_label))
        self.article_listbox.bind("<Button-3>", lambda event: self.am.on_click_listbox_menu(event, self.article_listbox, self.listbox_menu))
        self.scrape_button.bind("<Button-1>", lambda x: self.am.start_scraping_thread(self.project_combobox.get(), self.article_listbox, self.browser_combobox.get(), self.tree, self.root, self.total_price_label))
        self.project_combobox.bind("<<ComboboxSelected>>", lambda x: self.am.on_project_selected(self.tree, self.project_combobox.get(), self.total_price_label))
        self.tree.bind("<Button-3>", lambda event: self.am.on_treeview_click(event, self.root, self.tree))
        self.custom_furniture_button.bind("<Button-1>", lambda x: self.am.add_customfur_data_ui(self.custom_furniture_button, self.project_combobox, self.custom_furname_entry, self.custom_furdescription_entry, self.custom_furamount_spinbox, self.product_price_entry, self.tree))
        self.add_button.bind("<Button-1>", lambda x: self.am.append_to_listbox(self.article_listbox, self.article_id_entry, self.article_count_spinbox, self.store_combobox, self.add_button))
        self.delete_project_button.bind("<Button-1>", lambda x: self.am.confirm_project_deletion(self.project_combobox, self.tree, self.total_price_label))
        self.root.bind("<Delete>", lambda x: self.am.delete_selected_tree_item(self.tree, self.project_combobox.get()))

        # ---------------------
        # VALIDATION
        # Ensuring the accuracy of input elements by verifying their length and format.
        # ---------------------
        
        self.name_entry.bind("<KeyRelease>", lambda x: self.am.validate_name_surname(self.name_entry.get(), self.surname_entry.get(), self.save_customer_button, self.rename_button))
        self.surname_entry.bind("<KeyRelease>", lambda x: self.am.validate_name_surname(self.name_entry.get(), self.surname_entry.get(), self.save_customer_button, self.rename_button))
        self.store_combobox.bind("<<ComboboxSelected>>", lambda x: self.am.validate_article(self.article_id_entry.get(), self.store_combobox.get(), self.add_button))
        self.article_id_entry.bind("<KeyRelease>", lambda x: self.am.validate_article(self.article_id_entry.get(), self.store_combobox.get(), self.add_button))
        self.custom_furname_entry.bind("<KeyRelease>", lambda x: self.am.validate_custom_furniture(self.custom_furname_entry.get(), self.custom_furdescription_entry.get(), self.product_price_entry.get(), self.custom_furniture_button))
        self.custom_furdescription_entry.bind("<KeyRelease>", lambda x: self.am.validate_custom_furniture(self.custom_furname_entry.get(), self.custom_furdescription_entry.get(), self.product_price_entry.get(), self.custom_furniture_button))
        self.product_price_entry.bind("<KeyRelease>", lambda x: self.am.validate_custom_furniture(self.custom_furname_entry.get(), self.custom_furdescription_entry.get(), self.product_price_entry.get(), self.custom_furniture_button))
        self.create_project_entry.bind("<KeyRelease>", lambda x: self.am.validate_project(self.create_project_entry, self.create_project_button))

class EntryWithPlaceholder(tk.Entry):
    """
    Custom Tkinter Entry widget with placeholder functionality.
    This widget displays a placeholder text when empty and removes it upon focus. The placeholder
    reappears when the widget loses focus and remains empty.
    """
    def __init__(self, master=None, placeholder="", color='grey', font_size=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        if font_size:
            current_font = self.cget("font")
            self.configure(font=(current_font[0], font_size))
        
        self.insert("0", self.placeholder)
        self.bind("<FocusIn>", self.on_entry_click)
        self.bind("<FocusOut>", self.on_focus_out)
        
    def on_entry_click(self, event):
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self.config(fg=self.default_fg_color)

    def on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)