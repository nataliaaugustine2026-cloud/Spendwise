def calculate_total(expenses):
    total = 0.0
    for expense in expenses:
        total = total + expense["amount"]
    return total

def category_totals(expenses):
    totals = {}
    for expense in expenses:
        category = expense["category"]
        if category in totals:
            totals[category] = totals[category] + expense["amount"]
        else:
            totals[category] = expense["amount"]
    return totals

def search_expenses(expenses, keyword):
    results = []
    for expense in expenses:
        if keyword.lower() in expense["description"].lower():
            results.append(expense)
    return results

def sort_expenses(expenses, sort_by="amount", reverse=False):
    if sort_by == "amount":
        return sorted(expenses, key=lambda expense: expense["amount"], reverse=reverse)
    elif sort_by == "date":
        return sorted(expenses, key=lambda expense: expense["date"], reverse=reverse)
    else:
        return []

def monthly_total(expenses, month):
    selected_expenses = []
    for expense in expenses:
        if expense["date"][:7] == month:
            selected_expenses.append(expense)
    return calculate_total(selected_expenses)

def remaining_budget(monthly_budget, expenses, month):
    spending = monthly_total(expenses, month)
    remaining = monthly_budget - spending
    return remaining

if __name__ == "__main__":
    expenses = [
        {"description": "Lunch", "amount": 150, "category": "Food", "date": "2026-10-05"},
        {"description": "Bus ticket", "amount": 40, "category": "Travel", "date": "2026-10-12"},
        {"description": "Notebook", "amount": 100, "category": "Education", "date": "2026-10-15"},
        {"description": "Dinner", "amount": 120, "category": "Food", "date": "2026-10-18"}
    ]
    print("Total:", calculate_total(expenses))
    print("Categories:", category_totals(expenses))
    print("Search:", search_expenses(expenses, "LUNCH"))
    print("Sorted:", sort_expenses(expenses, "amount"))

    empty_expenses = []
    print("Empty total:", calculate_total(empty_expenses))
    print("Empty categories:", category_totals(empty_expenses))
    print("Empty search:", search_expenses(empty_expenses, "lunch"))
    print("Empty sort:", sort_expenses(empty_expenses))
    print("No matches:", search_expenses(expenses, "pizza"))
    
    repeated_expenses = [
    {"description": "Lunch", "amount": 150, "category": "Food", "date": "2026-10-05"},
    {"description": "Dinner", "amount": 120, "category": "Food", "date": "2026-10-18"},
    {"description": "Bus", "amount": 40, "category": "Travel", "date": "2026-10-12"}
    ]
    print("Repeated categories:", category_totals(repeated_expenses))
    
    equal_expenses = [
    {"description": "Lunch", "amount": 100, "category": "Food", "date": "2026-10-05"},
    {"description": "Bus", "amount": 40, "category": "Travel", "date": "2026-10-12"},
    {"description": "Book", "amount": 100, "category": "Education", "date": "2026-10-15"}
    ]
    print("Equal amounts:", sort_expenses(equal_expenses, "amount"))
