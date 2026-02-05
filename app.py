from flask import Flask, render_template, request, jsonify
from web3_job_aggregator import Web3JobAggregator
import json
from datetime import datetime
import threading
import uuid

app = Flask(__name__)

# Store search results in memory (dict with search_id as key)
search_cache = {}

def background_search(search_id, keywords):
    """Run search in background thread"""
    try:
        aggregator = Web3JobAggregator()
        jobs = aggregator.search_all(keywords=keywords if keywords else None, max_jobs_per_site=200)
        
        search_cache[search_id] = {
            'status': 'completed',
            'total': len(jobs),
            'jobs': jobs,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        search_cache[search_id] = {
            'status': 'error',
            'error': str(e)
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_jobs():
    """Start async job search"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', [])
        
        # Generate unique search ID
        search_id = str(uuid.uuid4())
        
        # Initialize search status
        search_cache[search_id] = {
            'status': 'searching',
            'progress': 0
        }
        
        # Start background thread
        thread = threading.Thread(target=background_search, args=(search_id, keywords))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'search_id': search_id,
            'message': 'Search started in background'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search/<search_id>', methods=['GET'])
def get_search_results(search_id):
    """Get search results by ID"""
    if search_id not in search_cache:
        return jsonify({
            'success': False,
            'error': 'Search not found'
        }), 404
    
    result = search_cache[search_id]
    
    if result['status'] == 'searching':
        return jsonify({
            'success': True,
            'status': 'searching',
            'message': 'Search in progress...'
        })
    elif result['status'] == 'completed':
        return jsonify({
            'success': True,
            'status': 'completed',
            'total': result['total'],
            'jobs': result['jobs'],
            'timestamp': result['timestamp']
        })
    else:
        return jsonify({
            'success': False,
            'status': 'error',
            'error': result.get('error', 'Unknown error')
        }), 500

@app.route('/api/boards')
def get_boards():
    """Get list of all job boards"""
    aggregator = Web3JobAggregator()
    boards = [
        {'id': k, 'name': v['name'], 'url': v['url']} 
        for k, v in aggregator.job_boards.items()
    ]
    return jsonify({'boards': boards})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
