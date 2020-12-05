from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape
from sqlalchemy import create_engine
import sqlalchemy

rds_connection_string = "postgres://lptdkrurwitgwv:3c931e0ab2fd366ac76902898dacfe8e0eeeabc5b2b222b12a48cefbc52c3fa5@ec2-34-237-236-32.compute-1.amazonaws.com:5432/d7e1q92pf06r6o"
engine = create_engine(f'postgresql://lptdkrurwitgwv:3c931e0ab2fd366ac76902898dacfe8e0eeeabc5b2b222b12a48cefbc52c3fa5@ec2-34-237-236-32.compute-1.amazonaws.com:5432/d7e1q92pf06r6o')


# Create an instance of Flask
app = Flask(__name__)

# Route to render index.html template using 
@app.route("/")
def welcome():
    return ("Home")

@app.route("/quotes")
def quotes():
    engine.execute("select quote_text from quotes")
    return "you found us"