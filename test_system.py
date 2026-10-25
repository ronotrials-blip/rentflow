from vehicle import EconomyCar, SUV, LuxuryCar
from customer import Customer
from payment import MpesaPayment, CashPayment
from rental_system import CarRentalSystem


def new_setup():
    system = CarRentalSystem("SafariDrive Rentals")
    axio = EconomyCar("KDK 123A", "Toyota", "Axio", 2022, 4000)
    prado = SUV("KDJ 456B", "Toyota", "Prado", 2023, 8000)
    xtrail = SUV("KDJ 672B", "Nissan", "X-Trail", 2021, 6500)
    eclass = LuxuryCar("KDL 789C", "Mercedes-Benz", "E-Class", 2024, 15000)
    for car in [axio, prado, xtrail, eclass]:
        system.add_vehicle(car)
    john = Customer("C001", "John Kamau", "0712345678", "12345678", "DL45821")
    system.register_customer(john)
    return system, john, axio, prado, xtrail, eclass


def expect_error(label, func, *args):
    try:
        func(*args)
    except ValueError as e:
        print(f"  Correctly rejected ({label}): {e}")
        return True
    print(f"  FAILED ({label}): no error raised")
    return False


print("=" * 50)
print("TESTING CARRENTALSYSTEM")
print("=" * 50)

# Test 1
print("\nTest 1: Renting makes the vehicle unavailable")
system, john, axio, prado, xtrail, eclass = new_setup()
rental = system.rent_vehicle(john, prado, 4)
assert rental.rental_id == "R001"
assert not prado.is_available()
print("  PASSED")

# Test 2
print("\nTest 2: Unregistered customer cannot rent")
system, john, axio, prado, xtrail, eclass = new_setup()
from customer import Customer as C
stranger = C("C002", "Jane Wanjiru", "0789876543", "87654321", "DL12345")
assert expect_error("unregistered", system.rent_vehicle, stranger, axio, 2)
print("  PASSED")

# Test 3
print("\nTest 3: Vehicle outside the fleet cannot be rented")
system, john, axio, prado, xtrail, eclass = new_setup()
outsider = EconomyCar("KDM 555Y", "Toyota", "Vitz", 2021, 3000)
assert expect_error("not in fleet", system.rent_vehicle, john, outsider, 2)
print("  PASSED")

# Test 4
print("\nTest 4: Rented vehicle cannot be rented again")
system, john, axio, prado, xtrail, eclass = new_setup()
system.rent_vehicle(john, prado, 4)
assert expect_error("already rented", system.rent_vehicle, john, prado, 2)
print("  PASSED")

# Test 5
print("\nTest 5: Full cycle (rent, return late, pay) adds 37,200 to revenue")
system, john, axio, prado, xtrail, eclass = new_setup()
rental = system.rent_vehicle(john, prado, 4)
system.return_vehicle(rental, actual_days=6)
assert prado.is_available()
assert rental.status == "COMPLETED"
assert system.process_payment(MpesaPayment(rental, "0712345678")) == True
assert system.revenue == 37200
assert rental.is_paid()
print("  PASSED")

# Test 6
print("\nTest 6: Rental cannot be paid twice")
system, john, axio, prado, xtrail, eclass = new_setup()
rental = system.rent_vehicle(john, prado, 4)
system.return_vehicle(rental, actual_days=4)
system.process_payment(MpesaPayment(rental, "0712345678"))
second = MpesaPayment(rental, "0712345678")
assert expect_error("paid twice", system.process_payment, second)
assert system.revenue == 34000
print("  PASSED")

# Test 7
print("\nTest 7: Failed cash payment does not change revenue")
system, john, axio, prado, xtrail, eclass = new_setup()
rental = system.rent_vehicle(john, axio, 3)
system.return_vehicle(rental, actual_days=3)
assert system.process_payment(CashPayment(rental, 5000)) == False
assert system.revenue == 0
assert not rental.is_paid()
print("  PASSED")

# Test 8
print("\nTest 8: Payment before return is rejected")
system, john, axio, prado, xtrail, eclass = new_setup()
rental = system.rent_vehicle(john, axio, 3)
assert expect_error("pay before return", MpesaPayment, rental, "0712345678")
print("  PASSED")

# Test 9
print("\nTest 9: Completed rental cannot be returned again")
system, john, axio, prado, xtrail, eclass = new_setup()
rental = system.rent_vehicle(john, axio, 2)
system.return_vehicle(rental, actual_days=2)
assert expect_error("return twice", system.return_vehicle, rental, 2)
print("  PASSED")

# Test 10
print("\nTest 10: Revenue cannot be set from outside")
system, john, axio, prado, xtrail, eclass = new_setup()
try:
    system.revenue = 10_000_000
    print("  FAILED")
except AttributeError:
    print("  Correctly rejected: revenue is read-only")
    print("  PASSED")

# Test 11
print("\nTest 11: Writing system.__revenue from outside does not change real revenue")
system, john, axio, prado, xtrail, eclass = new_setup()
system.__revenue = 10_000_000
assert system.revenue == 0
print("  PASSED (real revenue unchanged)")

# Test 12
print("\nTest 12: Search filters by type and budget")
system, john, axio, prado, xtrail, eclass = new_setup()
suvs = system.search_vehicles(vehicle_type="SUV")
assert len(suvs) == 2
cheap_suvs = system.search_vehicles(vehicle_type="SUV", max_daily_rate=7000)
assert len(cheap_suvs) == 1 and cheap_suvs[0] is xtrail
print("  PASSED")

# Test 13: report (check visually)
print("\nTest 13: Management report (check the numbers by eye)")
system, john, axio, prado, xtrail, eclass = new_setup()
system.rent_vehicle(john, prado, 4)
system.generate_report()
print("  Expected: Total 4, Available 3, Rented 1, Customers 1, Active 1, Economy 1, SUVs 2, Luxury 1")

print("\n" + "=" * 50)
print("ALL TESTS PASSED!")
print("=" * 50)