#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_restful import Resource, Api
from flask_migrate import Migrate

from models import db, Hero

import os 

abs_path=os.getcwd()
db_path=f'sqlite:///{abs_path}/db/app.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '🦸🏽‍♂️ Superheroes 🦸'

class HeroesId(Resource):
    
    def get(self, id):
        hero = Hero.query.filter(Hero.id == id).first()
        
        if hero:
            hero_dict = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": []
            }

            for hero_power in hero.hero_power:
                power_dict = {
                    "id": hero_power.power.id,
                    "name": hero_power.power.name,
                    "description": hero_power.power.description
                }
                hero_dict["powers"].append(power_dict)

            return make_response(jsonify(hero_dict), 200)
        else:
            return make_response(jsonify({"error": "Hero not found"}), 404)
        


if __name__ == '__main__':
    app.run(port=5555)