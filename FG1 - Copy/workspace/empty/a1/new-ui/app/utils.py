import random

def generate_routing_number():
    """
    Generate a valid 9-digit ABA routing number
    Uses the check digit algorithm for validation
    """
    # First 8 digits random
    first_eight = [random.randint(0, 9) for _ in range(8)]
    
    # Calculate check digit (9th digit)
    # Formula: (3(d1 + d4 + d7) + 7(d2 + d5 + d8) + (d3 + d6)) mod 10
    check_sum = (
        3 * (first_eight[0] + first_eight[3] + first_eight[6]) +
        7 * (first_eight[1] + first_eight[4] + first_eight[7]) +
        (first_eight[2] + first_eight[5])
    )
    check_digit = (10 - (check_sum % 10)) % 10
    
    # Combine all digits
    routing_number = ''.join(map(str, first_eight + [check_digit]))
    return routing_number

def generate_account_number():
    """
    Generate a random 10-12 digit account number
    """
    length = random.randint(10, 12)
    return ''.join(str(random.randint(0, 9)) for _ in range(length))