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
        
        # Load existing data
        self.load_data()
        
        # Create GUI
        self.create_widgets()
        self.update_display()
        
    def create_widgets(self):
        # Main frame with gradient-like background
        main_frame = tk.Frame(self.root, bg='#34495e', relief='raised', bd=2)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title with colorful styling
        title_frame = tk.Frame(main_frame, bg='#34495e')
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        
        title_label = tk.Label(title_frame, text="💰 Expense Tracker", 
                              font=('Arial', 28, 'bold'), 
                              foreground='#ecf0f1', 
                              bg='#34495e',
                              relief='raised',
                              bd=3)
        title_label.pack(pady=10)
        
        # Subtitle
        subtitle_label = tk.Label(title_frame, text="Personal Finance Manager", 
                                 font=('Arial', 12, 'italic'), 
                                 foreground='#bdc3c7', 
                                 bg='#34495e')
        subtitle_label.pack()
        
        # Left panel - Add Expense with colorful styling
        left_frame = tk.LabelFrame(main_frame, text="📝 Add New Expense", 
                                  font=('Arial', 12, 'bold'),
                                  fg='#2c3e50', bg='#ecf0f1', 
                                  relief='raised', bd=3)
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Expense form with colorful labels
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
        
        date_label = tk.Label(left_frame, text="📅 Date:", 
                             font=('Arial', 10, 'bold'), 
                             fg='#27ae60', bg='#ecf0f1')
        date_label.grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.date_entry = tk.Entry(left_frame, textvariable=self.date_var, width=25, font=('Arial', 10),
                                  bg='#ffffff', fg='#2c3e50', relief='sunken', bd=2)
        self.date_entry.grid(row=3, column=1, pady=5, padx=(10, 5))
        
        # Buttons with colorful styling
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
        
        # Middle panel - Statistics with colorful styling
        middle_frame = tk.LabelFrame(main_frame, text="📊 Statistics Dashboard", 
                                    font=('Arial', 12, 'bold'),
                                    fg='#2c3e50', bg='#ecf0f1', 
                                    relief='raised', bd=3)
        middle_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Statistics labels with colorful backgrounds
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
        
        # Chart button with colorful styling
        chart_btn = tk.Button(middle_frame, text="📊 View Charts", command=self.show_charts,
                             font=('Arial', 11, 'bold'), bg='#9b59b6', fg='white',
                             relief='raised', bd=3, padx=15, pady=8)
        chart_btn.grid(row=3, column=0, pady=15, padx=5, sticky=(tk.W, tk.E))
        
        # Right panel - Filters with colorful styling
        right_frame = tk.LabelFrame(main_frame, text="🔍 Filters & Search", 
                                   font=('Arial', 12, 'bold'),
                                   fg='#2c3e50', bg='#ecf0f1', 
                                   relief='raised', bd=3)
        right_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Filter options with colorful labels
        cat_label = tk.Label(right_frame, text="🏷️ Category:", 
                            font=('Arial', 10, 'bold'), 
                            fg='#3498db', bg='#ecf0f1')
        cat_label.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.filter_category_var = tk.StringVar()
        self.filter_category_combo = ttk.Combobox(right_frame, textvariable=self.filter_category_var,
                                                 values=["All"] + self.categories, width=15)
        self.filter_category_combo.grid(row=0, column=1, pady=5, padx=(10, 5))
        self.filter_category_combo.set("All")
        
        from_label = tk.Label(right_frame, text="📅 Date From:", 
                             font=('Arial', 10, 'bold'), 
                             fg='#27ae60', bg='#ecf0f1')
        from_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.date_from_var = tk.StringVar()
        self.date_from_entry = tk.Entry(right_frame, textvariable=self.date_from_var, width=15,
                                       bg='#ffffff', fg='#2c3e50', relief='sunken', bd=2)
        self.date_from_entry.grid(row=1, column=1, pady=5, padx=(10, 5))
        
        to_label = tk.Label(right_frame, text="📅 Date To:", 
                           font=('Arial', 10, 'bold'), 
                           fg='#e67e22', bg='#ecf0f1')
        to_label.grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.date_to_var = tk.StringVar()
        self.date_to_entry = tk.Entry(right_frame, textvariable=self.date_to_var, width=15,
                                     bg='#ffffff', fg='#2c3e50', relief='sunken', bd=2)
        self.date_to_entry.grid(row=2, column=1, pady=5, padx=(10, 5))
        
        # Filter buttons with colorful styling
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
        
        # Bottom panel - Expense List with colorful styling
        list_frame = tk.LabelFrame(main_frame, text="📋 Expense History", 
                                  font=('Arial', 12, 'bold'),
                                  fg='#2c3e50', bg='#ecf0f1', 
                                  relief='raised', bd=3)
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for expenses with colorful styling
        columns = ('Date', 'Description', 'Category', 'Amount')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure treeview colors
        style = ttk.Style()
        style.configure("Treeview", background="#ffffff", foreground="#2c3e50", fieldbackground="#ffffff")
        style.configure("Treeview.Heading", background="#3498db", foreground="white", font=('Arial', 10, 'bold'))
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor='center')
        
        # Scrollbar with colorful styling
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S), pady=5)
        
        # Context menu for treeview
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        # Action buttons with colorful styling
        action_frame = tk.Frame(list_frame, bg='#ecf0f1')
        action_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        edit_btn = tk.Button(action_frame, text="✏️ Edit Selected", command=self.edit_expense,
                            font=('Arial', 9, 'bold'), bg='#f39c12', fg='white',
                            relief='raised', bd=2, padx=8, pady=4)
        edit_btn.pack(side=tk.LEFT, padx=3)
        
        delete_btn = tk.Button(action_frame, text="🗑️ Delete Selected", command=self.delete_expense,
                              font=('Arial', 9, 'bold'), bg='#e74c3c', fg='white',
                              relief='raised', bd=2, padx=8, pady=4)
        delete_btn.pack(side=tk.LEFT, padx=3)
        
        export_btn = tk.Button(action_frame, text="📤 Export Data", command=self.export_data,
                              font=('Arial', 9, 'bold'), bg='#27ae60', fg='white',
                              relief='raised', bd=2, padx=8, pady=4)
        export_btn.pack(side=tk.LEFT, padx=3)
        
        import_btn = tk.Button(action_frame, text="📥 Import Data", command=self.import_data,
                              font=('Arial', 9, 'bold'), bg='#8e44ad', fg='white',
                              relief='raised', bd=2, padx=8, pady=4)
        import_btn.pack(side=tk.LEFT, padx=3)
        
    def add_expense(self):
        try:
            description = self.desc_entry.get().strip()
            amount = float(self.amount_entry.get())
            category = self.category_var.get()
            date_str = self.date_var.get()
            
            if not description:
                messagebox.showerror("Error", "Please enter a description")
                return
            
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return
            
            # Validate date
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Please enter date in YYYY-MM-DD format")
                return
            
            expense = {
                'id': len(self.expenses) + 1,
                'description': description,
                'amount': amount,
                'category': category,
                'date': date_str
            }
            
            self.expenses.append(expense)
            self.save_data()
            self.update_display()
            self.clear_form()
            messagebox.showinfo("Success", "Expense added successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def clear_form(self):
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_combo.set("Food")
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
    
    def update_display(self):
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add expenses to treeview
        for expense in self.expenses:
            self.tree.insert('', 'end', values=(
                expense['date'],
                expense['description'],
                expense['category'],
                f"${expense['amount']:.2f}"
            ))
        
        # Update statistics
        self.update_statistics()
    
    def update_statistics(self):
        if not self.expenses:
            self.total_label.config(text="💸 Total Expenses: $0.00")
            self.monthly_label.config(text="📅 This Month: $0.00")
            self.avg_label.config(text="📈 Daily Average: $0.00")
            return
        
        total = sum(expense['amount'] for expense in self.expenses)
        self.total_label.config(text=f"💸 Total Expenses: ${total:.2f}")
        
        # Monthly expenses
        current_month = datetime.now().strftime("%Y-%m")
        monthly_expenses = [expense for expense in self.expenses 
                           if expense['date'].startswith(current_month)]
        monthly_total = sum(expense['amount'] for expense in monthly_expenses)
        self.monthly_label.config(text=f"📅 This Month: ${monthly_total:.2f}")
        
        # Daily average
        if self.expenses:
            dates = [datetime.strptime(expense['date'], "%Y-%m-%d") for expense in self.expenses]
            date_range = (max(dates) - min(dates)).days + 1
            daily_avg = total / date_range if date_range > 0 else total
            self.avg_label.config(text=f"📈 Daily Average: ${daily_avg:.2f}")
    
    def apply_filter(self):
        filtered_expenses = self.expenses.copy()
        
        # Category filter
        category_filter = self.filter_category_var.get()
        if category_filter != "All":
            filtered_expenses = [exp for exp in filtered_expenses if exp['category'] == category_filter]
        
        # Date range filter
        date_from = self.date_from_var.get()
        date_to = self.date_to_var.get()
        
        if date_from:
            try:
                from_date = datetime.strptime(date_from, "%Y-%m-%d")
                filtered_expenses = [exp for exp in filtered_expenses 
                                   if datetime.strptime(exp['date'], "%Y-%m-%d") >= from_date]
            except ValueError:
                messagebox.showerror("Error", "Invalid 'Date From' format. Use YYYY-MM-DD")
                return
        
        if date_to:
            try:
                to_date = datetime.strptime(date_to, "%Y-%m-%d")
                filtered_expenses = [exp for exp in filtered_expenses 
                                   if datetime.strptime(exp['date'], "%Y-%m-%d") <= to_date]
            except ValueError:
                messagebox.showerror("Error", "Invalid 'Date To' format. Use YYYY-MM-DD")
                return
        
        # Update display with filtered data
        self.display_filtered_expenses(filtered_expenses)
    
    def display_filtered_expenses(self, expenses):
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add filtered expenses
        for expense in expenses:
            self.tree.insert('', 'end', values=(
                expense['date'],
                expense['description'],
                expense['category'],
                f"${expense['amount']:.2f}"
            ))
    
    def clear_filter(self):
        self.filter_category_var.set("All")
        self.date_from_var.set("")
        self.date_to_var.set("")
        self.update_display()
    
    def show_context_menu(self, event):
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="Edit", command=self.edit_expense)
            context_menu.add_command(label="Delete", command=self.delete_expense)
            context_menu.tk_popup(event.x_root, event.y_root)
    
    def edit_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to edit")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        
        # Find the expense in our data
        expense = None
        for exp in self.expenses:
            if (exp['date'] == values[0] and 
                exp['description'] == values[1] and 
                exp['category'] == values[2] and 
                f"${exp['amount']:.2f}" == values[3]):
                expense = exp
                break
        
        if expense:
            self.edit_expense_dialog(expense)
    
    def edit_expense_dialog(self, expense):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("✏️ Edit Expense")
        edit_window.geometry("450x350")
        edit_window.configure(bg='#34495e')
        
        # Center the window
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Title
        title_label = tk.Label(edit_window, text="✏️ Edit Expense", 
                              font=('Arial', 16, 'bold'), 
                              fg='#ecf0f1', bg='#34495e')
        title_label.pack(pady=10)
        
        # Form frame
        form_frame = tk.Frame(edit_window, bg='#ecf0f1', relief='raised', bd=2)
        form_frame.pack(pady=10, padx=20, fill='x')
        
        # Form fields with colorful styling
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
        
        date_label = tk.Label(form_frame, text="📅 Date:", 
                             font=('Arial', 10, 'bold'), 
                             fg='#27ae60', bg='#ecf0f1')
        date_label.pack(pady=5)
        date_entry = tk.Entry(form_frame, width=40, font=('Arial', 10), 
                             bg='#ffffff', fg='#2c3e50', relief='sunken', bd=2)
        date_entry.pack(pady=5)
        date_entry.insert(0, expense['date'])
        
        def save_changes():
            try:
                expense['description'] = desc_entry.get().strip()
                expense['amount'] = float(amount_entry.get())
                expense['category'] = category_var.get()
                expense['date'] = date_entry.get()
                
                self.save_data()
                self.update_display()
                edit_window.destroy()
                messagebox.showinfo("✅ Success", "Expense updated successfully!")
                
            except ValueError:
                messagebox.showerror("❌ Error", "Please enter valid values")
            except Exception as e:
                messagebox.showerror("❌ Error", f"An error occurred: {str(e)}")
        
        # Button frame
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
            
            # Find and remove the expense
            for i, exp in enumerate(self.expenses):
                if (exp['date'] == values[0] and 
                    exp['description'] == values[1] and 
                    exp['category'] == values[2] and 
                    f"${exp['amount']:.2f}" == values[3]):
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
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Expense Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Category breakdown (pie chart)
        category_totals = defaultdict(float)
        for expense in self.expenses:
            category_totals[expense['category']] += expense['amount']
        
        if category_totals:
            ax1.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=90)
            ax1.set_title('Expenses by Category')
        
        # 2. Monthly trend (line chart)
        monthly_totals = defaultdict(float)
        for expense in self.expenses:
            month = expense['date'][:7]  # YYYY-MM
            monthly_totals[month] += expense['amount']
        
        if monthly_totals:
            months = sorted(monthly_totals.keys())
            amounts = [monthly_totals[month] for month in months]
            ax2.plot(months, amounts, marker='o', linewidth=2, markersize=6)
            ax2.set_title('Monthly Expense Trend')
            ax2.set_xlabel('Month')
            ax2.set_ylabel('Amount ($)')
            ax2.tick_params(axis='x', rotation=45)
        
        # 3. Top categories (bar chart)
        if category_totals:
            categories = list(category_totals.keys())
            amounts = list(category_totals.values())
            ax3.bar(categories, amounts, color='skyblue', alpha=0.7)
            ax3.set_title('Expenses by Category')
            ax3.set_xlabel('Category')
            ax3.set_ylabel('Amount ($)')
            ax3.tick_params(axis='x', rotation=45)
        
        # 4. Daily expenses (scatter plot)
        dates = [datetime.strptime(expense['date'], "%Y-%m-%d") for expense in self.expenses]
        amounts = [expense['amount'] for expense in self.expenses]
        ax4.scatter(dates, amounts, alpha=0.6, s=50)
        ax4.set_title('Daily Expenses')
        ax4.set_xlabel('Date')
        ax4.set_ylabel('Amount ($)')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Embed in tkinter window
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
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.expenses = []

def main():
    root = tk.Tk()
    
    # Configure style for better appearance
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure custom styles for better integration with our colorful theme
    style.configure('TLabelFrame', background='#ecf0f1', foreground='#2c3e50')
    style.configure('TLabelFrame.Label', background='#ecf0f1', foreground='#2c3e50', font=('Arial', 10, 'bold'))
    
    app = ExpenseTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
