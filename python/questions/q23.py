"""
Stripe-Style Multi-Part Problem: Connect Platform Fee Calculator

This problem simulates the core accounting engine for a marketplace platform
built on Stripe Connect. The goal is to process a log of charges to
accurately calculate platform fees and the net amount owed to sellers.

The input is a single log string with charges separated by '~'.

The charge format is:
`transaction_id;connected_account_id;amount;currency;charge_type`
- charge_type: Can be `DIRECT` or `DESTINATION`.

---

Part 1: Gross Transaction Volume
- Calculate the total gross volume for each seller, ignoring fees.

Part 2: Net Payouts with a Flat Fee
- Calculate the total net payout for each seller after a flat 2% platform
  fee is deducted from all transactions.

Part 3: Differentiated Fee Structure
- Update the logic for a new fee structure: 2% for `DESTINATION` charges
  and 0.5% for `DIRECT` charges.

Part 4: Currency-Specific Reporting
- Generate a comprehensive report for each seller that breaks down their
  `gross_volume` and `net_payout` per currency.
"""
from collections import defaultdict

# ===================================================================================
# User's Approach
#
# This solution shows great improvement by using a dedicated helper function
# (`get_events`) to parse the input string. This separates parsing from logic.
# Each part is solved by a separate function that re-iterates over the parsed
# data to perform its specific calculation.
# ===================================================================================
class FeeCalculator:
    def get_events(self, log: str) -> list:
        events = []
        log_tokens = log.split("~")

        for log_token in log_tokens:
            if not log_token:
                continue
            
            id, account_id, amount, currency, type = log_token.split(";")

            events.append({
                "id": id,
                "account_id": account_id,
                "amount": int(amount),
                "currency": currency,
                "type": type
            })
        return events
    
    def get_gross_volume(self, log:str) -> dict:
        events = self.get_events(log)
        balances = defaultdict(int)

        for event in events:
            account_id = event["account_id"]
            amount = event["amount"]

            balances[account_id] += amount
        return balances

    def get_flat_fee(self, log: str) -> dict:
        events = self.get_events(log)

        balances = defaultdict(int)

        for event in events:
            account_id = event["account_id"]
            amount = event["amount"]

            fee = amount * 2 / 100

            balances[account_id] += amount - fee
        return balances

    def get_differentiated_fee(self, log:str) -> dict:
        events = self.get_events(log)
        balances = defaultdict(int)

        for event in events:
            account_id = event["account_id"]
            amount = event["amount"]
            type = event["type"]
            fee = 0
            if type == "DIRECT":
                fee = amount * 0.5/100
            else:
                fee = amount * 2/100
            
            balances[account_id] += amount - fee
        return balances

    def get_currency_specific_report(self, log:str) -> dict:
        events = self.get_events(log)
        ans = defaultdict(lambda: defaultdict(lambda: {'gross_volume': 0, 'net_payout': 0}))
        for event in events:
            account_id = event["account_id"]
            amount = event["amount"]
            type = event["type"]
            currency = event["currency"]
            
            fee = 0
            if type == "DIRECT":
                fee = int(amount * 5) // 1000 # 0.5%
            else:
                fee = int(amount * 2) // 100 # 2%
            
            net_amount = amount - fee
            
            ans[account_id][currency]['gross_volume'] += amount
            ans[account_id][currency]['net_payout'] += net_amount
        return ans

# ===================================================================================
# Optimized, Modular Solution
#
# This refactored solution centralizes all logic into a single private method,
# `_process_all_charges`. It processes the parsed log ONCE, calculating all
# required values for all parts and storing them in a single report object.
# The public methods are simple wrappers that just return a piece of the final
# report. This approach is more efficient, easier to maintain, and less prone
# ===================================================================================
class ConnectFeeCalculator:
    def _parse_log(self, log: str) -> list:
        """Parses the raw string into a clean list of charge objects."""
        charges = []
        for charge_str in log.strip().split('~'):
            if not charge_str:
                continue
            try:
                tx_id, acct_id, amount, currency, charge_type = charge_str.split(';')
                charges.append({
                    "id": tx_id,
                    "account_id": acct_id,
                    "amount": int(amount),
                    "currency": currency,
                    "type": charge_type
                })
            except (ValueError, IndexError):
                continue
        return charges

    def _process_all_charges(self, log: str) -> dict:
        """The core processing engine. Loops once to calculate all required values."""
        # Memoization: If we've processed this exact log before, return the cached result.
        if hasattr(self, '_cached_report') and self._cached_log == log:
            return self._cached_report

        charges = self._parse_log(log)
        
        # This single report object will hold the answers to all parts.
        report = {
            "gross_volume": defaultdict(int),
            "net_payout_flat": defaultdict(int),
            "net_payout_differentiated": defaultdict(int),
            "currency_report": defaultdict(lambda: defaultdict(lambda: {"gross_volume": 0, "net_payout": 0}))
        }

        for charge in charges:
            account_id = charge["account_id"]
            amount = charge["amount"]
            currency = charge["currency"]
            charge_type = charge["type"]

            # --- Calculations for ALL parts happen in this single loop ---
            
            # Part 1: Gross Volume
            report["gross_volume"][account_id] += amount
            
            # Part 2: Flat Fee (2%)
            flat_fee = (amount * 2) // 100
            report["net_payout_flat"][account_id] += amount - flat_fee
            
            # Part 3: Differentiated Fee (0.5% or 2%)
            differentiated_fee = (amount * 5) // 1000 if charge_type == "DIRECT" else (amount * 2) // 100
            report["net_payout_differentiated"][account_id] += amount - differentiated_fee
            
            # Part 4: Currency Report
            currency_report_for_acct = report["currency_report"][account_id][currency]
            currency_report_for_acct["gross_volume"] += amount
            currency_report_for_acct["net_payout"] += amount - differentiated_fee

        # Cache the result and return
        self._cached_log = log
        self._cached_report = report
        return report

    def calculate_gross_volume(self, log: str) -> dict:
        """Solves Part 1."""
        final_report = self._process_all_charges(log)
        return dict(final_report["gross_volume"])

    def calculate_net_payouts_flat(self, log: str) -> dict:
        """Solves Part 2."""
        final_report = self._process_all_charges(log)
        return dict(final_report["net_payout_flat"])

    def calculate_net_payouts_differentiated(self, log: str) -> dict:
        """Solves Part 3."""
        final_report = self._process_all_charges(log)
        return dict(final_report["net_payout_differentiated"])

    def generate_currency_report(self, log: str) -> dict:
        """Solves Part 4."""
        final_report = self._process_all_charges(log)
        # Convert nested defaultdicts to regular dicts for cleaner output
        return {acct: dict(currencies) for acct, currencies in final_report["currency_report"].items()}

if __name__ == "__main__":
    log_data = (
        "tx_1;acct_1;10000;USD;DESTINATION~"
        "tx_2;acct_1;5000;USD;DIRECT~"
        "tx_3;acct_2;8000;USD;DIRECT~"
        "tx_4;acct_1;20000;CAD;DESTINATION"
    )

    # Testing the Optimized Solution
    calculator = ConnectFeeCalculator()
    print("--- Testing Optimized Solution ---")

    print("\n## Part 1: Gross Transaction Volume ##")
    print(calculator.calculate_gross_volume(log_data))

    print("\n## Part 2: Net Payouts with a Flat Fee (2%) ##")
    print(calculator.calculate_net_payouts_flat(log_data))

    print("\n## Part 3: Net Payouts with Differentiated Fees ##")
    print(calculator.calculate_net_payouts_differentiated(log_data))

    print("\n## Part 4: Currency-Specific Reporting ##")
    print(calculator.generate_currency_report(log_data))