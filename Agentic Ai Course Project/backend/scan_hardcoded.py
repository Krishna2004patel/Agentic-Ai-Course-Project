import os, re

search_terms = ['KLE Tech', 'early disease', 'premature graying', 'Bharatesh', 'Dr. A. B. Joshi']
for root, dirs, files in os.walk('backend/app'):
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                txt = fp.read()
                for term in search_terms:
                    matches = list(re.finditer(re.escape(term), txt, re.IGNORECASE))
                    if matches:
                        print(f"{p}: found {len(matches)} occurrences of '{term}'")
