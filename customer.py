class Customer:
    """Manages customer information and rental history."""
    
    def __init__(self, customer_id, name, phone_number, national_id, driving_licence):
        """Initialize a customer."""
        # Rule 2: Customer must have a valid driving licence
        if not driving_licence or driving_licence.strip() == "":
            raise ValueError("Customer must have a valid driving licence.")
        
        self.customer_id = customer_id
        self.name = name
        self.phone_number = phone_number
        self.national_id = national_id
        self.driving_licence = driving_licence
        self.rentals = []  # List to store Rental objects (empty for now)
    
    def add_rental(self, rental):
        """Add a rental to this customer's history."""
        self.rentals.append(rental)
    
    def view_rental_history(self):
        """Print all rentals this customer has made."""
        if not self.rentals:
            print(f"\nNo rental history for {self.name}.")
            return
        
        print(f"\n{'='*50}")
        print(f"RENTAL HISTORY - {self.name} ({self.customer_id})")
        print(f"{'='*50}")
        for rental in self.rentals:
            print(f"  {rental.rental_id}: {rental.vehicle.make} {rental.vehicle.model} - Status: {rental.status}")
        print(f"{'='*50}\n")
    
    def display_details(self):
        """Print the customer's details."""
        print(f"\n{'='*50}")
        print(f"CUSTOMER DETAILS")
        print(f"{'='*50}")
        print(f"  ID: {self.customer_id}")
        print(f"  Name: {self.name}")
        print(f"  Phone: {self.phone_number}")
        print(f"  National ID: {self.national_id}")
        print(f"  Driving Licence: {self.driving_licence}")
        print(f"  Total Rentals: {len(self.rentals)}")
        print(f"{'='*50}\n")