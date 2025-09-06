# 💰 Expense Tracker - Personal Finance Manager

A comprehensive and user-friendly expense tracking application built with Python and tkinter. Track your daily expenses, analyze spending patterns, and manage your personal finances with ease.

## ✨ Features

### 📊 Core Functionality
- **Add Expenses**: Record expenses with description, amount, category, and date
- **Edit & Delete**: Modify or remove existing expense entries
- **Data Persistence**: Automatic saving to JSON file
- **Real-time Statistics**: View total expenses, monthly spending, and daily averages

### 📈 Analytics & Visualization
- **Interactive Charts**: Pie charts, line graphs, bar charts, and scatter plots
- **Category Analysis**: Breakdown of expenses by category
- **Monthly Trends**: Track spending patterns over time
- **Daily Expense Tracking**: Visualize daily spending habits

### 🔍 Advanced Features
- **Smart Filtering**: Filter by category and date range
- **Search Functionality**: Find specific expenses quickly
- **Data Export/Import**: Export to CSV or JSON, import existing data
- **Context Menus**: Right-click for quick actions
- **Responsive Design**: Modern, clean interface

### 🏷️ Predefined Categories
- Food
- Transportation
- Entertainment
- Shopping
- Bills
- Healthcare
- Education
- Other

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download** this repository to your local machine

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python expense_tracker.py
   ```

## 📱 How to Use

### Adding Expenses
1. Fill in the expense details in the "Add New Expense" panel
2. Enter description, amount, select category, and date
3. Click "Add Expense" to save

### Viewing Statistics
- **Total Expenses**: See your overall spending
- **Monthly View**: Track current month's expenses
- **Daily Average**: Understand your daily spending pattern

### Filtering Data
1. Use the "Filters" panel to narrow down your view
2. Filter by category or date range
3. Click "Apply Filter" to see filtered results
4. Use "Clear Filter" to reset

### Analyzing Data
1. Click "View Charts" to open the analytics dashboard
2. Explore different chart types:
   - **Pie Chart**: Category breakdown
   - **Line Chart**: Monthly trends
   - **Bar Chart**: Category comparison
   - **Scatter Plot**: Daily expenses

### Managing Data
- **Edit**: Select an expense and click "Edit Selected"
- **Delete**: Select an expense and click "Delete Selected"
- **Export**: Save your data as CSV or JSON
- **Import**: Load existing data from files

## 🎨 Interface Overview

The application features a clean, modern interface with:

- **Left Panel**: Add new expenses with form validation
- **Middle Panel**: Real-time statistics and chart access
- **Right Panel**: Advanced filtering options
- **Bottom Panel**: Comprehensive expense history table

## 💾 Data Storage

- Expenses are automatically saved to `expenses.json`
- Data persists between application sessions
- Export/import functionality for data backup and migration

## 🛠️ Technical Details

### Built With
- **Python 3.7+**: Core programming language
- **tkinter**: GUI framework (included with Python)
- **matplotlib**: Chart generation and visualization
- **pandas**: Data manipulation and CSV handling
- **json**: Data persistence

### File Structure
```
Expense Tracker/
├── expense_tracker.py    # Main application file
├── requirements.txt      # Python dependencies
├── README.md            # This documentation
└── expenses.json        # Data storage (created automatically)
```

## 🔧 Customization

### Adding New Categories
Edit the `categories` list in the `ExpenseTracker.__init__()` method:
```python
self.categories = ["Food", "Transportation", "Entertainment", "Shopping", "Bills", "Healthcare", "Education", "Other", "Your New Category"]
```

### Changing Data File Location
Modify the `data_file` variable in the `ExpenseTracker.__init__()` method:
```python
self.data_file = "your_custom_path/expenses.json"
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Error for matplotlib/pandas**:
   ```bash
   pip install --upgrade matplotlib pandas
   ```

2. **Permission Error on Data File**:
   - Ensure the application has write permissions in the directory
   - Try running as administrator if needed

3. **Date Format Issues**:
   - Use YYYY-MM-DD format for dates (e.g., 2024-01-15)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Review the code comments for implementation details
3. Create an issue in the project repository

---

**Happy Expense Tracking! 💰📊**
