"""Test configuration - disable rate limiting"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Disable rate limiting for tests
os.environ['RATE_LIMIT_ENABLED'] = 'false'
