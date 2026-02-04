#!/usr/bin/env python3
"""
Web3 Job Aggregator - Optimized for real job boards
Scrapes multiple Web3/crypto job boards and aggregates results
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
        
        # Job boards configuration
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
    
    def search_all(self, keywords: Optional[List[str]] = None, max_jobs_per_site: int = 50):
        """
        Search all enabled job boards
        
        Args:
            keywords: List of keywords to filter (e.g., ['solidity', 'remote'])
            max_jobs_per_site: Maximum jobs to fetch per site
        """
        print("\n" + "="*80)
        print("🚀 WEB3 JOB AGGREGATOR")
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
                jobs = self._scrape_generic(
                    board_info['url'], 
                    board_info['name'],
                    max_jobs=max_jobs_per_site
                )
                
                if keywords:
                    jobs = self._filter_by_keywords(jobs, keywords)
                
                self.jobs.extend(jobs)
                print(f"✅ {len(jobs)} jobs")
                
                # Be respectful - wait between requests
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error: {str(e)[:50]}")
        
        # Remove duplicates based on URL
        self._deduplicate_jobs()
        
        print(f"\n{'='*80}")
        print(f"✨ TOTAL: {len(self.jobs)} unique jobs found")
        print(f"{'='*80}\n")
        
        return self.jobs
    
    def _scrape_generic(self, url: str, source: str, max_jobs: int = 50) -> List[Dict]:
        """
        Generic scraper that works for most job boards
        """
        jobs = []
        
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Common selectors for job listings
            selectors = [
                {'name': 'article'},
                {'name': 'div', 'class': re.compile(r'job.*card|listing|position', re.I)},
                {'name': 'tr', 'class': re.compile(r'job|row', re.I)},
                {'name': 'li', 'class': re.compile(r'job|listing', re.I)},
                {'name': 'a', 'class': re.compile(r'job.*link|listing', re.I)},
            ]
            
            job_elements = []
            for selector in selectors:
                found = soup.find_all(**selector, limit=max_jobs)
                if len(found) > 5:  # If we found a reasonable number, use these
                    job_elements = found
                    break
            
            # Fallback: find all links that might be jobs
            if not job_elements:
                job_elements = soup.find_all('a', href=True, limit=max_jobs)
            
            for element in job_elements[:max_jobs]:
                try:
                    job_data = self._extract_job_data(element, url, source)
                    if job_data and job_data.get('title'):
                        jobs.append(job_data)
                except Exception:
                    continue
                    
        except Exception as e:
            raise Exception(f"Failed to scrape {source}: {str(e)}")
        
        return jobs
    
    def _extract_job_data(self, element, base_url: str, source: str) -> Optional[Dict]:
        """
        Extract job data from an HTML element
        """
        # Try to find title
        title = ''
        for tag in ['h1', 'h2', 'h3', 'h4', 'a', 'span', 'div']:
            title_elem = element.find(tag, class_=re.compile(r'title|position|role|job.*name', re.I))
            if title_elem:
                title = title_elem.get_text(strip=True)
                break
        
        # If no title with class, try first heading or link
        if not title:
            for tag in ['h2', 'h3', 'a']:
                elem = element.find(tag)
                if elem:
                    title = elem.get_text(strip=True)
                    break
        
        # Skip if title is too short or generic
        if not title or len(title) < 3 or title.lower() in ['jobs', 'careers', 'apply', 'more']:
            return None
        
        # Extract company
        company = ''
        for selector in [
            {'class': re.compile(r'company|employer|organization', re.I)},
            {'class': re.compile(r'subtitle', re.I)},
        ]:
            company_elem = element.find(['span', 'div', 'p', 'h3', 'h4'], **selector)
            if company_elem:
                company = company_elem.get_text(strip=True)
                break
        
        # Extract location
        location = ''
        for selector in [
            {'class': re.compile(r'location|remote|place|geo', re.I)},
        ]:
            loc_elem = element.find(['span', 'div', 'p'], **selector)
            if loc_elem:
                location = loc_elem.get_text(strip=True)
                break
        
        # Check for "remote" in text if no location found
        if not location:
            text = element.get_text().lower()
            if 'remote' in text:
                location = 'Remote'
        
        # Extract URL
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
        """
        Filter jobs by keywords (case-insensitive)
        """
        if not keywords:
            return jobs
        
        filtered = []
        keywords_lower = [k.lower() for k in keywords]
        
        for job in jobs:
            # Combine all searchable text
            searchable_text = ' '.join([
                job.get('title', ''),
                job.get('company', ''),
                job.get('location', '')
            ]).lower()
            
            # Check if any keyword matches
            if any(keyword in searchable_text for keyword in keywords_lower):
                filtered.append(job)
        
        return filtered
    
    def _deduplicate_jobs(self):
        """
        Remove duplicate jobs based on URL
        """
        seen_urls = set()
        unique_jobs = []
        
        for job in self.jobs:
            url = job.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_jobs.append(job)
            elif not url:  # Keep jobs without URL
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
            
            # Group by source
            jobs_by_source = {}
            for job in self.jobs:
                source = job.get('source', 'Unknown')
                if source not in jobs_by_source:
                    jobs_by_source[source] = []
                jobs_by_source[source].append(job)
            
            f.write(f"**Sources:** {len(jobs_by_source)} job boards\n\n")
            f.write("---\n\n")
            
            # Write jobs grouped by source
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
    ║     🚀 Web3 Job Aggregator v2.0           ║
    ║     Find your next crypto/Web3 role       ║
    ╚════════════════════════════════════════════╝
    """)
    
    # Create aggregator
    aggregator = Web3JobAggregator()
    
    # Get user input for keywords
    print("🔍 Enter keywords to filter jobs (comma-separated)")
    print("   Examples: solidity, rust, remote, developer, defi")
    print("   Or press Enter to see ALL jobs\n")
    
    user_input = input("Keywords: ").strip()
    
    keywords = None
    if user_input:
        keywords = [k.strip() for k in user_input.split(',') if k.strip()]
        print(f"\n✅ Filtering by: {', '.join(keywords)}")
    
    # Search jobs
    print("\n" + "⏳ Starting search...\n")
    jobs = aggregator.search_all(keywords=keywords)
    
    if jobs:
        # Display sample
        aggregator.display(limit=15)
        
        # Ask if user wants to save
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
