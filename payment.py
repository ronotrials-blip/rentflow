from abc import ABC, abstractmethod
import random
import string


class Payment(ABC):
    """Abstract base class for every payment. Pays one rental's final bill."""

    def __init__(self, rental):
        """
        Args:
            rental: The Rental object being paid for
        """
        if rental.status != "COMPLETED":
            raise ValueError("A rental must be completed before it can be paid.")
        self.rental = rental
        self.amount = rental.calculate_total()

    @abstractmethod
    def process_payment(self):
        """Process the payment. Return True if successful, False otherwise."""
        pass


class MpesaPayment(Payment):
    """Payment by M-Pesa. Generates a transaction code."""

    def __init__(self, rental, phone_number):
        super().__init__(rental)
        self.phone_number = phone_number

    def process_payment(self):
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        print("Processing M-Pesa payment...")
        print(f"Transaction: {code}")
        print(f"Payment of KSh {self.amount:,.0f} successful.")
        return True


class CardPayment(Payment):
    """Payment by card. Stores only the last four digits."""

    def __init__(self, rental, last_four_digits):
        super().__init__(rental)
        if len(str(last_four_digits)) != 4:
            raise ValueError("Card must be identified by exactly 4 digits.")
        self.last_four_digits = str(last_four_digits)

    def process_payment(self):
        print(f"Card ending {self.last_four_digits} charged KSh {self.amount:,.0f}")
        print("Payment successful.")
        return True


class CashPayment(Payment):
    """Payment in cash. Fails if the cash handed over is less than the bill."""

    def __init__(self, rental, cash_received):
        super().__init__(rental)
        if cash_received < 0:
            raise ValueError("Cash received cannot be negative.")
        self.cash_received = cash_received

    def process_payment(self):
        if self.cash_received < self.amount:
            print(f"Cash payment failed: KSh {self.cash_received:,.0f} is less than the bill of KSh {self.amount:,.0f}.")
            return False
        change = self.cash_received - self.amount
        print(f"Cash received: KSh {self.cash_received:,.0f}")
        print(f"Change due:    KSh {change:,.0f}")
        print(f"Cash payment of KSh {self.amount:,.0f} recorded.")
        return True