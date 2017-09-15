### python3.5

import psycopg2

# Connect to an existing database
# try:
conn = psycopg2.connect("dbname=bpapge user=nils")
# except psycopg2.OperationalError:
#     print('error no database found')
#     exit()

# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute("create table mRNA("
            "id_seq VARCHAR ,"
            "sequentie VARCHAR, "
            "PRIMARY KEY (id_seq)" 
            ");")
cur.execute("create table genen("
            "Id_gene VARCHAR, "
            "naam VARCHAR, "
            "sequentie VARCHAR, "
            "PRIMARY KEY (Id_gene)"
            ");")
cur.execute("create table mRNA_genen("
            "id_seq VARCHAR REFERENCES mRNA, "
            "id_gene VARCHAR REFERENCES genen, "
            "PRIMARY KEY(id_seq, id_gene) "
            ");")
with open('bpapge_seq_a1.txt', 'r') as seq:
    data = seq.read().strip().split('\n')
    for i in range(0, len(data), 2):
        #print(data[i], data[i+1])
        cur.execute("insert into mRNA (id_seq, sequentie) VALUES (%s, %s)", [data[i], data[i+1]])
#cur.execute("select * from mRNA;")
for line in cur.fetchall():
    print(line[0], line[1])
#cur.execute("insert into test (num) VALUES (%s)", [50])
#cur.execute('\d')
cur.execute("drop table mRNA CASCADE ")
cur.execute("drop table genen CASCADE ")
cur.execute("drop table mRNA_genen ")




# Execute a command: this creates a new table
#cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
#cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", [100, "abc'def"])

# Query the database and obtain data as Python objects
# cur.execute("SELECT * FROM test;")
# print(cur.fetchone())

# Make the changes to the database persistent
# conn.commit()

# Close communication with the database
conn.commit()
cur.close()
conn.close()

print('Connection closed')