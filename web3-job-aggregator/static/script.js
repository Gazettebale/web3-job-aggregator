let currentJobs = [];

function setKeyword(keyword) {
    document.getElementById('keywords').value = keyword;
    searchJobs();
}

async function searchJobs() {
    const keywords = document.getElementById('keywords').value.trim();
    const keywordArray = keywords ? keywords.split(',').map(k => k.trim()).filter(k => k) : [];
    
    // UI updates
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    document.getElementById('empty').style.display = 'none';
    document.getElementById('searchBtn').disabled = true;
    document.querySelector('.btn-text').style.display = 'none';
    document.querySelector('.btn-loading').style.display = 'inline';
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ keywords: keywordArray })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentJobs = data.jobs;
            displayJobs(data.jobs);
        } else {
            alert('Error: ' + data.error);
            document.getElementById('loading').style.display = 'none';
            document.getElementById('empty').style.display = 'block';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to fetch jobs. Please try again.');
        document.getElementById('loading').style.display = 'none';
        document.getElementById('empty').style.display = 'block';
    } finally {
        document.getElementById('searchBtn').disabled = false;
        document.querySelector('.btn-text').style.display = 'inline';
        document.querySelector('.btn-loading').style.display = 'none';
    }
}

function displayJobs(jobs) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('results').style.display = 'block';
    document.getElementById('jobCount').textContent = jobs.length;
    
    const jobsList = document.getElementById('jobsList');
    jobsList.innerHTML = '';
    
    if (jobs.length === 0) {
        jobsList.innerHTML = '<p style="text-align:center; color: var(--text-dim);">No jobs found. Try different keywords.</p>';
        return;
    }
    
    jobs.forEach(job => {
        const card = createJobCard(job);
        jobsList.appendChild(card);
    });
}

function createJobCard(job) {
    const card = document.createElement('div');
    card.className = 'job-card';
    
    const company = job.company || 'Company not listed';
    const location = job.location || 'Location not specified';
    
    card.innerHTML = `
        <div class="job-header">
            <div>
                <h3 class="job-title">${escapeHtml(job.title)}</h3>
            </div>
            <span class="job-source">${escapeHtml(job.source)}</span>
        </div>
        <div class="job-details">
            <span>🏢 ${escapeHtml(company)}</span>
            <span>📍 ${escapeHtml(location)}</span>
        </div>
        ${job.url ? `<a href="${escapeHtml(job.url)}" target="_blank" rel="noopener noreferrer" class="job-link">View Job →</a>` : ''}
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
        jobs: currentJobs
    }, null, 2);
    
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `web3_jobs_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
}

// Enter key to search
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('keywords').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchJobs();
        }
    });
});
