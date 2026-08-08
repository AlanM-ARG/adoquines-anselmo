import re

def fix_header_cta():
    pages = ['index.html', 'colocaciones.html', 'contacto.html']
    
    for page in pages:
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Target:
        # <li class="d-flex align-items-center ms-lg-3 mt-3 mt-lg-0">
        #     <a href="https://wa.me/5491170046534" class="btn btn-custom-dark...">
        #         1170046534 (Máximo)
        #     </a>
        # </li>
        
        pattern = re.compile(r'(<li class="d-flex align-items-center ms-lg-3 mt-3 mt-lg-0">\s*<a href="https://wa\.me/5491170046534"[^>]*>)\s*1170046534 \(Máximo\)\s*(</a>)', re.DOTALL)
        
        content = pattern.sub(r'\1\n                                                Solicitar Presupuesto\n                                            \2', content)
        
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)

    print("Fixed header CTA")

if __name__ == '__main__':
    fix_header_cta()
