expression = input("Expression: ")
x, y, z = expression.split(" ")
x = int(x)
z = int(z)
if y == "+":
    result = x + z
elif y == "-":
    result = x - z
elif y == "*":
    result = x * z
elif y == "/":
    result = x / z
else:
    result = "ERROR: Unknown operation."

if result == int(result):
    result = float(int(result))

print(result)

