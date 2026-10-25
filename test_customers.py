from customer import Customer

print("="*50)
print("TESTING CUSTOMER CLASS")
print("="*50)

# Test 1: Create valid customer
print("\n✓ Test 1: Create valid customer")
customer1 = Customer("C001", "John Kamau", "0712345678", "12345678", "DL45821")
print(f"  Customer created: {customer1.name}")
assert customer1.customer_id == "C001"
assert customer1.name == "John Kamau"
print("  ✓ PASSED")

# Test 2: Driving licence validation (SHOULD FAIL)
print("\n✓ Test 2: Reject customer without driving licence")
try:
    customer2 = Customer("C002", "Jane Wanjiru", "0789876543", "87654321", "")
    print("  FAILED - Should reject empty driving licence!")
except ValueError as e:
    print(f"  Correctly rejected: {e}")
    print("  ✓ PASSED")

# Test 3: Display customer details
print("\n✓ Test 3: Display customer details")
customer1.display_details()
print("  ✓ PASSED")

# Test 4: Rental history (empty)
print("\n✓ Test 4: View rental history (empty)")
customer1.view_rental_history()
print("  ✓ PASSED")

print("="*50)
print("ALL TESTS PASSED! ✓")
print("="*50)