from vehicle import EconomyCar, SUV, LuxuryCar

print("="*50)
print("TESTING VEHICLE CLASSES")
print("="*50)

# Test 1: Economy Car
print("\n Test 1: Economy Car (4,000/day × 3 days)")
economy = EconomyCar("KDK 123A", "Toyota", "Axio", 2022, 4000)
cost = economy.calculate_rental_cost(3)
print(f"  Expected: 12,000")
print(f"  Got: {cost}")
assert cost == 12000, "FAILED!"
print("   PASSED")

# Test 2: SUV
print("\n Test 2: SUV (8,000/day × 3 days + 2,000 service)")
suv = SUV("KDJ 456B", "Toyota", "Prado", 2023, 8000)
cost = suv.calculate_rental_cost(3)
print(f"  Expected: 26,000")
print(f"  Got: {cost}")
assert cost == 26000, "FAILED!"
print("   PASSED")

# Test 3: Luxury Car
print("\n Test 3: Luxury Car (15,000/day × 3 days + 10% insurance)")
luxury = LuxuryCar("KDL 789C", "Mercedes-Benz", "E-Class", 2024, 15000)
cost = luxury.calculate_rental_cost(3)
print(f"  Expected: 49,500")
print(f"  Got: {cost}")
assert cost == 49500, "FAILED!"
print("   PASSED")

# Test 4: Availability
print("\n Test 4: Availability Status")
print(f"  Economy available: {economy.is_available()}")
economy.mark_as_rented()
print(f"  After marking rented: {economy.is_available()}")
assert economy.is_available() == False, "FAILED!"
economy.mark_as_available()
print(f"  After marking available: {economy.is_available()}")
assert economy.is_available() == True, "FAILED!"
print("   PASSED")

# Test 5: Cannot create plain Vehicle (abstract)
print("\n Test 5: Cannot create plain Vehicle (abstract class)")
try:
    from vehicle import Vehicle
    plain = Vehicle("KDK 999Z", "Test", "Car", 2024, 5000)
    print("  FAILED - Should not allow plain Vehicle!")
except TypeError as e:
    print(f"  Correctly rejected: Can't instantiate abstract class")
    print("  PASSED")

print("\n" + "="*50)
print("ALL TESTS PASSED! ")
print("="*50)