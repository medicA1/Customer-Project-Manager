import tkinter as tk
from ui.ui_manager import CustomerFurnitureApp
from db.db_manager import SessionManager

def main():
    CUSTOMER_PATH = "src\customer.db"
    sm = SessionManager(CUSTOMER_PATH)
    session = sm.create_session()

    root = tk.Tk()
    app = CustomerFurnitureApp(root, session)
    root.mainloop()

if __name__ == "__main__":
    main()