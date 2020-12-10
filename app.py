from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
from sqlalchemy import create_engine
import sqlalchemy

rds_connection_string = "postgres://lptdkrurwitgwv:3c931e0ab2fd366ac76902898dacfe8e0eeeabc5b2b222b12a48cefbc52c3fa5@ec2-34-237-236-32.compute-1.amazonaws.com:5432/d7e1q92pf06r6o"
engine = create_engine(f'postgresql://lptdkrurwitgwv:3c931e0ab2fd366ac76902898dacfe8e0eeeabc5b2b222b12a48cefbc52c3fa5@ec2-34-237-236-32.compute-1.amazonaws.com:5432/d7e1q92pf06r6o')

# Create an instance of Flask
app = Flask(__name__)

# Route to render index.html template using 
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/quotes<br/>"
        f"/authors<br/>"
        f"/top10tags<br/>"
        f"/tags<br/>"
    )


# Kyle worked in this 
@app.route("/quotes")
def quotes():
    result = {}
    result_set = engine.execute('''select id, author_name, text
    from quotes q inner join author a on q.author_name = a.name
    order by id''')
    total_quotes = result_set.rowcount
    quotes = []
    for row in result_set:
        quote = {}
        quote['text'] = row.text
        quote['author'] = row.author_name
        tags = []
        tags_result = engine.execute(
            f'select tag  from tags where quote_id= {row.id}')
        for tagrow in tags_result:
            tags.append(tagrow.tag)
        quote['tags'] = tags
        quotes.append(quote)
    result['total'] = total_quotes      
    result['quotes'] = quotes
    return jsonify(result)

@app.route("/top10tags")
def top10tags():
    result = []
    tags_result_set = engine.execute('''select tag , count(*) as total from tags
    group by tag
    order by total desc
    limit 10''')
    for row in tags_result_set:
        tag = {}
        tag['tag'] = row.tag
        tag['quote count'] = row.total
        result.append(tag)
    return jsonify(result)

# @app.route("/tags")
# def tags():
#     result = {}
#     details = []
#     tags_result_set = engine.execute('''select tag ,q.text, count(*) as total from tags
#     t inner join quotes q on t.quote_id = q.id
#     group by tag,q.text
#     order by tag''')
#     total_tags = tags_result_set.rowcount
#     for row in tags_result_set:
#         tag = {}
#         tag['tag'] = row.tag
#         tag['quote count'] = row.total
#         details.append(tag)
#     result['count'] = total_tags
#     result['details'] = details
#     return jsonify(result)


# Miyshael 
@app.route("/authors")
def authors():
    results = engine.execute("select name, born, description from author")
    total = 0  
    all_authors = []
    for name, born, description in results:
        total+=1
        authors_dict = {}
        authors_dict["name"] = name
        authors_dict["born"] = born
        authors_dict["description"] = description
        all_authors.append(authors_dict)
    return jsonify(all_authors)

if __name__ == "__main__":
    app.run(debug=True)