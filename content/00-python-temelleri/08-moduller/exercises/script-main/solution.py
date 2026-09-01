import math


def area(radius):
    return round(math.pi * radius * radius, 2)


def main():
    for radius in [1, 2, 3]:
        print(area(radius))


if __name__ == "__main__":
    main()
