# Bob's Rentals Application

## Student
Rabab Misry

## Project
Bob's Rentals - Final Project Part 2

## Project Description
This project is a console application for Bob's Ski and Snowboard Rentals.

For Part 2 of the project, I used the assigned Bob's Rentals class library and created an application that allows the user to manage customer rentals, returns, inventory, discounts, and end-of-day totals.

The original assigned class files were kept unchanged. My application logic was created in `application.py`.

## Assigned Classes Used

The application uses the following assigned classes:

- Customer
- Rental
- RentalEquipment
- RentalShop
- Ski
- Snowboard

The Ski and Snowboard classes inherit from RentalEquipment.

## Application Features

The application allows the user to:

- Enter starting ski and snowboard inventory
- Create a new customer rental
- Rent skis, snowboards, or both
- Choose an hourly, daily, or weekly rental period
- Check available inventory
- Calculate the best rental price
- Apply a 25% family discount for 3 to 5 total items
- Apply a 10% coupon discount for coupon codes ending in BBP
- Store active customer rentals
- Process equipment returns
- Calculate the final bill using the actual rental length
- Restore inventory after equipment is returned
- Display current inventory
- Track skis and snowboards rented during the day
- Track revenue from completed returns
- Display end-of-day totals
- Validate user input

## How to Run the Program

1. Download or clone the repository.
2. Make sure all Python files are in the same folder.
3. Open `application.py` in Python IDLE.
4. Select Run > Run Module or press F5.
5. Enter the starting inventory for skis and snowboards.
6. Use the main menu to create rentals, process returns, show inventory, or end the day.

## Assigned Class Limitations

The assigned Rental class allows a maximum of 5 items in one Rental object. My application works with this limitation by creating additional Rental objects when needed.

The assigned Rental class calculates the family discount using the quantity of one Rental object. Since a customer can rent both skis and snowboards, my application calculates the family discount using the combined number of items.

The assigned RentalShop class records revenue when a rental is created. The Part 2 requirements state that revenue should be counted after a rental is returned and paid, so my application separately tracks revenue from completed returns.

## Reflection

This project helped me understand how to build an application using classes created by another programmer. I learned how to examine existing classes and use their properties and methods without changing the original code.

I also learned how to work around limitations in existing classes while keeping the application organized. Testing the rental, return, inventory, discount, and end-of-day features helped me understand how different classes can work together in one application.
