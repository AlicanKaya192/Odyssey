def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    # Şartlardan biri bozulursa False, hepsi tutarsa True döndür
    ...


main()
