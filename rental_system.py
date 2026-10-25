from vehicle import EconomyCar, SUV, LuxuryCar
from rental import Rental

VEHICLE_TYPES = {"EconomyCar": EconomyCar, "SUV": SUV, "LuxuryCar": LuxuryCar}


class CarRentalSystem:
    """Runs the business: holds the fleet, customers, rentals and payments, and tracks revenue."""

    def __init__(self, name):
        self.name = name
        self.vehicles = []
        self.customers = []
        self.rentals = []
        self.payments = []
        self.__revenue = 0            # private: changes only through process_payment()
        self.__rental_counter = 0

    # ---------- Fleet and customers ----------

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        print(f"Vehicle {vehicle.registration_number} added to the fleet.")

    def register_customer(self, customer):
        if self.find_customer(customer.customer_id) is not None:
            raise ValueError(f"Customer {customer.customer_id} is already registered.")
        self.customers.append(customer)
        print(f"Customer {customer.name} ({customer.customer_id}) registered.")

    def find_vehicle(self, registration_number):
        for vehicle in self.vehicles:
            if vehicle.registration_number == registration_number:
                return vehicle
        return None

    def find_customer(self, customer_id):
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        return None

    def show_available_vehicles(self):
        available = [v for v in self.vehicles if v.is_available()]
        self._print_vehicle_list(available, "AVAILABLE VEHICLES")

    def search_vehicles(self, vehicle_type=None, max_daily_rate=None):
        """Return available vehicles, optionally filtered by type ("EconomyCar", "SUV", "LuxuryCar") and maximum daily rate."""
        results = [v for v in self.vehicles if v.is_available()]

        if vehicle_type is not None:
            if vehicle_type not in VEHICLE_TYPES:
                raise ValueError(f"Unknown vehicle type: {vehicle_type}")
            category = VEHICLE_TYPES[vehicle_type]
            results = [v for v in results if isinstance(v, category)]

        if max_daily_rate is not None:
            results = [v for v in results if v.daily_rate <= max_daily_rate]

        self._print_vehicle_list(results, f"SEARCH RESULTS ({vehicle_type or 'all types'})")
        return results

    def _print_vehicle_list(self, vehicles, title):
        print(f"\n{'=' * 50}\n{title}\n{'=' * 50}")
        if not vehicles:
            print("No vehicles found.")
        for i, vehicle in enumerate(vehicles, 1):
            print(f"{i}. {vehicle.make} {vehicle.model} ({vehicle.year})")
            print(f"   Registration: {vehicle.registration_number}")
            print(f"   Rate: KSh {vehicle.daily_rate:,}/day")
        print("=" * 50)

    # ---------- Rentals ----------

    def rent_vehicle(self, customer, vehicle, days):
        """Create a rental after checking that the customer and vehicle are valid."""
        if customer not in self.customers:
            raise ValueError("Customer must be registered before renting.")        # Rule 3
        if vehicle not in self.vehicles:
            raise ValueError("Vehicle must be in the fleet before it can be rented.")  # Rule 4

        rental_id = f"R{self.__rental_counter + 1:03d}"
        rental = Rental(rental_id, customer, vehicle, days)   # Rules 5 and 6 are checked here
        self.__rental_counter += 1                            # count only rentals that succeeded
        self.rentals.append(rental)
        print(f"Rental {rental_id} created: {customer.name} rents {vehicle.make} {vehicle.model} for {days} days.")
        return rental

    def return_vehicle(self, rental, actual_days, damage_charge=0):
        if rental not in self.rentals:
            raise ValueError("This rental is not in the system.")
        if rental.status != "ACTIVE":                                              # Rules 7 and 8
            raise ValueError("Only an active rental can be returned.")
        rental.complete_rental(actual_days, damage_charge)
        print(f"Rental {rental.rental_id} completed. Final bill: KSh {rental.calculate_total():,.0f}")

    def show_active_rentals(self):
        self._print_rental_list([r for r in self.rentals if r.status == "ACTIVE"], "ACTIVE RENTALS")

    def show_completed_rentals(self):
        self._print_rental_list([r for r in self.rentals if r.status == "COMPLETED"], "COMPLETED RENTALS")

    def _print_rental_list(self, rentals, title):
        print(f"\n{'=' * 50}\n{title}\n{'=' * 50}")
        if not rentals:
            print("None.")
        for r in rentals:
            paid = "PAID" if r.is_paid() else "UNPAID"
            print(f"{r.rental_id}: {r.customer.name} - {r.vehicle.make} {r.vehicle.model} - {paid}")
        print("=" * 50)

    # ---------- Payments and revenue ----------

    def process_payment(self, payment):
        """Run a payment and add to revenue only if it succeeds."""
        rental = payment.rental
        if rental not in self.rentals:
            raise ValueError("This rental is not in the system.")
        if rental.status != "COMPLETED":                                          # Rule 10
            raise ValueError("A rental must be completed before it can be paid.")
        if rental.is_paid():                                                      # Rule 10
            raise ValueError("This rental has already been paid.")
        if payment.amount < 0:                                                    # Rule 9
            raise ValueError("Payment amounts cannot be negative.")

        if not payment.process_payment():
            print("Payment failed. Revenue not updated.")
            return False

        rental.mark_as_paid()
        self.payments.append(payment)
        self.__revenue += payment.amount
        return True

    @property
    def revenue(self):
        """Total revenue. Read-only: it can only change through process_payment()."""
        return self.__revenue

    # ---------- Report ----------

    def generate_report(self):
        total = len(self.vehicles)
        available = sum(1 for v in self.vehicles if v.is_available())
        active = sum(1 for r in self.rentals if r.status == "ACTIVE")
        completed = sum(1 for r in self.rentals if r.status == "COMPLETED")
        economy = sum(1 for v in self.vehicles if isinstance(v, EconomyCar))
        suvs = sum(1 for v in self.vehicles if isinstance(v, SUV))
        luxury = sum(1 for v in self.vehicles if isinstance(v, LuxuryCar))

        print(f"\n{'=' * 40}")
        print(f"{'SAFARIDRIVE MANAGEMENT REPORT':^40}")
        print(f"{'=' * 40}")
        print(f"Total Vehicles:          {total}")
        print(f"Available Vehicles:      {available}")
        print(f"Rented Vehicles:         {total - available}")
        print(f"Registered Customers:    {len(self.customers)}")
        print(f"Total Rentals:           {len(self.rentals)}")
        print(f"Active Rentals:          {active}")
        print(f"Completed Rentals:       {completed}")
        print(f"Total Revenue:           KSh {self.__revenue:,.0f}")
        print("-" * 40)
        print("VEHICLES BY CATEGORY")
        print(f"Economy Cars:            {economy}")
        print(f"SUVs:                    {suvs}")
        print(f"Luxury Cars:             {luxury}")
        print(f"{'=' * 40}\n")
        