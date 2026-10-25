from vehicle import SUV, LuxuryCar

class Rental:
    """Links one customer to one vehicle and tracks the bill."""

    LATE_PENALTY_RATE = 0.20  # 20% of the daily rate per late day

    def __init__(self, rental_id, customer, vehicle, rental_days):
        
        """
        Create a rental.

        Args:
            rental_id: Identifier such as "R001"
            customer: A Customer object
            vehicle: A Vehicle object (EconomyCar, SUV or LuxuryCar)
            rental_days: Days the customer agreed to rent for
        """
        if rental_days <= 0:
            raise ValueError("Rental days must be greater than zero.")
        if not vehicle.is_available():
            raise ValueError(
                f"Vehicle {vehicle.registration_number} is already rented."
            )

        self.rental_id = rental_id
        self.customer = customer
        self.vehicle = vehicle
        self.rental_days = rental_days
        self.actual_days = None
        self.status = "ACTIVE"
        self.base_cost = vehicle.calculate_rental_cost(rental_days)  # polymorphism
        self.late_fee = 0
        self.damage_charge = 0
        self.__paid = False

        vehicle.mark_as_rented()
        customer.add_rental(self)
        

    def calculate_late_fee(self):
        """Return the late fee for extra days (0 if returned on time or early)."""
        if self.actual_days is None:
            return 0
        late_days = max(0, self.actual_days - self.rental_days)
        daily_penalty = self.vehicle.daily_rate * self.LATE_PENALTY_RATE
        return daily_penalty * late_days

    def calculate_total(self):
        """Return base_cost + late_fee + damage_charge."""
        return self.base_cost + self.late_fee + self.damage_charge

    def complete_rental(self, actual_days, damage_charge=0):
        """Record the return, calculate late fee and free the vehicle."""
        if self.status != "ACTIVE":
            raise ValueError("This rental has already been completed.")
        if actual_days <= 0:
            raise ValueError("Actual days must be greater than zero.")

        self.actual_days = actual_days
        self.damage_charge = damage_charge
        self.late_fee = self.calculate_late_fee()
        self.status = "COMPLETED"
        self.vehicle.mark_as_available()

    def mark_as_paid(self):
        """Record that this rental has been paid."""
        self.__paid = True

    def is_paid(self):
        """Return True if this rental has been paid."""
        return self.__paid

    def display_rental_details(self):
        """Print a receipt matching the brief's example layout."""
        rental_charge = self.vehicle.daily_rate * self.rental_days

        print(f"\n{'=' * 36}")
        print(f"{'SAFARIDRIVE RENTALS':^36}")
        print(f"{'=' * 36}")
        print(f"Rental ID:        {self.rental_id}")
        print(f"Customer:         {self.customer.name}")
        print(f"Vehicle:          {self.vehicle.make} {self.vehicle.model}")
        print(f"Registration:     {self.vehicle.registration_number}")
        print(f"Rental Period:    {self.rental_days} days")
        print(f"Daily Rate:       KSh {self.vehicle.daily_rate:,}")
        print()
        print(f"Rental Charge:    KSh {rental_charge:,.0f}")

        # Extra charge depends on the vehicle type
        if isinstance(self.vehicle, SUV):
            print(f"Service Charge:   KSh {self.vehicle.service_charge:,}")
        elif isinstance(self.vehicle, LuxuryCar):
            insurance = rental_charge * 0.10
            print(f"Insurance (10%):  KSh {insurance:,.0f}")

        if self.late_fee:
            print(f"Late Fee:         KSh {self.late_fee:,.0f}")
        if self.damage_charge:
            print(f"Damage Charge:    KSh {self.damage_charge:,.0f}")

        print("-" * 36)
        print(f"TOTAL:            KSh {self.calculate_total():,.0f}")
        print(f"Status:           {self.status}")
        print(f"{'=' * 36}\n")