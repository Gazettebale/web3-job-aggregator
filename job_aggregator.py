#!/usr/bin/env python3
"""
Web3 Jobs Pro - Professional job aggregator using real APIs and optimized scraping
Built with love by @_Gazettebale for the Web3 community
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from typing import List, Dict, Optional
import time
from urllib.parse import urljoin, quote
import logging
import concurrent.futures

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Web3JobsPro:
    def __init__(self):
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,application/json;q=0.8,*/*;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        # Source registry
        self.sources = {
            'cryptocurrencyjobs': {'name': 'CryptocurrencyJobs.co', 'type': 'scraping', 'enabled': True},
            'web3career': {'name': 'Web3.career', 'type': 'api/scraping', 'enabled': True},
            'cryptojobslist': {'name': 'CryptoJobsList', 'type': 'scraping', 'enabled': True},
            'remote3': {'name': 'Remote3', 'type': 'scraping', 'enabled': True},
            'cryptojobs_com': {'name': 'CryptoJobs.com', 'type': 'scraping', 'enabled': True},
            'crypto_jobs_io': {'name': 'Crypto.Jobs', 'type': 'scraping', 'enabled': True},
            'beincrypto': {'name': 'BeInCrypto Jobs', 'type': 'scraping', 'enabled': True},
            'jobstash': {'name': 'JobStash', 'type': 'scraping', 'enabled': True},
            'crypto_careers': {'name': 'Crypto-Careers', 'type': 'scraping', 'enabled': True},
            'greenhouse': {'name': 'Greenhouse (Multi-company API)', 'type': 'api', 'enabled': True},
            'lever': {'name': 'Lever (Multi-company API)', 'type': 'api', 'enabled': True},
            'midnight': {'name': 'Midnight Network', 'type': 'scraping', 'enabled': True},
            'dragonfly': {'name': 'Dragonfly', 'type': 'scraping', 'enabled': True},
            'block': {'name': 'Block', 'type': 'scraping', 'enabled': True},
            'solana_jobs': {'name': 'Solana Job Board', 'type': 'scraping', 'enabled': True},
            'avalanche_jobs': {'name': 'Avalanche Job Board', 'type': 'scraping', 'enabled': True},
            'ethereum_jobboard': {'name': 'Ethereum Job Board', 'type': 'scraping', 'enabled': True},
        }

        # Web3.career API key (optional - get yours at web3.career/web3-jobs-api)
        # Set via environment variable or directly here
        import os
        self.web3career_api_key = os.environ.get('WEB3CAREER_API_KEY', '')

        # Greenhouse companies - FREE public JSON API, no auth!
        # Endpoint: boards-api.greenhouse.io/v1/boards/{token}/jobs
        # To add more: find the slug from boards.greenhouse.io/{slug}
        self.greenhouse_companies = [
            # === Tier 1: Major Exchanges & Infra ===
            ('coinbase', 'Coinbase'),
            ('kraken', 'Kraken'),
            ('blockchain', 'Blockchain.com'),
            ('robinhood', 'Robinhood'),
            ('fireblocks', 'Fireblocks'),
            ('chainalysis', 'Chainalysis'),
            ('ledger', 'Ledger'),
            ('bitgo', 'BitGo'),
            ('circle', 'Circle'),
            ('paxos', 'Paxos'),
            ('anchorage', 'Anchorage Digital'),
            ('figment', 'Figment'),
            # === Tier 2: DeFi / Protocols ===
            ('uniswaplabs', 'Uniswap Labs'),
            ('paradigm', 'Paradigm'),
            ('consensys', 'ConsenSys'),
            ('opensea', 'OpenSea'),
            ('dydx', 'dYdX'),
            ('compound-2', 'Compound'),
            ('aaborig', 'Aave'),
            ('arbitrum', 'Arbitrum'),
            ('optimism', 'Optimism'),
            # === Tier 3: L1 / L2 Chains ===
            ('celestiaorg', 'Celestia'),
            ('eigenlabs', 'EigenLayer'),
            ('starkware', 'StarkWare'),
            ('immutablex', 'Immutable'),
            ('sui49', 'Sui / Mysten Labs'),
            ('aptoslabs', 'Aptos Labs'),
            ('zetachain', 'ZetaChain'),
            ('startale', 'Startale (Astar)'),
            # === Tier 4: VCs / Funds ===
            ('galaxydigitalservices', 'Galaxy Digital'),
            ('gauntlet', 'Gauntlet'),
            ('polychaincapital', 'Polychain Capital'),
            ('paradigmxyz', 'Paradigm'),
            ('multicaborig', 'Multicoin Capital'),
            ('panteracapital', 'Pantera Capital'),
            # === Tier 5: Infra / Tools / Other ===
            ('wormholefoundation', 'Wormhole'),
            ('ecoinc', 'Eco Protocol'),
            ('hyphenconnect', 'Hyphen Connect'),
            ('alchemy55', 'Alchemy'),
            ('nethermind', 'Nethermind'),
            ('biconomy', 'Biconomy'),
            ('celo58', 'Celo'),
            ('litprotocol', 'Lit Protocol'),
            ('sprucesystems', 'Spruce (Sign-in with Ethereum)'),
            ('nansen2', 'Nansen'),
            ('messari', 'Messari'),
            ('dune', 'Dune Analytics'),
            ('goldfinch', 'Goldfinch'),
            ('across-protocol', 'Across Protocol'),
            ('raribleinc', 'Rarible'),
            ('yieldprotocol', 'Yield Protocol'),
            ('axelar', 'Axelar'),
            ('layerzero', 'LayerZero'),
            ('hashicorp', 'HashiCorp'),
        ]

        # Lever companies - FREE public JSON API, no auth!
        # Endpoint: api.lever.co/v0/postings/{company}
        # To add more: find the slug from jobs.lever.co/{slug}
        self.lever_companies = [
            # === Major Players ===
            ('crypto', 'Crypto.com'),
            ('binance', 'Binance'),
            ('animocabrands', 'Animoca Brands'),
            ('certik', 'CertiK'),
            # === Protocols & L1/L2 ===
            ('polygon-technology', 'Polygon'),
            ('chainlink', 'Chainlink'),
            ('offchainlabs', 'Offchain Labs (Arbitrum)'),
            ('arbitrumfoundation', 'Arbitrum Foundation'),
            ('ethereumfoundation', 'Ethereum Foundation'),
            ('Solana', 'Solana Foundation'),
            ('aztec', 'Aztec'),
            ('zksync', 'zkSync (Matter Labs)'),
            ('nibiru', 'Nibiru Chain'),
            ('aragon', 'Aragon'),
            # === Infra & Tools ===
            ('alchemy', 'Alchemy'),
            ('quicknode', 'QuickNode'),
            ('thegraph', 'The Graph'),
            ('tenderly', 'Tenderly'),
            ('phantom', 'Phantom'),
            ('MagicLabs', 'Magic'),
            ('WalletConnect', 'WalletConnect'),
            ('worldcoin', 'Worldcoin'),
            # === DeFi / Trading ===
            ('tokenmetrics', 'Token Metrics'),
            ('gauntlet', 'Gauntlet'),
            ('wintermute', 'Wintermute'),
            ('flowtraders', 'Flow Traders'),
            # === Gaming / NFT ===
            ('mythicalgames', 'Mythical Games'),
            ('skymavis', 'Sky Mavis (Axie Infinity)'),
            ('sandbox56', 'The Sandbox'),
            # === Other Web3 ===
            ('filecoin', 'Filecoin Foundation'),
            ('protocol', 'Protocol Labs'),
            ('livepeer', 'Livepeer'),
            ('kadena', 'Kadena'),
            ('lukso', 'LUKSO'),
            ('poap', 'POAP'),
            ('spruce-systems', 'Spruce Systems'),
        ]

    def search_all(self, keywords: Optional[List[str]] = None) -> List[Dict]:
        """Search ALL sources using parallel execution"""
        logger.info("Starting Web3 Jobs Pro - FULL SCAN")
        start_time = time.time()
        all_jobs = []

        fetch_tasks = [
            self._fetch_cryptocurrencyjobs,
            self._fetch_web3career,
            self._fetch_cryptojobslist,
            self._fetch_remote3,
            self._fetch_cryptojobs_com,
            self._fetch_crypto_jobs_io,
            self._fetch_beincrypto,
            self._fetch_jobstash,
            self._fetch_crypto_careers,
            self._fetch_greenhouse_boards,
            self._fetch_lever_boards,
            self._fetch_midnight,
            self._fetch_dragonfly,
            self._fetch_block,
            self._fetch_solana_jobs,
            self._fetch_avalanche_jobs,
            self._fetch_ethereum_jobboard,
        ]

        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            future_to_source = {executor.submit(task): task.__name__ for task in fetch_tasks}
            for future in concurrent.futures.as_completed(future_to_source):
                source_name = future_to_source[future]
                try:
                    jobs = future.result()
                    all_jobs.extend(jobs)
                except Exception as e:
                    logger.error(f"Error in {source_name}: {e}")

        if keywords:
            all_jobs = self._filter_jobs(all_jobs, keywords)

        all_jobs = self._deduplicate(all_jobs)
        self.jobs = all_jobs
        elapsed = time.time() - start_time
        logger.info(f"Found {len(all_jobs)} total jobs in {elapsed:.1f}s")
        return all_jobs

    # ============================================================
    #  GREENHOUSE API - Pure JSON, no scraping!
    # ============================================================

    def _fetch_greenhouse_boards(self) -> List[Dict]:
        jobs = []
        logger.info(f"Fetching from Greenhouse API ({len(self.greenhouse_companies)} companies)...")
        for slug, company_name in self.greenhouse_companies:
            try:
                url = f'https://boards-api.greenhouse.io/v1/boards/{slug}/jobs'
                response = requests.get(url, headers={'Accept': 'application/json'}, timeout=10)
                if response.status_code != 200:
                    continue
                data = response.json()
                for job in data.get('jobs', []):
                    location_name = ''
                    loc = job.get('location')
                    if loc and isinstance(loc, dict):
                        location_name = loc.get('name', '')
                    jobs.append({
                        'title': job.get('title', ''),
                        'company': company_name,
                        'location': location_name,
                        'url': job.get('absolute_url', ''),
                        'source': f'{company_name} (Greenhouse)',
                        'scraped_at': datetime.now().isoformat()
                    })
                time.sleep(0.2)
            except Exception:
                continue
        logger.info(f"Greenhouse API: {len(jobs)} jobs")
        return jobs

    # ============================================================
    #  LEVER API - Pure JSON, no scraping!
    # ============================================================

    def _fetch_lever_boards(self) -> List[Dict]:
        jobs = []
        logger.info(f"Fetching from Lever API ({len(self.lever_companies)} companies)...")
        for slug, company_name in self.lever_companies:
            try:
                url = f'https://api.lever.co/v0/postings/{slug}?mode=json'
                response = requests.get(url, headers={'Accept': 'application/json'}, timeout=10)
                if response.status_code != 200:
                    continue
                postings = response.json()
                if not isinstance(postings, list):
                    continue
                for posting in postings:
                    categories = posting.get('categories', {})
                    location = categories.get('location', '')
                    team = categories.get('team', '')
                    jobs.append({
                        'title': posting.get('text', ''),
                        'company': company_name,
                        'location': location,
                        'url': posting.get('hostedUrl', ''),
                        'source': f'{company_name} (Lever)',
                        'team': team,
                        'scraped_at': datetime.now().isoformat()
                    })
                time.sleep(0.2)
            except Exception:
                continue
        logger.info(f"Lever API: {len(jobs)} jobs")
        return jobs

    # ============================================================
    #  SCRAPING SOURCES
    # ============================================================

    def _safe_scrape(self, url, source_name):
        """Helper: fetch a page and return soup, or None on failure"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                return None
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.debug(f"{source_name} fetch error: {e}")
            return None

    def _extract_jobs_from_soup(self, soup, source_name, base_url, default_company=''):
        """Generic job extraction with multiple strategies"""
        jobs = []
        # Strategy 1: CSS selectors for common job card patterns
        cards = soup.select('[class*="job-card"], [class*="JobCard"], [class*="job-listing"], [class*="job_card"]')

        # Strategy 2: Broader class matching
        if not cards:
            cards = soup.find_all(['div', 'article', 'li', 'section'],
                                 class_=re.compile(r'(?:^|\s|-)(?:job|listing|posting|position|opening|vacancy)(?:\s|-|$|_)', re.I),
                                 limit=200)

        # Strategy 3: Links that look like job postings
        if not cards:
            cards = soup.find_all('a', href=re.compile(r'/jobs?/[a-z0-9]', re.I))

        for card in cards:
            try:
                # Title
                if card.name == 'a':
                    title = card.get_text(strip=True)
                    job_url = card.get('href', '')
                else:
                    title_elem = card.find(['h2', 'h3', 'h4'])
                    if not title_elem:
                        link = card.find('a', href=True)
                        title_elem = link if link else None
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)
                    link_elem = card.find('a', href=True)
                    job_url = link_elem['href'] if link_elem else ''

                if not title or len(title) < 5 or len(title) > 250:
                    continue

                # Skip nav/UI elements
                skip_words = ['login', 'sign up', 'post a job', 'home', 'about', 'contact', 'menu',
                              'newsletter', 'subscribe', 'cookie', 'privacy', 'terms']
                if title.lower().strip() in skip_words or len(title) < 5:
                    continue

                # URL
                if job_url and not job_url.startswith('http'):
                    job_url = base_url.rstrip('/') + '/' + job_url.lstrip('/')

                # Company
                company = default_company
                company_elem = card.find(class_=re.compile(r'company|employer|org', re.I))
                if company_elem:
                    company = company_elem.get_text(strip=True)

                # Location
                location = ''
                loc_elem = card.find(class_=re.compile(r'location|place|loc', re.I))
                if loc_elem:
                    location = loc_elem.get_text(strip=True)

                jobs.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'url': job_url,
                    'source': source_name,
                    'scraped_at': datetime.now().isoformat()
                })
            except Exception:
                continue

        return jobs

    def _fetch_cryptocurrencyjobs(self) -> List[Dict]:
        jobs = []
        try:
            logger.info("Fetching from CryptocurrencyJobs.co...")
            for page in range(1, 4):
                soup = self._safe_scrape(f'https://cryptocurrencyjobs.co/jobs/?page={page}', 'CryptocurrencyJobs')
                if not soup:
                    break
                page_jobs = self._extract_jobs_from_soup(soup, 'CryptocurrencyJobs', 'https://cryptocurrencyjobs.co')
                if not page_jobs:
                    break
                jobs.extend(page_jobs)
                time.sleep(0.5)
            logger.info(f"CryptocurrencyJobs: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error CryptocurrencyJobs: {e}")
        return jobs

    def _fetch_web3career_api(self) -> List[Dict]:
        """Web3.career API (requires API key from web3.career/web3-jobs-api)"""
        jobs = []
        try:
            logger.info("Fetching from Web3.career API...")
            url = f'https://web3.career/api/v1?token={self.web3career_api_key}'
            response = requests.get(url, headers={'Accept': 'application/json'}, timeout=15)
            if response.status_code != 200:
                logger.info("Web3.career API returned non-200, falling back to scraping")
                return []
            data = response.json()
            if isinstance(data, list):
                for item in data:
                    jobs.append({
                        'title': item.get('title', ''),
                        'company': item.get('company', ''),
                        'location': item.get('location', ''),
                        'url': item.get('url', ''),
                        'source': 'Web3.career (API)',
                        'scraped_at': datetime.now().isoformat()
                    })
            logger.info(f"Web3.career API: {len(jobs)} jobs")
        except Exception as e:
            logger.debug(f"Web3.career API error: {e}")
        return jobs

    def _fetch_web3career(self) -> List[Dict]:
        """
        Web3.career - tries API first (if key set), then scraping fallback
        API docs: web3.career/web3-jobs-api
        """
        # Try API first if key is configured
        if self.web3career_api_key:
            api_jobs = self._fetch_web3career_api()
            if api_jobs:
                return api_jobs

        # Fallback to scraping: tr.table_row structure
        jobs = []
        try:
            logger.info("Fetching from Web3.career (scraping)...")
            for page in range(1, 8):
                soup = self._safe_scrape(f'https://web3.career/?page={page}', 'Web3.career')
                if not soup:
                    break
                rows = soup.find_all('tr', class_='table_row')
                if not rows:
                    break
                for row in rows:
                    try:
                        title_elem = row.find('h2')
                        if not title_elem:
                            continue
                        title = title_elem.get_text(strip=True)
                        if not title or len(title) < 3:
                            continue
                        company_elem = row.find('h3')
                        location_elem = row.find('p', class_='job-location-salary')
                        link_elem = row.find('a', href=True)
                        job_url = ''
                        if link_elem:
                            href = link_elem['href']
                            job_url = href if href.startswith('http') else 'https://web3.career' + href
                        jobs.append({
                            'title': title,
                            'company': company_elem.get_text(strip=True) if company_elem else '',
                            'location': location_elem.get_text(strip=True) if location_elem else '',
                            'url': job_url,
                            'source': 'Web3.career',
                            'scraped_at': datetime.now().isoformat()
                        })
                    except Exception:
                        continue
                time.sleep(0.5)
            logger.info(f"Web3.career: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error Web3.career: {e}")
        return jobs

    def _fetch_cryptojobslist(self) -> List[Dict]:
        jobs = []
        try:
            logger.info("Fetching from CryptoJobsList...")
            for page in range(1, 4):
                soup = self._safe_scrape(f'https://cryptojobslist.com/?page={page}', 'CryptoJobsList')
                if not soup:
                    break
                page_jobs = self._extract_jobs_from_soup(soup, 'CryptoJobsList', 'https://cryptojobslist.com')
                if not page_jobs:
                    break
                jobs.extend(page_jobs)
                time.sleep(0.5)
            logger.info(f"CryptoJobsList: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error CryptoJobsList: {e}")
        return jobs

    def _fetch_remote3(self) -> List[Dict]:
        jobs = []
        try:
            logger.info("Fetching from Remote3...")
            soup = self._safe_scrape('https://www.remote3.co/', 'Remote3')
            if soup:
                jobs = self._extract_jobs_from_soup(soup, 'Remote3', 'https://www.remote3.co')
                # Set all as Remote
                for j in jobs:
                    if not j['location']:
                        j['location'] = 'Remote'
            logger.info(f"Remote3: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error Remote3: {e}")
        return jobs

    def _fetch_cryptojobs_com(self) -> List[Dict]:
        jobs = []
        try:
            logger.info("Fetching from CryptoJobs.com...")
            for page in range(1, 4):
                soup = self._safe_scrape(f'https://www.cryptojobs.com/jobs?page={page}', 'CryptoJobs.com')
                if not soup:
                    break
                page_jobs = self._extract_jobs_from_soup(soup, 'CryptoJobs.com', 'https://www.cryptojobs.com')
                if not page_jobs:
                    break
                jobs.extend(page_jobs)
                time.sleep(0.5)
            logger.info(f"CryptoJobs.com: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error CryptoJobs.com: {e}")
        return jobs

    def _fetch_crypto_jobs_io(self) -> List[Dict]:
        jobs = []
        try:
            logger.info("Fetching from Crypto.Jobs...")
            soup = self._safe_scrape('https://www.crypto.jobs/', 'Crypto.Jobs')
            if soup:
                jobs = self._extract_jobs_from_soup(soup, 'Crypto.Jobs', 'https://www.crypto.jobs')
            logger.info(f"Crypto.Jobs: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error Crypto.Jobs: {e}")
        return jobs

    def _fetch_beincrypto(self) -> List[Dict]:
        jobs = []
        try:
            logger.info("Fetching from BeInCrypto Jobs...")
            soup = self._safe_scrape('https://beincrypto.com/jobs/', 'BeInCrypto')
            if soup:
                jobs = self._extract_jobs_from_soup(soup, 'BeInCrypto', 'https://beincrypto.com')
            logger.info(f"BeInCrypto: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error BeInCrypto: {e}")
        return jobs

    def _fetch_jobstash(self) -> List[Dict]:
        jobs = []
        try:
            logger.info("Fetching from JobStash...")
            soup = self._safe_scrape('https://jobstash.xyz/jobs', 'JobStash')
            if soup:
                jobs = self._extract_jobs_from_soup(soup, 'JobStash', 'https://jobstash.xyz')
            logger.info(f"JobStash: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error JobStash: {e}")
        return jobs

    def _fetch_crypto_careers(self) -> List[Dict]:
        jobs = []
        try:
            logger.info("Fetching from Crypto Careers...")
            for page in range(1, 4):
                soup = self._safe_scrape(f'https://www.crypto-careers.com/jobs?page={page}', 'Crypto Careers')
                if not soup:
                    break
                page_jobs = self._extract_jobs_from_soup(soup, 'Crypto Careers', 'https://www.crypto-careers.com')
                if not page_jobs:
                    break
                jobs.extend(page_jobs)
                time.sleep(0.5)
            logger.info(f"Crypto Careers: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error Crypto Careers: {e}")
        return jobs

    def _fetch_midnight(self) -> List[Dict]:
        jobs = []
        try:
            logger.info("Fetching from Midnight Network...")
            soup = self._safe_scrape('https://midnight.network/careers', 'Midnight')
            if soup:
                jobs = self._extract_jobs_from_soup(soup, 'Midnight Network', 'https://midnight.network', 'Midnight Network')
            logger.info(f"Midnight Network: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error Midnight: {e}")
        return jobs

    def _fetch_dragonfly(self) -> List[Dict]:
        jobs = []
        try:
            logger.info("Fetching from Dragonfly...")
            soup = self._safe_scrape('https://jobs.dragonfly.xyz/jobs', 'Dragonfly')
            if soup:
                jobs = self._extract_jobs_from_soup(soup, 'Dragonfly', 'https://jobs.dragonfly.xyz', 'Dragonfly Portfolio')
            logger.info(f"Dragonfly: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error Dragonfly: {e}")
        return jobs

    def _fetch_block(self) -> List[Dict]:
        jobs = []
        try:
            logger.info("Fetching from Block...")
            soup = self._safe_scrape('https://block.xyz/careers', 'Block')
            if soup:
                jobs = self._extract_jobs_from_soup(soup, 'Block', 'https://block.xyz', 'Block (Square/Cash App)')
            logger.info(f"Block: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error Block: {e}")
        return jobs

    def _fetch_solana_jobs(self) -> List[Dict]:
        jobs = []
        try:
            logger.info("Fetching from Solana Jobs...")
            soup = self._safe_scrape('https://jobs.solana.com/jobs', 'Solana Jobs')
            if soup:
                jobs = self._extract_jobs_from_soup(soup, 'Solana Jobs', 'https://jobs.solana.com', 'Solana Ecosystem')
            logger.info(f"Solana Jobs: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error Solana Jobs: {e}")
        return jobs

    def _fetch_avalanche_jobs(self) -> List[Dict]:
        jobs = []
        try:
            logger.info("Fetching from Avalanche Jobs...")
            soup = self._safe_scrape('https://jobs.avax.network/jobs', 'Avalanche Jobs')
            if soup:
                jobs = self._extract_jobs_from_soup(soup, 'Avalanche Jobs', 'https://jobs.avax.network', 'Avalanche Ecosystem')
            logger.info(f"Avalanche Jobs: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error Avalanche Jobs: {e}")
        return jobs

    def _fetch_ethereum_jobboard(self) -> List[Dict]:
        jobs = []
        try:
            logger.info("Fetching from Ethereum Job Board...")
            soup = self._safe_scrape('https://www.ethereumjobboard.com/jobs', 'Ethereum Job Board')
            if soup:
                jobs = self._extract_jobs_from_soup(soup, 'Ethereum Job Board', 'https://www.ethereumjobboard.com')
            logger.info(f"Ethereum Job Board: {len(jobs)} jobs")
        except Exception as e:
            logger.error(f"Error Ethereum Job Board: {e}")
        return jobs

    # ============================================================
    #  UTILITIES
    # ============================================================

    def _filter_jobs(self, jobs: List[Dict], keywords: List[str]) -> List[Dict]:
        if not keywords:
            return jobs
        filtered = []
        keywords_lower = [k.lower() for k in keywords]
        for job in jobs:
            text = f"{job.get('title', '')} {job.get('company', '')} {job.get('location', '')} {job.get('team', '')}".lower()
            if all(kw in text for kw in keywords_lower):
                filtered.append(job)
        return filtered

    def _deduplicate(self, jobs: List[Dict]) -> List[Dict]:
        seen = set()
        unique = []
        for job in jobs:
            title = re.sub(r'\s+', ' ', job.get('title', '').lower().strip())
            company = re.sub(r'\s+', ' ', job.get('company', '').lower().strip())
            key = f"{title}|{company}"
            if key not in seen and key != '|':
                seen.add(key)
                unique.append(job)
        return unique

    def get_source_stats(self) -> Dict:
        stats = {}
        for job in self.jobs:
            source = job.get('source', 'Unknown')
            stats[source] = stats.get(source, 0) + 1
        return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))

    def to_json(self) -> str:
        return json.dumps({
            'total': len(self.jobs),
            'updated': datetime.now().isoformat(),
            'sources': self.get_source_stats(),
            'jobs': self.jobs
        }, indent=2)


if __name__ == '__main__':
    aggregator = Web3JobsPro()
    jobs = aggregator.search_all()
    print(f"\nTotal: {len(jobs)} jobs found")
    print("\nBy source:")
    for source, count in aggregator.get_source_stats().items():
        print(f"  {source}: {count}")
