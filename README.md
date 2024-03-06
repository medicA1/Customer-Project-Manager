# CUSTOMER FURNITURE MANAGER

### WHY I MADE THIS PROGRAM

I developed this application to streamline the managment of my customer base and oboarding of new clients. 
Assembling furniture for customers, who primarily purchase from IKEA, LESNINA and other retailers is a component
of my job. These customers often provide only the serial numbers of their items. Previously, I found myself manually
searching for each item, inputting their details into a spreadsheet aand calculating the total furniture cost.
This step is vital for setting the service fee.

The manual process was not just time-consuming but also diverted my attention from more important activities that
I could use my valuable time for, such as scrolling youtube shorts.

### WHAT IT DOES

This program features GUI designed for efficient customer managment and the organization of multiple
projects for each client. Upon selecting a customer and specific project, users are equipped to enter the provided
serial numbers, queantities, and the retailers of the product, adding these details to a  list. Once all items are
catalogued, the program can start the retrieval of necessary information crutial to calculating the final cost and
presents it inside a spreadsheet.
Additionally, should a customer request furniture crafted in my workshop(custom furniture), this too can be inserted
inside the spreadsheet.

### REQUIRED INSTALLS
- Tkinter
- SQLAlchemy
- Selenium
- BeautifulSoup

### HOW TO USE THE PROGRAM
Creating a New Customer
1. Enter the customers first and last name in the respective fields
2. Click the "Add Customer" button to register the new customer into the system
   Managing Customers:
    - Right click on a customers name to access options for deletion and renaming
      (Deleting a customer deletes all associated projects from the database)
    - Search for customer inserting name or last name inside a searchbox

Creating a new Project:
1. With a customer selcted, type the project name into the designated field
2. Click "Create Project" button to register the new project into the system
3. Selected the desired project presented inside a spinbox 
   Managing Projects:
     - Click "Delete Project" button to delete selected project (Deleting the project
       deletes all associated furniture items from the database)
     - The "Total Price" feature calculates and displays the sum of all item prices within the selected project.

Adding Product Information for Scraping:
1. After selecting a project, enter the product details (serial number, quantity, and retailer) in the scraping frame.
2. Click "Add" to include this information in a listbox. Repeat this step for all products you wish to include.
    Editing and Managing Product Entries:
      - To edit an entry, right-click on an item within the listbox. This allows you to modify the entered information.
4. Selected the browser you wish to use for scraping.(Current options: Mozilla and Chrome)
5. Once all items are listed, click "Scrape" to begin retrieving detailed information for each product and saving it
to the database.

Viewing and Managing Data in the Spreadsheet:
1. The retrieved information is displayed in a spreadsheet format. Right-click on any text within the spreadsheet
to copy it to the clipboard.
2. To delete an item from the spreadsheet, select it and press the DELETE key.
This removes the item from both the display and the database.

#### ISSUES AND FUTURE OPTIMIATIONS
Selenium Dependency for Browser Automation: Currently, the application leverages Selenium for initiating browser
sessions, which is essential for scraping IKEA's website. Combined with BeautifulSoup (bs4), has
proven successful where attempts with bs4 and requests alone were not. The dynamic content and client-side 
scripts of IKEA's website necessitate the use of a browser automation tool like Selenium to accurately render 
and access the necessary information.

Optimizing LESNINA Scraping: For scraping LESNINA's website, Selenium's browser automation may not be necessary.
LESNINA's site can be efficiently scraped using requests and BeautifulSoup,
without the overhead of a browser. In future iterations, I plan to refine the LESNINA scraper to eliminate 
Selenium dependency, aiming for a quicker and more streamlined data retrieval process.
