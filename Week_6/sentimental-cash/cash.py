from cs50 import get_float

while True:
    money = get_float("Change owed: ")
    if money >= 0:
        break
    else:
        print("Please enter a non-negative number.")

cents = round(money * 100)

quarters = cents // 25
cents = cents % 25

dimes = cents // 10
cents = cents % 10

nickels = cents // 5
cents = cents % 5

pennies = cents

coins = quarters + dimes + nickels + pennies

print(coins)
