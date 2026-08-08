import re

def main():
    # 1. Get gallery from index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    gallery_match = re.search(r'(<div id="trabajos" class="container-gallery.*?</div>\s*</div>\s*</div>\s*</div>)', html, re.DOTALL)
    if not gallery_match:
        print("Gallery not found in index.html")
        return
    gallery_code = gallery_match.group(1)

    # 2. Inject into colocaciones.html
    with open('colocaciones.html', 'r', encoding='utf-8') as f:
        col_html = f.read()

    # The block in colocaciones.html we want to replace starts at:
    # <div class="container py-5 my-5"> (around line 180)
    # And ends before:
    # <section class="section section-default border-0 m-0"> (around line 304)
    # Wait, the prompt says "Replica exactamente la misma estructura HTML". The section before <section class="section..." is what we want to replace.
    
    col_pattern = re.compile(r'<div class="container py-5 my-5">.*?(?=<section class="section section-default border-0 m-0">)', re.DOTALL)
    if col_pattern.search(col_html):
        col_html = col_pattern.sub(gallery_code + '\n\n            ', col_html)
    else:
        print("Could not find gallery block in colocaciones.html")
        
    with open('colocaciones.html', 'w', encoding='utf-8') as f:
        f.write(col_html)

if __name__ == '__main__':
    main()
