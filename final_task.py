import urllib.request
import re
import os

Vowels = ('а','е','ё','и','о','у','ы','э','ю','я')

def download_page(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode('UTF-8')
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

def get_rhymes(lexeme,morphology):
	base = lexeme.word.lower()
	page = urllib.request.urlopen(pageUrl)
	reversed = base[::-1]
	tail = re.search(r'.*[аеёиоуыэюя].*[аеёиоуыэюя]',reversed).group(0)[::-1]
	least_len = len(re.search(r'.*[аеёиоуыэюя]',reversed).group(0))
	for i in range(len(tail)-least_len):
		context = tail[i:]
		try:
			while True:
				pageUrl = 'http://search1.ruscorpora.ru/search.xml?sort=random&out=normal&dpp=100&spd=100&seed=11060&env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&text=lexgramm&mode=poetic&ext=10&nodia=1&parent1=0&level1=0&lex1='+context'&gramm1='+morphology+'&flags1=rhymed&sem1=&parent2=0&level2=0&min2=1&max2=1&lex2=&gramm2=&flags2=&sem2=&p=1'
				html = download_page(pageUrl)
				for word in re.findall(r'<span.*?g-em.*?>(.*?)</span>',html):
					
		except:
			pass


