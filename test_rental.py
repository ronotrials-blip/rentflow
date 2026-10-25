from vehicle import EconomyCar, SUV, LuxuryCar
from customer import Customer
from rental import Rental

print("=" * 50)
print("TESTING RENTAL CLASS")
print("=" * 50)

# Test 1: Worked example from the brief (late fee = 3,200)
print("\nTest 1: Late fee for Prado (8,000/day, 4 days, returned after 6)")
customer = Customer("C001", "John Kamau", "0712345678", "12345678", "DL45821")
prado = SUV("KDJ 456B", "Toyota", "Prado", 2023, 8000)
rental = Rental("R001", customer, prado, 4)
assert rental.base_cost == 34000, "Base cost should be 34,000"
rental.complete_rental(actual_days=6)
assert rental.late_fee == 3200, f"Late fee should be 3,200, got {rental.late_fee}"
assert rental.calculate_total() == 37200, "Final bill should be 37,200"
print(f"  Late fee: {rental.late_fee}  Final bill: {rental.calculate_total()}")
print("  PASSED")

# Test 2: Vehicle is available again after completion
print("\nTest 2: Vehicle is freed after return")
assert prado.is_available() == True
print("  PASSED")

# Test 3: Vehicle cannot be rented twice
print("\nTest 3: Vehicle cannot be rented while rented")
car = EconomyCar("KDK 123A", "Toyota", "Axio", 2022, 4000)
Rental("R002", customer, car, 3)
try:
    Rental("R003", customer, car, 2)
    print("  FAILED - should have raised ValueError")
except ValueError as e:
    print(f"  Correctly rejected: {e}")
    print("  PASSED")

# Test 4: Zero rental days rejected
print("\nTest 4: Zero rental days rejected")
try:
    Rental("R004", customer, EconomyCar("KDL 000X", "Test", "Car", 2024, 3000), 0)
    print("  FAILED")
except ValueError as e:
    print(f"  Correctly rejected: {e}")
    print("  PASSED")

# Test 5: On-time return has no late fee
print("\nTest 5: On-time return has no late fee")
c2 = Customer("C002", "Jane Wanjiru", "0789876543", "87654321", "DL12345")
v = EconomyCar("KDM 555Y", "Toyota", "Vitz", 2021, 3000)
r = Rental("R005", c2, v, 3)
r.complete_rental(actual_days=3)
assert r.late_fee == 0
print("  PASSED")

print("\n" + "=" * 50)
print("ALL TESTS PASSED!")
print("=" * 50)

