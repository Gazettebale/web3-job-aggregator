from flask import Flask, render_template, request, jsonify
from job_aggregator import Web3JobsPro
import threading
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'web3-jobs-pro-secret-key-change-in-production'

# In-memory cache
search_cache = {}

translations = {
    'en': {
        'title': 'Web3 Jobs Pro',
        'subtitle': 'Find your next role in crypto & Web3',
        'search': 'Search Jobs',
        'search_all': 'Search All Jobs',
        'searching': 'Searching...',
        'select_keywords': 'Select keywords or search all',
        'or_see_all': 'or see all jobs',
        'jobs_found': 'jobs found',
        'export': 'Export JSON',
        'clear_all': 'Clear All',
        'selected': 'Selected:',
        'company': 'Company',
        'location': 'Location',
        'view_job': 'View Job',
        'no_jobs': 'No jobs found. Try different keywords or search all.',
        'loading': 'Scanning job boards...',
        'ready': 'Ready to find your Web3 job?',
        'click_to_start': 'Select keywords or click "Search All Jobs" to browse everything',
        'footer': 'Aggregating from 90+ companies via API + 15 job boards',
        'sources': 'sources scanned',
        'api_powered': 'API-powered',
        'powered_by': 'Built by',
        'favorites_title': 'My Favorites',
        'confirm_clear_favs': 'Remove all favorites?',
        'no_favorites': 'No favorites to export',
    },
    'fr': {
        'title': 'Web3 Jobs Pro',
        'subtitle': 'Trouve ton prochain job dans la crypto & Web3',
        'search': 'Rechercher',
        'search_all': 'Tous les jobs',
        'searching': 'Recherche en cours...',
        'select_keywords': 'Sélectionne des mots-clés ou cherche tout',
        'or_see_all': 'ou voir tous les jobs',
        'jobs_found': 'jobs trouvés',
        'export': 'Exporter JSON',
        'clear_all': 'Tout effacer',
        'selected': 'Sélectionnés:',
        'company': 'Entreprise',
        'location': 'Localisation',
        'view_job': 'Voir l\'offre',
        'no_jobs': 'Aucun job trouvé. Essaie d\'autres mots-clés ou cherche tout.',
        'loading': 'Scan des sites en cours...',
        'ready': 'Prêt à trouver ton job Web3?',
        'click_to_start': 'Sélectionne des mots-clés ou clique "Tous les jobs"',
        'footer': 'Agrégation de 90+ entreprises via API + 15 job boards',
        'sources': 'sources scannées',
        'api_powered': 'Propulsé par API',
        'powered_by': 'Créé par',
        'favorites_title': 'Mes Favoris',
        'confirm_clear_favs': 'Supprimer tous les favoris ?',
        'no_favorites': 'Aucun favori à exporter',
    }
}


def background_search(search_id, keywords):
    try:
        search_cache[search_id]['status'] = 'searching'
        aggregator = Web3JobsPro()
        jobs = aggregator.search_all(keywords=keywords if keywords else None)
        search_cache[search_id] = {
            'status': 'completed',
            'total': len(jobs),
            'jobs': jobs,
            'sources': aggregator.get_source_stats(),
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        search_cache[search_id] = {
            'status': 'error',
            'error': str(e)
        }


@app.route('/')
def index():
    lang = request.args.get('lang', 'en')
    if lang not in translations:
        lang = 'en'
    return render_template('index.html', t=translations[lang], lang=lang)


@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        keywords = data.get('keywords', [])
        search_id = str(uuid.uuid4())
        search_cache[search_id] = {'status': 'starting'}
        thread = threading.Thread(target=background_search, args=(search_id, keywords))
        thread.daemon = True
        thread.start()
        return jsonify({'success': True, 'search_id': search_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/search/<search_id>')
def get_results(search_id):
    if search_id not in search_cache:
        return jsonify({'success': False, 'error': 'Not found'}), 404
    result = search_cache[search_id]
    if result['status'] == 'completed':
        return jsonify({
            'success': True,
            'status': 'completed',
            'total': result['total'],
            'jobs': result['jobs'],
            'sources': result.get('sources', {}),
            'timestamp': result['timestamp']
        })
    elif result['status'] == 'error':
        return jsonify({
            'success': False,
            'status': 'error',
            'error': result.get('error', 'Unknown error')
        }), 500
    else:
        return jsonify({'success': True, 'status': 'searching'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
