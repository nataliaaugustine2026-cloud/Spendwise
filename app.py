import math
from flask import Flask, render_template, request, redirect, url_for, flash
from storage import load_expenses, save_expenses
from validation import validate_expense_data
import calculations

app = Flask(__name__)
app.secret_key = "spendwise_final_production_secure_key"

@app.route('/')
def index():
    expenses = load_expenses()
    
    # 1. Handle Search Filters via calculations layer
    search_query = request.args.get('search', '').strip()
    if search_query:
        displayed_expenses = calculations.search_expenses(expenses, search_query)
    else:
        displayed_expenses = expenses

    # 2. Compute Dashboard Analytics via Natalia's calculations engine
    total_spent = calculations.calculate_total(expenses)
    cat_totals = calculations.category_totals(expenses)
    
    # Updated default placeholder config metrics from 50000.0 to ₹8,000 for test compatibility
    monthly_budget = 8000.0  
    remaining_budget = monthly_budget - total_spent
    
    show_no_results = len(displayed_expenses) == 0 and bool(search_query)

    return render_template(
        'index.html', 
        expenses=displayed_expenses, 
        total_spent=total_spent,
        month_spent=total_spent,
        monthly_budget=monthly_budget,
        remaining_budget=remaining_budget,
        category_totals=cat_totals,
        search_query=search_query,
        show_no_results=show_no_results
    )

@app.route('/add', methods=['POST'])
def add_expense():
    description = request.form.get('description', '').strip()
    amount_str = request.form.get('amount', '').strip()
    category = request.form.get('category', '').strip()
    date = request.form.get('date', '').strip()
    
    is_valid, error_msg, cleaned_amount = validate_expense_data(
        description, amount_str, category, date
    )
    
    if not is_valid:
        flash(error_msg, "error")
        return redirect(url_for('index'))
        
    expenses = load_expenses()
    new_id = max([e.get('id', 0) for e in expenses]) + 1 if expenses else 1
    
    new_expense = {
        "id": new_id,
        "description": description,
        "amount": cleaned_amount,
        "category": category,
        "date": date
    }
    
    expenses.append(new_expense)
    save_expenses(expenses)
    
    flash("Expense added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/delete/<int:expense_id>', methods=['POST', 'GET'])
def delete_expense(expense_id):
    expenses = load_expenses()
    updated_expenses = [e for e in expenses if e.get('id') != expense_id]
    save_expenses(updated_expenses)
    flash("Expense removed successfully.", "success")
    return redirect(url_for('index'))

@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    expenses = load_expenses()
    expense_to_edit = next((e for e in expenses if e.get('id') == expense_id), None)
    
    if not expense_to_edit:
        flash("Expense not found.", "error")
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        description = request.form.get('description', '').strip()
        amount_str = request.form.get('amount', '').strip()
        category = request.form.get('category', '').strip()
        date = request.form.get('date', '').strip()
        
        is_valid, error_msg, cleaned_amount = validate_expense_data(
            description, amount_str, category, date
        )
        
        if not is_valid:
            flash(error_msg, "error")
            return redirect(url_for('index'))
            
        expense_to_edit['description'] = description
        expense_to_edit['amount'] = cleaned_amount
        expense_to_edit['category'] = category
        expense_to_edit['date'] = date
        
        save_expenses(expenses)
        flash("Expense updated successfully!", "success")
        return redirect(url_for('index'))
        
    return render_template('edit.html', expense=expense_to_edit)

if __name__ == '__main__':
    app.run(debug=True)
