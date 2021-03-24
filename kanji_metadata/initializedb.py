import sqlite3
import sys

def printjp(string):
    out = string + '\n'
    sys.stdout.buffer.write(out.encode('utf8'))

con = sqlite3.connect('kanji.db')

def initialize_tables():
    init_tables = [
    """
        DROP TABLE IF EXISTS Kanji;
    """,
    """
        DROP TABLE IF EXISTS Radicals;
    """,
    """
        DROP TABLE IF EXISTS Krad;
    """,
    """
        CREATE TABLE Kanji (
            KANJI CHAR(1) PRIMARY KEY
        );
    """,
    """
        CREATE TABLE Radicals (
            RADICAL CHAR(1) PRIMARY KEY
        );   
    """,
    """
        CREATE TABLE Krad (
            KANJI CHAR(1),
            RADICAL CHAR(1),
            FOREIGN KEY(KANJI) REFERENCES Kanji(KANJI),
            FOREIGN KEY(RADICAL) REFERENCES Radicals(RADICAL),
            UNIQUE(KANJI, RADICAL)
        );
    """,
            ]

    for statement in init_tables:
        con.execute(statement)
    print("Tables should have initialized successfully")

def parse_krad(krad):
    with open(krad, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            # empty or comment line
            if line == '' or line[0] == '#':
                continue 
            kanji, radicals = line.split(':')
            kanji = kanji.strip()
            radicals = radicals.split()
            try:
                con.execute("INSERT INTO Kanji VALUES ('%s')" % kanji)
            except:
                printjp("Failed to insert kanji %s" % kanji)

            for rad in radicals:
                try:
                    con.execute("INSERT INTO Radical VALUES ('%s')" % rad)
                except:
                    printjp("Failed to insert radical %s" % rad)
            # it's possible that radical insertion may fail, as we may be inserting dupes. re-loop through
            # to make the relations to kanji

            for rad in radicals:
                try:
                    con.execute("INSERT INTO Krad VALUES ('%s', '%s')" % (kanji, rad))
                except:
                    printjp("Failed to create relation on %s and %s" % (kanji, rad))


if __name__ == "__main__":
    initialize_tables()
    parse_krad('kradfile')
    con.commit()
    con.close()


