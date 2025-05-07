def generate_fibonacci(n):

    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    sequence = [0, 1]
    for _ in range(2, n):
        next_number = sequence[-1] + sequence[-2]
        sequence.append(next_number)
    return sequence

def main():
    print("Fibonacci Sequence Generator")
    try:
        num_terms = int(input("Enter the number of terms to generate: "))
        if num_terms < 0:
            print("Please enter a positive integer.")
        else:
            fibonacci_sequence = generate_fibonacci(num_terms)
            print("Fibonacci sequence:")
            print(fibonacci_sequence)
    except ValueError:
        print("Invalid input! Please enter a valid integer.")

if __name__ == "__main__":
    main()
