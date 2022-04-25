from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from DBMS import DataBase
import re

app = Flask(__name__)

global DB


validComms = ['mailto', 'tel', 'skype',
              'whatsapp', 'telegram', 'sms']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def search():
    global DB
    Error = ''
    Query = request.form['QueryBox']
    Data = DB.searchContentRepository(Query)
    Results = []
    Count = 1
    for Entry in Data:
        Title = ''
        if len(Entry['pageTitle']) > 0:
            Title = removeTags(RemoveHTMLEntities(
                RemoveEscapeSequences(RemoveControlCharacters((Entry['pageTitle'][0])))))
        Description = ''
        if len(Entry['Description']) >= 10:
            Description = removeTags(RemoveHTMLEntities(
                RemoveEscapeSequences(RemoveControlCharacters((Entry['Description'])))))
        Summary = ''
        if len(Entry['Summary']) >= 10:
            Summary = removeTags(RemoveHTMLEntities(
                RemoveEscapeSequences(RemoveControlCharacters((Entry['Summary'])))))
        LogoURL = ''
        Domain = getDomain(Entry['URL'])
        if Domain is None:
            continue
        favicon = list(filter(lambda x: 'favicon' in x, Entry['MediaURLs']))
        if len(favicon) > 0:
            for icon in favicon:
                if Domain in icon:
                    LogoURL = icon
                    break
        ContactList = []
        for contact in Entry['ContactURLs']:
            if contact.split(':')[0] in validComms and len(contact.split(':')[1]) < 30:
                ContactList.append(
                    {'URL': contact, 'Text': contact.split(':')[-1]})
        MediaList = Entry['MediaURLs'][:12]
        Page = {'Count': Count, 'URL': Entry['URL'],
                'Title': Title, 'Description': Description, 'Summary': Summary, 'Contacts': ContactList, 'Logo': LogoURL, 'Media': MediaList}
        Results.append(Page)
        Count += 1
    Results = splitList(Results, 10)
    if len(Results) > 10:
        Results = Results[:10]
    if len(Results) == 0:
        Error = "No Results Found"
    return render_template('results.html', Results=Results, Query=Query, Error=Error)


def getDomain(url):
    try:
        domain = re.findall(r'(https://.*?)/', url)[0]
        return domain
    except:
        return None


def removeTags(text):
    try:
        for i in range(len(text)):
            try:
                text[i] = re.sub(r'<.*?>', '', text[i])
            except:
                continue
    finally:
        return text


def RemoveEscapeSequences(text):
    try:
        text = text.replace('\\n', '')
        text = re.sub(r'\\', '', text)
    finally:
        return text


def RemoveHTMLEntities(text):
    try:
        text = re.sub(r'&.*?;', '', text)
    finally:
        return text


def RemoveControlCharacters(text):
    try:
        text = re.sub(r'\\x\w{2}', '', text)
    finally:
        return text


def splitList(list, size):
    return [list[i:i + size] for i in range(0, len(list), size)]


DB = DataBase()
app.run(debug=True, port=5000)
