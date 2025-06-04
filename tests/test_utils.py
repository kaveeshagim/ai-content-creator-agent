import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("OPENAI_API_KEY", "test")

from utils import estimate_reading_time

def test_estimate_reading_time():
    text = "word " * 400
    assert estimate_reading_time(text) == "2 min read"

