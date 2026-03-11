import gradio as gr
from accounts import Account
 
account = Account(1000)
 
demo = gr.Interface(
    fn=lambda action, amount, symbol, quantity: execute_action(action, amount, symbol, quantity),
    inputs=[
        gr.Radio(
            choices=[
                "Deposit",
                "Withdraw",
                "Buy Shares",
                "Sell Shares",
                "Get Portfolio",
                "Get Balance",
                "Get Profit/Loss",
                "Get Transactions"
            ],
            label="Action"
        ),
        gr.Number(label="Amount", precision=2),
        gr.Textbox(label="Symbol"),
        gr.Number(label="Quantity", precision=0)
    ],
    outputs=[
        gr.Textbox(label="Result")
    ],
    title="Trading Simulation Platform",
    description="A simple trading simulation platform"
)
 
def execute_action(action, amount, symbol, quantity):
    if action == "Deposit":
        account.deposit(amount)
        return f"Deposited ${amount}"
    elif action == "Withdraw":
        if amount > account.get_balance():
            return "Insufficient funds"
        account.withdraw(amount)
        return f"Withdrew ${amount}"
    elif action == "Buy Shares":
        if symbol not in ['AAPL', 'TSLA', 'GOOGL']:
            return "Invalid symbol"
        if quantity <= 0:
            return "Invalid quantity"
        account.buy_shares(symbol, int(quantity))
        return f"Bought {quantity} shares of {symbol}"
    elif action == "Sell Shares":
        if symbol not in ['AAPL', 'TSLA', 'GOOGL']:
            return "Invalid symbol"
        if quantity <= 0:
            return "Invalid quantity"
        account.sell_shares(symbol, int(quantity))
        return f"Sold {quantity} shares of {symbol}"
    elif action == "Get Portfolio":
        return str(account.get_portfolio())
    elif action == "Get Balance":
        return f"Balance: ${account.get_balance()}"
    elif action == "Get Profit/Loss":
        return f"Profit/Loss: ${account.get_profit_loss()}"
    elif action == "Get Transactions":
        return "\n".join(account.get_transactions())
 
demo.launch()