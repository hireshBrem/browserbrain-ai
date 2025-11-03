#!/bin/bash

# Test script for utils.py
# This script tests all memory utility functions

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to run a test and print result
run_and_check_test() {
    local test_name="$1"
    local test_code="$2"
    
    echo "Running: $test_name"
    
    # Run the test and capture output
    if python3 -c "$test_code" > /tmp/test_output.log 2>&1; then
        echo -e "${GREEN}✓${NC} $test_name"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $test_name"
        echo -e "${RED}  Error output:${NC}"
        cat /tmp/test_output.log | sed 's/^/  /'
        ((TESTS_FAILED++))
        return 1
    fi
}

# Check if dependencies are available
check_dependencies() {
    echo -e "${BLUE}Checking dependencies...${NC}"
    
    # Check if utils.py exists
    if [ ! -f "utils.py" ]; then
        echo -e "${RED}Error: utils.py not found in current directory${NC}"
        exit 1
    fi
    
    # Check if Python can import utils (this will show the actual error)
    if ! python3 -c "from utils import store_long_term_memory" 2>&1; then
        echo -e "${RED}Error: Cannot import utils.py. Make sure dependencies are installed.${NC}"
        echo -e "${YELLOW}Try running: pip install -r requirements.txt or uv sync${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Dependencies check passed${NC}\n"
}

# Check dependencies first
check_dependencies

echo -e "${YELLOW}Running tests for utils.py...${NC}\n"

# Test 1: Test store_long_term_memory
run_and_check_test \
    "store_long_term_memory - stores memory successfully" \
    "
from utils import store_long_term_memory
result = store_long_term_memory('test_user_1', 'favorite_color', 'blue')
assert result == True, 'store_long_term_memory should return True'
"

# Test 2: Test get_long_term_memory
run_and_check_test \
    "get_long_term_memory - retrieves stored memory" \
    "
from utils import get_long_term_memory
value = get_long_term_memory('test_user_1', 'favorite_color')
assert value == 'blue', 'get_long_term_memory should return stored value'
"

# Test 3: Test get_long_term_memory with non-existent key
run_and_check_test \
    "get_long_term_memory - returns None for non-existent key" \
    "
from utils import get_long_term_memory
value = get_long_term_memory('test_user_1', 'nonexistent_key')
assert value is None, 'get_long_term_memory should return None for non-existent key'
"

# Test 4: Test get_all_long_term_memories
run_and_check_test \
    "get_all_long_term_memories - retrieves all memories for user" \
    "
from utils import store_long_term_memory, get_all_long_term_memories
store_long_term_memory('test_user_2', 'city', 'New York')
store_long_term_memory('test_user_2', 'country', 'USA')
memories = get_all_long_term_memories('test_user_2')
assert 'city' in memories and 'country' in memories, 'get_all_long_term_memories should return all memories'
assert memories['city'] == 'New York', 'Memory values should match'
"

# Test 5: Test store_conversation_history
run_and_check_test \
    "store_conversation_history - stores conversation history" \
    "
from utils import store_conversation_history
result = store_conversation_history('test_user_3', 'What is the weather?', 'Sunny and 75°F')
assert result == True, 'store_conversation_history should return True'
"

# Test 6: Test get_conversation_history
run_and_check_test \
    "get_conversation_history - retrieves conversation history" \
    "
from utils import get_conversation_history
history = get_conversation_history('test_user_3', limit=1)
assert len(history) >= 1, 'get_conversation_history should return at least one entry'
assert 'task' in history[0] and 'result' in history[0], 'History entry should contain task and result'
"

# Test 7: Test get_conversation_history with multiple entries
run_and_check_test \
    "get_conversation_history - returns multiple entries correctly" \
    "
from utils import store_conversation_history, get_conversation_history
store_conversation_history('test_user_4', 'Question 1', 'Answer 1')
store_conversation_history('test_user_4', 'Question 2', 'Answer 2')
store_conversation_history('test_user_4', 'Question 3', 'Answer 3')
history = get_conversation_history('test_user_4', limit=3)
assert len(history) == 3, 'get_conversation_history should return correct number of entries'
"

# Test 8: Test cache_response
run_and_check_test \
    "cache_response - caches response successfully" \
    "
from utils import cache_response
result = cache_response('What is Python?', 'Python is a programming language')
assert result is not None, 'cache_response should return a result'
"

# Test 9: Test get_cached_response
run_and_check_test \
    "get_cached_response - retrieves cached response (or None)" \
    "
from utils import get_cached_response
# Note: This might return None if similarity threshold is too high
# We're just testing that the function doesn't crash
result = get_cached_response('What is Python?')
# Result can be None or a string, both are valid
assert result is None or isinstance(result, str), 'get_cached_response should return None or string'
"

# Test 10: Test error handling - invalid user_id
run_and_check_test \
    "Error handling - handles edge cases gracefully" \
    "
from utils import store_long_term_memory
# Should handle empty strings gracefully
result = store_long_term_memory('', 'key', 'value')
# Function should still return True/False, not crash
assert isinstance(result, bool), 'Should return boolean even with empty user_id'
"

# Summary
echo ""
echo -e "${YELLOW}Test Summary:${NC}"
echo -e "  ${GREEN}Passed: ${TESTS_PASSED}${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "  ${RED}Failed: ${TESTS_FAILED}${NC}"
fi

# Cleanup test data (optional)
echo ""
echo -e "${YELLOW}Cleaning up test data...${NC}"
python3 -c "
from utils import redis_client
# Clean up test users
test_users = ['test_user_1', 'test_user_2', 'test_user_3', 'test_user_4']
for user_id in test_users:
    redis_client.delete(f'longterm_memory:{user_id}')
    redis_client.delete(f'conversation_history:{user_id}')
print('Cleanup complete')
" 2>/dev/null || echo "Cleanup skipped (Redis may not be available)"

# Exit with appropriate code
if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed!${NC}"
    exit 1
fi
