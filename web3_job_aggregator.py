#!/usr/bin/env python3
"""
Web3 Job Aggregator - Optimized with site-specific scrapers
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from typing import List, Dict, Optional
import time
from urllib.parse import urljoin, urlparse
import sys

class Web3JobAggregator:
    def __init__(self):
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        self.job_boards = {
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
    
    def search_all(self, keywords: Optional[List[str]] = None, max_jobs_per_site: int = 200):
        """Search all enabled job boards with MAXIMUM results"""
        print("\n" + "="*80)
        print("🚀 WEB3 JOB AGGREGATOR - MAXIMUM MODE")
        print("="*80)
        
        if keywords:
            print(f"🔍 Filtering by keywords: {', '.join(keywords)}")
        
        print(f"\n📋 Scanning {sum(1 for b in self.job_boards.values() if b['enabled'])} job boards...\n")
        
        for board_id, board_info in self.job_boards.items():
            if not board_info['enabled']:
                continue
                
            print(f"⏳ Fetching from {board_info['name']}...", end=' ')
            sys.stdout.flush()
            
            try:
                # Use specialized scraper if available
                scraper_method = getattr(self, f'_scrape_{board_id.replace("-", "_")}', None)
                
                if scraper_method:
                    jobs = scraper_method(max_jobs=max_jobs_per_site)
                else:
                    jobs = self._scrape_generic(
                        board_info['url'], 
                        board_info['name'],
                        max_jobs=max_jobs_per_site
                    )
                
                if keywords:
                    jobs = self._filter_by_keywords(jobs, keywords)
                
                self.jobs.extend(jobs)
                print(f"✅ {len(jobs)} jobs")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error: {str(e)[:50]}")
        
        self._deduplicate_jobs()
        
        print(f"\n{'='*80}")
        print(f"✨ TOTAL: {len(self.jobs)} unique jobs found")
        print(f"{'='*80}\n")
        
        return self.jobs
    
    def _scrape_web3_career(self, max_jobs: int = 200) -> List[Dict]:
        """Specialized scraper for web3.career"""
        jobs = []
        try:
            # Try multiple pages
            for page in range(1, 6):  # Pages 1-5
                url = f'https://web3.career/?page={page}' if page > 1 else 'https://web3.career/'
                response = requests.get(url, headers=self.headers, timeout=15)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards - web3.career uses table rows
                job_rows = soup.find_all('tr', class_='table_row')
                
                for row in job_rows[:max_jobs]:
                    try:
                        title_elem = row.find('h2', class_='fs-6')
                        company_elem = row.find('h3', class_='fs-6')
                        location_elem = row.find('p', class_='job-location-salary')
                        link_elem = row.find('a', href=True)
                        
                        if title_elem and link_elem:
                            job = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True) if company_elem else '',
                                'location': location_elem.get_text(strip=True) if location_elem else '',
                                'url': urljoin('https://web3.career', link_elem['href']),
                                'source': 'Web3 Career',
                                'scraped_at': datetime.now().isoformat()
                            }
                            jobs.append(job)
                    except:
                        continue
                
                if len(job_rows) == 0:
                    break
                    
        except Exception as e:
            print(f"Error in web3.career: {e}")
        
        return jobs
    
    def _scrape_cryptocurrencyjobs(self, max_jobs: int = 200) -> List[Dict]:
        """Specialized scraper for cryptocurrencyjobs.co"""
        jobs = []
        try:
            for page in range(1, 6):
                url = f'https://cryptocurrencyjobs.co/jobs/?page={page}' if page > 1 else 'https://cryptocurrencyjobs.co/jobs/'
                response = requests.get(url, headers=self.headers, timeout=15)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                job_cards = soup.find_all('div', class_='job-list-item') or soup.find_all('article')
                
                for card in job_cards[:max_jobs]:
                    try:
                        title_elem = card.find(['h2', 'h3', 'a'])
                        company_elem = card.find(class_=re.compile('company', re.I))
                        location_elem = card.find(class_=re.compile('location', re.I))
                        link_elem = card.find('a', href=True)
                        
                        if title_elem:
                            job = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True) if company_elem else '',
                                'location': location_elem.get_text(strip=True) if location_elem else '',
                                'url': link_elem['href'] if link_elem else '',
                                'source': 'Cryptocurrency Jobs',
                                'scraped_at': datetime.now().isoformat()
                            }
                            if job['title']:
                                jobs.append(job)
                    except:
                        continue
                
                if len(job_cards) == 0:
                    break
                    
        except Exception as e:
            print(f"Error in cryptocurrencyjobs: {e}")
        
        return jobs
    
    def _scrape_generic(self, url: str, source: str, max_jobs: int = 200) -> List[Dict]:
        """Enhanced generic scraper with better detection"""
        jobs = []
        
        try:
            # Try multiple pages
            for page_num in range(1, 4):
                page_url = url
                if page_num > 1:
                    # Try common pagination patterns
                    for pattern in [f'?page={page_num}', f'/page/{page_num}', f'?p={page_num}']:
                        test_url = url.rstrip('/') + pattern
                        try:
                            test_response = requests.head(test_url, headers=self.headers, timeout=5)
                            if test_response.status_code == 200:
                                page_url = test_url
                                break
                        except:
                            continue
                
                response = requests.get(page_url, headers=self.headers, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try multiple selectors
                job_elements = []
                
                selectors = [
                    {'name': 'article'},
                    {'name': 'div', 'class': re.compile(r'job.*item|job.*card|job.*listing|position.*item', re.I)},
                    {'name': 'tr', 'class': re.compile(r'job|position|listing', re.I)},
                    {'name': 'li', 'class': re.compile(r'job|listing|position', re.I)},
                    {'name': 'div', 'attrs': {'data-testid': re.compile(r'job', re.I)}},
                ]
                
                for selector in selectors:
                    found = soup.find_all(**selector, limit=max_jobs)
                    if len(found) > 3:
                        job_elements = found
                        break
                
                # Fallback to all links if nothing found
                if not job_elements:
                    job_elements = soup.find_all('a', href=True, limit=max_jobs)
                
                page_jobs = 0
                for element in job_elements[:max_jobs]:
                    try:
                        job_data = self._extract_job_data(element, url, source)
                        if job_data and job_data.get('title') and len(job_data['title']) > 3:
                            jobs.append(job_data)
                            page_jobs += 1
                    except:
                        continue
                
                # Stop if no jobs found on this page
                if page_jobs == 0:
                    break
                    
        except Exception as e:
            pass
        
        return jobs
    
    def _extract_job_data(self, element, base_url: str, source: str) -> Optional[Dict]:
        """Enhanced job data extraction"""
        # Title extraction
        title = ''
        for selector in [
            ('class', re.compile(r'title|job.*name|position', re.I)),
            ('name', ['h1', 'h2', 'h3', 'h4']),
        ]:
            if selector[0] == 'class':
                title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'a', 'span'], class_=selector[1])
            else:
                title_elem = element.find(selector[1])
            
            if title_elem:
                title = title_elem.get_text(strip=True)
                break
        
        if not title:
            title_elem = element.find('a')
            if title_elem:
                title = title_elem.get_text(strip=True)
        
        # Skip invalid titles
        if not title or len(title) < 3:
            return None
        
        skip_words = ['jobs', 'careers', 'apply', 'more', 'view all', 'see all', 'load more']
        if title.lower() in skip_words:
            return None
        
        # Company extraction
        company = ''
        company_elem = element.find(['span', 'div', 'p', 'h3', 'h4'], class_=re.compile(r'company|employer|organization', re.I))
        if company_elem:
            company = company_elem.get_text(strip=True)
        
        # Location extraction
        location = ''
        location_elem = element.find(['span', 'div', 'p'], class_=re.compile(r'location|remote|place|geo', re.I))
        if location_elem:
            location = location_elem.get_text(strip=True)
        
        # Check for remote in text
        if not location and 'remote' in element.get_text().lower():
            location = 'Remote'
        
        # URL extraction
        job_url = ''
        link = element.find('a', href=True)
        if link:
            href = link['href']
            if href.startswith('http'):
                job_url = href
            elif href.startswith('/'):
                job_url = urljoin(base_url, href)
            else:
                job_url = urljoin(base_url, '/' + href)
        elif element.name == 'a' and element.get('href'):
            href = element['href']
            job_url = href if href.startswith('http') else urljoin(base_url, href)
        
        return {
            'title': title,
            'company': company,
            'location': location,
            'url': job_url,
            'source': source,
            'scraped_at': datetime.now().isoformat()
        }
    
    def _filter_by_keywords(self, jobs: List[Dict], keywords: List[str]) -> List[Dict]:
        """Filter jobs by keywords (case-insensitive)"""
        if not keywords:
            return jobs
        
        filtered = []
        keywords_lower = [k.lower() for k in keywords]
        
        for job in jobs:
            searchable_text = ' '.join([
                job.get('title', ''),
                job.get('company', ''),
                job.get('location', '')
            ]).lower()
            
            if any(keyword in searchable_text for keyword in keywords_lower):
                filtered.append(job)
        
        return filtered
    
    def _deduplicate_jobs(self):
        """Remove duplicate jobs based on URL and title"""
        seen = set()
        unique_jobs = []
        
        for job in self.jobs:
            # Create identifier from URL or title+company
            identifier = job.get('url', '')
            if not identifier:
                identifier = f"{job.get('title', '')}|{job.get('company', '')}"
            
            identifier = identifier.lower().strip()
            
            if identifier and identifier not in seen:
                seen.add(identifier)
                unique_jobs.append(job)
        
        original_count = len(self.jobs)
        self.jobs = unique_jobs
        
        if original_count > len(self.jobs):
            print(f"🔄 Removed {original_count - len(self.jobs)} duplicates")
    
    def save_json(self, filename: str = 'web3_jobs.json'):
        """Save jobs to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'total_jobs': len(self.jobs),
                'last_updated': datetime.now().isoformat(),
                'jobs': self.jobs
            }, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved to {filename}")
    
    def save_markdown(self, filename: str = 'web3_jobs.md'):
        """Save jobs to Markdown file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# 🚀 Web3 Job Listings\n\n")
            f.write(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total Jobs:** {len(self.jobs)}\n\n")
            
            jobs_by_source = {}
            for job in self.jobs:
                source = job.get('source', 'Unknown')
                if source not in jobs_by_source:
                    jobs_by_source[source] = []
                jobs_by_source[source].append(job)
            
            f.write(f"**Sources:** {len(jobs_by_source)} job boards\n\n")
            f.write("---\n\n")
            
            for source, jobs in sorted(jobs_by_source.items()):
                f.write(f"## 📍 {source} ({len(jobs)} jobs)\n\n")
                
                for job in jobs:
                    f.write(f"### {job.get('title', 'N/A')}\n\n")
                    if job.get('company'):
                        f.write(f"**Company:** {job['company']}  \n")
                    if job.get('location'):
                        f.write(f"**Location:** {job['location']}  \n")
                    if job.get('url'):
                        f.write(f"**Apply:** [View Job]({job['url']})\n")
                    f.write("\n")
                
                f.write("---\n\n")
        
        print(f"📝 Saved to {filename}")
    
    def display(self, limit: int = 20):
        """Display jobs in terminal"""
        print(f"\n{'='*80}")
        print(f"SHOWING {min(limit, len(self.jobs))} OF {len(self.jobs)} JOBS")
        print(f"{'='*80}\n")
        
        for i, job in enumerate(self.jobs[:limit], 1):
            print(f"[{i}] {job.get('title', 'N/A')}")
            
            if job.get('company'):
                print(f"    🏢 {job['company']}")
            
            if job.get('location'):
                print(f"    📍 {job['location']}")
            
            print(f"    🌐 {job.get('source', 'N/A')}")
            
            if job.get('url'):
                print(f"    🔗 {job['url']}")
            
            print()


def main():
    """Main execution"""
    print("""
    ╔════════════════════════════════════════════╗
    ║     🚀 Web3 Job Aggregator v3.0           ║
    ║     MAXIMUM MODE - All jobs included      ║
    ╚════════════════════════════════════════════╝
    """)
    
    aggregator = Web3JobAggregator()
    
    print("🔍 Enter keywords to filter jobs (comma-separated)")
    print("   Examples: solidity, rust, remote, developer, defi")
    print("   Or press Enter to see ALL jobs\n")
    
    user_input = input("Keywords: ").strip()
    
    keywords = None
    if user_input:
        keywords = [k.strip() for k in user_input.split(',') if k.strip()]
        print(f"\n✅ Filtering by: {', '.join(keywords)}")
    
    print("\n" + "⏳ Starting MAXIMUM search (this will take 60-90 seconds)...\n")
    jobs = aggregator.search_all(keywords=keywords, max_jobs_per_site=200)
    
    if jobs:
        aggregator.display(limit=15)
        
        print("💾 Save results?")
        print("   1. JSON only")
        print("   2. Markdown only")
        print("   3. Both (recommended)")
        print("   4. Don't save")
        
        choice = input("\nChoice [3]: ").strip() or "3"
        
        if choice in ['1', '3']:
            aggregator.save_json()
        
        if choice in ['2', '3']:
            aggregator.save_markdown()
        
        print("\n✨ Done! Happy job hunting! 🎯\n")
    else:
        print("\n❌ No jobs found. Try different keywords or check your connection.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user. Goodbye!")
        sys.exit(0)
