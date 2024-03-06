import tkinter as tk
from tkinter import messagebox
from db.db_manager import DatabaseManager
from utils.scrape_manager import ScrapeManager
from threading import Thread
import re


class AppManager():
    def __init__(self, session):
        self.customer_id = None
        self.project_id = None
        self.is_scraping = False
        self.session = session
        self.dbm = DatabaseManager(self.session)
        self.sm = ScrapeManager(self.session)

    # ---------------------
    # Section: Validation
    # ---------------------

    def validate_name_surname(self, name, surname, submit_button, rename_button):
        min_length = 2
        if len(name) >= min_length and len(surname) >= min_length:
            submit_button.config(state=tk.NORMAL)
            rename_button.config(state=tk.NORMAL)
        else:
            submit_button.config(state=tk.DISABLED)
            rename_button.config(state=tk.DISABLED)
    
    def validate_article(self, article_number, selected_store, submit_button):
        if len(article_number) > 7 and selected_store:
            submit_button.config(state=tk.NORMAL)
        else:
            submit_button.config(state=tk.DISABLED)

    def validate_custom_furniture(self, furniture_name, furniture_description, price, submit_button):
        price_pattern = re.compile(r'^\d*\.?\d+$')
        if furniture_name and furniture_description and price and re.match(price_pattern, price):
            submit_button.config(state=tk.NORMAL)
        else:
            submit_button.config(state=tk.DISABLED)

    def validate_project(self, new_project_entry, submit_button):
        if len(new_project_entry.get()) >= 1 and self.project_id is not None:
            submit_button.config(state=tk.NORMAL)
        else:
            submit_button.config(state=tk.DISABLED)

    # ---------------------
    # Section: Customer Managment and Listbox
    # ---------------------
            
    def on_customer_selected(self, event, customer_info_label, projects_combobox, tree, price_label):
        """
        Clears and updates the customer info label, projects combobox, treeview, and price label based on the selected customer.
        """
        customers = self.dbm.get_customers()
        selection = event.widget.curselection()
        if selection:
            self.delete_tree(tree)
            index = selection[0]
            selected_customer = customers[index]
            self.customer_id = selected_customer.id
            self.update_customer_label(customer_info_label)
            self.update_projects_combobox(projects_combobox, tree, price_label)
            self.on_project_selected(tree, projects_combobox.get(), price_label)

    def on_click_customer_menu(self, event, listbox, popup_menu, customer_info_label, projects_combobox, tree, price_label):
        """
        Selects customer on click and shows a popup menu inside a listbox. 
        """
        try:
            index = listbox.nearest(event.y)
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(index)
            listbox.activate(index)

            self.on_customer_selected(event, customer_info_label, projects_combobox, tree, price_label)

            popup_menu.tk_popup(event.x_root, event.y_root)

        finally:
            popup_menu.grab_release()

    def refresh_listbox(self, listbox):
        """"
        Refreshes customer listbox.
        """
        customers = self.dbm.get_customers()
        listbox.delete(0, tk.END)
        for customer in customers:
            listbox.insert(tk.END, f"{customer.name} {customer.surname}")
    
    def add_customer_ui(self, submit_button, rename_button, name, surname, name_entry, surname_entry, listbox):
        """
        Adds a new customer to the database and refreshes the UI components to reflect the update.
        """
        new_customer = self.dbm.add_new_customer(name, surname)
        name_entry.delete(0, tk.END)
        surname_entry.delete(0, tk.END)
        self.refresh_listbox(listbox)
        submit_button.config(state=tk.DISABLED)
        rename_button.config(state=tk.DISABLED)

    def rename_customer_ui(self, rename_button, submit_button, new_name, new_surname, name_entry, surname_entry, listbox):
        """
        Renames customer from the database and refreshes the UI components to reflect the update.
        """
        if rename_button["state"] == tk.DISABLED:
            return
        customer = self.dbm.get_customer_by_id(self.customer_id)
        renamed_customer = self.dbm.rename_customer(new_name, new_surname, customer)
        name_entry.delete(0, tk.END)
        surname_entry.delete(0, tk.END)
        self.refresh_listbox(listbox)       
        submit_button.config(state=tk.DISABLED)
        rename_button.config(state=tk.DISABLED)

    def confirm_customer_deletion(self, listbox, customer_info_label, projects_combobox, tree, price_label):
        """"
        Shows a popup messagebox asking if you want to delete selected customer from the database.
        On clicking yes project is deleted and UI is updated.
        """
        name, surname = self.dbm.get_customer_name_surname(self.customer_id)
        result = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {name} {surname}?")
        if result:
            result = self.dbm.delete_customer_by_id(self.customer_id)
            if result:
                self.refresh_listbox(listbox)
                self.update_customer_label(customer_info_label)
                self.update_projects_combobox(projects_combobox, tree, price_label)
                self.on_project_selected(tree, projects_combobox.get(), price_label)

    def prepare_customer_rename_ui(self, name_entry, surname_entry, submit_button, rename_button):
        """
        Prepares UI fields for customer name and surname update, populating them with current values and enabling buttons.
        """
        customer = self.dbm.get_customer_by_id(self.customer_id)
        name_entry.delete(0, tk.END)
        surname_entry.delete(0, tk.END)
        name_entry.insert(tk.END, customer.name)
        surname_entry.insert(tk.END, customer.surname)
        submit_button.config(state=tk.NORMAL)
        rename_button.config(state=tk.NORMAL)

    def update_search_results(self, search_term, listbox):
        """
        Filters and displays search results in the listbox based on the query entered in the search box.
        """
        search_terms = search_term.lower().split()
        if not search_terms:
            self.refresh_listbox(listbox)
            return
        
        results = self.dbm.search_like_customer(search_term)

        listbox.delete(0, tk.END)
        for result in results:
            listbox_item = f"{result.name} {result.surname}"
            listbox.insert(tk.END, listbox_item)

    def update_customer_label(self, customer_info_label):
        """
        Updates customer name and surname label based on values returned by querying customer_id
        """
        name, surname = self.dbm.get_customer_name_surname(self.customer_id)
        if name and surname:
            customer_info_label.config(text=f"{name} {surname}")
        else:
            customer_info_label.config(text="Customer not found")
    
    # ---------------------
    # Section: Managing article listbox
    # ---------------------

    def append_to_listbox(self, listbox, article_number_entry, article_count_spinbox, store_combobox, submit_button):
        """
        Append to list and update UI elements.
        """
        listbox.insert(tk.END, f"{article_number_entry.get()}    {article_count_spinbox.get()}    {store_combobox.get()}")
        article_number_entry.delete(0, tk.END)
        article_count_spinbox.delete(0, tk.END)
        article_count_spinbox.insert(0, 1)
        submit_button.config(state=tk.DISABLED)

    def on_click_listbox_menu(self, event, listbox, menu):
        """
        Shows popup menu inside a listbox
        """
        try:
            listbox.selection_clear(0, tk.END)
            index = listbox.nearest(event.y)
            listbox.selection_set(index)
            listbox.activate(index)
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def clear_listbox(self, listbox):
        listbox.delete(0, tk.END)

    def delete_selected_item(self, listbox):
        selected = listbox.curselection()
        if selected:
            listbox.delete(selected[0])

    # ---------------------
    # Section: Managing projects
    # ---------------------

    def on_project_selected(self, tree, project_name, price_label):
        """
        Updates UI elements based on the selected project.
        This method refreshes the treeview with furniture items and updates the price label to reflect the total price of furniture for the selected project.  
        """
        project_id = self.update_treeview_for_selected_project(tree, project_name)
        total_price = self.dbm.get_total_price_by_project_id(project_id)
        if total_price is not None:
            price_label.config(text=f"Furniture price: {total_price:.2f} €")
        else:
            price_label.config(text=f"Furniture price: ")

    def update_projects_combobox(self, projects_combobox, tree, price_label):
        """
        Populates the projects combobox with values returned by querying customer_id.
        """
        projects = self.dbm.get_projects(self.customer_id)
        projects_combobox["values"] = projects
        if projects:
            selected_project = projects[0]  
            projects_combobox.set(selected_project)   
            self.on_project_selected(tree, selected_project, price_label)
        else:
            projects_combobox.set('') 
            self.on_project_selected(tree, None, price_label)

    def create_project_ui(self, project_name, project_entry, projects_combobox, tree, submit_button, price_label):
        """
        Adds new project to the database and updates UI elements.
        """
        if submit_button["state"] == tk.DISABLED:
            return
        # Bandating problem with 2 or more projects with the same name, needs more sophisticated logic to deal with project querying(querying with project_id). At the moment creating 2 projects with the same name is not allowed.
        project_exists = self.dbm.get_project_id(project_name)
        if project_exists:
            messagebox.showwarning("Warning", "Entered project name already exists. Try another name.")
            return
        else:
            project = self.dbm.add_project(project_name, self.customer_id)
            project_entry.delete(0, tk.END)
            self.update_projects_combobox(projects_combobox, tree, price_label)

    def confirm_project_deletion(self, projects_combobox, tree, price_label):
        """
        Shows a popup messagebox asking if you want to delete selected project from the database.
        On clicking yes project is deleted and UI is updated.
        """
        project_name = self.dbm.get_project_name_by_id(self.project_id)
        result = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {project_name}?")
        if result:
            self.dbm.delete_project_by_project_id(self.project_id)
            self.update_projects_combobox(projects_combobox, tree, price_label)

    # ---------------------
    # Section: Trieview Manager
    # ---------------------
    
    def update_treeview_for_selected_project(self, tree, project_name):
        """
        Populates the treeview with furniture data related to the selected project.
        """
        project_id = self.dbm.get_project_id(project_name)
        if project_id is not None:
            self.project_id = project_id
            furniture_data = self.dbm.fetch_furniture_data(project_id)
            self.delete_tree(tree)
            for furniture in furniture_data:
                formatted_amount = f"{int(furniture['amount'])}"
                formatted_price = f"{furniture['price']:.2f} €"
                tree.insert('', tk.END, iid=str(furniture['furniture_id']), values=(
                    furniture['furniture_name'],
                    furniture['description'],
                    furniture['serial_number'],
                    formatted_amount,
                    formatted_price,
                    furniture['url']
                ))
        return project_id

    def copy_to_clipboard(self, root, value):
        root.clipboard_clear()
        root.clipboard_append(value)
        root.update()

    def on_treeview_click(self, event, root, tree):
        """
        Clicked item in treeview is copied to clipboard.
        """
        # Identify the clicked item
        item_id = tree.identify_row(event.y)
        if not item_id:
            return  # Clicked outside any item
        
        # Identify the clicked column (returns column # as '#1', '#2', ...)
        column_id = tree.identify_column(event.x)
        column_index = int(column_id.replace('#', '')) - 1  # Convert to 0-based index
        
        # Get the item's values
        item_values = tree.item(item_id, 'values')
        if column_index < len(item_values):
            clicked_value = item_values[column_index]
            self.copy_to_clipboard(root, clicked_value)
            print(f"Copied to clipboard: {clicked_value}")

    def delete_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)
    
    def delete_selected_tree_item(self, tree, project_name):
        if not tree.selection():
            messagebox.showwarning("Warning", "No item selected for deletion.")
            return
        
        selected_item = tree.selection()[0]
        furniture_id = int(selected_item)
        self.dbm.delete_furniture_by_furniture_id(furniture_id)
        self.update_treeview_for_selected_project(tree, project_name)

    # NOT USED
    def on_click_tree_menu(self, event, tree, menu):
        item_id = tree.identify_row(event.y)
        if item_id:
            # Set the selection to the item that was right-clicked
            tree.selection_set(item_id)
            
            # Get the item's position to place the context menu
            x, y, width, height = tree.bbox(item_id)
            menu.post(event.x_root, event.y_root)
        else:
            menu.unpost()

    # ---------------------
    # Section: Furniture Manager and Scraping
    # ---------------------

    def add_customfur_data_ui(self, submit_button, selected_project, furniture_name_entry, furniture_description_entry, amount_entry, price_entry, tree):
        """
        Takes inserted values and adds new furniture to the database. Updates UI elements related to customer furniture inputs and treeview.
        """
        if submit_button["state"] == tk.DISABLED:
            return
        
        project_id = self.dbm.get_project_id(selected_project.get().strip())
        if project_id is None:
            messagebox.showinfo("Error", "Selected project not found.")
            return
        try:
            self.dbm.add_furniture_data(
                furniture_name_entry.get(), 
                furniture_description_entry.get(), 
                "WORKSHOP", # PLACEHOLDER for now
                amount_entry.get(), 
                price_entry.get(), 
                "WORKSHOP", # PLACEHOLDER for now
                project_id
            )

        except Exception as e:
            messagebox.showerror("Error", "Failed to add furniture")
            return

        furniture_name_entry.delete(0, tk.END)
        furniture_description_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, 1)
        price_entry.delete(0, tk.END)

        self.update_treeview_for_selected_project(tree, selected_project.get().strip())
    
    def get_article_information(self, item_listbox):
        """
        Extracts article information from a Listbox and returns article details.
        Parses each item in the Listbox to extract and return article numbers, counts, and manufacturers. If the Listbox is empty, it displays an error message.
        """
        article_numbers = []
        article_counts = []
        manufacturers = []

        if item_listbox.size() == 0:
            messagebox.showinfo("Error", "Add articles")
            return [], [], [] 
        # Iterate over all items in the Listbox
        for i in range(item_listbox.size()):
            item = item_listbox.get(i)
            # Split the item by the separator used during insertion
            parts = item.split('    ')
            if len(parts) == 3:
                article_number, article_count, manufacturer = parts
                article_numbers.append(article_number)
                article_counts.append(article_count)
                manufacturers.append(manufacturer)

        return article_numbers, article_counts, manufacturers


    def scrape(self, project_name, item_listbox, browser, tree, root, price_label):
        """
        Initiates scraping process for articles based on selected project and updates UI accordingly.
        Retrieves article information from the listbox, generates URLs for scraping based on manufacturer and article number, performs scraping for each article, and updates the project's treeview with the new data. Handles browser management and UI updates upon completion.
        """
        if self.is_scraping:
            messagebox.showinfo("Info", "Scraping is already in progress. Please wait.")
            return
        self.is_scraping = True
        driver = None
        try:
            if not project_name.strip():
                messagebox.showinfo("Error", "No project selected.")
                return
            urls = []
            article_numbers, article_counts, manufacturers = self.get_article_information(item_listbox)
            self.clear_listbox(item_listbox)
            if manufacturers:
                project_id = self.dbm.get_project_id(project_name)
                if project_id:
                    driver = self.sm.get_browser(browser)
                    for i, manufacturer in enumerate(manufacturers):
                        article_number = article_numbers[i]
                        article_count = article_counts[i]
                        url = self.sm.generate_article_url(manufacturer, article_number)
                        urls.append(url)

                        if manufacturer == "Ikea":
                            self.sm.scrape_ikea(project_id, url, driver, article_count)
                        elif manufacturer == "Lesnina":
                            self.sm.scrape_lesnina(project_id, url, driver, article_count)
        finally:
            if driver:
                driver.quit()
            self.is_scraping = False
            current_project_id = self.dbm.get_project_id(project_name)
            if current_project_id == self.project_id:
                # Updates treeview and total price
                root.after(0, self.on_project_selected(tree, project_name, price_label))

    def start_scraping_thread(self, project_name, item_listbox, browser, tree, root, price_label):
        """
        Starts a separate thread for the scraping process.
        Launches the scraping process in a non-blocking manner by initiating a separate thread. This allows the UI to remain responsive while scraping operations are performed in the background.
        """
        threading_task = Thread(target=self.scrape, args=(project_name, item_listbox, browser, tree, root, price_label))
        threading_task.start()