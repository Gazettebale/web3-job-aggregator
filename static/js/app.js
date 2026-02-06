let currentJobs = [];
let selectedKeywords = new Set();
let searchInterval = null;

function toggleKeyword(keyword) {
    if (selectedKeywords.has(keyword)) {
        selectedKeywords.delete(keyword);
    } else {
        selectedKeywords.add(keyword);
    }
    updateSelectedDisplay();
    updateKeywordInput();
}

function updateSelectedDisplay() {
    const container = document.getElementById('selectedKeywords');
    const tagsContainer = document.getElementById('selectedTags');
    
    if (selectedKeywords.size === 0) {
        container.style.display = 'none';
        return;
    }
    
    container.style.display = 'flex';
    tagsContainer.innerHTML = '';
    
    selectedKeywords.forEach(keyword => {
        const tag = document.createElement('span');
        tag.className = 'selected-tag';
        tag.innerHTML = `
            ${keyword}
            <button onclick="removeKeyword('${keyword.replace(/'/g, "\\'")}'); event.stopPropagation();" class="remove-tag">×</button>
        `;
        tagsContainer.appendChild(tag);
    });
    
    document.querySelectorAll('.tag').forEach(btn => {
        const text = btn.textContent.trim();
        if (selectedKeywords.has(text.toLowerCase()) || selectedKeywords.has(text)) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

function updateKeywordInput() {
    const input = document.getElementById('keywords');
    if (selectedKeywords.size > 0) {
        input.value = Array.from(selectedKeywords).join(', ');
    } else {
        input.value = '';
    }
}

function removeKeyword(keyword) {
    selectedKeywords.delete(keyword);
    updateSelectedDisplay();
    updateKeywordInput();
}

function clearKeywords() {
    selectedKeywords.clear();
    updateSelectedDisplay();
    updateKeywordInput();
}

async function searchJobs(searchAll = false) {
    const keywordArray = searchAll ? [] : Array.from(selectedKeywords);
    
    if (!searchAll && keywordArray.length === 0) {
        // Flash the search all button
        const btn = document.getElementById('searchAllBtn');
        btn.classList.add('pulse');
        setTimeout(() => btn.classList.remove('pulse'), 1000);
        return;
    }
    
    // UI updates
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    document.getElementById('empty').style.display = 'none';
    document.getElementById('searchBtn').disabled = true;
    document.getElementById('searchAllBtn').disabled = true;
    document.querySelector('.btn-text').style.display = 'none';
    document.querySelector('.btn-loading').style.display = 'inline';
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keywords: keywordArray })
        });
        
        const data = await response.json();
        
        if (data.success && data.search_id) {
            pollResults(data.search_id);
        } else {
            throw new Error(data.error || 'Failed to start search');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to start search. Please try again.');
        resetUI();
    }
}

function pollResults(searchId) {
    let attempts = 0;
    const maxAttempts = 300; // 5 minutes
    
    const scanMessages = [
        'Scanning Greenhouse API...',
        'Scanning Lever API...',
        'Crawling Web3.career...',
        'Checking CryptoJobsList...',
        'Scanning Remote3...',
        'Checking CryptoJobs.com...',
        'Crawling BeInCrypto...',
        'Almost done...'
    ];
    
    searchInterval = setInterval(async () => {
        attempts++;
        
        const msgIndex = Math.min(Math.floor(attempts / 8), scanMessages.length - 1);
        const dots = '.'.repeat((attempts % 4));
        document.getElementById('loadingText').textContent = 
            `${scanMessages[msgIndex]}${dots} (${attempts}s)`;
        
        try {
            const response = await fetch(`/api/search/${searchId}`);
            const data = await response.json();
            
            if (data.status === 'completed') {
                clearInterval(searchInterval);
                currentJobs = data.jobs;
                displayJobs(data.jobs, data.sources || {});
                resetUI();
            } else if (data.status === 'error') {
                clearInterval(searchInterval);
                alert('Error: ' + (data.error || 'Unknown error'));
                resetUI();
                document.getElementById('empty').style.display = 'block';
            } else if (attempts >= maxAttempts) {
                clearInterval(searchInterval);
                alert('Search timeout. Please try again.');
                resetUI();
                document.getElementById('empty').style.display = 'block';
            }
        } catch (error) {
            if (attempts >= 10) {
                clearInterval(searchInterval);
                alert('Connection error. Please try again.');
                resetUI();
                document.getElementById('empty').style.display = 'block';
            }
        }
    }, 1000);
}

function resetUI() {
    document.getElementById('searchBtn').disabled = false;
    document.getElementById('searchAllBtn').disabled = false;
    document.querySelector('.btn-text').style.display = 'inline';
    document.querySelector('.btn-loading').style.display = 'none';
    document.getElementById('loading').style.display = 'none';
}

function displayJobs(jobs, sources) {
    document.getElementById('results').style.display = 'block';
    document.getElementById('jobCount').textContent = jobs.length;
    
    // Display source stats
    const statsContainer = document.getElementById('sourceStats');
    if (sources && Object.keys(sources).length > 0) {
        const badges = Object.entries(sources)
            .slice(0, 8)
            .map(([name, count]) => {
                const isApi = name.includes('Greenhouse') || name.includes('Lever');
                return `<span class="source-badge ${isApi ? 'api' : ''}">${name}: ${count}</span>`;
            })
            .join('');
        const remaining = Object.keys(sources).length - 8;
        statsContainer.innerHTML = badges + (remaining > 0 ? `<span class="source-badge">+${remaining} more</span>` : '');
    }
    
    const jobsList = document.getElementById('jobsList');
    jobsList.innerHTML = '';
    
    if (jobs.length === 0) {
        jobsList.innerHTML = `<p style="text-align:center; grid-column: 1/-1; color: var(--text-dim); padding: 3rem;">${translations.no_jobs}</p>`;
        return;
    }
    
    jobs.forEach(job => {
        jobsList.appendChild(createJobCard(job));
    });
}

function createJobCard(job) {
    const card = document.createElement('div');
    card.className = 'job-card';
    
    const company = job.company || '';
    const location = job.location || '';
    const isApi = job.source && (job.source.includes('Greenhouse') || job.source.includes('Lever'));
    
    card.innerHTML = `
        <div class="job-header">
            <h3 class="job-title">${escapeHtml(job.title)}</h3>
            <span class="job-source ${isApi ? 'api-source' : ''}">${escapeHtml(job.source)}${isApi ? ' ⚡' : ''}</span>
        </div>
        <div class="job-details">
            ${company ? `<span>🏢 ${escapeHtml(company)}</span>` : ''}
            ${location ? `<span>📍 ${escapeHtml(location)}</span>` : ''}
        </div>
        ${job.url ? `<a href="${escapeHtml(job.url)}" target="_blank" rel="noopener noreferrer" class="job-link">${translations.view_job || 'View Job'} →</a>` : ''}
    `;
    
    return card;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function exportResults() {
    if (currentJobs.length === 0) {
        alert('No jobs to export');
        return;
    }
    
    const dataStr = JSON.stringify({
        total: currentJobs.length,
        timestamp: new Date().toISOString(),
        keywords: Array.from(selectedKeywords),
        jobs: currentJobs
    }, null, 2);
    
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `web3_jobs_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
}

// Keyboard shortcuts
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('keywords').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchJobs(selectedKeywords.size === 0);
        }
    });
});

window.addEventListener('beforeunload', function() {
    if (searchInterval) clearInterval(searchInterval);
});
