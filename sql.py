import psycopg2

connection = psycopg2.connect(user="postgres", password="Plofkip17", host="localhost", database="StationsZuill", port="5432")

c = connection.cursor()

query = "CREATE TABLE berichten (berichtnummer integer, bericht varchar(255))"

c.execute(query)

connection.commit()
c.close()
connection.close()