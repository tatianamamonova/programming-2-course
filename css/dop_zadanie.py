from flask import Flask
from flask import request
from flask import render_template
from random import choice
import urllib.request
import re
import os

def get_dic():
	f = open("data.txt","r",encoding="utf-8")
	lines = f.readlines()
	dic = {}
	for line in lines:
		pair = line.split('\t')
		dic[pair[0]] = pair[1]
	return dic

d = get_dic()

def transliterate(arr,dic):
	transliterated_list = []
	
	f = open("temporary.txt","w",encoding="utf-8")
	for word in arr:
		f.write(word+'\n')
	f.close()
	command = "C:\mystem.exe -idn "+os.getcwd()+"/temporary.txt "+os.getcwd()+"/grammar.txt"
	print(command)
	os.system(command)
	f = open("grammar.txt","r",encoding="utf-8")
	grammar = f.readlines()
	f.close()
	command = "C:\mystem.exe -ln "+os.getcwd()+"/temporary.txt "+os.getcwd()+"/lemmas.txt"
	print(command)
	os.system(command)
	f = open("lemmas.txt","r",encoding="utf-8")
	lemmas = f.readlines()
	for i in range(len(lemmas)):
		lemmas[i] = re.sub(r'[{}]','',lemmas[i])
	f.close()
	
	for i in range(len(arr)):
		old_word = ''
		base = ''
		ending = ''
		newletter = False
		for l in range(len(arr[i])):
			if l >= len(lemmas[i]) or newletter:
				ending += arr[i][l]
			elif arr[i][l] == lemmas[i][l]:
				base += arr[i][l]
			else:
				ending += arr[i][l]
				newletter = True
		
		if lemmas[i] in dic:
			base = dic[lemmas[i]][:len(base)]
		
		if 'S' in grammar[i] and ('дат' in grammar[i] or 'пр' in grammar[i] or 'местн' in grammar[i]):
			ending = re.sub('е','ѣ',ending)
			if ending == '' and base[-1] == 'е':
				base = base[:-1]+'ѣ'
		
		old_word = base+ending
		
		if i>0 and i<len(arr)-1:
			if 'A' in grammar[i] and (('жен' in grammar[i] and 'жен' in grammar[i-1] and 'S' in grammar[i-1]) or ('жен' in grammar[i] and 'жен' in grammar[i+1] and 'S' in grammar[i+1]) or ('сред' in grammar[i] and 'сред' in grammar[i-1] and 'S' in grammar[i-1]) or ('сред' in grammar[i] and 'сред' in grammar[i+1] and 'S' in grammar[i+1])):
				if old_word[-2:] == 'ие':
					old_word = old_word[:-2] + 'iя'
				elif old_word[-2:] == 'ые':
					old_word = old_word[:-2] + 'ыя'
				elif old_word[-4:] == 'иеся':
					old_word = old_word[:-4] + 'iяся'
		elif i>0:
			if 'A' in grammar[i] and (('жен' in grammar[i] and 'жен' in grammar[i+1] and 'S' in grammar[i+1]) or ('сред' in grammar[i] and 'сред' in grammar[i+1] and 'S' in grammar[i+1])):
				if old_word[-2:] == 'ие':
					old_word = old_word[:-2] + 'iя'
				elif old_word[-2:] == 'ые':
					old_word = old_word[:-2] + 'ыя'
				elif old_word[-4:] == 'иеся':
					old_word = old_word[:-4] + 'iяся'
		else:
			if 'A' in grammar[i] and (('жен' in grammar[i] and 'жен' in grammar[i-1] and 'S' in grammar[i-1]) or ('сред' in grammar[i] and 'сред' in grammar[i-1] and 'S' in grammar[i-1])):
				if old_word[-2:] == 'ие':
					old_word = old_word[:-2] + 'iя'
				elif old_word[-2:] == 'ые':
					old_word = old_word[:-2] + 'ыя'
				elif old_word[-4:] == 'иеся':
					old_word = old_word[:-4] + 'iяся'
		
		if old_word[:3] == 'бес':
			old_word = 'бес' + old_word[3:]
		if old_word[:4] == 'чрес':
			old_word = 'чрес' + old_word[4:]
		if old_word[:5] == 'черес':
			old_word = 'черес' + old_word[5:]
		
		if re.search(r'[бвгджзклмнпрстфхцчшщ]$',old_word):
			old_word += 'ъ'
		
		old_word = re.sub(r'и([аеёиоуэюяѣѵ])',r'i\1',old_word)
		
		transliterated_list.append(old_word)
	os.remove('temporary.txt')
	os.remove('grammar.txt')
	os.remove('lemmas.txt')
	return transliterated_list


app = Flask(__name__)

@app.route('/')
def weather():
	req = urllib.request.Request('http://www.bbc.com/weather/785842')
	with urllib.request.urlopen(req) as response:
		html = response.read().decode('utf-8')
	regPostTitle = re.compile('<li class="daily__day-tab .*? first active ".*?</li>', flags=re.DOTALL)
	titles = regPostTitle.findall(html)
	weather_staff = []
	regTag = re.compile('<.*?>', re.DOTALL)
	regSpace = re.compile('\s{2,}', re.DOTALL)
	Temp = re.findall('<span class="units-values temperature-units-values"><span data-unit="c" class="units-value temperature-value temperature-value-unit-c">(.*?)<span class="unit">',titles[0])[0]
	Deg = re.findall('<span class="unit">(.*?)</span></span><span class="unit-types-separator">',titles[0])[0]
	Cond = re.findall('alt="(.*?)"',titles[0])[0]
	if request.args:
		temp_list = []
		temp_list.append(request.args['word'])
		return render_template("t_index.html", word = transliterate(temp_list,d)[0], T = Temp+' '+Deg, Cond = Cond)
	return render_template("t_index.html", word = '', T = Temp+' '+Deg, Cond = Cond)

@app.route('/page')
def page():
	page = 'https://theoryandpractice.ru/'
	req = urllib.request.urlopen(page)
	code = req.read().decode('utf-8')
	mess = re.split(r'([а-яёА-ЯЁ]+)',code)
	russian = []
	for word in mess:
		if re.search(r'[а-яёА-ЯЁ]', word):
			russian.append(word)
	result = transliterate(russian,get_dic())
	return render_template("t_page.html", transliterated = result)

	def translate_text(text):
		li = lemmatize(text)
		data = load_data()
		new = []
		for di in li:
			lemma = di['lemma']
			lemma_word = lemma.split("=")[0]
			if is_rus_word(di['word']):
				slovar = compare_to_slovar(di['word'], lemma_word, data)
				next_word = False
				if not li.index(di) + 1 >= len(li):
					next_word = li[li.index(di) + 1]
				translated = ortho(slovar, di, next_word)
				new.append(translated)
		return " ".join(new)



if __name__ == '__main__':
	app.run(debug=True)
