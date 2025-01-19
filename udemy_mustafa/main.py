# message = "Hello World"
# print(message)

# def convert_to_celsius(fahrenheit: float) -> float:
#     try:
#         return (fahrenheit - 32) * 5/9
#     except ValueError:
#         return "Invalid input: Please enter a number."
# print(convert_to_celsius(100))

# Function that takes either a celsius or fahrenheit value and converts it to the other
def convert_temperature(temperature: float, unit: str) -> float:
    if unit == "C":
        return (temperature * 9/5) + 32
    elif unit == "F":
        return (temperature - 32) * 5/9
    else:
        return "Invalid input: Please enter a valid unit (C or F)."
print(convert_temperature(100, "C"))
