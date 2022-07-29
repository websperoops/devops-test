from django.db import connection


cursor = connection.cursor()
cursor.execute('SHOW TABLES')
results = []
for row in cursor.fetchall():
    results.append(row)

cmd = "ALTER TABLE %s CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;"

failures = []
for row in results:
    print("Converting table %s" % (row[0]))
    try:
        cursor.execute(cmd % (row[0]))
    except Exception as e:
        print("Failed to convert table %s " % (row[0]))
        failures.append((row[0], str(e)))

print("Failed to convert the following tables:")
for failure in failures:
    print("%20s %s" % failure)