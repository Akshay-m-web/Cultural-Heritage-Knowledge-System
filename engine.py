from pyDatalog import pyDatalog
import json
import os

# Initialize the logic engine
pyDatalog.Logic()

def load_and_query(monument_id, rule_key):
    # 1. Clear previous state
    pyDatalog.clear()
    
    # 2. Define terms as strings for the engine
    pyDatalog.create_terms('Monument, UNESCO, Photo, X')

    # 3. Load JSON Knowledge Base
    if not os.path.exists('data.json'):
        return False, []

    with open('data.json', 'r') as f:
        data = json.load(f)
    
    # 4. Assert Facts using the 'assert_fact' method (Cleaner for scripts)
    for m in data:
        pyDatalog.assert_fact('Monument', m['id'], m['name'])
        pyDatalog.assert_fact('UNESCO', m['id'], m['unesco'])
        pyDatalog.assert_fact('Photo', m['id'], m['photography_allowed'])

    # 5. Define Rules using logic strings
    # "is_unesco(X) if UNESCO(X, True)"
    pyDatalog.load("""
        is_unesco_site(X) <= UNESCO(X, True)
        can_photo(X) <= Photo(X, True)
    """)

    # 6. Run Inference
    if rule_key == "photo":
        result = pyDatalog.ask(f'can_photo("{monument_id}")')
        return bool(result), data
    elif rule_key == "unesco":
        result = pyDatalog.ask(f'is_unesco_site("{monument_id}")')
        return bool(result), data
    
    return False, data

def get_recommendations(state_name):
    if not os.path.exists('data.json'): return []
    with open('data.json', 'r') as f:
        data = json.load(f)
    return [m['name'] for m in data if m['state'].lower() == state_name.lower()]