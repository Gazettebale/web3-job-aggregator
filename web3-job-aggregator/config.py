# Configuration for Web3 Job Aggregator

# Keywords to search for (edit this list based on your interests)
DEFAULT_KEYWORDS = [
    'developer',
    'engineer',
    'solidity',
    'rust',
    'smart contract',
    'blockchain',
    'defi',
    'protocol',
    'remote',
    'backend',
    'frontend',
    'full stack',
]

# Job boards configuration
# Set 'enabled': False to skip a job board
JOB_BOARDS = {
    'crypto-careers': {
        'name': 'Crypto Careers',
        'url': 'https://www.crypto-careers.com/',
        'enabled': True
    },
    'web3-career': {
        'name': 'Web3 Career',
        'url': 'https://web3.career/',
        'enabled': True
    },
    'cryptocurrencyjobs': {
        'name': 'Cryptocurrency Jobs',
        'url': 'https://cryptocurrencyjobs.co/',
        'enabled': True
    },
    'cryptojobslist': {
        'name': 'Crypto Jobs List',
        'url': 'https://cryptojobslist.com/',
        'enabled': True
    },
    'beincrypto': {
        'name': 'BeInCrypto Jobs',
        'url': 'https://beincrypto.com/jobs/',
        'enabled': True
    },
    'jobstash': {
        'name': 'JobStash',
        'url': 'https://jobstash.xyz/jobs',
        'enabled': True
    },
    'remote3': {
        'name': 'Remote3',
        'url': 'https://www.remote3.co/',
        'enabled': True
    },
    'midnight': {
        'name': 'Midnight Network',
        'url': 'https://midnight.network/careers',
        'enabled': True
    },
    'dragonfly': {
        'name': 'Dragonfly',
        'url': 'https://jobs.dragonfly.xyz/jobs',
        'enabled': True
    },
    'block': {
        'name': 'Block',
        'url': 'https://block.xyz/careers/jobs',
        'enabled': True
    },
    'solana': {
        'name': 'Solana Jobs',
        'url': 'https://jobs.solana.com/jobs',
        'enabled': True
    },
    'avalanche': {
        'name': 'Avalanche Jobs',
        'url': 'https://jobs.avax.network/jobs',
        'enabled': True
    },
    'ethereum': {
        'name': 'Ethereum Job Board',
        'url': 'https://www.ethereumjobboard.com/jobs',
        'enabled': True
    }
}

# Maximum jobs to fetch per site
MAX_JOBS_PER_SITE = 50

# Delay between requests (seconds) - be respectful!
REQUEST_DELAY = 1

# Output settings
OUTPUT_JSON = True
OUTPUT_MARKDOWN = True
DEFAULT_JSON_FILE = 'web3_jobs.json'
DEFAULT_MD_FILE = 'web3_jobs.md'
