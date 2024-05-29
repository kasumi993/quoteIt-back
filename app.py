from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define the Quote model
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    creator = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, default=0, nullable=False)

# Initial data to be seeded
initial_quotes = [
  {"author": "Albert Einstein", "content": "Nous aurons le destin que nous aurons mérité.", "creator": "@mira_the_lake", "likes": 100},
  {"author": "Franklin D. Roosevelt", "content": "The only limit to our realization of tomorrow is our doubts of today.", "creator": "@Mike_garden", "likes": 130},
  {"author": "John Lennon", "content": "Life is what happens when you're busy making other plans.", "creator": "@Mike_garden", "likes": 14},
  {"author": "Alan Kay", "content": "The best way to predict the future is to invent it.", "creator": "@pompom", "likes": 23},
  {"author": "Winston Churchill", "content": "Success is not final, failure is not fatal: It is the courage to continue that counts.", "creator": "@pompom", "likes": 76},
  {"author": "Confucius", "content": "It does not matter how slowly you go as long as you do not stop.", "creator": "@minie_mouse", "likes": 456},
  {"author": "Confucius", "content": "Our greatest glory is not in never falling, but in rising every time we fall.", "creator": "@Mike_garden", "likes": 67},
  {"author": "Abraham Lincoln", "content": "In the end, it's not the years in your life that count. It's the life in your years.", "creator": "@Mike_garden", "likes": 87},
  {"author": "Dalai Lama", "content": "The purpose of our lives is to be happy.", "creator": "@Mike_garden", "likes": 34},
  {"author": "Confucius", "content": "Life is really simple, but we insist on making it complicated.", "creator": "@Mike_garden", "likes": 7},
  {"author": "Jonathan Swift", "content": "May you live all the days of your life.", "creator": "@Mike_garden", "likes": 3},
  {"author": "Stephen King", "content": "Get busy living or get busy dying.", "creator": "@Mike_garden", "likes": 0},
  {"author": "Brian Tracy", "content": "You have within you right now, everything you need to deal with whatever the world can throw at you.", "creator": "@Mike_garden", "likes": 0},
  {"author": "Theodore Roosevelt", "content": "Believe you can and you're halfway there.", "creator": "@Mike_garden", "likes": 43},
  {"author": "William James", "content": "Act as if what you do makes a difference. It does.", "creator": "@Mike_garden", "likes": 0},
  {"author": "Henry David Thoreau", "content": "Success usually comes to those who are too busy to be looking for it.", "creator": "@Mike_garden", "likes": 0},
  {"author": "Sam Levenson", "content": "Don't watch the clock; do what it does. Keep going.", "creator": "@Mike_garden", "likes": 12},
  {"author": "Walt Whitman", "content": "Keep your face always toward the sunshine—and shadows will fall behind you.", "creator": "@Mike_garden", "likes": 0},
  {"author": "Ralph Waldo Emerson", "content": "What lies behind us and what lies before us are tiny matters compared to what lies within us.", "creator": "@Mike_garden", "likes": 0},
  {"author": "Tony Robbins", "content": "The only impossible journey is the one you never begin.", "creator": "@Mike_garden", "likes": 1},
  {"author": "Charles Kingsleigh (Alice in Wonderland)", "content": "The only way to achieve the impossible is to believe it is possible.", "creator": "@Mike_garden", "likes": 0}
]

# Function to seed the database
def seed_database():
    for quote_data in initial_quotes:
        quote = Quote(**quote_data)
        db.session.add(quote)
    db.session.commit()

# Create the database and the tables, and seed the data
with app.app_context():
    db.create_all()
    seed_database()

@app.route('/quotes', methods=['GET'])
def get_quotes():
    search_query = request.args.get('search')
    if search_query and search_query != 'null' and search_query != '':
        search_query_lower = search_query.lower()
        filtered_quotes = Quote.query.filter(
            (Quote.content.ilike(f'%{search_query_lower}%')) |
            (Quote.author.ilike(f'%{search_query_lower}%'))
        ).all()
    else:
        filtered_quotes = Quote.query.all()

    quotes = [{
        "id": quote.id,
        "author": quote.author,
        "content": quote.content,
        "creator": quote.creator,
        'likes': quote.likes
    } for quote in filtered_quotes]
    return jsonify(quotes), 200

@app.route('/quotes', methods=['POST'])
def add_quote():
    new_quote_data = request.json
    new_quote = Quote(author=new_quote_data['author'], content=new_quote_data['content'], likes=0, creator=new_quote_data['creator'])
    db.session.add(new_quote)
    db.session.commit()
    return jsonify({"id": new_quote.id, "author": new_quote.author, "content": new_quote.content, "creator": new_quote.creator, "likes": new_quote.likes}), 201

@app.route('/quotes', methods=['OPTIONS'])
def options_quotes():
    return '', 204

@app.route('/quotes/<int:quote_id>/like', methods=['PATCH'])
def like_quote(quote_id):
    quote = Quote.query.get(quote_id)
    if quote is None:
        return jsonify({"error": "Quote not found"}), 404
    quote.likes += 1
    db.session.commit()
    return jsonify({"id": quote.id, "author": quote.author, "content": quote.content, "likes": quote.likes}), 200


@app.route('/quotes/<int:quote_id>/unlike', methods=['PATCH'])
def unlike_quote(quote_id):
    quote = Quote.query.get(quote_id)
    if quote is None:
        return jsonify({"error": "Quote not found"}), 404
    quote.likes -= 1
    db.session.commit()
    return jsonify({"id": quote.id, "author": quote.author, "content": quote.content, "likes": quote.likes}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
