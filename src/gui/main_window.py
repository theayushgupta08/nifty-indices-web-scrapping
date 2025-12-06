"""
Main GUI Window
Tkinter-based GUI for Nifty Indices scraper
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
from ..services.scraper import NiftyIndicesScraper
from ..utils.date_parser import parse_date
from ..utils.export import export_to_excel
from ..config.settings import Settings


class NiftyIndicesGUI:
    """Main GUI class for Nifty Indices scraper"""
    
    def __init__(self):
        """Initialize GUI components"""
        self.scraper = NiftyIndicesScraper(timeout=Settings.API_TIMEOUT)
        self.root = None
        self._setup_gui()
    
    def _setup_gui(self):
        """Setup GUI components"""
        self.root = tk.Tk()
        self.root.title(Settings.GUI_TITLE)
        self.root.geometry(f"{Settings.GUI_WIDTH}x{Settings.GUI_HEIGHT}")
        self.root.resizable(Settings.GUI_RESIZABLE, Settings.GUI_RESIZABLE)
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Nifty Indices Data Scraper",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Index Type dropdown
        ttk.Label(
            main_frame,
            text="Select an Index Type:",
            font=('Arial', 10)
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.index_type_var = tk.StringVar()
        self.index_type_combo = ttk.Combobox(
            main_frame,
            textvariable=self.index_type_var,
            width=27,
            state='readonly'
        )
        self.index_type_combo.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)
        self.index_type_combo['values'] = self.scraper.get_index_types()
        
        # Sub-Index Type dropdown
        ttk.Label(
            main_frame,
            text="Select a Sub-IndexType:",
            font=('Arial', 10)
        ).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.sub_index_type_var = tk.StringVar()
        self.sub_index_type_combo = ttk.Combobox(
            main_frame,
            textvariable=self.sub_index_type_var,
            width=27,
            state='readonly'
        )
        self.sub_index_type_combo.grid(row=2, column=1, pady=5, padx=10, sticky=tk.W)
        
        # Index dropdown
        ttk.Label(
            main_frame,
            text="Select an Index:",
            font=('Arial', 10)
        ).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.index_var = tk.StringVar()
        self.index_combo = ttk.Combobox(
            main_frame,
            textvariable=self.index_var,
            width=27,
            state='readonly'
        )
        self.index_combo.grid(row=3, column=1, pady=5, padx=10, sticky=tk.W)
        
        # Start Date field
        ttk.Label(
            main_frame,
            text="Start Date:",
            font=('Arial', 10)
        ).grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.start_date_entry = ttk.Entry(main_frame, width=30, font=('Arial', 10))
        self.start_date_entry.grid(row=4, column=1, pady=5, padx=10)
        self.start_date_entry.insert(0, Settings.DEFAULT_START_DATE)
        
        ttk.Label(
            main_frame,
            text="(Format: DD-MMM-YYYY)",
            font=('Arial', 8),
            foreground='gray'
        ).grid(row=5, column=1, sticky=tk.W, padx=10)
        
        # End Date field
        ttk.Label(
            main_frame,
            text="End Date:",
            font=('Arial', 10)
        ).grid(row=6, column=0, sticky=tk.W, pady=5)
        
        self.end_date_entry = ttk.Entry(main_frame, width=30, font=('Arial', 10))
        self.end_date_entry.grid(row=6, column=1, pady=5, padx=10)
        self.end_date_entry.insert(0, Settings.DEFAULT_END_DATE)
        
        ttk.Label(
            main_frame,
            text="(Format: DD-MMM-YYYY)",
            font=('Arial', 8),
            foreground='gray'
        ).grid(row=7, column=1, sticky=tk.W, padx=10)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Ready",
            font=('Arial', 9),
            foreground='green',
            wraplength=400
        )
        self.status_label.grid(row=8, column=0, columnspan=2, pady=15)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.grid(row=9, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Bind events for cascading dropdowns
        self.index_type_combo.bind('<<ComboboxSelected>>', self._on_index_type_selected)
        self.sub_index_type_combo.bind('<<ComboboxSelected>>', self._on_sub_index_type_selected)
        
        # Scrape button
        self.scrape_button = ttk.Button(
            main_frame,
            text="Submit",
            command=self._scrape_data,
            width=25
        )
        self.scrape_button.grid(row=10, column=0, columnspan=2, pady=20)
    
    def _on_index_type_selected(self, event=None):
        """Handle index type selection"""
        selected_index_type = self.index_type_var.get()
        if selected_index_type:
            self.status_label.config(text="Loading sub-index types...", foreground='blue')
            self.sub_index_type_combo.set('')
            self.index_combo.set('')
            self.index_combo['values'] = []
            
            def fetch_sub_index_types():
                try:
                    sub_types = self.scraper.get_sub_index_types(selected_index_type)
                    self.sub_index_type_combo['values'] = sub_types
                    self.status_label.config(text="Ready", foreground='green')
                except Exception as e:
                    self.status_label.config(
                        text=f"Error loading sub-index types: {str(e)}",
                        foreground='red'
                    )
            
            thread = threading.Thread(target=fetch_sub_index_types, daemon=True)
            thread.start()
    
    def _on_sub_index_type_selected(self, event=None):
        """Handle sub-index type selection"""
        selected_sub_index_type = self.sub_index_type_var.get()
        if selected_sub_index_type:
            self.status_label.config(text="Loading indices...", foreground='blue')
            self.index_combo.set('')
            
            def fetch_indices():
                try:
                    indices = self.scraper.get_indices(selected_sub_index_type)
                    self.index_combo['values'] = indices
                    self.status_label.config(text="Ready", foreground='green')
                except Exception as e:
                    self.status_label.config(
                        text=f"Error loading indices: {str(e)}",
                        foreground='red'
                    )
            
            thread = threading.Thread(target=fetch_indices, daemon=True)
            thread.start()
    
    def _scrape_data(self):
        """Handle scraping in a separate thread"""
        # Get values from dropdowns and entries
        index_type = self.index_type_var.get().strip()
        sub_index_type = self.sub_index_type_var.get().strip()
        index_name = self.index_var.get().strip()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()
        
        # Validate inputs
        if not all([index_type, sub_index_type, index_name, start_date, end_date]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        # Validate date format and range
        start_dt = parse_date(start_date)
        end_dt = parse_date(end_date)
        
        if start_dt is None:
            messagebox.showerror(
                "Error",
                f"Invalid start date format: {start_date}\n"
                f"Expected format: DD-MMM-YYYY (e.g., 02-Dec-2025)"
            )
            return
        
        if end_dt is None:
            messagebox.showerror(
                "Error",
                f"Invalid end date format: {end_date}\n"
                f"Expected format: DD-MMM-YYYY (e.g., 06-Dec-2025)"
            )
            return
        
        if start_dt >= end_dt:
            messagebox.showerror("Error", "Start date must be before end date!")
            return
        
        # Use index_name for both name and indexName parameters
        name = index_name
        
        # Disable button and show progress
        self.scrape_button.config(state='disabled')
        self.status_label.config(text="Scraping data...", foreground='blue')
        self.progress.start()
        
        def run_scrape():
            try:
                # Scrape data using API
                df = self.scraper.scrape_historical_data(
                    name=name,
                    start_date=start_date,
                    end_date=end_date,
                    index_name=index_name
                )
                
                if df is not None and not df.empty:
                    # Ask user for save location
                    default_filename = f"{index_name.replace(' ', '_')}_historical_data.xlsx"
                    file_path = filedialog.asksaveasfilename(
                        defaultextension=".xlsx",
                        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                        initialfile=default_filename,
                        title="Save Excel File"
                    )
                    
                    if file_path:
                        # Export to Excel
                        if export_to_excel(df, file_path):
                            self.status_label.config(
                                text=f"Success! Data exported to:\n{os.path.basename(file_path)}\n({len(df)} rows)",
                                foreground='green'
                            )
                            messagebox.showinfo(
                                "Success",
                                f"Data successfully exported!\n\n"
                                f"File: {os.path.basename(file_path)}\n"
                                f"Rows: {len(df)}"
                            )
                        else:
                            self.status_label.config(
                                text="Error: Failed to export Excel file. Check console for details.",
                                foreground='red'
                            )
                            messagebox.showerror(
                                "Export Error",
                                "Failed to export to Excel.\n\n"
                                "Please ensure openpyxl is installed:\npip install openpyxl"
                            )
                    else:
                        self.status_label.config(text="Export cancelled", foreground='orange')
                else:
                    self.status_label.config(
                        text="Error: No data retrieved. Please check your inputs.",
                        foreground='red'
                    )
                    messagebox.showerror(
                        "Error",
                        "Failed to scrape data. Please check:\n"
                        "1. Internet connection\n"
                        "2. Valid date format (DD-MMM-YYYY)\n"
                        "3. Valid index name"
                    )
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}", foreground='red')
                messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            finally:
                # Re-enable button and stop progress
                self.progress.stop()
                self.scrape_button.config(state='normal')
        
        # Run scraping in a separate thread to prevent UI freezing
        thread = threading.Thread(target=run_scrape, daemon=True)
        thread.start()
    
    def run(self):
        """Run the GUI main loop"""
        self.root.mainloop()


def create_gui():
    """Create and run the tkinter GUI"""
    app = NiftyIndicesGUI()
    app.run()

