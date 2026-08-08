from Ski import ski
from Snowboard import snowboard
from Customer import customer
from Rental import rental
from RentalShop import rental_shop


def get_starting_inventory(message):
    while True:
        try:
            amount = int(input(message))

            if amount < 0:
                print("Inventory cannot be negative.")
            else:
                return amount

        except ValueError:
            print("Please enter a whole number.")


def get_quantity(message):
    while True:
        try:
            quantity = int(input(message))

            if quantity < 0:
                print("Quantity cannot be negative.")
            else:
                return quantity

        except ValueError:
            print("Please enter a whole number.")


def get_positive_number(message):
    while True:
        try:
            number = int(input(message))

            if number <= 0:
                print("Please enter a number greater than 0.")
            else:
                return number

        except ValueError:
            print("Please enter a whole number.")


def get_yes_no(message):
    while True:
        answer = input(message).strip().lower()

        if answer == "yes" or answer == "y":
            return True
        elif answer == "no" or answer == "n":
            return False
        else:
            print("Please enter yes or no.")


def get_rental_period():
    while True:
        print("\nRental Period")
        print("1. Hourly")
        print("2. Daily")
        print("3. Weekly")

        choice = input("Choose a rental period: ")

        if choice == "1":
            return "Hourly"
        elif choice == "2":
            return "Daily"
        elif choice == "3":
            return "Weekly"
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")


def convert_to_hours(period, length):
    if period == "Hourly":
        return length
    elif period == "Daily":
        return length * 8
    else:
        return length * 56


def create_rental_objects(customer_object, equipment, quantity,
                          hours, coupon_code):
    rentals = []

    remaining = quantity

    while remaining > 0:
        if remaining > 5:
            rental_quantity = 5
        else:
            rental_quantity = remaining

        new_rental = rental(
            customer_object,
            equipment,
            rental_quantity,
            hours,
            coupon_code
        )

        rentals.append(new_rental)
        remaining -= rental_quantity

    return rentals


def new_customer_rental(skis, snowboards, active_rentals, daily_totals):
    print("\n--- New Customer Rental ---")

    ski_quantity = get_quantity("Number of skis requested: ")
    snowboard_quantity = get_quantity("Number of snowboards requested: ")

    total_items = ski_quantity + snowboard_quantity

    if total_items == 0:
        print("The customer must rent at least one item.")
        return

    # Check inventory
    if ski_quantity > skis.available_inventory:
        print(
            f"Not enough skis available. "
            f"Available: {skis.available_inventory}"
        )
        return

    if snowboard_quantity > snowboards.available_inventory:
        print(
            f"Not enough snowboards available. "
            f"Available: {snowboards.available_inventory}"
        )
        return

    period = get_rental_period()

    length = get_positive_number(
        f"Enter estimated rental length in {period.lower()} units: "
    )

    hours = convert_to_hours(period, length)

    coupon_code = input(
        "Enter coupon code or press Enter if there is none: "
    ).strip()

    # Calculate price before discounts
    ski_cost = skis.get_best_price(hours) * ski_quantity
    snowboard_cost = snowboards.get_best_price(hours) * snowboard_quantity

    price_before_discounts = ski_cost + snowboard_cost
    final_price = price_before_discounts

    family_discount = 0
    coupon_discount = 0

    # Family discount is based on combined equipment quantity
    if 3 <= total_items <= 5:
        family_discount = final_price * 0.25
        final_price -= family_discount

    # Coupon discount is applied after family discount
    if coupon_code.upper().endswith("BBP"):
        coupon_discount = final_price * 0.10
        final_price -= coupon_discount

    print("\n--- Rental Estimate ---")

    if ski_quantity > 0:
        print(f"Skis: {ski_quantity}")

    if snowboard_quantity > 0:
        print(f"Snowboards: {snowboard_quantity}")

    print(f"Rental period: {period}")
    print(f"Estimated rental length: {length} {period.lower()} units")
    print(f"Price before discounts: ${price_before_discounts:.2f}")

    if family_discount > 0:
        print(f"Family discount: -${family_discount:.2f}")

    if coupon_discount > 0:
        print(f"Coupon discount: -${coupon_discount:.2f}")

    print(f"Estimated final price: ${final_price:.2f}")

    complete = get_yes_no(
        "\nDoes the customer want to complete the rental? (yes/no): "
    )

    if not complete:
        print("Rental cancelled.")
        return

    # Collect customer information
    while True:
        name = input("Customer name: ").strip()

        if name == "":
            print("Customer name cannot be blank.")
        else:
            break

    while True:
        customer_id = get_positive_number("Customer ID: ")

        if customer_id in active_rentals:
            print("That customer ID already has an active rental.")
        else:
            break

    try:
        customer_object = customer(name, customer_id)

        transaction_rentals = []

        if ski_quantity > 0:
            ski_rentals = create_rental_objects(
                customer_object,
                skis,
                ski_quantity,
                hours,
                coupon_code
            )

            transaction_rentals.extend(ski_rentals)

        if snowboard_quantity > 0:
            snowboard_rentals = create_rental_objects(
                customer_object,
                snowboards,
                snowboard_quantity,
                hours,
                coupon_code
            )

            transaction_rentals.extend(snowboard_rentals)

        # Reduce inventory
        if ski_quantity > 0:
            skis.rent(ski_quantity)

        if snowboard_quantity > 0:
            snowboards.rent(snowboard_quantity)

        # Store complete transaction
        active_rentals[customer_id] = {
            "customer": customer_object,
            "rentals": transaction_rentals,
            "ski_quantity": ski_quantity,
            "snowboard_quantity": snowboard_quantity,
            "period": period,
            "coupon_code": coupon_code,
            "returned": False
        }

        daily_totals["skis"] += ski_quantity
        daily_totals["snowboards"] += snowboard_quantity

        print("\nRental completed successfully.")
        print(f"Customer ID: {customer_id}")

    except Exception as e:
        print(f"Rental could not be completed: {e}")
def rental_return(skis, snowboards, active_rentals, daily_totals):
    print("\n--- Rental Return ---")

    customer_id = get_positive_number("Enter customer ID: ")

    if customer_id not in active_rentals:
        print("No active rental was found for that customer ID.")
        return

    transaction = active_rentals[customer_id]
    customer_object = transaction["customer"]

    print(f"\nCustomer: {customer_object.name}")
    print(f"Customer ID: {customer_object.customer_id}")

    period = transaction["period"]

    actual_length = get_positive_number(
        f"Enter actual rental length in {period.lower()} units: "
    )

    actual_hours = convert_to_hours(period, actual_length)

    ski_quantity = transaction["ski_quantity"]
    snowboard_quantity = transaction["snowboard_quantity"]
    total_items = ski_quantity + snowboard_quantity

    # Calculate final price using actual rental time
    ski_cost = skis.get_best_price(actual_hours) * ski_quantity
    snowboard_cost = (
        snowboards.get_best_price(actual_hours) * snowboard_quantity
    )

    price_before_discounts = ski_cost + snowboard_cost
    final_price = price_before_discounts

    family_discount = 0
    coupon_discount = 0

    # Family discount uses combined number of items
    if 3 <= total_items <= 5:
        family_discount = final_price * 0.25
        final_price -= family_discount

    coupon_code = transaction["coupon_code"]

    # Coupon discount comes after family discount
    if coupon_code.upper().endswith("BBP"):
        coupon_discount = final_price * 0.10
        final_price -= coupon_discount

    print("\n--- Final Invoice ---")
    print(f"Customer: {customer_object.name}")
    print(f"Customer ID: {customer_object.customer_id}")

    if ski_quantity > 0:
        print(f"Skis rented: {ski_quantity}")

    if snowboard_quantity > 0:
        print(f"Snowboards rented: {snowboard_quantity}")

    print(f"Rental period: {period}")
    print(
        f"Total rental time: "
        f"{actual_length} {period.lower()} units"
    )
    print(f"Price before discounts: ${price_before_discounts:.2f}")

    if family_discount > 0:
        print(f"Family discount: -${family_discount:.2f}")

    if coupon_discount > 0:
        print(f"Coupon discount: -${coupon_discount:.2f}")

    print(f"Final amount due: ${final_price:.2f}")

    complete_return = get_yes_no(
        "\nComplete return and payment? (yes/no): "
    )

    if not complete_return:
        print("Return cancelled.")
        return

    try:
        # Restore equipment to inventory
        if ski_quantity > 0:
            skis.return_equipment(ski_quantity)

        if snowboard_quantity > 0:
            snowboards.return_equipment(snowboard_quantity)

        # Revenue is recorded only after return/payment
        daily_totals["revenue"] += final_price

        # Rental is no longer active
        del active_rentals[customer_id]

        print("\nReturn completed successfully.")
        print(f"Payment received: ${final_price:.2f}")

    except Exception as e:
        print(f"Return could not be completed: {e}")

def main():
    print("Welcome to Bob's Ski & Snowboard Rentals")

    ski_inventory = get_starting_inventory(
        "Enter starting ski inventory: "
    )

    snowboard_inventory = get_starting_inventory(
        "Enter starting snowboard inventory: "
    )

    skis = ski(ski_inventory)
    snowboards = snowboard(snowboard_inventory)

    shop = rental_shop()
    shop.set_inventory(skis, snowboards)

    active_rentals = {}

    daily_totals = {
        "skis": 0,
        "snowboards": 0,
        "revenue": 0.0
    }

    while True:
        print("\n--- Main Menu ---")
        print("1. New Customer Rental")
        print("2. Rental Return")
        print("3. Show Inventory")
        print("4. End of Day")

        choice = input("Enter your choice: ")

        if choice == "1":
            new_customer_rental(
                skis,
                snowboards,
                active_rentals,
                daily_totals
            )

        elif choice == "2":
            rental_return(
                skis,
                snowboards,
                active_rentals,
                daily_totals
            )

        elif choice == "3":
            shop.display_available()

        elif choice == "4":
            print("\n--- End of Day ---")
            print(f"Skis rented today: {daily_totals['skis']}")
            print(f"Snowboards rented today: {daily_totals['snowboards']}")
            print(f"Revenue from completed returns: ${daily_totals['revenue']:.2f}")
            break

        else:
            print(
                "Invalid selection. Please choose 1, 2, 3, or 4."
            )


main()
