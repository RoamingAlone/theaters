class Movie:
    def __init__(self, title: str, duration: int, rating: str):
        self.title = title
        self.duration = duration  # Duration in minutes
        self.rating = rating

    def __str__(self):
        return f"{self.title} ({self.rating}) - {self.duration} mins"

class User:
    def __init__(self, name: str):
        self.name = name

class Customer(User):
    def __init__(self, name: str):
        super().__init__(name)

class Employee(User):
    def __init__(self, name: str):
        super().__init__(name)

class Theater:
    def __init__(self, name: str, total_seats: int):
        self.name = name
        self.total_seats = total_seats
        self.movies = []
        # Mapping of movie title to number of available seats
        self.available_seats = {}

    def _add_movie(self, movie: Movie):
        if movie not in self.movies:
            self.movies.append(movie)
            # Initialize available seats for the new movie
            self.available_seats[movie.title] = self.total_seats

    def _update_movie(self, old_movie_title: str, new_movie: Movie) -> bool:
        for i, m in enumerate(self.movies):
            if m.title == old_movie_title:
                self.movies[i] = new_movie
                # Reset seats for the new movie, assuming a completely new schedule
                self.available_seats.pop(old_movie_title, None)
                self.available_seats[new_movie.title] = self.total_seats
                return True
        return False

    def __str__(self):
        return f"Theater: {self.name} | Total Seats: {self.total_seats}"

class BookingSystem:
    def __init__(self):
        self.theaters = []
        self.customers = []
        self.employees = []

    def add_theater(self, theater: Theater):
        self.theaters.append(theater)

    def add_customer(self, customer: Customer):
        if customer not in self.customers:
            self.customers.append(customer)

    def add_employee(self, employee: Employee):
        if employee not in self.employees:
            self.employees.append(employee)

    def employee_add_movie(self, employee: Employee, theater: Theater, movie: Movie) -> bool:
        """Only actual employees can add a movie to a theater"""
        if employee not in self.employees:
            print(f"Authorization Error: {employee.name} is not a registered employee.")
            return False
            
        if theater not in self.theaters:
            print(f"Error: {theater.name} is not registered in the system.")
            return False

        theater._add_movie(movie)
        print(f"Employee {employee.name} successfully added movie '{movie.title}' to {theater.name}.")
        return True

    def employee_update_movie(self, employee: Employee, theater: Theater, old_movie_title: str, new_movie: Movie) -> bool:
        """Only actual employees can update a movie in a theater"""
        if employee not in self.employees:
            print(f"Authorization Error: {employee.name} is not a registered employee.")
            return False
            
        if theater not in self.theaters:
            print(f"Error: {theater.name} is not registered in the system.")
            return False

        success = theater._update_movie(old_movie_title, new_movie)
        if success:
            print(f"Employee {employee.name} successfully updated movie '{old_movie_title}' to '{new_movie.title}' at {theater.name}.")
        else:
            print(f"Error: Movie '{old_movie_title}' not found in {theater.name}.")
        return success

    def check_availability(self, theater: Theater, movie: Movie) -> int:
        """Returns the number of available seats for a specific movie in a given theater."""
        if theater in self.theaters and movie in theater.movies:
            return theater.available_seats.get(movie.title, 0)
        return 0

    def customer_book_seat(self, customer: Customer, theater: Theater, movie: Movie, num_seats: int = 1) -> bool:
        """Attempts to reserve a specified number of seats for a customer. Returns True if successful."""
        if customer not in self.customers:
            print(f"Authorization Error: {customer.name} is not a registered customer.")
            return False
            
        if theater not in self.theaters:
            print(f"Error: {theater.name} is not registered in the booking system.")
            return False
            
        if movie not in theater.movies:
            print(f"Error: '{movie.title}' is not currently playing at {theater.name}.")
            return False
            
        current_available = theater.available_seats[movie.title]
        if current_available >= num_seats:
            theater.available_seats[movie.title] -= num_seats
            print(f"Success! {customer.name} reserved {num_seats} seat(s) for '{movie.title}' at {theater.name}.")
            return True
        else:
            print(f"Sorry {customer.name}, could not reserve {num_seats} seat(s). Only {current_available} seat(s) available for '{movie.title}'.")
            return False


# Example usage
if __name__ == "__main__":
    # 1. Initialize the system
    booking_system = BookingSystem()

    # 2. Add Employees and Customers
    emp1 = Employee("Alice")
    cust1 = Customer("Bob")
    cust2 = Customer("Charlie")

    booking_system.add_employee(emp1)
    booking_system.add_customer(cust1)
    booking_system.add_customer(cust2)

    # 3. Create a theater and add it to system
    theater1 = Theater(name="Downtown Cinema", total_seats=100)
    booking_system.add_theater(theater1)

    # 4. Create some movies
    movie1 = Movie(title="The Matrix", duration=136, rating="R")
    movie2 = Movie(title="Inception", duration=148, rating="PG-13")
    movie3 = Movie(title="Interstellar", duration=169, rating="PG-13")

    # 5. Employees adding and updating movies
    # Should fail because anon_emp isn't a registered employee
    anon_emp = Employee("Eve")
    booking_system.employee_add_movie(anon_emp, theater1, movie1)

    # Should succeed because emp1 is registered
    booking_system.employee_add_movie(emp1, theater1, movie1)
    booking_system.employee_add_movie(emp1, theater1, movie2)

    # Update Inception to Interstellar
    booking_system.employee_update_movie(emp1, theater1, "Inception", movie3)

    # 6. Customers booking seats
    print(f"\\nInitial availability for {movie1.title}: {booking_system.check_availability(theater1, movie1)}")
    
    # Should fail because anon_cust isn't a registered customer
    anon_cust = Customer("David")
    booking_system.customer_book_seat(anon_cust, theater1, movie1, 2)

    # Reserve 5 seats as Charlie
    booking_system.customer_book_seat(cust2, theater1, movie1, 5)
    
    print(f"Availability after booking for {movie1.title}: {booking_system.check_availability(theater1, movie1)}")
    
    # Attempt to overbook
    booking_system.customer_book_seat(cust1, theater1, movie3, 105)
