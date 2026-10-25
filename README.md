# RentFlow – Car Rental Management System

A Python command-line program for **SafariDrive Rentals**, a fictional car rental company in Kenya. RentFlow is a Python OOP capstone project that tracks vehicles, customers, rentals, payments and revenue.

## Project Overview

SafariDrive Rentals currently tracks its vehicles, customers, bookings, payments and returns by hand, in notebooks and spreadsheets. As the fleet grows, staff find it hard to answer simple questions: which cars are available, who has which car, how long a car has been out, whether a car came back late, and how much money the business has made.

RentFlow answers these questions using Object-Oriented Programming. It models vehicles, customers, rentals and payments as classes, and a central `CarRentalSystem` class enforces the business rules and tracks revenue.

## How to Run

1. Open a Terminal and move into the project folder:
```bash
   cd rentflow
```
2. Run the program with Python 3:
```bash
   python3 main.py
```

No external libraries are needed. The program uses only the Python standard library (`abc`, `random` and `string`).

## Files

| File | Contents |
|------|----------|
| `main.py` | Sample data and a demo of the full rental workflow |
| `vehicle.py` | `Vehicle` (abstract), `EconomyCar`, `SUV`, `LuxuryCar` |
| `customer.py` | `Customer` |
| `rental.py` | `Rental` |
| `payment.py` | `Payment` (abstract), `MpesaPayment`, `CardPayment`, `CashPayment` |
| `rental_system.py` | `CarRentalSystem` (the manager that enforces the rules) |
| `test_*.py` | Test scripts used during development |

## Features

- Register customers and add vehicles to the fleet
- Search for available vehicles by type and maximum daily rate
- Rent a vehicle for a number of days, with business rules enforced
- Return a vehicle, with late fees and damage charges
- Pay by M-Pesa, card or cash, with change calculated for cash payments
- View active and completed rentals and a customer's rental history
- Generate a management report with totals calculated from the data

## OOP Concepts

**Abstraction.** `Vehicle` and `Payment` are abstract base classes, so a plain `Vehicle` or `Payment` cannot be created. `Vehicle` declares `calculate_rental_cost()` as an abstract method, and `Payment` declares `process_payment()`. Each child class must provide its own version, so the parent defines what every vehicle or payment must do without saying how.

**Encapsulation.** Data that must be protected is stored in private attributes. A vehicle's availability is stored in `__available`, a rental's payment status in `__paid`, and the business's revenue in `__revenue`. Each can only change through methods such as `mark_as_rented()`, `mark_as_paid()` and `process_payment()`. Revenue is exposed as a read-only property, so `system.revenue = 10_000_000` raises an error.

**Inheritance.** `EconomyCar`, `SUV` and `LuxuryCar` inherit from `Vehicle`, so they reuse its attributes and methods. Each child calls `super().__init__()` to set up the shared parts. `MpesaPayment`, `CardPayment` and `CashPayment` inherit from `Payment` in the same way. `SUV` adds a service charge and `LuxuryCar` adds insurance.

**Polymorphism.** `Rental` calls `vehicle.calculate_rental_cost(days)` without checking what type of vehicle it has. Each class returns its own price: a plain daily rate for an economy car, the daily rate plus a KSh 2,000 service charge for an SUV, and the daily rate plus 10% insurance for a luxury car. The same happens with payments: `process_payment()` is called on every payment, and each type behaves differently, such as generating an M-Pesa transaction code, showing the last four card digits, or calculating change for cash.

## Business Rules

The system enforces these rules and raises a `ValueError` with a clear message when one is broken:

- Daily rates cannot be negative
- A customer must have a driving licence
- A customer must be registered before renting
- A vehicle must be in the fleet before it is rented
- Rental days must be greater than zero
- A rented vehicle cannot be rented again
- A vehicle can only be returned if it is currently rented
- A completed rental cannot be completed again
- Payment amounts cannot be negative
- A rental can only be paid once, and only after it has been returned

## Real-World Problem

Without a system, SafariDrive's staff must check notebooks and spreadsheets to find out whether a car is free, who has it and when it is due back. Late returns are easy to miss, and the company's total revenue is only known after someone adds up the records by hand.

RentFlow keeps these records in one place. A car is marked as rented when it is booked and available again once it is returned. Late fees are calculated automatically from the agreed and actual days, and revenue increases only when a payment succeeds. The management report gives an up-to-date view of the fleet, customers, rentals and income.

## Sample Data

`main.py` loads sample data to demonstrate the system:

- **Vehicles (5):** Toyota Axio (economy), Toyota Prado (SUV), Nissan X-Trail (SUV), Mercedes-Benz E-Class (luxury), Toyota Vitz (economy)
- **Customers (3):** John Kamau, Jane Wanjiru, Peter Otieno
- **Rentals (4):** the Prado with a late return and M-Pesa payment, the Axio paid in cash, the E-Class with a damage charge paid by card, and the Vitz paid by M-Pesa

The demo produces total revenue of KSh 93,200.

## Author

Joan Rono
(https://github.com/ronotrials-blip/rentflow)
