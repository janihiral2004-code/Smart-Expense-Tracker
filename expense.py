import sqlite3
from datetime import datetime

class ExpenseTracker:
    def __init__(self, db_name="expenses.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            date TEXT
        )
        """)
        self.conn.commit()

    def add_expense(self, amount, category, date):
        self.cursor.execute(
            "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
            (amount, category, date)
        )
        self.conn.commit()
        print("✅ Expense added successfully!")

    def monthly_summary(self, month):
        self.cursor.execute("""
        SELECT SUM(amount) FROM expenses
        WHERE strftime('%Y-%m', date) = ?
        """, (month,))
        total = self.cursor.fetchone()[0]
        print(f"\n📅 Total expenses for {month}: ₹{total if total else 0}")

    def category_summary(self):
        self.cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        """)
        data = self.cursor.fetchall()

        print("\n📊 Category-wise Spending:")
        for category, total in data:
            print(f"{category}: ₹{total}")

    def spending_insights(self):
        self.cursor.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
        """)
        result = self.cursor.fetchone()
        if result:
            print(f"\n💡 Highest spending category: {result[0]} (₹{result[1]})")
        else:
            print("\nNo data available.")

    def close(self):
        self.conn.close()


def main():
    tracker = ExpenseTracker()

    while True:
        print("\n--- Smart Expense Tracker ---")
        print("1. Add Expense")
        print("2. Monthly Summary")
        print("3. Category-wise Summary")
        print("4. Spending Insights")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            amount = float(input("Enter amount: "))
            category = input("Enter category (Food, Travel, etc.): ")
            date = input("Enter date (YYYY-MM-DD): ")
            tracker.add_expense(amount, category, date)

        elif choice == "2":
            month = input("Enter month (YYYY-MM): ")
            tracker.monthly_summary(month)

        elif choice == "3":
            tracker.category_summary()

        elif choice == "4":
            tracker.spending_insights()

        elif choice == "5":
            tracker.close()
            print("👋 Exiting... Thank you!")
            break

        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()




# -------- TEMPORARY: VIEW DATABASE DATA --------
import sqlite3

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM expenses")
rows = cursor.fetchall()

print("\n📂 All Expenses in Database:")
for row in rows:
    print(row)

conn.close()
