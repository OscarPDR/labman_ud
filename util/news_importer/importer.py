import os
import sys
import json
import pprint
import traceback
import datetime
import psycopg2 as dbi

try:
    from config import PG_USER, PG_PASSWORD, PG_DBNAME
except:
    print "config.py not found. Add PG_USER, PG_PASSWORD, PG_TABLE in that file"
    traceback.print_exc()
    sys.exit(-1)

try:
    news = json.load(open('news.json'))
except:
    print "Is news.json there?"
    traceback.print_exc()
    sys.exit(-2)

connection = dbi.connect(database=PG_DBNAME, user=PG_USER, password=PG_PASSWORD, host = 'localhost')
cursor = connection.cursor()

cursor.execute("select id, short_name from projects_project")
project_names = {}
for project_id, short_name in cursor.fetchall():
    short_name = short_name.lower().decode('utf-8')
    project_names[u' %s ' % short_name] = project_id
    if '/' in short_name:
        for partial in short_name.split('/'):
            project_names[u' %s ' % partial] = project_id
    if '!' in short_name:
        project_names[u' %s ' % short_name.replace('!', '')] = project_id


cursor.execute("select person_id, nickname from persons_nickname")
nicknames = {}
for person_id, nickname in cursor.fetchall():
    nickname = nickname.lower().decode('utf-8')
    nicknames[nickname] = person_id

cursor.execute("select id, full_name from persons_person")
for person_id, full_name in cursor.fetchall():
    full_name = full_name.lower().decode('utf-8')
    nicknames[full_name] = person_id

news_slugs = []

cursor.execute("select slug from news_news")
for existing_slug, in cursor.fetchall():
    news_slugs.append(existing_slug)

for new_item in news:
    content = new_item['content']
    title   = new_item['title']
    slug    = new_item['slug']
    print slug, news_slugs
    print
    if slug in news_slugs:
        continue
    else:
        news_slugs.append(slug)
    created = datetime.datetime.strptime(new_item['log_created'], '%Y-%m-%d %H:%M:%S')
    modified = datetime.datetime.strptime(new_item['log_modified'], '%Y-%m-%d %H:%M:%S')

    text_altogether = u' ' + title.lower() + u' ' + content.lower()  + u' '

    cursor.execute("insert into news_news(content, title, slug, log_created, log_modified) values(%s, %s, %s, %s, %s, %s)", (content, title, slug, created, modified))
    connection.commit()

    cursor.execute("select id from news_news where title = %s", (title,))
    news_id = cursor.fetchall()[0][0]

    used_projects = []

    for project_name in project_names:
        if project_name in text_altogether:
            # print title, 'related with project', project_name, 'which has id=',project_names[project_name]
            project_id = project_names[project_name]
            if project_id not in used_projects:
                cursor.execute("insert into news_projectrelatedtonews(project_id, news_id, log_created, log_modified) values(%s, %s, %s, %s)", (project_id, news_id, created, modified))
                connection.commit()
                used_projects.append(project_id)

    used_persons = []

    for nickname in nicknames:
        if nickname in text_altogether:
            # print title, 'related with nick', nickname, 'which has id=',nicknames[nickname]
            person_id = nicknames[nickname]
            if person_id not in used_persons:
                cursor.execute("insert into news_personrelatedtonews(person_id, news_id, log_created, log_modified) values(%s, %s, %s, %s)", (person_id, news_id, created, modified))
                connection.commit()
                used_persons.append(person_id)


cursor.close()
connection.close()
