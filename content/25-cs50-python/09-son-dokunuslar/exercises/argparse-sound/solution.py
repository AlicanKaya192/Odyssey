import argparse


def main():
    parser = argparse.ArgumentParser(description="Make an animal sound")
    parser.add_argument("-n", "--number", default=1, type=int, help="number of times")
    parser.add_argument("-s", "--sound", default="meow", help="the sound to make")
    args = parser.parse_args()
    for _ in range(args.number):
        print(args.sound)


if __name__ == "__main__":
    main()
