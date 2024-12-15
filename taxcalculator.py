import tkinter as tk
from tkinter import messagebox

def calculate_tax_and_take_home(income, filing_status, income_type, deductions, employee_salaries):
    """
    Calculate total tax and take-home pay.
    Filing statuses: 'single', 'married'
    Income types: 'w2', 'self_employed'
    """
    # 2024 Federal tax brackets (simplified)
    tax_brackets = {
        'single': [
            (10275, 0.10),  # 10%
            (41775, 0.12),  # 12%
            (89075, 0.22),  # 22%
            (170050, 0.24), # 24%
            (215950, 0.32), # 32%
            (539900, 0.35), # 35%
            (float('inf'), 0.37) # 37%
        ],
        'married': [
            (20550, 0.10),
            (83550, 0.12),
            (178150, 0.22),
            (340100, 0.24),
            (431900, 0.32),
            (647850, 0.35),
            (float('inf'), 0.37)
        ]
    }

    # Standard deductions for 2024
    standard_deduction = {
        'single': 13850,
        'married': 27700
    }

    # Self-employed tax rate (FICA)
    self_employment_tax_rate = 0.153

    # Adjust income for deductions and employee salaries
    adjusted_income = max(0, income - deductions - employee_salaries)

    # Apply standard deduction
    taxable_income = max(0, adjusted_income - standard_deduction[filing_status])

    # Calculate federal income tax
    tax = 0
    previous_limit = 0

    for limit, rate in tax_brackets[filing_status]:
        if taxable_income > limit:
            tax += (limit - previous_limit) * rate
            previous_limit = limit
        else:
            tax += (taxable_income - previous_limit) * rate
            break

    # Self-employment tax
    self_employment_tax = 0
    if income_type == 'self_employed':
        self_employment_tax = adjusted_income * self_employment_tax_rate

    total_tax = tax + self_employment_tax

    # Take-home pay
    take_home_pay = adjusted_income - total_tax
    return total_tax, take_home_pay

def calculate():
    try:
        income = float(income_entry.get())
        deductions = float(deductions_entry.get())
        employee_salaries = float(employee_salaries_entry.get())

        filing_status = filing_status_var.get()
        income_type = income_type_var.get()

        total_tax, take_home_pay = calculate_tax_and_take_home(
            income, filing_status, income_type, deductions, employee_salaries
        )

        result_text.set(f"Total Tax: ${total_tax:,.2f}\nTake-Home Pay: ${take_home_pay:,.2f}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for income, deductions, and employee salaries.")

# Create GUI application
app = tk.Tk()
app.title("2024 US Tax Calculator")

# Input fields
tk.Label(app, text="Total Income (USD):").grid(row=0, column=0, sticky="w")
income_entry = tk.Entry(app)
income_entry.grid(row=0, column=1)

filing_status_var = tk.StringVar(value="single")
tk.Label(app, text="Filing Status:").grid(row=1, column=0, sticky="w")
tk.Radiobutton(app, text="Single", variable=filing_status_var, value="single").grid(row=1, column=1, sticky="w")
tk.Radiobutton(app, text="Married", variable=filing_status_var, value="married").grid(row=1, column=2, sticky="w")

income_type_var = tk.StringVar(value="w2")
tk.Label(app, text="Income Type:").grid(row=2, column=0, sticky="w")
tk.Radiobutton(app, text="W-2 Employee", variable=income_type_var, value="w2").grid(row=2, column=1, sticky="w")
tk.Radiobutton(app, text="Self-Employed", variable=income_type_var, value="self_employed").grid(row=2, column=2, sticky="w")

tk.Label(app, text="Deductions (USD):").grid(row=3, column=0, sticky="w")
deductions_entry = tk.Entry(app)
deductions_entry.grid(row=3, column=1)

tk.Label(app, text="Employee Salaries (USD):").grid(row=4, column=0, sticky="w")
employee_salaries_entry = tk.Entry(app)
employee_salaries_entry.grid(row=4, column=1)

# Result display
result_text = tk.StringVar()
result_label = tk.Label(app, textvariable=result_text, justify="left")
result_label.grid(row=6, column=0, columnspan=3, sticky="w")

# Calculate button
tk.Button(app, text="Calculate", command=calculate).grid(row=5, column=0, columnspan=3)

# Run the application
app.mainloop()
