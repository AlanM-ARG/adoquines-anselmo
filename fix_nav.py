import os
import re

def fix_active_nav():
    pages = ['index.html', 'colocaciones.html', 'contacto.html']
    
    for page in pages:
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()
            
        nav_pattern = re.compile(r'<ul class="nav nav-pills" id="mainNav">.*?</ul>', re.DOTALL)
        nav_match = nav_pattern.search(content)
        if not nav_match: continue
        nav = nav_match.group(0)
        
        # Reset all
        nav = re.sub(r'class="nav-link[^"]*"', 'class="nav-link text-3"', nav)
        nav = re.sub(r'href="#"', 'href="index.html"', nav)
        nav = re.sub(r'href="[^"]*#(inicio|trabajos|nosotros)"', r'href="index.html#\1"', nav)
        
        target_text = ''
        if page == 'index.html': target_text = 'INICIO'
        elif page == 'colocaciones.html': target_text = 'COLOCACIONES'
        elif page == 'contacto.html': target_text = 'CONTACTO'
            
        if target_text:
            # specifically replace the link class of the target
            def repl(m):
                return m.group(1) + '#' + m.group(3) + 'class="nav-link text-3 active font-weight-bold"' + m.group(5)
            # Find the target anchor
            active_regex = re.compile(r'(<a\s+href=")([^"]+)("\s+)(class="nav-link text-3")([^>]*>\s*' + target_text + r'\s*</a>)', re.DOTALL)
            nav = active_regex.sub(repl, nav)
            
        content = nav_pattern.sub(nav, content)
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print("Nav fixed")

if __name__ == '__main__':
    fix_active_nav()
