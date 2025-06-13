from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes by default

@app.route('/outline', methods=['GET'])
def wikipedia_outline():
    country = request.args.get('country')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    if not country:
        return jsonify({'error': 'Country parameter is required'}), 400

    formatted_country = country.replace(' ', '_')
    wiki_url = f'https://en.wikipedia.org/wiki/{formatted_country}'

    try:
        resp = requests.get(wiki_url, headers=headers)
        if not resp.ok:
            return jsonify({'error': f'Failed to fetch Wikipedia page for {country}'}), 500

        soup = BeautifulSoup(resp.text, 'html.parser')
        headings = soup.select('h1, h2, h3, h4, h5, h6')

        outline_lines = []
        for h in headings:
            level = int(h.name[1])
            for edit_section in h.select('.mw-editsection'):
                edit_section.decompose()
            text = h.get_text(strip=True)
            outline_lines.append('#' * level + ' ' + text)

        outline = '\n'.join(outline_lines)

        return Response(outline, mimetype='text/plain; charset=utf-8')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
