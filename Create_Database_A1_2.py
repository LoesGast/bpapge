#!/usr/bin/python
import psycopg2
import sys


def create_tables():
    SQL_Genes = """CREATE TABLE IF NOT EXISTS Genes(
                   Gene_ID          CHAR(14),
                   Gene_Name        VARCHAR(50)     NOT NULL,
                   Nucleotide_Seq   VARCHAR(3000)   NOT NULL,
                   CDS_stop         INT             NOT NULL,
                   CDS_start        INT             NOT NULL,
                   Protein_ID       CHAR(14)        NOT NULL,
                   PRIMARY KEY      (Gene_ID),
                   FOREIGN KEY      (Protein_ID)    REFERENCES Protein(Protein_ID)           
                );
    """

    SQL_Protein = """CREATE TABLE IF NOT EXISTS Protein(
                     Protein_ID         CHAR(14),
                     Protein_Name       VARCHAR(50)     NOT NULL,
                     Protein_Sequence   VARCHAR(3000)   NOT NULL,
                     PRIMARY KEY        (Protein_ID),
                     EC_nummer          VARCHAR(16)
                  );
    """

    SQL_Exon = """CREATE TABLE IF NOT EXISTS Exon(
                  EXON_Start    INT     NOT NULL,
                  EXON_End      INT     NOT NULL,
                  Gene_ID       CHAR(14),
                  FOREIGN KEY   (Gene_ID)   REFERENCES Genes(Gene_ID)
                  );
    """

    SQL_Region = """CREATE TABLE IF NOT EXISTS Region(
                    Area            INT,
                    Protein_ID      CHAR(14),
                    PRIMARY KEY     (Area),
                    FOREIGN KEY     (Protein_ID)    REFERENCES Protein(Protein_ID)
                    );
    """

    SQL_Sites = """CREATE TABLE IF NOT EXISTS Sites(
                   Volgorde         INT,
                   Protein_ID       CHAR(14),
                   PRIMARY KEY      (Volgorde),
                   FOREIGN KEY      (Protein_ID)    REFERENCES Protein(Protein_ID)
                   );
    """

    SQL_Protein_Ec_nummer = """CREATE TABLE IF NOT EXISTS Protein_EC_Nummer(
                            Protein_ID       CHAR(14),
                            EC_nummer        VARCHAR(16),
                            PRIMARY KEY      (Protein_ID, EC_nummer),
                            FOREIGN KEY      (Protein_ID)   REFERENCES  Protein(Protein_ID),
                            FOREIGN KEY      (EC_nummer)    REFERENCES   Ec_Nummer(EC_nummer)
                            );
    """

    SQL_EC_Nummer = """CREATE TABLE IF NOT EXISTS EC_Nummer(
                       EC_nummer        VARCHAR(16),
                       PRIMARY KEY     (EC_nummer)
                       )
    """

    SQL_Pathways = """CREATE TABLE IF NOT EXISTS Pathways(
                      Pathway       VARCHAR(100),
                      PRIMARY KEY   (Pathway)
                      );
    """

    SQL_Ec_nummer_Pathway = """CREATE TABLE IF NOT EXISTS EC_Pathway(
                                EC_nummer       VARCHAR(16),
                                Pathway         VARCHAR(100),
                                PRIMARY KEY     (EC_nummer, Pathway),
                                FOREIGN KEY     (EC_nummer)         REFERENCES  Ec_nummer(EC_nummer),
                                FOREIGN KEY     (Pathway)           REFERENCES  Pathways(Pathway)
                               );
    """

    table_list = [SQL_Genes, SQL_Protein, SQL_Exon, SQL_Region, SQL_Sites, SQL_Protein_Ec_nummer, SQL_EC_Nummer, SQL_Pathways, SQL_Ec_nummer_Pathway]
    for item in table_list:
        cursor.execute(item)
        conn.commit()


def main():
    # Define our connection string
    conn_string = "host='localhost' dbname='a1_tijger_2' user='hanna' password='Hanna'"

    # print the connection string we will use to connect
    print("Connecting to database\n	->%s" % (conn_string))

    # get a connection, if a connect cannot be made an exception will be raised here
    global conn
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    global cursor
    cursor = conn.cursor()
    print("Connected!\n")
    #drop_tables()
    create_tables()

if __name__ == "__main__":
    main()