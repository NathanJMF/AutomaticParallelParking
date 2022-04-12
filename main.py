def get_start_vars(lower, upper, prompt):
    value = int
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a valid input.")
            continue
        if lower <= value <= upper:
            break
        else:
            print("Please enter a valid input.")
    return value


def main():
    print("Start!")
    x = get_start_vars(0, 100, "Starting X co-ordinate:\nPlease enter a number from 0 and 100\n")
    y = get_start_vars(0, 100, "Starting Y co-ordinate:\nPlease enter a number from 0 and 100\n")
    angle = get_start_vars(0, 360, "Starting angle:\nPlease enter a number from 0 to 360\n")
    parking_spot = get_start_vars(0, 24, "Desired parking spot:\nPlease enter a number from 0 to 24\n")
    print(x, y, angle, parking_spot)


if __name__ == "__main__":
    main()
