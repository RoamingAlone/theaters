class Movie:
    def __init__(self, title: str, duration: int, rating: str):
        self.title = title
        self.duration = duration  # Duration in minutes
        self.rating = rating

    def __str__(self):
        return f"{self.title} ({self.rating}) - {self.duration} mins"


class Theater:
    def __init__(self, name: str, total_seats: int):
        self.name = name
        self.total_seats = total_seats
        self.movies = []
        # Mapping of movie title to number of available seats
        self.available_seats = {}

    def add_movie(self, movie: Movie):
        if movie not in self.movies:
            self.movies.append(movie)
            # Initialize available seats for the new movie
            self.available_seats[movie.title] = self.total_seats

    def __str__(self):
        return f"Theater: {self.name} | Total Seats: {self.total_seats}"


class BookingSystem:
    def __init__(self):
        self.theaters = []

    def add_theater(self, theater: Theater):
        self.theaters.append(theater)

    def check_availability(self, theater: Theater, movie: Movie) -> int:
        """Returns the number of available seats for a specific movie in a given theater."""
        if theater in self.theaters and movie in theater.movies:
            return theater.available_seats.get(movie.title, 0)
        return 0

    def reserve_seat(self, theater: Theater, movie: Movie, num_seats: int = 1) -> bool:
        """Attempts to reserve a specified number of seats. Returns True if successful."""
        if theater not in self.theaters:
            print(f"Error: {theater.name} is not registered in the booking system.")
            return False
            
        if movie not in theater.movies:
            print(f"Error: '{movie.title}' is not currently playing at {theater.name}.")
            return False
            
        current_available = theater.available_seats[movie.title]
        if current_available >= num_seats:
            theater.available_seats[movie.title] -= num_seats
            print(f"Success! Reserved {num_seats} seat(s) for '{movie.title}' at {theater.name}.")
            return True
        else:
            print(f"Sorry, could not reserve {num_seats} seat(s). Only {current_available} seat(s) available for '{movie.title}'.")
            return False


# Example usage
if __name__ == "__main__":
    # 1. Initialize the system
    booking_system = BookingSystem()

    # 2. Create some movies
    movie1 = Movie(title="The Matrix", duration=136, rating="R")
    movie2 = Movie(title="Inception", duration=148, rating="PG-13")

    # 3. Create a theater and add movies to it
    theater1 = Theater(name="Downtown Cinema", total_seats=100)
    theater1.add_movie(movie1)
    theater1.add_movie(movie2)

    # 4. Add theater to the booking system
    booking_system.add_theater(theater1)

    # 5. Check availability and reserve seats
    print(f"Initial availability for {movie1.title}: {booking_system.check_availability(theater1, movie1)}")
    
    # Reserve 5 seats
    booking_system.reserve_seat(theater1, movie1, 5)
    
    print(f"Availability after booking for {movie1.title}: {booking_system.check_availability(theater1, movie1)}")
    
    # Attempt to overbook
    booking_system.reserve_seat(theater1, movie2, 105)
