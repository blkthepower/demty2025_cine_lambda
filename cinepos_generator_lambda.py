
import json
import random
import string
import datetime
import boto3
 
def lambda_handler(event, context):
    """
    Generates 200 fictitious cinema POS transaction records and saves them to S3.
    """
    # Replace with your actual S3 bucket name
    bucket_name = "xideralpos"
    
    # We'll generate a unique file name using the current timestamp
    object_key = f"cinema-pos-{int(datetime.datetime.now().timestamp())}.json"
    
    # Example list of movies
    movies = [
        "Avatar: The Way of Water",
        "Spider-Man: No Way Home",
        "Top Gun: Maverick",
        "Black Panther: Wakanda Forever",
        "Jurassic World: Dominion",
        "Minions: The Rise of Gru",
        "Doctor Strange in the Multiverse of Madness",
        "Fast & Furious 9",
        "Elvis",
        "Lightyear",
        "The Batman"
    ]
    
    # Example payment methods
    payment_methods = [
        "Cash",
        "Credit Card",
        "Debit Card",
        "PayPal",
        "Mobile Payment"
    ]
    
    # Example snack items
    snack_options = [
        {"name": "Popcorn", "price": 50},
        {"name": "Soda", "price": 30},
        {"name": "Nachos", "price": 45},
        {"name": "Hot Dog", "price": 40},
        {"name": "Candy",  "price": 25}
    ]
    
    # List of 20 fictitious membership numbers
    membership_numbers = [
        "CIN-54729", "MOV-82734", "FLM-13456", "CIN-98301", "FLIC-29837",
        "MOV-71029", "FILM-83647", "CIN-56392", "MOV-18465", "FLIC-47328",
        "CIN-20984", "FILM-59283", "MOV-61402", "CIN-47892", "FLIC-10293",
        "MOV-83071", "FILM-42710", "CIN-65283", "FLIC-39457", "MOV-21836"
    ]
    
    def get_random_item(items):
        """Return a random element from a list."""
        return random.choice(items)
    
    def get_random_number(min_val, max_val):
        """Return a random integer between min_val and max_val (inclusive)."""
        return random.randint(min_val, max_val)
    
    def generate_transaction_id():
        """Generate a simple unique transaction ID (e.g. 'TX-ABCD1234')."""
        # 8 random alphanumeric characters
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"TX-{random_part}"
    
    def generate_random_date():
        """
        Generate a random date/time (as ISO 8601 string) between now and 30 days ago.
        """
        now = datetime.datetime.now()
        thirty_days_ago = now - datetime.timedelta(days=30)
        
        # Get a random number of seconds between thirty_days_ago and now
        total_seconds_diff = int((now - thirty_days_ago).total_seconds())
        random_offset = random.randint(0, total_seconds_diff)
        
        random_time = thirty_days_ago + datetime.timedelta(seconds=random_offset)
        return random_time.isoformat()
    
    def generate_seats(quantity):
        """
        Generate a list of seat strings, e.g., ['A5', 'C7'].
        """
        rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
        seats = []
        for _ in range(quantity):
            row = get_random_item(rows)
            seat_number = get_random_number(1, 12)
            seats.append(f"{row}{seat_number}")
        return seats
    
    # Generate 200 records
    record_count = 200
    transactions = []
    
    for _ in range(record_count):
        selected_movie = get_random_item(movies)
        
        # Ticket quantity (between 1 and 5)
        ticket_quantity = get_random_number(1, 5)
        
        # Generate seat assignments
        selected_seats = generate_seats(ticket_quantity)
        
        # Ticket price per seat (between 70 and 150)
        ticket_price = get_random_number(70, 150)
        ticket_subtotal = ticket_price * ticket_quantity
        
        # Generate random snack items (0 to 3 different types)
        snack_items = []
        snack_count = get_random_number(0, 3)
        for _snack_idx in range(snack_count):
            chosen_snack = get_random_item(snack_options)
            # Quantity of each snack type (1 or 2)
            snack_quantity = get_random_number(1, 2)
            snack_items.append({
                "name": chosen_snack["name"],
                "quantity": snack_quantity,
                "unitPrice": chosen_snack["price"],
                "subtotal": chosen_snack["price"] * snack_quantity
            })
        
        # Calculate total for snacks
        snack_total = sum(item["subtotal"] for item in snack_items)
        
        # Total transaction price
        total_price = ticket_subtotal + snack_total
        
        # Determine if the purchase was made with a membership
        is_membership = random.choice([True, False])
        membership_number = get_random_item(membership_numbers) if is_membership else None
        
        # Build the transaction object
        transaction = {
            "transactionId": generate_transaction_id(),
            "dateTime": generate_random_date(),
            "movie": selected_movie,
            "ticketQuantity": ticket_quantity,
            "seats": selected_seats,
            "paymentMethod": get_random_item(payment_methods),
            "ticketSubtotal": ticket_subtotal,
            "snackItems": snack_items,
            "totalPrice": total_price,
            "membershipNumber": membership_number
        }
        
        transactions.append(transaction)
    
    # Convert transactions to JSON
    data_string = json.dumps(transactions, indent=2)
    
    # Upload to S3
    s3_client = boto3.client("s3")
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=data_string.encode("utf-8"),
            ContentType="application/json"
        )
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Data generated and saved to S3 successfully.",
                "location": f"s3://{bucket_name}/{object_key}"
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Error saving data to S3.",
                "error": str(e)
            })
        }