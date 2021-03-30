import sqlite3
import sqlalchemy
from sqlalchemy import text
import sys
import atexit
from bs4 import BeautifulSoup
from lxml import etree
from io import BytesIO

def printjp(string):
    out = string + '\n'
    sys.stdout.buffer.write(out.encode('utf8'))

# con = sqlite3.connect('wnjpn.db')
HOST = 'localhost'
TABLE = 'japanese'
PASS = 'password'
PORT = '5432'
LANG = 'postgresql'
USER = 'postgres'
DATABASE = '%s://%s:%s@%s:%s/%s' % (LANG, USER, PASS, HOST, PORT, TABLE)
try:
    engine = sqlalchemy.create_engine(DATABASE)
    con = engine.connect()
except Exception as e:
    print("Could not establish a connection to the database")
    print(e)
    exit()

def exit_handler():
    con.close()
    print("closing the connection...")
atexit.register(exit_handler)


print("Type commands() for help")
def commands():
    print("commands()")
    print("initialize_tables()")
    print("parse_krad(<filename>)")

def initialize_tables():
    init_tables = [
    """
        DROP TABLE IF EXISTS kanji;
    """,
    """
        DROP TABLE IF EXISTS radical;
    """,
    """
        DROP TABLE IF EXISTS krad;
    """,
    """
        CREATE TABLE kanji (
            kanji CHAR(1) PRIMARY KEY,
            strokes INTEGER,
            frequency INTEGER
        );
    """,
    """
        CREATE TABLE radical (
            radical CHAR(1) PRIMARY KEY,
            strokes INTEGER
        );   
    """,
    """
        CREATE TABLE krad (
            kanji CHAR(1),
            radical CHAR(1),
            CONSTRAINT "fk_kanji" FOREIGN KEY(kanji) REFERENCES kanji(kanji),
            CONSTRAINT "fk_rad" FOREIGN KEY(radical) REFERENCES radical(radical),
            CONSTRAINT "krad_pair" UNIQUE(kanji, radical)
        );
    """,
            ]

    for statement in init_tables:
        con.execute(statement)
    print("Tables should have initialized successfully", flush=True)

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
                    con.execute("INSERT INTO radical VALUES ('%s')" % rad)
                except:
                    printjp("Failed to insert radical %s" % rad)
            # it's possible that radical insertion may fail, as we may be inserting dupes. re-loop through
            # to make the relations to kanji

            for rad in radicals:
                try:
                    con.execute("INSERT INTO Krad VALUES ('%s', '%s')" % (kanji, rad))
                except:
                    printjp("Failed to create relation on %s and %s" % (kanji, rad))

def parse_radk(radk):
    with open(radk, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        cur = None
        for line in lines:
            line = line.strip()
            # empty or comment line
            if line == '' or line[0] == '#':
                continue
            data = line.split()
            if data[0] == '$':
                cur = data[1] # New radical found. Update current
                try:
                    # insert radical
                    con.execute(text("INSERT INTO radical VALUES(:rad, :strokes)"), rad=cur, strokes=int(data[2]))
                except Exception as e:
                    printjp("Failed to insert radical %s" % cur)
            else:
                # we have kanji that belong to a radical
                for char in line:
                    try:
                        con.execute(text("INSERT INTO Krad(kanji, radical) VALUEs(:kanji, :rad)"), kanji=char, rad=cur)
                    except Exception as e:
                        printjp("Failed to create relation on %s and %s" % (char, cur))

                    

#TODO maybe switch to using pure lxml
def parse_kanjidic(kanjidic):
    with open(kanjidic, mode='rb') as f:
        tree = etree.iterparse(f)
        print("iterparse created", flush=True)
        for action, elm in tree:
            if elm.tag == 'character':
                KANJI = elm[0].text # should be the literal
                STROKES = None
                FREQ = None
                for misc in elm.iter('misc'):
                    # kinda annoying, but we don't necessarily know the position of these tags
                    for strokes in elm.iter('stroke_count'): 
                        STROKES = int(strokes.text)
                    for freq in elm.iter('freq'):
                        FREQ = int(freq.text)

                try:
                    con.execute(text("INSERT INTO kanji(kanji, strokes, frequency) VALUES (:kanji, :strokes, :freq)"), kanji=KANJI, strokes=STROKES, freq=FREQ)
                except Exception as e:
                    print(e, flush=True)
                    printjp("Failed to insert kanji %s" % KANJI)

                elm.clear()

def parse_jmdic(jmdic):
    with open(jmdic, mode='rb') as f:
        tree = etree.iterparse(f)
        print("iterparse created", flush=True)
        for action, elm in tree:
            if elm.tag == 'entry':
                ID = int(elm[0].text)
                # put id in
                try:
                    con.execute(text("INSERT INTO entry (id) VALUES (:ID);"), ID=ID)
                except Exception as e:
                    print(e)
                words = []
                definitions = []
                for k_ele in elm.iter("k_ele"):
                    words.append(k_ele[0].text) # 0th element should always be a way to pronounce

                for r_ele in elm.iter("r_ele"):
                    words.append(r_ele[0].text) # 0th element should always be a way to pronounce

                # put the words in
                for word in words:
                    try:
                        con.execute(text("INSERT INTO word VALUES (:ID, :word);"), ID=ID, word=word)
                    except Exception as e:
                        print(e)

                for sense in elm.iter("sense"):
                    #TODO more info to pick up here
                    for gloss in sense.iter("gloss"):
                        definitions.append(gloss.text)
                # add some definitions
                for definition in definitions:
                    try:
                        con.execute(text("INSERT INTO definition VALUES (:ID, :defn);"), ID=ID, defn=definition)
                    except Exception as e:
                        print(e)

                #print("=====", flush=True)
                #print(ID, flush=True)
                #for word in words:
                #    printjp(word)
                #for defn in definitions:
                #    printjp(defn)
                #print("=====", flush=True)


                elm.clear() # we must do this to save memory. this is a massive file after all







# if __name__ == "__main__":
#     con.execute("SELECT * FROM entry")
#     parse_jmdic("JMdict_e.xml")
