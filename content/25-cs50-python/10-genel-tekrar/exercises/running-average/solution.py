def main():
    numbers = []
    while True:
        try:
            numbers.append(float(input("Number: ")))
        except ValueError:
            print("Not a number")
        except EOFError:
            break
    if numbers:
        print(f"Average: {sum(numbers) / len(numbers):.2f}")
    else:
        print("No numbers")


if __name__ == "__main__":
    main()
