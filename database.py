import os
import sqlite3
from shutil import copy
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import seaborn

def create_connection(db_file):

	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
	except Error as e:
		print(e)
	finally:
		conn.close()
		
 
if __name__ == '__main__':
	create_connection("db.sqlite")
	conn = sqlite3.connect('hittite.db')
	cur = conn.cursor()
	
	cur.execute("SELECT * FROM wordforms")
	rows = cur.fetchall()

	for row in rows:
		print(row)


Glosses = {'ADJ':'adjective',
'ADV':'adverb',
'AUX':'auxiliary',
'COMP':'complementizer',
'CONJ':'conjunction',
'CONN':'connective',
'DEM':'demonstrative pronoun',
'INDEF':'indefinite pronoun',
'N':'noun',
'NEG':'negative',
'NUM':'cardinal',
'P':'preposition (postposition)',
'PART':'particle',
'POSS':'possessive pronoun',
'PRON':'pronoun',
'PRV':'preverb',
'PTCP':'participle',
'REL':'relative pronoun',
'Q':'question word',
'V':'verb'}

if os.path.isfile('main.db'):
	os.remove('main.db')
	copy('empty/main.db',os.getcwd())

conn = sqlite3.connect('hittite.db')
cur = conn.cursor()
cur.execute("SELECT * FROM wordforms")
rows = cur.fetchall()

data = []
for row in rows:
	data.append(list(row))

conn = sqlite3.connect('main.db')
cur = conn.cursor()
cur.execute("CREATE TABLE words(id INTEGER, Lemma TEXT, Wordform TEXT, Glosses TEXT)")
cur.execute("CREATE TABLE glosses(id INTEGER, Gloss TEXT, Description TEXT)")
cur.execute("CREATE TABLE words_glosses(word_id INTEGER, gloss_id INTEGER)")
conn.commit()

for i in range(len(data)):
	for g in data[i][2].split('.'):
		cur.execute("INSERT INTO words (id, Lemma, Wordform, Glosses) VALUES (?, ?, ?, ?)", [i, data[i][0], data[i][1], g])
conn.commit()

k = sorted(list(Glosses.keys()))
for i in range(len(k)):
	cur.execute("INSERT INTO glosses (id, Gloss, Description) VALUES (?, ?, ?)", [i, k[i], Glosses[k[i]]])
conn.commit()

for i in range(len(data)):
	id = {}
	for l in range(len(k)):
		id[k[l]] = l
	for g in data[i][2].split('.'):
		if g in Glosses:
			cur.execute("INSERT INTO words_glosses (word_id, gloss_id) VALUES (?, ?)", [i, id[g]])
conn.commit()

def draw_pic():
        wordcount = {}
        for row in cur.execute('SELECT * FROM words_glosses'):
            gloss = k[row[1]-1]
            if gloss not in wordcount:
                    wordcount[gloss] = 1
            else:
                wordcount[gloss] +=1
        dots = []
        Y = []
        X = []
        n = 1
        for word in sorted(wordcount):
            dots.append(word)
            Y.append(wordcount[word])
            X.append(n)
            n+=1
        for x, y, d in zip(X, Y, dots):
            plt.scatter(x, y, marker='^', s=100)
            plt.text(x+0.1, y+0.1, d)
        plt.ylabel('Number of glosses')
        plt.show()
draw_pic()
