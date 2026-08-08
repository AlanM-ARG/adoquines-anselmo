import subprocess
import re

commits = subprocess.check_output(['git', 'log', '--oneline', 'colocaciones.html']).decode('utf-8').split('\n')

for line in commits:
    if not line: continue
    commit_hash = line.split()[0]
    
    html = subprocess.check_output(['git', 'show', f'{commit_hash}:colocaciones.html'], errors='ignore')
    if 'img/products/' in html:
        print(f"Found old images in {commit_hash}")
        with open('original_colocaciones.html', 'w', encoding='utf-8') as f:
            f.write(html)
        break
else:
    print("Not found")
