"""
Simple Speed Benchmark: Cache Response vs Browser Agent Task

Measures how much faster cached responses are compared to creating new browser agent tasks.
"""

import asyncio
import time
import os
from dotenv import load_dotenv
from utils import get_cached_response, cache_response
from browser_use import Agent, ChatGoogle

load_dotenv()

TEST_QUERY = "Find the number 1 post on Show HN"


async def test_agent_execution():
    """Execute a browser agent task and measure time"""
    print("\n🤖 Testing Agent Execution...")
    print(f"   Task: {TEST_QUERY}")
    
    try:
        start = time.time()
        
        llm = ChatGoogle(
            model="gemini-flash-latest",
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        agent = Agent(task=TEST_QUERY, llm=llm)
        result = await agent.run()
        
        duration = time.time() - start
        
        print(f"   ✓ Completed in {duration:.2f} seconds")
        
        # Cache the result for the next test
        cache_response(TEST_QUERY, str(result))
        
        return duration
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        return None


def test_cache_retrieval(iterations=5):
    """Retrieve from cache multiple times and measure time"""
    print(f"\n💾 Testing Cache Retrieval ({iterations} times)...")
    print(f"   Query: {TEST_QUERY}")
    
    times = []
    for i in range(iterations):
        start = time.time()
        result = get_cached_response(TEST_QUERY)
        duration = time.time() - start
        
        if result:
            times.append(duration)
            print(f"   Hit {i+1}: {duration*1000:.2f}ms")
        else:
            print(f"   Hit {i+1}: Cache miss (skipped)")
    
    return times


async def main():
    """Run the speed benchmark"""
    print("\n" + "="*60)
    print("CACHE vs AGENT SPEED BENCHMARK")
    print("="*60)
    
    # Step 1: Execute agent to populate cache
    print("\nStep 1: Running browser agent (to populate cache)...")
    agent_time = await test_agent_execution()
    
    if agent_time is None:
        print("\n❌ Agent execution failed. Skipping cache test.")
        return
    
    # Step 2: Test cache retrieval
    print("\nStep 2: Testing cache retrieval...")
    cache_times = test_cache_retrieval(iterations=5)
    
    # Show results
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    
    if cache_times:
        avg_cache = sum(cache_times) / len(cache_times)
        print(f"\nAgent Execution Time:  {agent_time:.2f} seconds")
        print(f"Avg Cache Retrieval:   {avg_cache*1000:.2f}ms")
        print(f"\nSpeedup:               {agent_time / avg_cache:.0f}x faster with cache")
        print(f"Time Saved Per Query:  {(agent_time - avg_cache):.2f} seconds")
    else:
        print("\n❌ No cache results to compare")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    asyncio.run(main())
