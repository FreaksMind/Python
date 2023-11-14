#----------------------------------------------- EX 1 ----------------------------------------------------------
import numpy

class Shape:
    def area(self):
        pass
    
    def perimeter(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return numpy.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * numpy.pi * self.radius

class Triangle(Shape):
    def __init__(self, side_a, side_b, side_c):
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    def area(self):
        s = (self.side_a + self.side_b + self.side_c) / 2
        return numpy.sqrt(s * (s - self.side_a) * (s - self.side_b) * (s - self.side_c))
    
    def perimeter(self):
        return self.side_a + self.side_b + self.side_c


#----------------------------------------------- EX 2 ----------------------------------------------------------

class Account:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            print("Invalid number.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"New balance: ${self.balance}")
        else:
            print("Invalid amount.")

    def calculate_interest(self):
        pass


class SavingsAccount(Account):
    interest_rate = 0.02

    def calculate_interest(self):
        interest = self.balance * self.interest_rate
        self.deposit(interest)


class CheckingAccount(Account):
    overdraft_fee = 20

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
            self.balance -= self.overdraft_fee
        self.withdraw(amount)


#----------------------------------------------- EX 4 ----------------------------------------------------------


class Employee:
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id
        self.salary = 0

class Manager(Employee):
    def __init__(self, name, employee_id, department):
        super().__init__(name, employee_id)
        self.department = department
    
    def present(self):
        print("Yay! You called present.")

class Engineer(Employee):
    def __init__(self, name, employee_id, programming_language):
        super().__init__(name, employee_id)
        self.programming_language = programming_language

    def code(self):
        print("Yay! You called code.")

class Salesperson(Employee):
    def __init__(self, name, employee_id, sales_target):
        super().__init__(name, employee_id)
        self.sales_target = sales_target
   
    def sell(self):
        print("Yay! You called sell.")


#----------------------------------------------- EX 5 ----------------------------------------------------------


class Animal:
    def __init__(self, name, habitat):
        self.name = name
        self.habitat = habitat

    def move(self):
        pass


class Mammal(Animal):
    def __init__(self, name, habitat, fur_color):
        super().__init__(name, habitat)
        self.fur_color = fur_color

    def move(self):
        print("Mammal is walking.")

class Bird(Animal):
    def __init__(self, name, habitat, wingspan):
        super().__init__(name, habitat)
        self.wingspan = wingspan

    def move(self):
        print("Bird is flying.")

class Fish(Animal):
    def __init__(self, name, habitat, fin_type):
        super().__init__(name, habitat)
        self.fin_type = fin_type

    def move(self):
        print("Fish is swimming.")


#----------------------------------------------- EX 6 ----------------------------------------------------------

class LibraryItem:
    def __init__(self, title, release_year):
        self.title = title
        self.release_year = release_year

    def check_out(self):
        print(f"Check out {self.title}")

    def return_item(self):
        print(f"Return {self.title}")

    def display_info(self):
        print(f"{self.title} released in {self.release_year}")


class Book(LibraryItem):
    def __init__(self, title, release_year, author):
        super().__init__(title, release_year)
        self.author = author

    def check_out(self):
        super().__init__()

    def return_item(self):
        super().__init__()

    def display_info(self):
        print(f"{self.title} released in {self.release_year} (Author: {self.author})")

class DVD(LibraryItem):
    def __init__(self, title, release_year, director):
        super().__init__(title, release_year)
        self.director = director

    def check_out(self):
        super().__init__()

    def return_item(self):
        super().__init__()

    def display_info(self):
        print(f"{self.title} released in {self.release_year} (Director: {self.director})")

class Magazine(LibraryItem):
    def __init__(self, title, release_year, issue_number):
        super().__init__(title, release_year)
        self.issue_number = issue_number

    def check_out(self):
        super().__init__()

    def return_item(self):
        super().__init__()

    def display_info(self):
        print(f"{self.title} released in {self.release_year} (Issue Number: {self.issue_number})")

#----------------------------------------------- EX 3 ----------------------------------------------------------


class Vehicle:
    def __init__(self, company, model, year):
        self.company = company
        self.model = model
        self.year = year

    def display_info(self):
        print(f"{self.year} {self.company} {self.model}")


class Car(Vehicle):
    def __init__(self, company, model, year, fuel_efficiency):
        super().__init__(company, model, year)
        self.fuel_efficiency = fuel_efficiency

    def get_mileage(self, distance):
        return distance / self.fuel_efficiency

class Motorcycle(Vehicle):
    def __init__(self, company, model, year, fuel_efficiency):
        super().__init__(company, model, year)
        self.fuel_efficiency = fuel_efficiency

    def get_mileage(self, distance):
        return distance / self.fuel_efficiency

class Truck(Vehicle):
    def __init__(self, company, model, year, towing_capacity):
        super().__init__(company, model, year)
        self.towing_capacity = towing_capacity

    def get_towing_capacity(self):
        return f"{self.towing_capacity} kg"
