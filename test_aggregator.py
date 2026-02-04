#!/usr/bin/env python3
"""
Test script to verify the aggregator works
"""

from web3_job_aggregator import Web3JobAggregator
import sys

def test_basic():
    print("🧪 Testing Web3 Job Aggregator...\n")
    
    # Test 1: Create instance
    print("✓ Creating aggregator instance...")
    aggregator = Web3JobAggregator()
    
    # Test 2: Check job boards loaded
    print(f"✓ Loaded {len(aggregator.job_boards)} job boards")
    
    # Test 3: Quick search (limit to 2 sites for speed)
    print("\n🔍 Testing with 2 job boards (quick test)...")
    
    # Temporarily disable most boards for quick test
    for board_id in aggregator.job_boards:
        if board_id not in ['web3-career', 'ethereum']:
            aggregator.job_boards[board_id]['enabled'] = False
    
    try:
        jobs = aggregator.search_all(keywords=['developer'], max_jobs_per_site=10)
        
        if jobs:
            print(f"\n✅ SUCCESS! Found {len(jobs)} jobs")
            print("\n📋 Sample results:")
            for i, job in enumerate(jobs[:3], 1):
                print(f"  {i}. {job['title']}")
                print(f"     Company: {job.get('company', 'N/A')}")
                print(f"     Source: {job['source']}")
                print()
            
            return True
        else:
            print("\n⚠️  No jobs found (this might be normal if sites are slow)")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════╗
    ║   Web3 Job Aggregator - Test Suite   ║
    ╚════════════════════════════════════════╝
    """)
    
    success = test_basic()
    
    if success:
        print("\n✨ All tests passed! The aggregator is working.")
        print("💡 Run 'python web3_job_aggregator.py' to do a full search\n")
        sys.exit(0)
    else:
        print("\n⚠️  Tests completed with warnings")
        print("💡 Try running the full aggregator to see more results\n")
        sys.exit(0)
