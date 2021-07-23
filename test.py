x, y = 5, 1

try:
  z = int(x/y)
except ZeroDivisionError as error:
  z = error

print(z)