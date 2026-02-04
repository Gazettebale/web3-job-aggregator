#!/usr/bin/env python3
"""
Automated job search script
Run this daily via cron or task scheduler
"""

from web3_job_aggregator import Web3JobAggregator
from datetime import datetime
import sys

# Customize these based on your preferences
MY_KEYWORDS = [
    'solidity',
    'smart contract',
    'remote',
    'developer',
    'engineer'
]

def main():
    print(f"\n🤖 Automated Web3 Job Search - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    # Create aggregator
    aggregator = Web3JobAggregator()
    
    # Search with your keywords
    print(f"🔍 Searching with keywords: {', '.join(MY_KEYWORDS)}\n")
    jobs = aggregator.search_all(keywords=MY_KEYWORDS)
    
    if jobs:
        # Save results with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        json_file = f'jobs_{timestamp}.json'
        md_file = f'jobs_{timestamp}.md'
        
        aggregator.save_json(json_file)
        aggregator.save_markdown(md_file)
        
        print(f"\n✅ Found {len(jobs)} jobs!")
        print(f"📁 Saved to:")
        print(f"   - {json_file}")
        print(f"   - {md_file}")
        
        # Display top 5
        print("\n📋 Top 5 matches:")
        for i, job in enumerate(jobs[:5], 1):
            print(f"  {i}. {job['title']} @ {job.get('company', 'N/A')}")
        
        return 0
    else:
        print("❌ No jobs found matching your criteria")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted!")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
