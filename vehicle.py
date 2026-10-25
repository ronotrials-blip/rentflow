from abc import ABC, abstractmethod


class Vehicle(ABC):
    """Abstract base class for all vehicles in the fleet."""
    
    def __init__(self, registration_number, make, model, year, daily_rate):
        """Initialize a vehicle."""
        if daily_rate < 0:
            raise ValueError("Daily rate cannot be negative.")
        
        self.registration_number = registration_number
        self.make = make
        self.model = model
        self.year = year
        self.daily_rate = daily_rate
        self.__available = True  # Private attribute
    
    def is_available(self):
        """Return True if the vehicle is available for rent."""
        return self.__available
    
    def mark_as_rented(self):
        """Mark the vehicle as rented (unavailable)."""
        self.__available = False
    
    def mark_as_available(self):
        """Mark the vehicle as available for rent."""
        self.__available = True
    
    @abstractmethod
    def calculate_rental_cost(self, days):
        """Calculate total rental cost. Each vehicle type implements this."""
        pass
    
    def display_details(self):
        """Print the vehicle's details and current status."""
        print(f"\n{self.year} {self.make} {self.model}")
        print(f"  Registration: {self.registration_number}")
        print(f"  Daily Rate: KSh {self.daily_rate:,}")
        print(f"  Available: {'Yes' if self.is_available() else 'No'}")


class EconomyCar(Vehicle):
    """Economy car - standard pricing."""
    
    def __init__(self, registration_number, make, model, year, daily_rate):
        super().__init__(registration_number, make, model, year, daily_rate)
    
    def calculate_rental_cost(self, days):
        """Economy: daily_rate × days"""
        return self.daily_rate * days


class SUV(Vehicle):
    """SUV - daily rate plus KSh 2,000 service charge per rental."""
    
    def __init__(self, registration_number, make, model, year, daily_rate):
        super().__init__(registration_number, make, model, year, daily_rate)
        self.service_charge = 2000
    
    def calculate_rental_cost(self, days):
        """SUV: (daily_rate × days) + 2,000"""
        return (self.daily_rate * days) + self.service_charge


class LuxuryCar(Vehicle):
    """Luxury car - daily rate plus 10% insurance."""
    
    def __init__(self, registration_number, make, model, year, daily_rate):
        super().__init__(registration_number, make, model, year, daily_rate)
    
    def calculate_rental_cost(self, days):
        """Luxury: (daily_rate × days) + 10% insurance"""
        base_cost = self.daily_rate * days
        insurance = base_cost * 0.10
        return base_cost + insurance




    