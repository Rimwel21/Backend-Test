import sqlite3

# eto pang delete ng specific
conn = sqlite3.connect("database/app.db")
cursor = conn.cursor()

user_id = 11

cursor.execute("DELETE FROM accounts WHERE id = ?", (user_id,))

conn.commit()
conn.close()

print("User deleted successfully")


# eto pang check kung anong mga columns meron sa table
# conn = sqlite3.connect("database/app.db")
# cursor = conn.cursor()

# cursor.execute("SELECT * FROM accounts;")
# print(cursor.fetchall())

# conn.close()