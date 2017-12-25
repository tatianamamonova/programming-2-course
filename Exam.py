import flask
import json
import re
import os
import urllib

from flask import Flask
from flask import render_template
from flask import request

def create_dictionary():
	dictionary = {}
	for page in os.listdir('thai_pages'):
		f = open('thai_pages'+os.sep+page,'r',encoding='utf-8')
		r = f.read()
		thai_words = []
		for thai in re.findall(r'<td .*?class=th><a.*?>(.*?)</a>',r,flags=re.DOTALL):
			thai_words.append(re.sub(r'<.*?/>','',re.sub(r'<.*?>(.*?)</.*?>','\g<1>',thai)))
		translations = []
		for translation in re.findall(r'<td .*?class=th>.*?<td class=pos>.*?<td>(.*?)</td>',r,flags=re.DOTALL):
			translations.append(re.sub(r'<.*?/>','',re.sub(r'<.*?>(.*?)</.*?>','\g<1>',translation)))
		for i in range(len(thai_words)):
			dictionary[thai_words[i]] = translations[i]
		f.close()
	return dictionary

def create_json(dictionary):
	f = open('1.json','w',encoding='utf-8')
	json.dump(dictionary, f, ensure_ascii = False, indent = 4)
	f.close()
	
	thai_words = list(dictionary.keys())
	english_words = []

	for thai_word in thai_words:
		english_words.append(dictionary[thai_word])
	
	english_dictionary = {}
	
	for i in range(len(english_words)):
		if english_words[i] in english_dictionary:
			english_dictionary[english_words[i]].append(thai_words[i])
		else:
			english_dictionary[english_words[i]] = [thai_words[i]]

	f = open('2.json','w',encoding='utf-8')
	json.dump(english_dictionary, f, ensure_ascii = False, indent = 4)
	f.close()

Dict = create_dictionary()
create_json(Dict)

app = Flask(__name__)

@app.route('/')
def dictionary_app():
	text = request.args ['word']
	answer = english_dictionary{}
	return render_template("dictionary.html", req=text, answer=Markup(answer))
if __name__ == "__main__":
    app.run(debug=True)