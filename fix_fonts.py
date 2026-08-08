import os
import re

def fix_font_links():
    pages = ['index.html', 'colocaciones.html', 'contacto.html']
    
    for page in pages:
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace href="css2?family=..." with href="https://fonts.googleapis.com/css2?family=..."
        content = re.sub(r'href="(css2\?family=[^"]*)"', r'href="https://fonts.googleapis.com/\1"', content)
        
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)

    print("Fixed Google Fonts links")

if __name__ == '__main__':
    fix_font_links()
