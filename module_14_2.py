import sqlite3

connection = sqlite3.connect('not_telegram_2.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

# for i in range(1,11):
#     cursor.execute('INSERT INTO Users (username, email, age, BALANCE) VALUES (?,?,?,?)', (f'User{i}', f'example{i}@gmail.com', i*10, 1000))

# for i in range(1, 11):
#     cursor.execute('UPDATE Users SET balance = ? WHERE id % 2 = ?', (500, 1))

# for i in range(1, 11):
#     cursor.execute('DELETE FROM Users WHERE id % 3 = ?', (1,))

# cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != ?', (60,))
# users = cursor.fetchall()
# for user in users:
#     print(f'Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}')

cursor.execute('DELETE FROM Users WHERE id = ?', (6,))

cursor.execute('SELECT COUNT(*) FROM Users')
total1 = cursor.fetchone()[0]

cursor.execute('SELECT SUM(balance) FROM Users')
total2 = cursor.fetchone()[0]

print(total2/total1)

# cursor.execute('SELECT AVG(balance) FROM Users')
# avg_balance = round(cursor.fetchone()[0], 2)
# print(avg_balance)


connection.commit()
connection.close()