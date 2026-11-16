
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Temporary account storage
accounts = []


# Search account
def search_account(account_number):
    for account in accounts:
        if account["account_number"] == account_number:
            return account
    return None


# Add transaction history
def add_transaction(account, transaction_type, amount):
    transaction = {
        "type": transaction_type,
        "amount": amount,
        "balance": account["balance"],
        "date": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    }

    account["transactions"].append(transaction)


# Main route
@app.route("/", methods=["GET", "POST"])
def home():

    message = ""
    result = None
    active_panel = request.args.get("panel", "")

    if request.method == "POST":

        choice = request.form.get("action", "")
        active_panel = choice

        account_number = request.form.get(
            "account_number", ""
        ).strip()

        # 1. CREATE ACCOUNT
        if choice == "create":

            customer_name = request.form.get(
                "customer_name", ""
            ).strip()

            initial_balance = request.form.get(
                "initial_balance", ""
            ).strip()

            if not customer_name or not account_number or not initial_balance:
                message = "Please fill all the required fields!"

            elif search_account(account_number):
                message = "Account number already exists!"

            else:
                try:
                    balance = float(initial_balance)

                    if balance < 0:
                        message = "Initial deposit cannot be negative!"

                    else:
                        account = {
                            "customer_name": customer_name,
                            "account_number": account_number,
                            "balance": balance,
                            "transactions": []
                        }

                        accounts.append(account)

                        add_transaction(
                            account,
                            "Account Created",
                            balance
                        )

                        message = "Account created successfully!"
                        result = account

                except ValueError:
                    message = "Please enter a valid initial deposit!"

        # OTHER OPERATIONS
        else:

            if not account_number:
                message = "Please enter account number!"

            else:
                account = search_account(account_number)

                if account is None:
                    message = "Account not found!"

                # 2. DEPOSIT
                elif choice == "deposit":

                    try:
                        amount = float(request.form.get("amount", ""))

                        if amount <= 0:
                            message = "Deposit amount must be greater than zero!"

                        else:
                            account["balance"] += amount

                            add_transaction(
                                account,
                                "Deposit",
                                amount
                            )

                            message = "Money deposited successfully!"
                            result = account

                    except ValueError:
                        message = "Please enter a valid deposit amount!"

                # 3. WITHDRAW
                elif choice == "withdraw":

                    try:
                        amount = float(request.form.get("amount", ""))

                        if amount <= 0:
                            message = "Withdrawal amount must be greater than zero!"

                        elif amount > account["balance"]:
                            message = "Insufficient balance!"

                        else:
                            account["balance"] -= amount

                            add_transaction(
                                account,
                                "Withdrawal",
                                amount
                            )

                            message = "Money withdrawn successfully!"
                            result = account

                    except ValueError:
                        message = "Please enter a valid withdrawal amount!"

                # 4. CHECK BALANCE
                elif choice == "check":

                    message = "Balance retrieved successfully!"
                    result = account

                # 5. ACCOUNT DETAILS
                elif choice == "details":

                    message = "Account details retrieved successfully!"
                    result = account

                else:
                    message = "Invalid operation!"

    return render_template(
        "index.html",
        active_panel=active_panel,
        message=message,
        result=result
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
