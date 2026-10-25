from vehicle import EconomyCar, SUV
from customer import Customer
from rental import Rental
from payment import Payment, MpesaPayment, CardPayment, CashPayment

print("=" * 50)
print("TESTING PAYMENT CLASSES")
print("=" * 50)

customer = Customer("C001", "John Kamau", "0712345678", "12345678", "DL45821")
prado = SUV("KDJ 456B", "Toyota", "Prado", 2023, 8000)

# Test 1: Payment is abstract
print("\nTest 1: Cannot create a plain Payment")
rental = Rental("R001", customer, prado, 4)
rental.complete_rental(actual_days=6)
try:
    Payment(rental)
    print("  FAILED")
except TypeError:
    print("  Correctly rejected (abstract class)")
    print("  PASSED")

# Test 2: M-Pesa
print("\nTest 2: M-Pesa payment")
mpesa = MpesaPayment(rental, "0712345678")
assert mpesa.amount == 37200
assert mpesa.process_payment() == True
print("  PASSED")

# Test 3: Card stores only last 4 digits
print("\nTest 3: Card payment")
car = EconomyCar("KDK 123A", "Toyota", "Axio", 2022, 4000)
r2 = Rental("R002", customer, car, 3)
r2.complete_rental(actual_days=3)
card = CardPayment(r2, 4417)
assert card.last_four_digits == "4417"
assert card.process_payment() == True
print("  PASSED")

# Test 4: Cash with enough money
print("\nTest 4: Cash payment with enough money")
cash = CashPayment(rental, 40000)
assert cash.process_payment() == True
print("  PASSED")

# Test 5: Cash with too little money fails
print("\nTest 5: Cash payment with too little money")
short = CashPayment(rental, 1000)
assert short.process_payment() == False
print("  PASSED")

# Test 6: Cannot pay for a rental that is not completed
print("\nTest 6: Cannot pay before completion")
r3 = Rental("R003", customer, EconomyCar("KDL 000X", "Test", "Car", 2024, 3000), 2)
try:
    MpesaPayment(r3, "0712345678")
    print("  FAILED")
except ValueError as e:
    print(f"  Correctly rejected: {e}")
    print("  PASSED")

print("\n" + "=" * 50)
print("ALL TESTS PASSED!")
print("=" * 50)