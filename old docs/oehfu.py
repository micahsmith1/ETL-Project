from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape
from sqlalchemy import create_engine
import sqlalchemy
