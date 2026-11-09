import csv
import os

# Define file paths
PORTFOLIO_FILE = 'portfolio_summary.csv'

# Sample mock ticker database (fallback if live prices/sample CSV aren't queried)
# Prices can be looked up or simulated from this dictionary
MARKET_PRICES = {
    'AAPL': 185.50,
    'MSFT': 420.25,
    'GOOGL': 175.80,
    'AMZN': 180.10,
    'TSLA': 172.50,
    'NVDA': 880.00,
    'JPM': 198.40,
    'V': 275.60
}

def get_current_price(ticker):
    """
    Looks up the current market price for a given ticker symbol.
    Defaults to a mock lookup or prompts the user if not found.
    """
    ticker = ticker.upper()
    if ticker in MARKET_PRICES:
        return MARKET_PRICES[ticker]
    else:
        # Prompt user if ticker is custom/unknown
        while True:
            try:
                price = float(input(f"Enter current market price for '{ticker}': $"))
                return price
            except ValueError:
                print("Invalid input. Please enter a valid numerical price.")

def main():
    print("=" * 60)
    print("       STOCK PORTFOLIO PERFORMANCE TRACKER")
    print("=" * 60)
    
    portfolio_positions = {}

    # Input loop for user holdings
    while True:
        ticker = input("\nEnter stock ticker symbol (e.g., AAPL, MSFT) or type 'done' to finish: ").strip().upper()
        if ticker == 'DONE':
            break
        if not ticker:
            print("Ticker cannot be empty. Try again.")
            continue

        try:
            shares = float(input(f"Enter number of shares for {ticker}: "))
            buy_price = float(input(f"Enter average buy price per share for {ticker} ($): "))
        except ValueError:
            print("Invalid numerical input for shares or price. Please try adding this stock again.")
            continue

        portfolio_positions[ticker] = {
            'shares': shares,
            'buy_price': buy_price
        }

    if not portfolio_positions:
        print("\nNo portfolio positions entered. Exiting program.")
        return

    # Calculations and Console Output
    print("\n" + "=" * 80)
    print(f"{'Ticker':<10} | {'Shares':<10} | {'Buy Price':<12} | {'Current':<10} | {'Invested ($)':<12} | {'Current ($)':<12} | {'Gain/Loss (%)':<12}")
    print("-" * 80)

    total_invested_capital = 0.0
    total_current_market_value = 0.0
    summary_rows = []

    for ticker, data in portfolio_positions.items():
        shares = data['shares']
        buy_price = data['buy_price']
        current_price = get_current_price(ticker)

        invested_val = shares * buy_price
        current_val = shares * current_price
        
        gain_loss_dollar = current_val - invested_val
        gain_loss_pct = (gain_loss_dollar / invested_val) * 100 if invested_val > 0 else 0.0

        total_invested_capital += invested_val
        total_current_market_value += current_val

        # Formatting output row
        print(f"{ticker:<10} | {shares:<10.2f} | ${buy_price := buy_price:<11.2f} | ${current_price:<9.2f} | ${invested_val:<11.2f} | ${current_val:<11.2f} | {gain_loss_pct:>+.2f}%")

        summary_rows.append({
            'Ticker': ticker,
            'Shares': shares,
            'BuyPrice': buy_price,
            'CurrentPrice': current_price,
            'TotalInvested': round(invested_val, 2),
            'CurrentValue': round(current_val, 2),
            'GainLossPct': round(gain_loss_pct, 2)
        })

    total_gain_loss = total_current_market_value - total_invested_capital
    total_gain_loss_pct = (total_gain_loss / total_invested_capital) * 100 if total_invested_capital > 0 else 0.0

    print("-" * 80)
    print(f"Total Invested Capital:     ${total_invested_capital:,.2f}")
    print(f"Total Current Market Value: ${total_current_market_value:,.2f}")
    print(f"Total Portfolio Gain/Loss:  ${total_gain_loss:+,.2f} ({total_gain_loss_pct:+.2f}%)")
    print("=" * 80)

    file_exists = os.path.isfile(PORTFOLIO_FILE)
    
    with open(PORTFOLIO_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Ticker', 'Shares', 'BuyPrice', 'CurrentPrice', 'TotalInvested', 'CurrentValue', 'GainLossPct']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)

    print(f"\n[Success] Transaction summary successfully saved to '{PORTFOLIO_FILE}'.")

if __name__ == '__main__':
    main()