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
    )
# Kyle worked in this 
@app.route("/quotes")
def quotes():
    results = engine.execute("select text, author_name from quotes")
    total = 0  
    all_quotes = []
    for text,author in results:
        total+=1
        quote_dict = {}
        quote_dict["text"] = text
        quote_dict["author"] = author
        all_quotes.append(quote_dict)
    return jsonify(all_quotes)
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