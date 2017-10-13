#!/usr/bin/python3
import psycopg2
import sys


#Dropt alle tabellen, als ze al bestaan, om errors te voorkomen
def drop_tables():
    tables = ['gene', 'protein', 'sites', 'region', 'exon', 'ec_number_protein', 'ec_pathway', 'pathway']
    for name in tables:
        sql = """DROP TABLE IF EXISTS {};""".format(name)
        cursor.execute(sql)
        conn.commit()

#Creëert alle tabellen met daarin de attributen en bijbehorende datatypen
def create_tables():
    sql1 = """
           CREATE TABLE gene (
               id          CHAR(14) NOT NULL UNIQUE,
               name        VARCHAR(100) NOT NULL,
               accession   CHAR(8) NOT NULL UNIQUE,
               n_sequence  VARCHAR(1100) NOT NULL,
               cds_start   INT NOT NULL,
               cds_stop    INT NOT NULL,
               protein_id  CHAR(14) NOT NULL UNIQUE
               );"""

    sql2 = """
                   CREATE TABLE exon (
                       start   INT NOT NULL,
                       id      INT NOT NULL,
                       gene_id CHAR(14) NOT NULL
                       );"""

    sql3 = """
           CREATE TABLE protein (
               id          CHAR(14) NOT NULL,
               name        VARCHAR(100) NOT NULL,
               p_sequence  VARCHAR(2000) NOT NULL,
               ec_number   VARCHAR(16) NOT NULL
               );"""

    sql4 = """
               CREATE TABLE region (
                   protein_id  CHAR(14) NOT NULL,
                   area        INT NOT NULL
                   );"""

    sql5 = """
               CREATE TABLE sites (
                   protein_id  CHAR(14) NOT NULL,
                   sites_order INT NOT NULL
                   );"""

    sql6 = """
                   CREATE TABLE ec_number_protein (
                       protein_id   CHAR(14) NOT NULL,
                       ec_nummer    VARCHAR(16) NOT NULL
                       );"""

    sql7 = """
                   CREATE TABLE ec_pathway (
                       ec_number       VARCHAR(16) NOT NULL,
                       pathway_number  CHAR(8) NOT NULL
                       );"""
    
        # Moet pathway in de tabel PATHWAY geen pahtway_number zijn??
        # We hebben in 2 tabellen 2 keer id gebruikt dat iets anders betekend zullen we er p_id en g_id van maken?
        # In tabel EXON staat gene_id en id maar je gebruikt ook protein_id in bv TABLE ec_number_protein
        # De datatypes van alle id's kloppen nog niet

    sql8 = """
                   CREATE TABLE pathway (
                       pathway     VARCHAR(50) NOT NULL, #als dit pathway_number wordt CHAR(8) van maken graag.
                       reaction    VARCHAR(150) NOT NULL,
                       pathways    VARCHAR(50) NOT NULL
                       );"""

    table_list = [sql1, sql2, sql3, sql4, sql5, sql6, sql7, sql8]
    for item in table_list:
        cursor.execute(item)
        conn.commit()

def set_pk():
    pass

def set_fk():
    pass


if __name__ == "__main__":
    # Define our connection string
    conn_string = "host='localhost' dbname='bpapge' user='shirley' password='shirley'"

    # print the connection string we will use to connect
    print("Connecting to database\n	->%s" % (conn_string))
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print("Connected!\n")
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    drop_tables()
    create_tables()

    conn.close()
