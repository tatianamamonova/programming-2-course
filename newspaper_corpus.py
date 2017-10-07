
import urllib.request
import re
import os
import html
def download_page(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode('UTF-8')
        return (text)
    except:
        print('Error at', pageUrl)
        return
    # do something with the downloaded text

commonUrl = 'https://vecherka.su/articles/news/'
for i in range(128500, 129972):
    pageUrl = commonUrl + str(i) + '/'
    try:
        text = download_page(pageUrl)
    except:
        print("Error at",pageUrl)
        continue
    regPostDate = re.compile('<div class="date">(.*?)</div>', flags=re.DOTALL)
    try:
        classdate = regPostDate.search(text).group(1)
    except:
        continue
    classdate = re.sub(r'\r\n', '', classdate)
    classdate = re.sub(r'\r', '', classdate)
    classdate = re.sub(r'\n', '', classdate)
    classdate = re.sub(r'\t', '', classdate)
    date = classdate.split()[0]
    try:
        month = date.split('.')[1]
        if month[0] == "0":
            month = month[1]
        year = date.split('.')[2]
    except:
        continue

    if not os.path.exists('plain'):
        os.mkdir('plain')
    if not os.path.exists('mystem-xml'):
        os.mkdir('mystem-xml')
    if not os.path.exists('mystem-plain'):
        os.mkdir('mystem-plain')

    if not os.path.exists(os.path.join('plain',year)):
        os.mkdir(os.path.join('plain',year))
    if not os.path.exists(os.path.join('plain',year,month)):
        os.mkdir(os.path.join('plain',year,month))

    f = open('metadata.csv', 'a', encoding='utf-8')
    path = os.path.join('plain',year,month,str(i)+'.txt')
    f.write(path+'\t')
    regPostAuthor = re.compile('<span class="link">(.*?)</span>', flags=re.DOTALL)
    author = ""
    try:
        a = regPostAuthor.search(text).group(1)
        regTag = re.compile('<.*?>', re.DOTALL)
        regSpace = re.compile('\s{2,}', re.DOTALL)
        author = regSpace.sub("", a)
        author = regTag.sub("", author)
    except:
        pass
    f.write(author+'\t')
    sex = ""
    f.write(sex + '\t')
    birthday = ""
    f.write(birthday + '\t')
    regPostTitle = re.compile('<h1>(.*?)</h1>', flags=re.DOTALL)
    t = regPostTitle.search(text).group(1)
    regTag = re.compile('<.*?>', re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    title = regSpace.sub("", t)
    title = regTag.sub("", title)
    regPostTheme = re.compile('<a href="/articles/news/" title="Новости">(.*?)</a>', flags=re.DOTALL)
    f.write(title + '\t')
    f.write(date + '\t')
    sphere = ""
    f.write(sphere + '\t')
    genre_fi = ""
    f.write(genre_fi+ '\t')
    type = ""
    f.write(type + '\t')
    theme = ""
    theme = regPostTheme.search(text).group(1)
    regTag = re.compile('<.*?>', re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    theme = regSpace.sub("", theme)
    theme = regTag.sub("", theme)
    f.write(theme+'\n')
    chronotope = ""
    f.write(chronotope + '\t')
    style = "нейтральный"
    f.write(style + '\t')
    audience_age = "н-возраст"
    f.write(audience_age + '\t')
    audience_level = "н-уровень"
    f.write(audience_level + '\t')
    audience_size = "городская"
    f.write(audience_size+ '\t')
    url=pageUrl
    f.write(url+'\n')
    publication = "Вечерний Челябинск"
    f.write(publication + '\t')
    publisher = ""
    f.write(publisher + '\t')
    f.write(year+'\t')
    medium = "газета"
    f.write(medium + '\t')
    country = "Россия"
    f.write(country + '\t')
    region = "Челябинская область"
    f.write(region + '\t')
    language = "ru"
    f.write(language + '\t')
    f = open('temporary.txt',"w",encoding="utf-8")
    regPostText = re.compile('<div class="detail-text">(.*?)</div>', flags=re.DOTALL)
    text = regPostText.search(text).group(1)
    regTag = re.compile('<.*?>', re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    text = regSpace.sub("", text)
    text = re.sub("</p>.*?<p>",r'\n',text)
    text = re.sub("<br>",r'\n',text)
    text = regTag.sub("", text)
    text = html.unescape(text)
    f.write(text)
    f = open(os.path.join('plain',year,month,str(i)+'.txt'),"w",encoding="utf-8")
    f.write('@au '+author+'\n')
    f.write('@ti ' + title + '\n')
    f.write('@da ' + date + '\n')
    f.write('@topic ' + theme + '\n')
    f.write('@url ' + url + '\n')
    f.write(text)

    if not os.path.exists(os.path.join('mystem-xml',year)):
        os.mkdir(os.path.join('mystem-xml',year))
    if not os.path.exists(os.path.join('mystem-xml',year,month)):
        os.mkdir(os.path.join('mystem-xml',year,month))
    os.system("C:\mystem.exe -cid --format xml temporary.txt "+os.path.join('mystem-xml',year,month,str(i)+'.xml'))

    if not os.path.exists(os.path.join('mystem-plain',year)):
        os.mkdir(os.path.join('mystem-plain',year))
    if not os.path.exists(os.path.join('mystem-plain',year,month)):
        os.mkdir(os.path.join('mystem-plain',year,month))
    os.system("C:\mystem.exe -cid temporary.txt "+os.path.join('mystem-plain',year,month,str(i)+'.txt'))

    os.remove('temporary.txt')