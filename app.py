from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load quotes from JSON file
def load_quotes():
    with open('quotes.json', 'r') as file:
        return json.load(file)

# Save quotes to JSON file
def save_quotes(quotes):
    with open('quotes.json', 'w') as file:
        json.dump(quotes, file, indent=4)

# Route to get all quotes
@app.route('/quotes', methods=['GET'])
def get_quotes():
    quotes = load_quotes()
    return jsonify(quotes), 200

# Route to add a new quote
@app.route('/quotes', methods=['POST'])
def add_quote():
    new_quote = request.json
    quotes = load_quotes()
    new_quote['id'] = quotes[-1]['id'] + 1 if quotes else 1
    quotes.append(new_quote)
    save_quotes(quotes)
    return jsonify(new_quote), 201

# Route to search for quotes
@app.route('/quotes/search', methods=['GET'])
def search_quotes():
    author = request.args.get('author')
    text = request.args.get('quote')
    quotes = load_quotes()
    results = [quote for quote in quotes if
               (author.lower() in quote['author'].lower() if author else True) and
               (text.lower() in quote['quote'].lower() if text else True)]
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)
