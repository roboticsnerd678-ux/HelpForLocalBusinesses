import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import json
import os
import shutil
import uuid
import time

# Load or create JSON database
DATA_FILE = "businesses.json"
IMAGE_FOLDER = "Photos"

def load_businesses():
    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_businesses(businesses):
    with open(DATA_FILE, "w") as f:
        json.dump(businesses, f, indent=2)

# Main Application
class BusinessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phoenix Local Business Directory")
        self.root.geometry("900x700")
        
        # Consistent Styles
        self.setup_styles()
        self.root.configure(bg=self.colors["background"])
        
        # Better Visual Hierarchy 
        # Create header that persists across pages
        self.header_frame = tk.Frame(self.root, bg=self.colors["primary"], height=80)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)
        
        self.app_title = tk.Label(self.header_frame, 
                                  text="📍 Phoenix Local Business Directory", 
                                  font=self.fonts["title"], 
                                  bg=self.colors["primary"], 
                                  fg="white")
        self.app_title.pack(pady=20)
        
        self.subtitle = tk.Label(self.header_frame, 
                                 text="Discover and support local businesses in your community", 
                                 font=self.fonts["subheading"], 
                                 bg=self.colors["primary"], 
                                 fg="#e0e0e0")
        self.subtitle.pack()
        
        # Main content area
        self.content_frame = tk.Frame(self.root, bg=self.colors["background"], padx=30, pady=20)
        self.content_frame.pack(fill="both", expand=True)
        
        # Loading State Setup 
        self.is_loading = False
        
        # Keyboard Shortcuts (Bonus Accessibility)
        self.root.bind('<Escape>', lambda e: self.show_start_page())
        
        # Start Page
        self.show_start_page()
    
    def setup_styles(self):
        """Define consistent colors and fonts"""
        self.colors = {
            "primary": "#2C3E50",      # Dark blue
            "secondary": "#3498DB",     # Medium blue
            "accent": "#E74C3C",        # Red for errors
            "success": "#27AE60",       # Green for success
            "background": "#ECF0F1",    # Light gray background
            "surface": "#FFFFFF",       # White for cards
            "text": "#2C3E50",          # Dark text
            "text_light": "#7F8C8D",    # Light text
            "error": "#E74C3C",         # Error red
            "warning": "#F39C12",       # Warning orange
        }
        
        self.fonts = {
            "title": ("Segoe UI", 24, "bold"),
            "heading": ("Segoe UI", 18, "bold"),
            "subheading": ("Segoe UI", 12),
            "body": ("Segoe UI", 10),
            "button": ("Segoe UI", 10, "bold"),
            "label": ("Segoe UI", 9, "bold"),
        }
    
    def clear_content(self):
        """Clear only the content area, not header"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def create_card(self, parent, **kwargs):
        """Create a card container for content grouping"""
        card = tk.Frame(parent, 
                       bg=self.colors["surface"], 
                       relief="flat",
                       borderwidth=1,
                       padx=20, 
                       pady=15)
        
        # Add subtle shadow effect
        card.configure(highlightbackground="#BDC3C7", highlightthickness=1)
        return card
    
    def show_start_page(self):
        
        self.clear_content()
        
        # Welcome card
        welcome_card = self.create_card(self.content_frame)
        welcome_card.pack(fill="x", pady=(0, 20))
        
        tk.Label(welcome_card, 
                text="Welcome to That's Near Me?!", 
                font=self.fonts["heading"], 
                bg=self.colors["surface"],
                fg=self.colors["primary"]).pack(pady=(0, 10))
        
        tk.Label(welcome_card, 
                text="Help local businesses thrive by adding them to our directory or exploring existing ones.", 
                font=self.fonts["subheading"], 
                bg=self.colors["surface"],
                fg=self.colors["text_light"],
                wraplength=600).pack(pady=(0, 20))
        
        # Action buttons in a grid
        button_frame = tk.Frame(welcome_card, bg=self.colors["surface"])
        button_frame.pack(pady=20)
        
        enter_btn = tk.Button(button_frame, 
                             text="➕ Add a Business", 
                             command=self.show_enter_page,
                             font=self.fonts["button"],
                             bg=self.colors["success"],
                             fg="white",
                             padx=30,
                             pady=15,
                             cursor="hand2")
        enter_btn.grid(row=0, column=0, padx=10, pady=10)
        
        explore_btn = tk.Button(button_frame, 
                               text="🔍 Explore Businesses", 
                               command=self.show_explore_page,
                               font=self.fonts["button"],
                               bg=self.colors["secondary"],
                               fg="white",
                               padx=30,
                               pady=15,
                               cursor="hand2")
        explore_btn.grid(row=0, column=1, padx=10, pady=10)
        
        # Keyboard shortcut hint
        shortcut_frame = tk.Frame(welcome_card, bg=self.colors["surface"])
        shortcut_frame.pack(pady=10)
        tk.Label(shortcut_frame, 
                text="💡 Tip: Press ESC to return here from any page", 
                font=("Segoe UI", 9, "italic"),
                bg=self.colors["surface"],
                fg=self.colors["text_light"]).pack()


     # ENTER BUSINESS PAGE
    def show_enter_page(self):
        self.clear_content()
        
        # Page header (STAYS FIXED AT TOP - NO SCROLLING)
        header_card = self.create_card(self.content_frame)
        header_card.pack(fill="x", pady=(0, 10)) # Reduced pady slightly
        
        tk.Label(header_card, 
                text="Add a Local Business", 
                font=self.fonts["heading"], 
                bg=self.colors["surface"],
                fg=self.colors["primary"]).pack(anchor="w")
        
        tk.Label(header_card, 
                text="Help promote local businesses by adding them to our directory", 
                font=self.fonts["subheading"], 
                bg=self.colors["surface"],
                fg=self.colors["text_light"]).pack(anchor="w", pady=(0, 10))
        
      
        #   Main container card for the scrollable area
        form_container_card = self.create_card(self.content_frame)
        form_container_card.pack(fill="both", expand=True, pady=(0, 10)) # Fills available space
        
        #   Create a Canvas and a vertical Scrollbar
        form_canvas = tk.Canvas(form_container_card, bg=self.colors["surface"], highlightthickness=0)
        form_scrollbar = ttk.Scrollbar(form_container_card, orient="vertical", command=form_canvas.yview)
        
        #   This is the inner frame that holds ALL the form widgets and will scroll
        form_scrollable_frame = tk.Frame(form_canvas, bg=self.colors["surface"])
        
        #   Configure the canvas scrolling region
        form_scrollable_frame.bind(
            "<Configure>",
            lambda e: form_canvas.configure(scrollregion=form_canvas.bbox("all"))
        )
        #   Put the scrollable frame inside the canvas
        form_canvas.create_window((0, 0), window=form_scrollable_frame, anchor="nw")
        form_canvas.configure(yscrollcommand=form_scrollbar.set)
        
        #   Pack the canvas and scrollbar
        form_canvas.pack(side="left", fill="both", expand=True)
        form_scrollbar.pack(side="right", fill="y")
        
        #   Bind mouse wheel for easier scrolling (Windows/Mac/Linux compatible)
        def _on_mousewheel(event):
            form_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        form_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    
        #  Grouped Form Fields
        # Business Info Group
        business_frame = tk.LabelFrame(form_scrollable_frame, # PARENT CHANGED
                                      text=" Business Information ", 
                                      font=self.fonts["label"],
                                      bg=self.colors["surface"],
                                      fg=self.colors["primary"],
                                      padx=15,
                                      pady=15)
        business_frame.pack(fill="x", pady=(0, 15))
        
        # Store references for validation
        self.entries = {}
        
        # Name field
        tk.Label(business_frame, 
                text="Business Name *", 
                font=self.fonts["label"],
                bg=self.colors["surface"]).grid(row=0, column=0, sticky="w", pady=(0, 5))
        name_entry = tk.Entry(business_frame, width=40, font=self.fonts["body"])
        name_entry.grid(row=0, column=1, sticky="w", pady=(0, 5), padx=(10, 0))
        self.entries["name"] = name_entry
        
        # Address field
        tk.Label(business_frame, 
                text="Address *", 
                font=self.fonts["label"],
                bg=self.colors["surface"]).grid(row=1, column=0, sticky="w", pady=5)
        address_entry = tk.Entry(business_frame, width=40, font=self.fonts["body"])
        address_entry.grid(row=1, column=1, sticky="w", pady=5, padx=(10, 0))
        self.entries["address"] = address_entry
        
        # Category dropdown
        tk.Label(business_frame, 
                text="Category *", 
                font=self.fonts["label"],
                bg=self.colors["surface"]).grid(row=2, column=0, sticky="w", pady=5)
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(business_frame, 
                                     textvariable=category_var, 
                                     values=["Food", "Retail", "Services", "Entertainment", "Other"],
                                     width=37,
                                     state="readonly")
        category_combo.grid(row=2, column=1, sticky="w", pady=5, padx=(10, 0))
        self.entries["category"] = category_combo
        
        # Description
        tk.Label(business_frame, 
                text="Description (max 30 words) *", 
                font=self.fonts["label"],
                bg=self.colors["surface"]).grid(row=3, column=0, sticky="w", pady=5)
        desc_entry = tk.Text(business_frame, height=4, width=40, font=self.fonts["body"])
        desc_entry.grid(row=3, column=1, sticky="w", pady=5, padx=(10, 0))
        self.entries["description"] = desc_entry
        
        # Contact Info Group
        contact_frame = tk.LabelFrame(form_scrollable_frame, # PARENT CHANGED
                                     text=" Contact Details ", 
                                     font=self.fonts["label"],
                                     bg=self.colors["surface"],
                                     fg=self.colors["primary"],
                                     padx=15,
                                     pady=15)
        contact_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(contact_frame, 
                text="Phone (optional)", 
                font=self.fonts["label"],
                bg=self.colors["surface"]).grid(row=0, column=0, sticky="w", pady=5)
        contact_entry = tk.Entry(contact_frame, width=20, font=self.fonts["body"])
        contact_entry.grid(row=0, column=1, sticky="w", pady=5, padx=(10, 0))
        self.entries["contact"] = contact_entry
        
        tk.Label(contact_frame, 
                text="Distance from Paradise Valley HS (miles) *", 
                font=self.fonts["label"],
                bg=self.colors["surface"]).grid(row=1, column=0, sticky="w", pady=5)
        distance_entry = tk.Entry(contact_frame, width=10, font=self.fonts["body"])
        distance_entry.grid(row=1, column=1, sticky="w", pady=5, padx=(10, 0))
        self.entries["distance"] = distance_entry
        
        # Image Upload Section
        image_frame = tk.LabelFrame(form_scrollable_frame, # PARENT CHANGED
                                   text=" Business Image ", 
                                   font=self.fonts["label"],
                                   bg=self.colors["surface"],
                                   fg=self.colors["primary"],
                                   padx=15,
                                   pady=15)
        image_frame.pack(fill="x", pady=(0, 20)) # Added bottom padding
        
        self.image_path_var = tk.StringVar()
        
        def upload_image():
            filetypes = [("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
            filename = filedialog.askopenfilename(filetypes=filetypes)
            if filename:
                if not os.path.exists(IMAGE_FOLDER):
                    os.makedirs(IMAGE_FOLDER)
                unique_filename = str(uuid.uuid4())[:8] + os.path.splitext(filename)[1]
                dest_path = os.path.join(IMAGE_FOLDER, unique_filename)
                shutil.copy(filename, dest_path)
                self.image_path_var.set(dest_path)
        
        upload_btn = tk.Button(image_frame, 
                              text="📁 Upload Image (Optional)", 
                              command=upload_image,
                              font=self.fonts["button"],
                              bg=self.colors["secondary"],
                              fg="white",
                              padx=15,
                              pady=8,
                              cursor="hand2")
        upload_btn.pack(side="left", padx=(0, 10))
        
        tk.Label(image_frame, 
                textvariable=self.image_path_var, 
                font=self.fonts["body"],
                bg=self.colors["surface"],
                fg=self.colors["text_light"],
                wraplength=300).pack(side="left")
        
        
        #   Create a new card for buttons that stays outside the scrollable container
        button_card = self.create_card(self.content_frame)
        button_card.pack(fill="x", pady=(0, 10))
        
        button_frame = tk.Frame(button_card, bg=self.colors["surface"])
        button_frame.pack(pady=10)
        
      
        #   Error label now lives in the fixed button area
        self.error_label = tk.Label(button_frame, 
                                   text="", 
                                   font=self.fonts["label"],
                                   bg=self.colors["surface"],
                                   fg=self.colors["error"])
        self.error_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        #Loading State Button 
        self.submit_btn = tk.Button(button_frame, 
                                   text="✅ Submit Business", 
                                   command=self.submit_business,
                                   font=self.fonts["button"],
                                   bg=self.colors["success"],
                                   fg="white",
                                   padx=25,
                                   pady=10,
                                   cursor="hand2")
        self.submit_btn.grid(row=1, column=0, padx=(0, 10))
        
        back_btn = tk.Button(button_frame, 
                            text="⬅ Back to Home", 
                            command=self.show_start_page,
                            font=self.fonts["button"],
                            bg=self.colors["text_light"],
                            fg="white",
                            padx=25,
                            pady=10,
                            cursor="hand2")
        back_btn.grid(row=1, column=1)
        
        # Bind Enter key to submit
        self.root.bind('<Return>', lambda e: self.submit_business())
        
        # Initial field validation setup
        for entry in [name_entry, address_entry, distance_entry]:
            entry.bind('<KeyRelease>', lambda e: self.validate_field(e.widget))

    #Clear Error States
    def validate_field(self, widget):
        """Validate individual field and update UI"""
        field_name = ""
        value = widget.get()
        
        # Determine which field we're validating
        for name, entry in self.entries.items():
            if widget == entry:
                field_name = name
                break
        
        if field_name == "name":
            if not value.strip():
                self.show_field_error(widget, "Business name is required")
            else:
                self.clear_field_error(widget)
        elif field_name == "address":
            if not value.strip():
                self.show_field_error(widget, "Address is required")
            else:
                self.clear_field_error(widget)
        elif field_name == "distance":
            try:
                if not value.strip():
                    self.show_field_error(widget, "Distance is required")
                elif float(value) < 0:
                    self.show_field_error(widget, "Distance must be positive")
                else:
                    self.clear_field_error(widget)
            except ValueError:
                self.show_field_error(widget, "Distance must be a number")
    
    def show_field_error(self, widget, message):
        """Show error state for a field"""
        widget.config(bg="#FFE6E6", highlightbackground=self.colors["error"], highlightthickness=1)
        self.error_label.config(text=message)
    
    def clear_field_error(self, widget):
        """Clear error state for a field"""
        widget.config(bg="white", highlightbackground="#BDC3C7", highlightthickness=1)
        self.error_label.config(text="")
    
    def submit_business(self):
        """Handle business submission with loading state"""
        #Loading State 
        if self.is_loading:
            return
            
        self.is_loading = True
        self.submit_btn.config(state="disabled", text="⏳ Processing...")
        self.root.update()  # Force UI update
        
        try:
            # Validate all required fields
            errors = []
            
            # Check name
            name = self.entries["name"].get().strip()
            if not name:
                errors.append("Business name is required")
                self.show_field_error(self.entries["name"], "Business name is required")
            
            # Check address
            address = self.entries["address"].get().strip()
            if not address:
                errors.append("Address is required")
                self.show_field_error(self.entries["address"], "Address is required")
            
            # Check category
            category = self.entries["category"].get()
            if not category:
                errors.append("Category is required")
            
            # Check description word count
            desc_words = self.entries["description"].get("1.0", tk.END).strip().split()
            if len(desc_words) > 30:
                errors.append("Description must be 30 words or less")
            
            # Check distance
            distance_str = self.entries["distance"].get().strip()
            if not distance_str:
                errors.append("Distance is required")
                self.show_field_error(self.entries["distance"], "Distance is required")
            else:
                try:
                    distance = float(distance_str)
                    if distance < 0:
                        errors.append("Distance must be positive")
                except ValueError:
                    errors.append("Distance must be a number")
            
            # Check contact
            contact = self.entries["contact"].get().strip()
            if contact and (not contact.replace("-", "").isdigit() or len(contact.replace("-", "")) > 11):
                errors.append("Contact must be up to 11 digits")
            
            if errors:
                self.error_label.config(text=" | ".join(errors[:3]), fg=self.colors["error"])
                return
            
            # All validation passed - save business
            businesses = load_businesses()
            businesses.append({
                "name": name[:50],
                "address": address,
                "category": category,
                "description": " ".join(desc_words[:30]),
                "contact": contact,
                "distance": float(distance_str),
                "image_path": self.image_path_var.get(),
                "reviews": []
            })
            save_businesses(businesses)
            
            # Show success message
            self.error_label.config(text="✅ Business added successfully!", fg=self.colors["success"])
            
            # Brief delay to show success, then return to home
            self.root.after(1000, self.show_start_page)
            
        finally:
            # Reset Loading State
            self.root.after(500, self.reset_loading_state)
    
    def reset_loading_state(self):
        """Reset button to normal state"""
        self.is_loading = False
        self.submit_btn.config(state="normal", text="✅ Submit Business")

    # EXPLORE PAGE 
    # EXPLORE PAGE (Enhanced with similar improvements)
    def show_explore_page(self):
        self.clear_content()
        
        # Page header
        header_card = self.create_card(self.content_frame)
        header_card.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_card, 
                text="Explore Local Businesses", 
                font=self.fonts["heading"], 
                bg=self.colors["surface"],
                fg=self.colors["primary"]).pack(anchor="w")
        
        tk.Label(header_card, 
                text="Discover and support businesses in your community", 
                font=self.fonts["subheading"], 
                bg=self.colors["surface"],
                fg=self.colors["text_light"]).pack(anchor="w", pady=(0, 10))
        
        # Search and filter card
        filter_card = self.create_card(self.content_frame)
        filter_card.pack(fill="x", pady=(0, 20))
        
        # Search bar with icon
        search_frame = tk.Frame(filter_card, bg=self.colors["surface"])
        search_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(search_frame, 
                text="🔍 Search Businesses:", 
                font=self.fonts["label"],
                bg=self.colors["surface"]).pack(side="left", padx=(0, 10))
        
        search_entry = tk.Entry(search_frame, width=40, font=self.fonts["body"])
        search_entry.pack(side="left")
        
        # Filter controls
        filter_frame = tk.Frame(filter_card, bg=self.colors["surface"])
        filter_frame.pack(fill="x")
        
        tk.Label(filter_frame, 
                text="Category:", 
                font=self.fonts["label"],
                bg=self.colors["surface"]).grid(row=0, column=0, padx=(0, 5))
        
        category_filter = ttk.Combobox(filter_frame, 
                                    values=["All", "Food", "Retail", "Services", "Entertainment", "Other"],
                                    width=15,
                                    state="readonly")
        category_filter.set("All")
        category_filter.grid(row=0, column=1, padx=(0, 20))
        
        tk.Label(filter_frame, 
                text="Max Distance:", 
                font=self.fonts["label"],
                bg=self.colors["surface"]).grid(row=0, column=2, padx=(0, 5))
        
        distance_filter = ttk.Combobox(filter_frame, 
                                    values=["All", "5", "10", "15"],
                                    width=10,
                                    state="readonly")
        distance_filter.set("All")
        distance_filter.grid(row=0, column=3)
        
        # Business list card
        list_card = self.create_card(self.content_frame)
        list_card.pack(fill="both", expand=True, pady=(0, 20))
        
        # Business list with scrollbar
        list_frame = tk.Frame(list_card, bg=self.colors["surface"])
        list_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.business_listbox = tk.Listbox(list_frame, 
                                        yscrollcommand=scrollbar.set,
                                        font=self.fonts["body"],
                                        bg="white",
                                        selectbackground=self.colors["secondary"],
                                        selectforeground="white",
                                        height=15)
        self.business_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.business_listbox.yview)
        
        # Store filtered businesses
        self.filtered_businesses = []
        
        def refresh_list():
            self.business_listbox.delete(0, tk.END)
            businesses = load_businesses()
            
            # Apply filters
            self.filtered_businesses = businesses
            if category_filter.get() != "All":
                self.filtered_businesses = [b for b in self.filtered_businesses if b["category"] == category_filter.get()]
            if distance_filter.get() != "All":
                self.filtered_businesses = [b for b in self.filtered_businesses if b["distance"] <= float(distance_filter.get())]
            if search_entry.get().strip():
                search_term = search_entry.get().strip().lower()
                self.filtered_businesses = [b for b in self.filtered_businesses if search_term in b["name"].lower()]
            
            # Display with icons
            for b in self.filtered_businesses:
                rating = "No ratings"
                if b["reviews"]:
                    avg = sum(r["rating"] for r in b["reviews"]) / len(b["reviews"])
                    rating = f"⭐{avg:.1f}/5"
                
                # Add icons based on category
                icon = "🍽️" if b["category"] == "Food" else \
                    "🛍️" if b["category"] == "Retail" else \
                    "🔧" if b["category"] == "Services" else \
                    "🎭" if b["category"] == "Entertainment" else "🏢"
                
                has_image = " 📷" if b.get("image_path") and os.path.exists(b.get("image_path")) else ""
                
                self.business_listbox.insert(tk.END, 
                    f"{icon} {b['name']} | {b['category']} | {b['distance']}mi | {rating}{has_image}")
        
        # Bind filter changes
        for widget in [search_entry, category_filter, distance_filter]:
            if isinstance(widget, tk.Entry):
                widget.bind('<KeyRelease>', lambda e: refresh_list())
            else:
                widget.bind('<<ComboboxSelected>>', lambda e: refresh_list())
        
        # Initial load
        refresh_list()
        
        # Action buttons
        action_frame = tk.Frame(list_card, bg=self.colors["surface"])
        action_frame.pack(pady=10)
        
        view_btn = tk.Button(action_frame, 
                            text="👁️ View Details", 
                            command=self.view_business_details,  # Fixed: removed lambda
                            font=self.fonts["button"],
                            bg=self.colors["secondary"],
                            fg="white",
                            padx=20,
                            pady=8,
                            cursor="hand2")
        view_btn.pack(side="left", padx=(0, 10))
        
        refresh_btn = tk.Button(action_frame, 
                            text="🔄 Refresh List", 
                            command=refresh_list,
                            font=self.fonts["button"],
                            bg=self.colors["text_light"],
                            fg="white",
                            padx=20,
                            pady=8,
                            cursor="hand2")
        refresh_btn.pack(side="left", padx=(0, 10))
        
        back_btn = tk.Button(action_frame, 
                            text="⬅ Back to Home", 
                            command=self.show_start_page,
                            font=self.fonts["button"],
                            bg=self.colors["text_light"],
                            fg="white",
                            padx=20,
                            pady=8,
                            cursor="hand2")
        back_btn.pack(side="left")
        
        # Double-click to view details
        self.business_listbox.bind('<Double-Button-1>', lambda e: self.view_business_details())

    def view_business_details(self):
        """View details of selected business"""
        selection = self.business_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a business first.")
            return
        
        index = selection[0]
        if index >= len(self.filtered_businesses):
            return
        
        selected_business = self.filtered_businesses[index]
        
        # Find the actual index in the full database
        all_businesses = load_businesses()
        actual_index = None
        for i, b in enumerate(all_businesses):
            if b["name"] == selected_business["name"] and b["address"] == selected_business["address"]:
                actual_index = i
                break
        
        if actual_index is None:
            messagebox.showerror("Error", "Could not locate business in database.")
            return
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Details: {selected_business['name']}")
        details_window.geometry("700x800")
        details_window.configure(bg=self.colors["background"])
        
        # Make window modal
        details_window.transient(self.root)
        details_window.grab_set()
        

        header = tk.Frame(details_window, bg=self.colors["primary"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, 
                text=selected_business["name"], 
                font=("Segoe UI", 16, "bold"),
                bg=self.colors["primary"],
                fg="white").pack(pady=15)
        
        #     Create a main frame to hold the canvas and scrollbar
        main_container = tk.Frame(details_window, bg=self.colors["background"])
        main_container.pack(fill="both", expand=True)
        
        #     Create Canvas and Scrollbar
        content_canvas = tk.Canvas(main_container, bg=self.colors["background"], highlightthickness=0)
        content_scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=content_canvas.yview)
        
        #     This is the inner frame that will hold all scrollable content
        scrollable_content_frame = tk.Frame(content_canvas, bg=self.colors["background"], padx=30, pady=20)
        
        #     Configure canvas scrolling
        scrollable_content_frame.bind(
            "<Configure>",
            lambda e: content_canvas.configure(scrollregion=content_canvas.bbox("all"))
        )
        content_canvas.create_window((0, 0), window=scrollable_content_frame, anchor="nw")
        content_canvas.configure(yscrollcommand=content_scrollbar.set)
        
        #     Pack canvas and scrollbar
        content_canvas.pack(side="left", fill="both", expand=True)
        content_scrollbar.pack(side="right", fill="y")
        
        #     Bind mouse wheel for easier scrolling
        def _on_mousewheel(event):
            content_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        content_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        #     Make sure to unbind when window closes to prevent errors
        def _cleanup_bind():
            content_canvas.unbind_all("<MouseWheel>")
        details_window.protocol("WM_DELETE_WINDOW", lambda: [details_window.destroy(), _cleanup_bind()])
        
        #     All main content now goes into 'scrollable_content_frame'
        # Business info card
        info_card = self.create_card(scrollable_content_frame) # PARENT CHANGED
        info_card.pack(fill="x", pady=(0, 20))
        
        # Category icon
        icon = "🍽️" if selected_business["category"] == "Food" else \
               "🛍️" if selected_business["category"] == "Retail" else \
               "🔧" if selected_business["category"] == "Services" else \
               "🎭" if selected_business["category"] == "Entertainment" else "🏢"
        
        tk.Label(info_card, 
                text=f"{icon} {selected_business['category']}", 
                font=self.fonts["heading"],
                bg=self.colors["surface"],
                fg=self.colors["primary"]).pack(anchor="w", pady=(0, 10))
        
        # Details grid
        details = [
            ("📍 Address:", selected_business["address"]),
            ("📞 Contact:", selected_business.get("contact", "Not provided")),
            ("📏 Distance:", f"{selected_business['distance']} miles from Paradise Valley HS"),
            ("📝 Description:", selected_business["description"])
        ]
        
        for label, value in details:
            detail_frame = tk.Frame(info_card, bg=self.colors["surface"])
            detail_frame.pack(fill="x", pady=5)
            
            tk.Label(detail_frame, 
                    text=label, 
                    font=self.fonts["label"],
                    bg=self.colors["surface"],
                    fg=self.colors["text_light"],
                    width=15,
                    anchor="w").pack(side="left")
            
            tk.Label(detail_frame, 
                    text=value, 
                    font=self.fonts["body"],
                    bg=self.colors["surface"],
                    wraplength=400,
                    justify="left").pack(side="left", padx=(10, 0))
        
        # Display image if available
        image_path = selected_business.get("image_path", "")
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                img_frame = tk.Frame(info_card, bg=self.colors["surface"])
                img_frame.pack(pady=10)
                
                tk.Label(img_frame, 
                        text="Business Image:", 
                        font=self.fonts["label"],
                        bg=self.colors["surface"]).pack()
                
                img_label = tk.Label(img_frame, image=photo, bg=self.colors["surface"])
                img_label.image = photo
                img_label.pack(pady=5)
            except Exception as e:
                tk.Label(info_card, 
                        text="📷 Image not available", 
                        font=self.fonts["body"],
                        bg=self.colors["surface"],
                        fg=self.colors["text_light"]).pack()
        
        # Reviews section
        reviews_card = self.create_card(scrollable_content_frame) # PARENT CHANGED
        reviews_card.pack(fill="x", pady=(0, 20))
        
        tk.Label(reviews_card, 
                text="⭐ Customer Reviews", 
                font=self.fonts["heading"],
                bg=self.colors["surface"],
                fg=self.colors["primary"]).pack(anchor="w", pady=(0, 10))
        
        if selected_business["reviews"]:
            avg_rating = sum(r["rating"] for r in selected_business["reviews"]) / len(selected_business["reviews"])
            tk.Label(reviews_card, 
                    text=f"Average Rating: {avg_rating:.1f}/5", 
                    font=self.fonts["subheading"],
                    bg=self.colors["surface"]).pack(anchor="w", pady=(0, 10))
            
            for review in selected_business["reviews"]:
                review_frame = tk.Frame(reviews_card, bg="#F8F9FA", padx=10, pady=8)
                review_frame.pack(fill="x", pady=5)
                
                stars = "⭐" * review["rating"] + "☆" * (5 - review["rating"])
                tk.Label(review_frame, 
                        text=stars, 
                        font=self.fonts["body"],
                        bg="#F8F9FA",
                        fg="#FFD700").pack(anchor="w")
                
                if review.get("text"):
                    tk.Label(review_frame, 
                            text=f'"{review["text"]}"', 
                            font=self.fonts["body"],
                            bg="#F8F9FA",
                            wraplength=400,
                            justify="left").pack(anchor="w")
        else:
            tk.Label(reviews_card, 
                    text="No reviews yet. Be the first to review!", 
                    font=self.fonts["body"],
                    bg=self.colors["surface"],
                    fg=self.colors["text_light"]).pack(pady=10)
        
        # Add review section (still inside scrollable area for input fields)
        add_review_frame = self.create_card(scrollable_content_frame) # PARENT CHANGED
        add_review_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(add_review_frame, 
                text="Add Your Review", 
                font=self.fonts["heading"],
                bg=self.colors["surface"],
                fg=self.colors["primary"]).pack(anchor="w", pady=(0, 10))
        
        rating_frame = tk.Frame(add_review_frame, bg=self.colors["surface"])
        rating_frame.pack(fill="x", pady=5)
        
        tk.Label(rating_frame, 
                text="Rating:", 
                font=self.fonts["label"],
                bg=self.colors["surface"]).pack(side="left", padx=(0, 10))
        
        rating_var = tk.IntVar(value=5)
        rating_scale = tk.Scale(rating_frame, 
                               from_=1, to=5, 
                               variable=rating_var,
                               orient="horizontal",
                               length=200,
                               showvalue=True,
                               tickinterval=1,
                               bg=self.colors["surface"])
        rating_scale.pack(side="left")
        
        tk.Label(add_review_frame, 
                text="Review (optional):", 
                font=self.fonts["label"],
                bg=self.colors["surface"]).pack(anchor="w", pady=(10, 5))
        
        review_text = tk.Entry(add_review_frame, 
                              width=50,
                              font=self.fonts["body"])
        review_text.pack(fill="x", pady=(0, 10))
        
    
        #     Create a separate frame for buttons at the bottom of the window
        button_container = tk.Frame(details_window, bg=self.colors["background"], padx=30, pady=20)
        button_container.pack(fill="x", side="bottom")
        
        def save_review():
            all_businesses = load_businesses()
            all_businesses[actual_index]["reviews"].append({
                "rating": rating_var.get(),
                "text": review_text.get()
            })
            save_businesses(all_businesses)
            messagebox.showinfo("Success", "Thank you for your review!")
            # Clean up mouse wheel binding before closing
            content_canvas.unbind_all("<MouseWheel>")
            details_window.destroy()
            self.show_explore_page()  # Refresh explore page
        
        button_frame = tk.Frame(button_container, bg=self.colors["background"])
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, 
                 text="Submit Review", 
                 command=save_review,
                 font=self.fonts["button"],
                 bg=self.colors["success"],
                 fg="white",
                 padx=20,
                 pady=8).pack(side="left", padx=(0, 10))
        
        tk.Button(button_frame, 
                 text="Close", 
                 command=lambda: [content_canvas.unbind_all("<MouseWheel>"), details_window.destroy()],
                 font=self.fonts["button"],
                 bg=self.colors["text_light"],
                 fg="white",
                 padx=20,
                 pady=8).pack(side="left")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = BusinessApp(root)
    root.mainloop()