import tkinter as tk
from tkinter import ttk
import record_handler as logic


class Gui:
    def __init__(self, master) -> None:
        """
        Initializes elements for the Gui. Returns None.
        """
        self.master = master
        self.master.title('The Scraper 3000')
        self.master.geometry('700x480')

        self.label_planet = ttk.Label(master, text='Scrape the Planet')
        self.label_planet.grid(row=1, column=0, pady=10)

        self.label_artist_name = ttk.Label(master, text='Artist Name')
        self.label_artist_name.grid(row=2, column=0, pady=0)

        self.input_artist_name = ttk.Entry(master, width=30)
        self.input_artist_name.grid(row=3, column=0, padx=(10, 5), pady=0)

        self.label_artist_url = ttk.Label(master, text='Soundcloud URL')
        self.label_artist_url.grid(row=4, column=0, pady=5)

        self.input_artist_url = ttk.Entry(master, width=60)
        self.input_artist_url.grid(row=5, column=0, padx=(10, 5), pady=0)

        self.submit_button1 = ttk.Button(master, text='Check Artist', command=self.submit_1)
        self.submit_button1.grid(row=6, column=0, padx=(10, 5), pady=10)

        self.table_frame = ttk.Frame(master)
        self.table_frame.grid(row=0, column=0, padx=10, pady=10,)

        self.columns = ('Artist', 'URL', 'New')

        self.tree = ttk.Treeview(master, columns=self.columns, show='headings')
        self._setup_table()

        self.data = logic.table_list()
        self._populate_table(self.data)

        self.scrollbar = ttk.Scrollbar(self.table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        self.tree.heading('Artist', text='Artist')
        self.tree.heading('URL', text='URL')
        self.tree.heading('New', text='New')

        self.tree.column('Artist', width=100)
        self.tree.column('URL', width=550, anchor='center')
        self.tree.column('New', width=50)

    def _setup_table(self) -> None:
        """
        Creates heading logic in gui table. Returns None.
        """
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

    def _populate_table(self, data) -> None:
        """
        Passes 'data' into table. Would you believe that??? Returns None.
        """
        for row in data:
            self.tree.insert('', tk.END, values=row)

    def submit_1(self) -> None:
        """
        Passes user input to record_handler.py to handle program logic. Returns None.
        """
        user_input_artist = self.input_artist_name.get()
        user_input_url = self.input_artist_url.get()
        print(f'User artist input: {user_input_artist}')
        print(f'User URL input: {user_input_url}')
        logic.update_record(user_input_artist, user_input_url)


