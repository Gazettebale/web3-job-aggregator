from flask import Flask, render_template, request, jsonify
from web3_job_aggregator import Web3JobAggregator
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_jobs():
    """API endpoint to search jobs"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', [])
        
        # Create aggregator and search with MORE results per site
        aggregator = Web3JobAggregator()
        # Increase max_jobs_per_site to get WAY more results
        jobs = aggregator.search_all(keywords=keywords if keywords else None, max_jobs_per_site=100)
        
        return jsonify({
            'success': True,
            'total': len(jobs),
            'jobs': jobs,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
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
