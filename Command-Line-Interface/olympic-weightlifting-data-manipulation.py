# olympic last five years data manipulation cli based mini project for weightlifting sports
import datetime

# List to store all the records as dictionaries
records = []

# Function to add data
def add_data():
    game = input("Enter the game: ")
    year = int(input("Enter the conducted year: "))
    sports = input("Enter the sports name: ")
    event = input("Enter the event name: ")
    athlete = input("Enter the athlete name: ")
    country = input("Enter the winner's country: ")
    placement = int(input("Enter the placement position: "))
    medal = input("Enter the medal type (1.GOLD/2.SILVER/3.BRONZE): ")

    # Create a new data as a dictionary and add it to the list
    new_data = {
        "game": game,
        "year": year,
        "sports": sports,
        "event": event,
        "athlete": athlete,
        "country": country,
        "placement": placement,
        "medal": medal
    }
    records.append(new_data)
    print("Data added successfully!\n")

# Function to delete data
def delete_data():
    if not records:
        print("No data available to delete.\n")
        return

    print("Select a data to delete:")
    for i, record in enumerate(records):
        print(f"{i + 1}. Game: {record['game']}, Year: {record['year']}, Sports: {record['sports']}, Event: {record['event']}, Athlete: {record['athlete']}, Country: {record['country']}, Placement: {record['placement']}, Medal: {record['medal']}")

    choice = int(input("Enter the number of the data to delete: "))
    
    if 1 <= choice <= len(records):
        records.pop(choice - 1)
        print("Data deleted successfully!\n")
    else:
        print("Invalid choice. Please try again.\n")

# Function to show all the data available in the dictionary
def view_all_records():
    if not records:
        print("No records available.\n")
    else:
        for i, record in enumerate(records):
            print(f"{i + 1}. Game: {record['game']}, Year: {record['year']}, Sports: {record['sports']}, Event: {record['event']}, Athlete: {record['athlete']}, Country: {record['country']}, Placement: {record['placement']}, Medal: {record['medal']}")
        print()

# Function to view last 5 years' winners
def view_last_five_years_winners():
    game = input("Enter the game to view last 5 years' winners: ")
    current_year = datetime.datetime.now().year

    # Filter records safely
    relevant_records = []
    for record in records:
        if 'game' in record and 'year' in record:
            if record['game'].lower() == game.lower() and record['year'] >= current_year - 5*4:
                relevant_records.append(record)
    
    if not relevant_records:
        print(f"No records found for the game '{game}' in the last 5 years.\n")
    else:
        for i, record in enumerate(relevant_records):
            print(f"{i + 1}. Game: {record['game']}, Year: {record['year']}, Sports: {record['sports']}, Event: {record['event']}, Athlete: {record['athlete']}, Country: {record['country']}, Placement: {record['placement']}, Medal: {record['medal']}")
        print()

def main_menu():
    while True:
        print("Olympic Records Management System")
        print("1. Add a New Record")
        print("2. Delete a Record")
        print("3. View All Records")
        print("4. View last 5 years' winners in the given game")
        print("5. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            add_data()
        elif choice == '2':
            delete_data()
        elif choice == '3':
            view_all_records()
        elif choice == '4':
            view_last_five_years_winners()
        elif choice == '5':
            print("We are glad to help you with Data Manipulation!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main_menu()
