import csv
import bcrypt
import re
import requests

# Constants
CSV_FILE = "C:/Users/shubh/Desktop/CAP776-python/minor-project2/regno.csv"
MAX_ATTEMPTS = 5
API_KEY = 'cefaf198ac0f4c2ba333ecd5cff3fb90'  # Replace with your actual NewsAPI key

# --- User Class ---
class User:
    def __init__(self):
        self.users_data = self.load_users()

    # Load users from CSV
    def load_users(self):
        users = {}
        try:
            with open(CSV_FILE, mode='r') as file:
                csv_reader = csv.DictReader(file)
                headers = csv_reader.fieldnames  # Get the headers
                if 'email' not in headers or 'hashed_password' not in headers:
                    print("CSV file does not have the required headers. Please check the file format.")
                    return users

                for row in csv_reader:
                    # Store email in lowercase and strip whitespaces to avoid matching issues
                    users[row['email'].strip().lower()] = row
        except FileNotFoundError:
            print("User data file not found. Please ensure 'regno.csv' exists.")
        return users

    # Validate email format
    @staticmethod
    def validate_email(email):
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.match(email_regex, email)

    # Hash a password using bcrypt
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Check if the provided password matches the stored hash
    @staticmethod
    def check_password(stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

    # Register a new user
    def register_user(self, email, password, security_question, security_answer):
        if email in self.users_data:
            print("Email already registered. Please log in.")
            return False

        hashed_password = self.hash_password(password).decode('utf-8')
        hashed_answer = self.hash_password(security_answer).decode('utf-8')

        with open(CSV_FILE, mode='a', newline='') as file:
            fieldnames = ['email', 'hashed_password', 'security_question', 'security_answer']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if file.tell() == 0:
                writer.writeheader()

            writer.writerow({
                'email': email,
                'hashed_password': hashed_password,
                'security_question': security_question,
                'security_answer': hashed_answer
            })

        self.users_data[email] = {
            'email': email,
            'hashed_password': hashed_password,
            'security_question': security_question,
            'security_answer': hashed_answer
        }

        print("Registration successful.")
        return True

    # Login user with email and password check
    def login_user(self, email, password):
        email = email.strip().lower()

        if email not in self.users_data:
            print("Email not found. Please register first.")
            return False

        stored_hashed_password = self.users_data[email]['hashed_password']

        # If the password does not match the stored hashed password
        if not self.check_password(stored_hashed_password, password):
            print("Incorrect password. Please try again.")
            return False

        print("Login successful!")
        return True

    # Password recovery (forgot password)
    def forgot_password(self, email, security_answer, new_password):
        email = email.strip().lower()

        if email not in self.users_data:
            print("Email not found.")
            return False

        stored_security_answer = self.users_data[email]['security_answer']

        # Check if security answer matches
        if not self.check_password(stored_security_answer, security_answer):
            print("Incorrect answer to security question.")
            return False

        hashed_new_password = self.hash_password(new_password).decode('utf-8')
        self.users_data[email]['hashed_password'] = hashed_new_password

        # Update CSV file with the new password
        self.update_csv_file()

        print("Password reset successful!")
        return True

    # Update CSV after password reset
    def update_csv_file(self):
        with open(CSV_FILE, mode='w', newline='') as file:
            fieldnames = ['email', 'hashed_password', 'security_question', 'security_answer']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for email, user_data in self.users_data.items():
                writer.writerow(user_data)


# --- NewsAPI Class ---
class NewsAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    # Fetch top 5 news headlines based on a keyword
    def fetch_news_headlines(self, keyword):
        url = f'https://newsapi.org/v2/everything?q={keyword}&pageSize=5&apiKey={self.api_key}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['articles']:
                    return data['articles'][:5]  # Return top 5 news articles
                else:
                    return "No news articles found for the given keyword."
            else:
                return f"Error: {response.status_code}, Invalid API Key or Network Error"
        except requests.exceptions.ConnectionError:
            return "Network error: Please check your internet connection."


# --- NewsNexusApp Class ---
class NewsNexusApp:
    def __init__(self):
        self.user = User()
        self.news_api = NewsAPI(API_KEY)

    # Run the application with a menu-driven interface
    def run(self):
        while True:
            print("\n--- NewsNexus Menu ---")
            print("1. Register")
            print("2. Login")
            print("3. Forgot Password")
            print("4. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                self.handle_register()
            elif choice == '2':
                if self.handle_login():
                    keyword = input("Enter a keyword or topic for news: ")
                    news = self.news_api.fetch_news_headlines(keyword)
                    self.display_news(news)
            elif choice == '3':
                self.handle_forgot_password()
            elif choice == '4':
                print("Exiting NewsNexus. Goodbye!")
                break
            else:
                print("Invalid option selected. Please try again.")

    # Handle user registration
    def handle_register(self):
        email = input("Enter your email: ")
        if not self.user.validate_email(email):
            print("Invalid email format.")
            return

        password = input("Enter your password: ")
        if len(password) < 8:
            print("Password must be at least 8 characters long.")
            return

        security_question = input("Enter a security question: ")
        security_answer = input("Enter the answer to your security question: ")

        self.user.register_user(email, password, security_question, security_answer)

    # Handle user login
    def handle_login(self):
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        return self.user.login_user(email, password)

    # Handle password recovery
    def handle_forgot_password(self):
        email = input("Enter your email: ")
        security_answer = input("Enter your security answer: ")
        new_password = input("Enter a new password: ")

        self.user.forgot_password(email, security_answer, new_password)

    # Display news headlines
    def display_news(self, news):
        if isinstance(news, list):
            print("\nTop 5 News Headlines:")
            for i, article in enumerate(news, 1):
                print(f"{i}. {article['title']} - {article['source']['name']}")
        else:
            print(news)


# --- Main Program ---
if __name__ == "__main__":
    app = NewsNexusApp()
    app.run()
