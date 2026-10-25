from vehicle import EconomyCar, SUV, LuxuryCar
from customer import Customer
from payment import MpesaPayment, CardPayment, CashPayment
from rental_system import CarRentalSystem


def main():
    system = CarRentalSystem("SafariDrive Rentals")

    # ---------- Fleet ----------
    car1 = EconomyCar("KDK 123A", "Toyota", "Axio", 2022, 4000)
    car2 = SUV("KDJ 456B", "Toyota", "Prado", 2023, 8000)
    car3 = SUV("KDJ 672B", "Nissan", "X-Trail", 2021, 6500)
    car4 = LuxuryCar("KDL 789C", "Mercedes-Benz", "E-Class", 2024, 15000)
    car5 = EconomyCar("KDM 555Y", "Toyota", "Vitz", 2021, 3000)

    for car in [car1, car2, car3, car4, car5]:
        system.add_vehicle(car)

    # ---------- Customers ----------
    customer1 = Customer("C001", "John Kamau", "0712345678", "12345678", "DL45821")
    customer2 = Customer("C002", "Jane Wanjiru", "0789876543", "87654321", "DL12345")
    customer3 = Customer("C003", "Peter Otieno", "0723456789", "23456789", "DL67890")
    system.register_customer(customer3)
    system.register_customer(customer1)
    system.register_customer(customer2)
    

    # ---------- Rent the Prado for 4 days (brief Part 10) ----------
    print("\n--- Available vehicles ---")
    system.show_available_vehicles()

    rental1 = system.rent_vehicle(customer1, car2, 4)
    rental1.display_rental_details()

    # Try to rent it again while it is out (should be rejected)
    print("--- Trying to rent the Prado again ---")
    try:
        system.rent_vehicle(customer1, car2, 2)
    except ValueError as error:
        print(f"Error: {error}\n")

    # Return 2 days late, then pay by M-Pesa
    print("--- Returning Prado (6 days, 2 late) ---")
    system.return_vehicle(rental1, actual_days=6)
    rental1.display_rental_details()
    system.process_payment(MpesaPayment(rental1, "0712345678"))

    # ---------- Jane rents an Axio, cash payment ----------
    print("\n--- Jane rents an Axio for 3 days ---")
    rental2 = system.rent_vehicle(customer2, car1, 3)
    system.return_vehicle(rental2, actual_days=3)

    # Cash too low: payment fails, revenue does not change
    print("--- Jane pays with KSh 10,000 (too little) ---")
    system.process_payment(CashPayment(rental2, 10000))

    # Enough cash: payment succeeds
    print("--- Jane pays with KSh 12,000 ---")
    system.process_payment(CashPayment(rental2, 12000))

    # ---------- John rents the luxury car, returns with damage, pays by card ----------
    print("\n--- John rents the Mercedes E-Class for 2 days ---")
    rental3 = system.rent_vehicle(customer1, car4, 2)
    print("--- Returned with KSh 5,000 damage charge ---")
    system.return_vehicle(rental3, actual_days=2, damage_charge=5000)
    rental3.display_rental_details()
    system.process_payment(CardPayment(rental3, 4417))

    rental4 = system.rent_vehicle(customer3, car5, 2)
    system.return_vehicle(rental4, actual_days=2)
    system.process_payment(MpesaPayment(rental4, "0723456789"))

    # ---------- Errors the system must catch ----------
    print("\n--- Trying to pay Jane's rental again ---")
    try:
        system.process_payment(CashPayment(rental2, 12000))
    except ValueError as error:
        print(f"Error: {error}\n")

    # ---------- Management report ----------
    system.generate_report()

    print("--- Jane's rental history ---")
    customer2.view_rental_history()


if __name__ == "__main__":
    main()