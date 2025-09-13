import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from collections import defaultdict

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Expense Tracker - Personal Finance Manager")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Data storage
        self.expenses = []
        self.categories = ["Food", "Transportation", "Entertainment", "Shopping", "Bills", "Healthcare", "Education", "Other"]
        self.data_file = "expenses.json"
        self.logs = []  # Store action logs
        
        # Create GUI
        self.create_widgets()

        # Load existing data (after widgets so logs can render)
        self.load_data()

        self.update_display()
        
    def create_widgets(self):
        # Main frame with gradient-like background
        main_frame = tk.Frame(self.root, bg='#34495e', relief='raised', bd=2)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)  # Left panel
        main_frame.columnconfigure(1, weight=1)  # Right panel
        main_frame.rowconfigure(1, weight=0)  # Upper panels
        main_frame.rowconfigure(2, weight=1)  # Middle panels
        main_frame.rowconfigure(3, weight=0)  # Lower components
        
        # Title with colorful styling
        title_frame = tk.Frame(main_frame, bg='#34495e')
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))
        
        title_label = tk.Label(title_frame, text="💰 Expense Tracker", 
                              font=('Arial', 28, 'bold'), 
                              foreground='#ecf0f1', 
                              bg='#34495e',
                              relief='raised',
                              bd=3)
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(title_frame, text="Personal Finance Manager", 
                                 font=('Arial', 12, 'italic'), 
                                 foreground='#bdc3c7', 
                                 bg='#34495e')
        subtitle_label.pack()
        
        # Upper Left panel - Add Expense with enhanced styling
        left_frame = tk.LabelFrame(main_frame, text="📝 Add New Expense", 
                                  font=('Arial', 12, 'bold'),
                                  fg='#2c3e50', bg='#ecf0f1', 
                                  relief='raised', bd=3)
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        desc_label = tk.Label(left_frame, text="📄 Description:", 
                             font=('Arial', 10, 'bold'), 
                             fg='#2c3e50', bg='#ecf0f1')
        desc_label.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.desc_entry = tk.Entry(left_frame, width=25, font=('Arial', 10), 
                                  bg='#ffffff', fg='#2c3e50', relief='sunken', bd=2)
        self.desc_entry.grid(row=0, column=1, pady=5, padx=(10, 5))
        
        amount_label = tk.Label(left_frame, text="💰 Amount ($):", 
                               font=('Arial', 10, 'bold'), 
                               fg='#e74c3c', bg='#ecf0f1')
        amount_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.amount_entry = tk.Entry(left_frame, width=25, font=('Arial', 10), 
                                    bg='#ffffff', fg='#2c3e50', relief='sunken', bd=2)
        self.amount_entry.grid(row=1, column=1, pady=5, padx=(10, 5))
        
        category_label = tk.Label(left_frame, text="🏷️ Category:", 
                                 font=('Arial', 10, 'bold'), 
                                 fg='#3498db', bg='#ecf0f1')
        category_label.grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(left_frame, textvariable=self.category_var, 
                                          values=self.categories, width=22, font=('Arial', 10))
        self.category_combo.grid(row=2, column=1, pady=5, padx=(10, 5))
        self.category_combo.set("Food")
        
        date_label = tk.Label(left_frame, text="📅 Date (Y/M/D):", 
                             font=('Arial', 10, 'bold'), 
                             fg='#27ae60', bg='#ecf0f1')
        date_label.grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        
        date_selector_frame = tk.Frame(left_frame, bg='#ecf0f1')
        date_selector_frame.grid(row=3, column=1, pady=5, padx=(10, 5))
        
        self.year_var = tk.StringVar(value="2025")
        year_combo = ttk.Combobox(date_selector_frame, textvariable=self.year_var, width=6, values=[str(y) for y in range(2000, 2031)])
        year_combo.pack(side=tk.LEFT, padx=2)
        year_combo.bind("<<ComboboxSelected>>", lambda e: self.update_day_options(self.day_combo, self.day_var))
        
        self.month_var = tk.StringVar(value="09")
        month_combo = ttk.Combobox(date_selector_frame, textvariable=self.month_var, width=4, values=[f"{m:02d}" for m in range(1, 13)])
        month_combo.pack(side=tk.LEFT, padx=2)
        month_combo.bind("<<ComboboxSelected>>", lambda e: self.update_day_options(self.day_combo, self.day_var))
        
        self.day_var = tk.StringVar(value="12")
        self.day_combo = ttk.Combobox(date_selector_frame, textvariable=self.day_var, width=4, values=[f"{d:02d}" for d in range(1, 32)])
        self.day_combo.pack(side=tk.LEFT, padx=2)
        self.update_day_options(self.day_combo, self.day_var)
        
        button_frame = tk.Frame(left_frame, bg='#ecf0f1')
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        add_btn = tk.Button(button_frame, text="➕ Add Expense", command=self.add_expense,
                           font=('Arial', 10, 'bold'), bg='#27ae60', fg='white',
                           relief='raised', bd=3, padx=10, pady=5)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="🗑️ Clear", command=self.clear_form,
                             font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white',
                           relief='raised', bd=3, padx=10, pady=5)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Upper Middle panel - Statistics Dashboard with enhanced styling
        middle_frame = tk.LabelFrame(main_frame, text="📊 Statistics Dashboard", 
                                    font=('Arial', 12, 'bold'),
                                    fg='#2c3e50', bg='#ecf0f1', 
                                    relief='raised', bd=3)
        middle_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        middle_frame.columnconfigure(0, weight=1)
        
        stats_bg = '#f8f9fa'
        self.total_label = tk.Label(middle_frame, text="💸 Total Expenses: $0.00", 
                                   font=('Arial', 12, 'bold'), 
                                   fg='#e74c3c', bg=stats_bg,
                                   relief='raised', bd=2, padx=10, pady=5)
        self.total_label.grid(row=0, column=0, pady=5, padx=5, sticky=(tk.W, tk.E))
        
        self.monthly_label = tk.Label(middle_frame, text="📅 This Month: $0.00", 
                                     font=('Arial', 10, 'bold'), 
                                     fg='#3498db', bg=stats_bg,
                                     relief='raised', bd=2, padx=10, pady=5)
        self.monthly_label.grid(row=1, column=0, pady=5, padx=5, sticky=(tk.W, tk.E))
        
        self.avg_label = tk.Label(middle_frame, text="📈 Daily Average: $0.00", 
                                 font=('Arial', 10, 'bold'), 
                                 fg='#27ae60', bg=stats_bg,
                                 relief='raised', bd=2, padx=10, pady=5)
        self.avg_label.grid(row=2, column=0, pady=5, padx=5, sticky=(tk.W, tk.E))
        
        # Upper Right panel - Filters with enhanced styling
        right_frame = tk.LabelFrame(main_frame, text="🔍 Filters & Search", 
                                   font=('Arial', 12, 'bold'),
                                   fg='#2c3e50', bg='#ecf0f1', 
                                   relief='raised', bd=3)
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 0))
        
        cat_label = tk.Label(right_frame, text="🏷️ Category:", 
                            font=('Arial', 10, 'bold'), 
                            fg='#3498db', bg='#ecf0f1')
        cat_label.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.filter_category_var = tk.StringVar()
        self.filter_category_combo = ttk.Combobox(right_frame, textvariable=self.filter_category_var,
                                                 values=["All"] + self.categories, width=15)
        self.filter_category_combo.grid(row=0, column=1, pady=5, padx=(10, 5))
        self.filter_category_combo.set("All")
        
        from_label = tk.Label(right_frame, text="📅 Date From (Y/M/D):", 
                             font=('Arial', 10, 'bold'), 
                             fg='#27ae60', bg='#ecf0f1')
        from_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        
        date_from_frame = tk.Frame(right_frame, bg='#ecf0f1')
        date_from_frame.grid(row=1, column=1, pady=5, padx=(10, 5))
        
        self.from_year_var = tk.StringVar(value="")
        from_year_combo = ttk.Combobox(date_from_frame, textvariable=self.from_year_var, width=6, values=[""] + [str(y) for y in range(2000, 2031)])
        from_year_combo.pack(side=tk.LEFT, padx=2)
        from_year_combo.bind("<<ComboboxSelected>>", lambda e: self.update_day_options(self.from_day_combo, self.from_day_var))
        
        self.from_month_var = tk.StringVar(value="")
        from_month_combo = ttk.Combobox(date_from_frame, textvariable=self.from_month_var, width=4, values=[""] + [f"{m:02d}" for m in range(1, 13)])
        from_month_combo.pack(side=tk.LEFT, padx=2)
        from_month_combo.bind("<<ComboboxSelected>>", lambda e: self.update_day_options(self.from_day_combo, self.from_day_var))
        
        self.from_day_var = tk.StringVar(value="")
        self.from_day_combo = ttk.Combobox(date_from_frame, textvariable=self.from_day_var, width=4, values=[""] + [f"{d:02d}" for d in range(1, 32)])
        self.from_day_combo.pack(side=tk.LEFT, padx=2)
        
        to_label = tk.Label(right_frame, text="📅 Date To (Y/M/D):", 
                           font=('Arial', 10, 'bold'), 
                           fg='#e67e22', bg='#ecf0f1')
        to_label.grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        
        date_to_frame = tk.Frame(right_frame, bg='#ecf0f1')
        date_to_frame.grid(row=2, column=1, pady=5, padx=(10, 5))
        
        self.to_year_var = tk.StringVar(value="")
        to_year_combo = ttk.Combobox(date_to_frame, textvariable=self.to_year_var, width=6, values=[""] + [str(y) for y in range(2000, 2031)])
        to_year_combo.pack(side=tk.LEFT, padx=2)
        to_year_combo.bind("<<ComboboxSelected>>", lambda e: self.update_day_options(self.to_day_combo, self.to_day_var))
        
        self.to_month_var = tk.StringVar(value="")
        to_month_combo = ttk.Combobox(date_to_frame, textvariable=self.to_month_var, width=4, values=[""] + [f"{m:02d}" for m in range(1, 13)])
        to_month_combo.pack(side=tk.LEFT, padx=2)
        to_month_combo.bind("<<ComboboxSelected>>", lambda e: self.update_day_options(self.to_day_combo, self.to_day_var))
        
        self.to_day_var = tk.StringVar(value="")
        self.to_day_combo = ttk.Combobox(date_to_frame, textvariable=self.to_day_var, width=4, values=[""] + [f"{d:02d}" for d in range(1, 32)])
        self.to_day_combo.pack(side=tk.LEFT, padx=2)
        
        filter_button_frame = tk.Frame(right_frame, bg='#ecf0f1')
        filter_button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        apply_btn = tk.Button(filter_button_frame, text="🔍 Apply Filter", command=self.apply_filter,
                             font=('Arial', 9, 'bold'), bg='#3498db', fg='white',
                             relief='raised', bd=2, padx=8, pady=4)
        apply_btn.pack(side=tk.LEFT, padx=2)
        
        clear_filter_btn = tk.Button(filter_button_frame, text="🗑️ Clear Filter", command=self.clear_filter,
                                   font=('Arial', 9, 'bold'), bg='#e74c3c', fg='white',
                                   relief='raised', bd=2, padx=8, pady=4)
        clear_filter_btn.pack(side=tk.LEFT, padx=2)
        
        # Middle Left panel - Expense History with enhanced styling
        history_frame = tk.LabelFrame(main_frame, text="📜 Expense History", 
                                     font=('Arial', 12, 'bold'),
                                     fg='#2c3e50', bg='#ecf0f1', 
                                     relief='raised', bd=3)
        history_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5), pady=5)
        
        self.tree = ttk.Treeview(history_frame, columns=('ID', 'Date', 'Description', 'Category', 'Amount'), show='headings')
        self.tree.heading('ID', text='🆔 ID')
        self.tree.heading('Date', text='📅 Date')
        self.tree.heading('Description', text='📄 Description')
        self.tree.heading('Category', text='🏷️ Category')
        self.tree.heading('Amount', text='💰 Amount')
        self.tree.column('ID', width=50)
        self.tree.column('Date', width=100)
        self.tree.column('Description', width=200)
        self.tree.column('Category', width=150)
        self.tree.column('Amount', width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="✏️ Edit", command=self.edit_expense)
        self.context_menu.add_command(label="🗑️ Delete", command=self.delete_expense)
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        action_frame = tk.Frame(history_frame, bg='#ecf0f1')
        action_frame.pack(fill=tk.X, pady=5)
        
        edit_btn = tk.Button(action_frame, text="✏️ Edit Selected", command=self.edit_expense,
                            font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                            relief='raised', bd=3, padx=10, pady=5)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(action_frame, text="🗑️ Delete Selected", command=self.delete_expense,
                              font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white',
                              relief='raised', bd=3, padx=10, pady=5)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = tk.Button(action_frame, text="📤 Export Data", command=self.export_data,
                              font=('Arial', 10, 'bold'), bg='#27ae60', fg='white',
                              relief='raised', bd=3, padx=10, pady=5)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        import_btn = tk.Button(action_frame, text="📥 Import Data", command=self.import_data,
                              font=('Arial', 10, 'bold'), bg='#9b59b6', fg='white',
                              relief='raised', bd=3, padx=10, pady=5)
        import_btn.pack(side=tk.LEFT, padx=5)
        
        # Middle Right panel - Category Breakdown with enhanced styling
        category_chart_frame = tk.LabelFrame(main_frame, text="🏷️ Category Breakdown", 
                                            font=('Arial', 12, 'bold'), fg='#2c3e50', bg='#ecf0f1',
                                            relief='raised', bd=3)
        category_chart_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0), pady=5)
        
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=category_chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Lower panel - Quick Stats, Activity Log, View Detailed Charts
        lower_frame = tk.Frame(main_frame, bg='#34495e')
        lower_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        lower_frame.columnconfigure(0, weight=1)
        
        # Quick Stats
        quick_stats_frame = tk.LabelFrame(lower_frame, text="⚡ Quick Stats", 
                                         font=('Arial', 10, 'bold'), fg='#2c3e50', bg='#ecf0f1',
                                         relief='raised', bd=2)
        quick_stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        stats_bg = '#f8f9fa'
        self.highest_label = tk.Label(quick_stats_frame, text="📈 Highest: None", 
                                     font=('Arial', 9, 'bold'), fg='#e67e22', bg=stats_bg,
                                     relief='flat', padx=5, pady=2)
        self.highest_label.pack(fill=tk.X, padx=5, pady=2)
        
        self.lowest_label = tk.Label(quick_stats_frame, text="📉 Lowest: None", 
                                    font=('Arial', 9, 'bold'), fg='#9b59b6', bg=stats_bg,
                                    relief='flat', padx=5, pady=2)
        self.lowest_label.pack(fill=tk.X, padx=5, pady=2)
        
        # Activity Log
        log_frame = tk.LabelFrame(lower_frame, text="📜 Activity Log", 
                                 font=('Arial', 10, 'bold'), fg='#2c3e50', bg='#ecf0f1',
                                 relief='raised', bd=2)
        log_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.log_text = tk.Text(log_frame, height=5, font=('Arial', 9), 
                                bg='#ffffff', fg='#2c3e50', relief='sunken', bd=2, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # View Detailed Charts button
        detailed_chart_btn = tk.Button(lower_frame, text="📊 View Detailed Charts", command=self.show_charts,
                                      font=('Arial', 11, 'bold'), bg='#9b59b6', fg='white',
                                      relief='raised', bd=3, padx=15, pady=8)
        detailed_chart_btn.pack(pady=10)
    
    def add_log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(f"{timestamp}: {message}")
        if len(self.logs) > 50:
            self.logs.pop(0)
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        for log in self.logs:
            self.log_text.insert(tk.END, log + "\n")
        self.log_text.configure(state='disabled')
        self.log_text.see(tk.END)
    
    def update_day_options(self, day_combo, day_var, event=None):
        try:
            from_day_combo = getattr(self, 'from_day_combo', None)
            to_day_combo = getattr(self, 'to_day_combo', None)

            if day_combo is from_day_combo:
                year_var = self.from_year_var
                month_var = self.from_month_var
            elif day_combo is to_day_combo:
                year_var = self.to_year_var
                month_var = self.to_month_var
            else:
                year_var = self.year_var
                month_var = self.month_var

            year = year_var.get()
            month = month_var.get()
            if not year or not month:
                day_combo['values'] = [""] + [f"{d:02d}" for d in range(1, 32)]
                day_var.set("")
                return
            year = int(year)
            month = int(month)
            if month == 2:
                max_days = 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
            elif month in [4, 6, 9, 11]:
                max_days = 30
            else:
                max_days = 31
            day_combo['values'] = [""] + [f"{d:02d}" for d in range(1, max_days + 1)]
            if day_var.get() and int(day_var.get()) > max_days:
                day_var.set(f"{max_days:02d}")
        except ValueError:
            pass
    
    def add_expense(self):
        description = self.desc_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_var.get()
        year = self.year_var.get()
        month = self.month_var.get()
        day = self.day_var.get()
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
            if not description:
                raise ValueError("Description cannot be empty")
            date = f"{year}-{month}-{day}"
            datetime.strptime(date, "%Y-%m-%d")
            
            max_id = max([exp['id'] for exp in self.expenses], default=0)
            new_expense = {
                'id': max_id + 1,
                'description': description,
                'amount': amount,
                'category': category,
                'date': date
            }
            
            self.expenses.append(new_expense)
            self.save_data()
            self.add_log(f"Added expense: {description} (${amount:.2f}, {category}, {date})")
            self.clear_form()
            self.update_display()
            messagebox.showinfo("✅ Success", "Expense added successfully!")
            
        except ValueError as e:
            messagebox.showerror("❌ Error", f"Invalid input: {str(e)}")
    
    def clear_form(self):
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_var.set("Food")
        self.year_var.set("2025")
        self.month_var.set("09")
        self.day_var.set("12")
        self.update_day_options(self.day_combo, self.day_var)
    
    def update_display(self):
        # Clear current treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add filtered expenses
        filtered_expenses = self.get_filtered_expenses()
        for expense in filtered_expenses:
            self.tree.insert('', tk.END, values=(
                expense['id'],
                expense['date'],
                expense['description'],
                expense['category'],
                f"${expense['amount']:.2f}"
            ))
        
        # Update statistics
        total = sum(exp['amount'] for exp in filtered_expenses)
        self.total_label.config(text=f"💸 Total Expenses: ${total:.2f}")
        
        current_month = datetime.now().strftime("%Y-%m")
        monthly_total = sum(exp['amount'] for exp in filtered_expenses 
                           if exp['date'].startswith(current_month))
        self.monthly_label.config(text=f"📅 This Month: ${monthly_total:.2f}")
        
        if filtered_expenses:
            dates = [datetime.strptime(exp['date'], "%Y-%m-%d") for exp in filtered_expenses]
            if dates:
                days = (max(dates) - min(dates)).days + 1
                daily_avg = total / days if days > 0 else total
                self.avg_label.config(text=f"📈 Daily Average: ${daily_avg:.2f}")
            else:
                self.avg_label.config(text="📈 Daily Average: $0.00")
        else:
            self.avg_label.config(text="📈 Daily Average: $0.00")
        
        # Update quick stats
        if filtered_expenses:
            highest = max(filtered_expenses, key=lambda x: x['amount'])
            lowest = min(filtered_expenses, key=lambda x: x['amount'])
            self.highest_label.config(text=f"📈 Highest: {highest['description']} (${highest['amount']:.2f})")
            self.lowest_label.config(text=f"📉 Lowest: {lowest['description']} (${lowest['amount']:.2f})")
        else:
            self.highest_label.config(text="📈 Highest: None")
            self.lowest_label.config(text="📉 Lowest: None")
        
        # Update pie chart
        self.ax.clear()
        category_totals = defaultdict(float)
        for expense in filtered_expenses:
            category_totals[expense['category']] += expense['amount']
        if category_totals:
            self.ax.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=90)
            self.ax.set_title('Category Breakdown')
        else:
            self.ax.text(0.5, 0.5, 'No Data', horizontalalignment='center', verticalalignment='center')
        self.canvas.draw()
    
    def get_filtered_expenses(self):
        filtered = self.expenses[:]
        
        category = self.filter_category_var.get()
        if category != "All":
            filtered = [exp for exp in filtered if exp['category'] == category]
        
        from_year = self.from_year_var.get()
        from_month = self.from_month_var.get()
        from_day = self.from_day_var.get()
        to_year = self.to_year_var.get()
        to_month = self.to_month_var.get()
        to_day = self.to_day_var.get()
        
        if from_year and from_month and from_day:
            try:
                date_from = f"{from_year}-{from_month}-{from_day}"
                datetime.strptime(date_from, "%Y-%m-%d")
                filtered = [exp for exp in filtered if exp['date'] >= date_from]
            except ValueError:
                pass
        
        if to_year and to_month and to_day:
            try:
                date_to = f"{to_year}-{to_month}-{to_day}"
                datetime.strptime(date_to, "%Y-%m-%d")
                filtered = [exp for exp in filtered if exp['date'] <= date_to]
            except ValueError:
                pass
        
        return filtered
    
    def apply_filter(self):
        self.update_display()
    
    def clear_filter(self):
        self.filter_category_var.set("All")
        self.from_year_var.set("")
        self.from_month_var.set("")
        self.from_day_var.set("")
        self.to_year_var.set("")
        self.to_month_var.set("")
        self.to_day_var.set("")
        self.update_day_options(self.from_day_combo, self.from_day_var)
        self.update_day_options(self.to_day_combo, self.to_day_var)
        self.update_display()
    
    def show_context_menu(self, event):
        if self.tree.identify_row(event.y):
            self.tree.selection_set(self.tree.identify_row(event.y))
            self.context_menu.post(event.x_root, event.y_root)
    
    def edit_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to edit")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        
        for expense in self.expenses:
            if (expense['id'] == values[0] and 
                expense['date'] == values[1] and 
                expense['description'] == values[2] and 
                expense['category'] == values[3] and 
                f"${expense['amount']:.2f}" == values[4]):
                self.edit_expense_dialog(expense)
                break
    
    def edit_expense_dialog(self, expense):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("✏️ Edit Expense")
        edit_window.geometry("450x350")
        edit_window.configure(bg='#34495e')
        
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        title_label = tk.Label(edit_window, text="✏️ Edit Expense", 
                              font=('Arial', 16, 'bold'), 
                              fg='#ecf0f1', bg='#34495e')
        title_label.pack(pady=10)
        
        form_frame = tk.Frame(edit_window, bg='#ecf0f1', relief='raised', bd=2)
        form_frame.pack(pady=10, padx=20, fill='x')
        
        desc_label = tk.Label(form_frame, text="📄 Description:", 
                             font=('Arial', 10, 'bold'), 
                             fg='#2c3e50', bg='#ecf0f1')
        desc_label.pack(pady=5)
        desc_entry = tk.Entry(form_frame, width=40, font=('Arial', 10), 
                             bg='#ffffff', fg='#2c3e50', relief='sunken', bd=2)
        desc_entry.pack(pady=5)
        desc_entry.insert(0, expense['description'])
        
        amount_label = tk.Label(form_frame, text="💰 Amount ($):", 
                               font=('Arial', 10, 'bold'), 
                               fg='#e74c3c', bg='#ecf0f1')
        amount_label.pack(pady=5)
        amount_entry = tk.Entry(form_frame, width=40, font=('Arial', 10), 
                               bg='#ffffff', fg='#2c3e50', relief='sunken', bd=2)
        amount_entry.pack(pady=5)
        amount_entry.insert(0, str(expense['amount']))
        
        category_label = tk.Label(form_frame, text="🏷️ Category:", 
                                 font=('Arial', 10, 'bold'), 
                                 fg='#3498db', bg='#ecf0f1')
        category_label.pack(pady=5)
        category_var = tk.StringVar(value=expense['category'])
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, 
                                     values=self.categories, width=37)
        category_combo.pack(pady=5)
        
        date_label = tk.Label(form_frame, text="📅 Date (Y/M/D):", 
                             font=('Arial', 10, 'bold'), 
                             fg='#27ae60', bg='#ecf0f1')
        date_label.pack(pady=5)
        
        date_edit_frame = tk.Frame(form_frame, bg='#ecf0f1')
        date_edit_frame.pack(pady=5)
        
        existing_date = datetime.strptime(expense['date'], "%Y-%m-%d")
        year_var = tk.StringVar(value=str(existing_date.year))
        year_combo = ttk.Combobox(date_edit_frame, textvariable=year_var, width=6, values=[str(y) for y in range(2000, 2031)])
        year_combo.pack(side=tk.LEFT, padx=2)
        
        month_var = tk.StringVar(value=f"{existing_date.month:02d}")
        month_combo = ttk.Combobox(date_edit_frame, textvariable=month_var, width=4, values=[f"{m:02d}" for m in range(1, 13)])
        month_combo.pack(side=tk.LEFT, padx=2)
        
        day_var = tk.StringVar(value=f"{existing_date.day:02d}")
        day_combo = ttk.Combobox(date_edit_frame, textvariable=day_var, width=4, values=[f"{d:02d}" for d in range(1, 32)])
        day_combo.pack(side=tk.LEFT, padx=2)
        
        def save_changes():
            try:
                old_desc = expense['description']
                expense['description'] = desc_entry.get().strip()
                expense['amount'] = float(amount_entry.get())
                expense['category'] = category_var.get()
                year = year_var.get()
                month = month_var.get()
                day = day_var.get()
                date = f"{year}-{month}-{day}"
                datetime.strptime(date, "%Y-%m-%d")
                expense['date'] = date
                
                self.save_data()
                self.add_log(f"Edited expense: {old_desc} to {expense['description']} (${expense['amount']:.2f}, {expense['category']}, {date})")
                self.update_display()
                edit_window.destroy()
                messagebox.showinfo("✅ Success", "Expense updated successfully!")
                
            except ValueError:
                messagebox.showerror("❌ Error", "Please enter valid values")
            except Exception as e:
                messagebox.showerror("❌ Error", f"An error occurred: {str(e)}")
        
        button_frame = tk.Frame(edit_window, bg='#34495e')
        button_frame.pack(pady=20)
        
        save_btn = tk.Button(button_frame, text="💾 Save Changes", command=save_changes,
                            font=('Arial', 11, 'bold'), bg='#27ae60', fg='white',
                            relief='raised', bd=3, padx=15, pady=8)
        save_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(button_frame, text="❌ Cancel", command=edit_window.destroy,
                              font=('Arial', 11, 'bold'), bg='#e74c3c', fg='white',
                              relief='raised', bd=3, padx=15, pady=8)
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this expense?"):
            item = self.tree.item(selected[0])
            values = item['values']
            
            for i, exp in enumerate(self.expenses):
                if (exp['id'] == values[0] and 
                    exp['date'] == values[1] and 
                    exp['description'] == values[2] and 
                    exp['category'] == values[3] and 
                    f"${exp['amount']:.2f}" == values[4]):
                    self.add_log(f"Deleted expense: {exp['description']} (${exp['amount']:.2f}, {exp['category']}, {exp['date']})")
                    del self.expenses[i]
                    break
            
            self.save_data()
            self.update_display()
            messagebox.showinfo("Success", "Expense deleted successfully!")
    
    def show_charts(self):
        if not self.expenses:
            messagebox.showinfo("Info", "No expenses to display in charts")
            return
        
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Expense Analysis Charts")
        chart_window.geometry("800x600")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Expense Analysis Dashboard', fontsize=16, fontweight='bold')
        
        category_totals = defaultdict(float)
        for expense in self.expenses:
            category_totals[expense['category']] += expense['amount']
        
        if category_totals:
            ax1.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=90)
            ax1.set_title('Expenses by Category')
        
        monthly_totals = defaultdict(float)
        for expense in self.expenses:
            month = expense['date'][:7]
            monthly_totals[month] += expense['amount']
        
        if monthly_totals:
            months = sorted(monthly_totals.keys())
            amounts = [monthly_totals[month] for month in months]
            ax2.plot(months, amounts, marker='o', linewidth=2, markersize=6)
            ax2.set_title('Monthly Expense Trend')
            ax2.set_xlabel('Month')
            ax2.set_ylabel('Amount ($)')
            ax2.tick_params(axis='x', rotation=45)
        
        if category_totals:
            categories = list(category_totals.keys())
            amounts = list(category_totals.values())
            ax3.bar(categories, amounts, color='skyblue', alpha=0.7)
            ax3.set_title('Expenses by Category')
            ax3.set_xlabel('Category')
            ax3.set_ylabel('Amount ($)')
            ax3.tick_params(axis='x', rotation=45)
        
        dates = [datetime.strptime(expense['date'], "%Y-%m-%d") for expense in self.expenses]
        amounts = [expense['amount'] for expense in self.expenses]
        ax4.scatter(dates, amounts, alpha=0.6, s=50)
        ax4.set_title('Daily Expenses')
        ax4.set_xlabel('Date')
        ax4.set_ylabel('Amount ($)')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def export_data(self):
        if not self.expenses:
            messagebox.showinfo("Info", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.csv'):
                    df = pd.DataFrame(self.expenses)
                    df.to_csv(filename, index=False)
                else:
                    with open(filename, 'w') as f:
                        json.dump(self.expenses, f, indent=2)
                
                self.add_log(f"Exported data to {filename}")
                messagebox.showinfo("Success", f"Data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")
    
    def import_data(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.csv'):
                    df = pd.read_csv(filename)
                    self.expenses = df.to_dict('records')
                else:
                    with open(filename, 'r') as f:
                        self.expenses = json.load(f)
                
                self.save_data()
                self.add_log(f"Imported data from {filename}")
                self.update_display()
                messagebox.showinfo("Success", f"Data imported from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import data: {str(e)}")
    
    def save_data(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.expenses, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.expenses = json.load(f)
                self.add_log("Loaded existing data from expenses.json")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.expenses = []

def main():
    root = tk.Tk()
    
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure('TLabelFrame', background='#ecf0f1', foreground='#2c3e50')
    style.configure('TLabelFrame.Label', background='#ecf0f1', foreground='#2c3e50', font=('Arial', 10, 'bold'))
    
    app = ExpenseTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()