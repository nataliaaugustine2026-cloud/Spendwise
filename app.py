from flask import Flask, render_template, request, redirect, url_for, flash, Response
from datetime import date
import storage
import calculations
import csv

app = Flask(__name__)
app.secret_key = 'spendwise-secret-key'

# Define standard categories available in the app
CATEGORIES = ["Food", "Travel", "Education", "Shopping", "Hostel", "Entertainment", "Other"]

@app.route('/')
def index():
    # Load all saved expenses
    expenses = storage.load_expenses() if hasattr(storage, 'load_expenses') else []
    
    # Calculate totals, budget, and remaining balance using your modules
    monthly_budget = 8000.0  # Default monthly budget
    total_spent = calculations.calculate_total(expenses) if hasattr(calculations, 'calculate_total') else sum(e.get('amount', 0) for e in expenses)
    remaining_budget = monthly_budget - total_spent
    
    cat_totals = calculations.calculate_category_totals(expenses) if hasattr(calculations, 'calculate_category_totals') else {}
    
    # Get current month name nicely formatted (e.g., "October 2026")
    current_month_name = date.today().strftime('%B %Y')

    return render_template(
        'index.html',
        expenses=expenses,
        displayed_expenses=expenses,
        total_spent=total_spent,
        month_spent=total_spent,
        monthly_budget=monthly_budget,
        remaining_budget=remaining_budget,
        remaining=remaining_budget,
        category_totals=cat_totals,
        categories=CATEGORIES,
        month_name=current_month_name,
        today=str(date.today()),
        search_query="",
        show_no_results=False
    )

@app.route('/add', methods=['POST'])
def add_expense():
    try:
        description = request.form.get('description')
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        exp_date = request.form.get('date', str(date.today()))
        
        # Save expense logic
        if hasattr(storage, 'add_expense'):
            storage.add_expense(description, amount, category, exp_date)
        flash('Expense added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding expense: {str(e)}', 'danger')
        
    return redirect(url_for('index'))

@app.route('/delete/<string:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    if hasattr(storage, 'delete_expense'):
        storage.delete_expense(expense_id)
    flash('Expense deleted.', 'info')
    return redirect(url_for('index'))

@app.route('/export_csv')
def export_csv():
    expenses = storage.load_expenses() if hasattr(storage, 'load_expenses') else []
    
    def generate():
        yield 'ID,Title,Amount,Category,Date\n'
        for exp in expenses:
            yield f"{exp.get('id','')},{exp.get('title','exp.get(\'description\', \'\'))},{exp.get('amount','')},{exp.get('category','')},{exp.get('date','')}\n"
            
    return Response(
        generate(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=expenses.csv'}
    )

if __name__ == '__main__':
    app.run(debug=True)
