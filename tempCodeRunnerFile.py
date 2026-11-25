try:
    num1 = int(input("enter the number are:"))
    num2 = int(input("enter the number are:"))


    result = num1/num2
    print("the result are:", result)

except ValueError:
    print("Error: Invalid input. Please enter numeric values.")

except ZeroDivisionError:
    print("Error: Division by zero is not allowed.")