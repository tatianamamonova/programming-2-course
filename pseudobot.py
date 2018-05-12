import flask
import json
import re
import os
import pymorphy2

from flask import Flask
from flask import render_template
from flask import request

morph = pymorphy2.MorphAnalyzer()

def create_dictionary():
	dictionary = []
	with open ('dlya_progi.txt', 'r', encoding='utf-8') as SPb:
		text = SPb.read()
		for pseudoword in text.split():
			if re.search(r'[а-яёА-ЯЁ]', pseudoword):
				word = pseudoword.lower()
				grammar = morph.parse(word)[0]
				dictionary.append(grammar.normal_form.lower())
	return dictionary

def transform(text):
	pseudowords = text.split()
	outwords = []
	for pseudoword in pseudowords:
		if re.search(r'[а-яёА-ЯЁ]', pseudoword):
			grammar = morph.parse(pseudoword)[0]
			listed = 0
			word = ""
			for lemma in Dictionary:
				gram = ""
				lemmagrams = morph.parse(lemma)
				for lemmagram in lemmagrams:
					if str(grammar.tag) == str(lemmagram.tag):
						gram = lemmagram
						break
				if gram != "":
					for item in re.split(r'[, ]',str(grammar.tag)):
						try:
							gram = gram.inflect({item})
						except:
							pass
					word = gram.word
				if listed == 400:
					break
			if word == "":
				outwords.append(pseudoword)
			else:
				outwords.append(word)
		else:
			outwords.append(pseudoword)
	
	transformed_text = ' '.join(outwords)
	return transformed_text

app = Flask(__name__)
Dictionary = create_dictionary()


@app.route('/')
def dictionary_app():
	if request.args:
		text = request.args['word']
		answer = transform(text)
		return render_template("transformer.html", req=text, answer=Markup(answer))
	return render_template("transformer.html", req="", answer="")
if __name__ == "__main__":
    app.run(debug=True)