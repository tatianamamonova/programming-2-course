import flask
import requests
import urllib.request
import json
import re
import os
import pymorphy2
import random

from urllib.parse import quote
from flask import Flask
from flask import render_template
from flask import request

Vowels = ('а','е','ё','и','о','у','ы','э','ю','я')
morph = pymorphy2.MorphAnalyzer()

def pymorphy_to_ruscorpora(tag_string):
	allowed = ('NOUN', 'ADJF', 'ADJS', 'COMP', 'VERB', 'INFN', 'PRTF', 'PRTS', 'GRND', 'NUMR', 'ADVB', 'NPRO', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ', 'anim', 'inan', 'masc', 'femn', 'neut', 'ms-f', 'sing', 'plur', 'Sgtm', 'Pltm', 'Fixd', 'nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct', 'gen1', 'gen2', 'acc2', 'loc1', 'loc2', 'Name', 'Surn', 'Patr', 'perf', 'impf', 'tran', 'intr', '1per', '2per', '3per', 'pres', 'past', 'futr', 'indc', 'impr', 'actv', 'pssv')
	#  'Abbr', 'Dist', 'Init', 'NUMB'
	tag_string = re.sub(' ',',',tag_string)
	tags = re.findall(r'[a-zA-Z0-9\-]+',tag_string)
	for tag in tags:
		if tag not in allowed:
			tag_string=re.sub(tag+',','',tag_string)
			tag_string=re.sub(tag,'',tag_string)
	tag_string = re.sub('NOUN','S',tag_string)
	tag_string = re.sub('ADJF','A,plen',tag_string)
	tag_string = re.sub('ADJS','A,brev',tag_string)
	tag_string = re.sub('COMP','comp',tag_string)
	tag_string = re.sub('VERB','V,plen',tag_string)
	tag_string = re.sub('INFN','V,inf',tag_string)
	tag_string = re.sub('PRTF','partcp,plen',tag_string)
	tag_string = re.sub('PRTS','partcp,brev',tag_string)
	tag_string = re.sub('GRND','ger',tag_string)
	tag_string = re.sub('NUMR','NUM',tag_string)
	tag_string = re.sub('ADVB','ADV',tag_string)
	tag_string = re.sub('NPRO','SPRO',tag_string)
	tag_string = re.sub('PRED','PRAEDIC',tag_string)
	tag_string = re.sub('PREP','PR',tag_string)
	tag_string = re.sub('CONJ','CONJ',tag_string)
	tag_string = re.sub('PRCL','PART',tag_string)
	tag_string = re.sub('INTJ','INTJ',tag_string)
	tag_string = re.sub('anim','anim',tag_string)
	tag_string = re.sub('inan','inan',tag_string)
	tag_string = re.sub('masc','m',tag_string)
	tag_string = re.sub('femn','f',tag_string)
	tag_string = re.sub('neut','n',tag_string)
	tag_string = re.sub('ms-f','m-f',tag_string)
	tag_string = re.sub('sing','sg',tag_string)
	tag_string = re.sub('plur','pl',tag_string)
	tag_string = re.sub('Sgtm','sg',tag_string)
	tag_string = re.sub('Pltm','pl',tag_string)
	tag_string = re.sub('Fixd','0',tag_string)
	tag_string = re.sub('nomn','nom',tag_string)
	tag_string = re.sub('gent','gen',tag_string)
	tag_string = re.sub('datv','dat',tag_string)
	tag_string = re.sub('accs','acc',tag_string)
	tag_string = re.sub('ablt','ins',tag_string)
	tag_string = re.sub('loct','loc',tag_string)
	tag_string = re.sub('voct','voc',tag_string)
	tag_string = re.sub('gen1','gen',tag_string)
	tag_string = re.sub('gen2','gen2',tag_string)
	tag_string = re.sub('acc2','acc2',tag_string)
	tag_string = re.sub('loc1','loc',tag_string)
	tag_string = re.sub('loc2','loc2',tag_string)
	tag_string = re.sub('Abbr','abbr',tag_string)
	tag_string = re.sub('Name','persn',tag_string)
	tag_string = re.sub('Surn','famn',tag_string)
	tag_string = re.sub('Patr','patrn',tag_string)
	tag_string = re.sub('perf','pf',tag_string)
	tag_string = re.sub('impf','ipf',tag_string)
	tag_string = re.sub('tran','tran',tag_string)
	tag_string = re.sub('intr','intf',tag_string)
	tag_string = re.sub('1per','1p',tag_string)
	tag_string = re.sub('2per','2p',tag_string)
	tag_string = re.sub('3per','3p',tag_string)
	tag_string = re.sub('pres','praes',tag_string)
	tag_string = re.sub('past','praet',tag_string)
	tag_string = re.sub('futr','fut',tag_string)
	tag_string = re.sub('indc','indic',tag_string)
	tag_string = re.sub('impr','imper',tag_string)
	tag_string = re.sub('actv','act',tag_string)
	tag_string = re.sub('pssv','pass',tag_string)
	tag_string = re.sub('Dist','distort',tag_string)
	tag_string = re.sub('Init','INIT',tag_string)
	tag_string = re.sub('NUMB','ciph',tag_string)
	return tag_string


def download_page(pageUrl):
    try:
        page = requests.get(pageUrl)
        text = page.text
        return (text)
    except:
        print('Error at', pageUrl)
        return
    # do something with the downloaded text

def count_syllables(word):
	syllables = len(re.findall(r'[аеёиоуыэюя]',word.lower()))
	return syllables

def stressed_syllables(cleaned_text):
	stressed = []
	body = cleaned_text
	if len(body) == 0:
		return [0]
	myurl = "https://ws3.morpher.ru/russian/addstressmarks"
	req = urllib.request.Request(myurl)
	req.add_header('Content-Type', 'text/plain; charset=utf-8')
	dataasbytes = body.encode('utf-8')
	req.add_header('Content-Length', len(dataasbytes))
	while True:
		try:
			response = urllib.request.urlopen(req, dataasbytes)
			res = re.findall(r'<string>(.*?)</string>',response.read().decode('UTF-8'),flags=re.DOTALL)[0].lower()
			break
		except:
			pass
	for word in res.split():
		if len(re.findall(r'[аеёиоуыэюя]',word)) == 1:
			stressed.append(1)
			continue
		sylls = 0
		out = False
		for i in range(len(word)-1):
			if word[i] in Vowels:
				sylls += 1
				if ord(word[i+1]) == 769:
					stressed.append(sylls)
					out = True
					break
		if out:
			continue
		else:
			stressed.append(0)
	return stressed

def get_rhyme(lexeme):
	print('ENTERED')
	lxm = lexeme.lower()
	morphology = morph.parse(lxm)[0]
	base = morphology.normal_form
	stressed_lexeme = stressed_syllables(lxm)[0]
	rc_morpho = pymorphy_to_ruscorpora(str(morphology.tag))
	reversed = base[::-1]
	if count_syllables(base) > 1:
		tail = re.search(r'.*[аеёиоуыэюя].*[аеёиоуыэюя]',reversed).group(0)[::-1]
	elif count_syllables(base) == 1:
		tail = base
	else:
		return lexeme
	least_len = len(re.search(r'.*?[аеёиоуыэюя]',reversed).group(0))
	for i in range(len(tail)-least_len):
		context = tail[i:]
		try:
			pages_tried = 0
			appendix = ""
			while True:
				pageUrl = """http://search1.ruscorpora.ru/search.xml?sort=random&out=normal&dpp=100&spd=100&seed=11060&env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&text=lexgramm&mode=poetic&ext=10&nodia=1&parent1=0&level1=0&lex1=*"""+urllib.parse.quote(context)+"""&gramm1="""+rc_morpho+"""&flags1=rhymed&sem1=&parent2=0&level2=0&min2=1&max2=1&lex2=&gramm2=&flags2=&sem2="""+appendix
				html = download_page(pageUrl)
				possibilities = re.findall(r'<span.*?g-em.*?>(.*?)</span>',html)
				if len(possibilities) == 0:
					break
				for word in possibilities:
					if count_syllables(word) == count_syllables(lxm) and stressed_syllables(word)[0] == stressed_lexeme and word != lxm:
						return word
				pages_tried += 1
				appendix = "&p="+str(pages_tried)
		except:
			pass
	return lexeme



def create_dictionary(json_dict_filename):
	dictionary = {}
	with open ('dlya_progi.txt', 'r', encoding='utf-8') as dp:
		text = dp.read()
		for pseudoword in text.split():
			if re.search(r'[а-яёА-ЯЁ]', pseudoword):
				word = pseudoword.lower()
				try:
					word = re.findall(r'[а-яёА-ЯЁ-]+',word)[0]
					if len(word) < 1:
						continue
				except:
					continue
				grammar_object = morph.parse(word)[0].normalized
				grammar = str(grammar_object.tag)
				if grammar in dictionary:
					dictionary[grammar].append(grammar_object.word)
				else:
					dictionary[grammar] = []
					dictionary[grammar].append(grammar_object.word)
	with open (json_dict_filename, 'w', encoding='utf-8') as json_out:
		json.dump(dictionary, json_out, ensure_ascii = False)

def transform(text):
	allowed = ('NOUN', 'ADJF', 'ADJS', 'COMP', 'VERB', 'INFN', 'PRTF', 'PRTS', 'GRND')
	stressed_text = stressed_syllables(re.sub(r'[^A-Za-zА-ЯЁа-яё\- \n]','',text))
	slices = re.split(r'([а-яёА-ЯЁ]+)',text)
	result = ""
	w = 0
	for i in range(len(slices)):
		cap = False
		up = False
		slice = slices[i]
		if re.search(r'[а-яёА-ЯЁ]', slice) and (i == len(slices) - 1 or i == len(slices) - 2):
			if slice.istitle():
				cap = True
			if slice.isupper():
				up = True
			word = get_rhyme(slice)
			if cap:
				word = word.capitalize()
			if up:
				word = word.upper()
			result += word
		else:
			if re.search(r'[а-яёА-ЯЁ]', slice):
				grammar_object = morph.parse(slice)[0]
				if grammar_object.tag.POS in allowed:
					if slice.istitle():
						cap = True
					if slice.isupper():
						up = True
					slice = slice.lower()
					normalized_grammar_object = grammar_object.normalized
					normalized_grammar = str(normalized_grammar_object.tag)
					word = ""
					if normalized_grammar in Dictionary:
						lemmalist = Dictionary[normalized_grammar]
						random.shuffle(lemmalist)
						for lemma in lemmalist:
							if lemma != normalized_grammar_object.word:
								word = lemma
								gram = morph.parse(lemma)[0]
								for item in re.split(r'[, ]',str(grammar_object.tag)):
									x = gram.inflect({item})
									if x is not None:
										gram = x
								word = gram.word
								if count_syllables(word) == count_syllables(slice) and stressed_syllables(word)[0] == stressed_text[w]:
									if cap:
										word = word.capitalize()
									if up:
										word = word.upper()
									result += word
									break
								else:
									continue
					else:
						result += slice
				else:
					result += slice
				w += 1
			else:
				result += slice
	return result

app = Flask(__name__)

if os.path.isfile('dictionary.json'):
	with open ('dictionary.json','r',encoding='utf-8') as json_dict:
		Dictionary = json.loads(json_dict.read())
else:
	create_dictionary('dictionary.json')
	with open ('dictionary.json','r',encoding='utf-8') as json_dict:
		Dictionary = json.loads(json_dict.read())


@app.route('/')
def dictionary_app():
	if request.args:
		text = request.args['words']
		answer = transform(text)
		return render_template("transformer.html", res=answer)
	return render_template("transformer.html", res="")
if __name__ == "__main__":
    app.run(debug=True)