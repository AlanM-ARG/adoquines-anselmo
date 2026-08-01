import os
import re

def main():
    # ---------------------------------------------------------
    # 1. Consistencia del Header en TODAS las páginas
    # ---------------------------------------------------------
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_html = f.read()

    header_pattern = re.compile(r'(<header id="header".*?</header>)', re.DOTALL)
    header_match = header_pattern.search(idx_html)
    base_header = header_match.group(1) if header_match else ""

    # Fix WA links in the base header to end with 6534
    base_header = re.sub(r'wa\.me/\d+', 'wa.me/5491170046534', base_header)

    # ---------------------------------------------------------
    # 3. Estado Activo en el Navbar (Negrita y href="#")
    # ---------------------------------------------------------
    def apply_active_nav(html_content, page_name):
        nav_pattern = re.compile(r'<ul class="nav nav-pills" id="mainNav">.*?</ul>', re.DOTALL)
        nav_match = nav_pattern.search(html_content)
        if not nav_match: return html_content
        nav = nav_match.group(0)
        
        # Reset all
        nav = re.sub(r'class="nav-link[^"]*"', 'class="nav-link text-3"', nav)
        nav = re.sub(r'href="#"', 'href="index.html"', nav)
        nav = re.sub(r'href="[^"]*#(inicio|trabajos|nosotros)"', r'href="index.html#\1"', nav)
        
        target_text = ''
        if page_name == 'index.html': target_text = 'INICIO'
        elif page_name == 'colocaciones.html': target_text = 'COLOCACIONES'
        elif page_name == 'contacto.html': target_text = 'CONTACTO'
            
        if target_text:
            active_regex = re.compile(r'(<a\s+href=")([^"]+)("\s+class="nav-link text-3"[^>]*>\s*' + target_text + r'\s*</a>)', re.DOTALL)
            nav = active_regex.sub(r'\1#\3', nav)
            nav = nav.replace('class="nav-link text-3"', 'class="nav-link text-3 active font-weight-bold"')
            
        return html_content.replace(nav_match.group(0), nav)

    # ---------------------------------------------------------
    # 4. Restaurar Imágenes Previas en Colocaciones
    # ---------------------------------------------------------
    with open('original_colocaciones.html', 'r', encoding='utf-8') as f:
        old_html = f.read()
    
    old_imgs = re.findall(r'<img[^>]+src="([^"]+img/products/[^"]+)"', old_html)
    # Filter to unique
    old_imgs = list(dict.fromkeys(old_imgs))
    
    # We will append these old_imgs to "Pisos de Pórfido" or a new category "Trabajos Anteriores"
    # To be safe and clean, let's create a new category in the gallery called "Trabajos Anteriores"
    # Or just add them to the "Pisos de Pórfido" since they are porfido.
    # The user said: "(como las de "granitullo"). Mantén las anteriores y suma las 16 imágenes nuevas a esa misma grilla."
    # Let's just create a new category "Trabajos Anteriores"
    
    old_imgs_html = '''
                <div class="col-12 mt-5 mb-4">
                    <h3 class="font-weight-bold text-7 text-color-dark">Trabajos Anteriores</h3>
                </div>
                <div class="row row-cols-1 row-cols-md-2 row-cols-lg-2 g-4 mb-5 gallery-container">'''
    for src in old_imgs:
        old_imgs_html += f'''
                    <div class="col">
                        <img src="{src}" class="img-fluid lightbox-trigger w-100" alt="Trabajo Anterior - Colocación de adoquines" style="aspect-ratio: 16/9; object-fit: cover;">
                    </div>'''
    old_imgs_html += '''
                </div>'''

    # Apply all to files
    pages = ['index.html', 'colocaciones.html', 'contacto.html']
    for page in pages:
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update Header
        if page != 'index.html' and base_header:
            content = header_pattern.sub(base_header, content)
            
        # Active Nav
        content = apply_active_nav(content, page)
        
        # WA Links
        content = re.sub(r'wa\.me/\d+', 'wa.me/5491170046534', content)
        
        # 5. Restore banner background
        if page in ['colocaciones.html', 'contacto.html']:
            banner_pattern = re.compile(r'(<section class="page-header[^>]*style="[^"]*)(\bbackground-image:[^;]+;|\bbackground:[^;]+;)([^"]*")')
            def banner_repl(m):
                return m.group(1) + " background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('img/photo-ground-texture-pattern.jpg'); background-size: cover; background-position: center;" + m.group(3)
            
            # if it doesn't match, maybe it doesn't have a background style yet.
            if not banner_pattern.search(content):
                # find the page-header class and inject the style
                content = re.sub(r'(<section class="page-header[^>]*")>', r'\1 style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url(\'img/photo-ground-texture-pattern.jpg\'); background-size: cover; background-position: center;">', content)
            else:
                content = banner_pattern.sub(banner_repl, content)

        # 4. In colocaciones.html, inject old images
        if page == 'colocaciones.html':
            if 'Trabajos Anteriores' not in content:
                # Find the end of the gallery-container before the `</div>` of id="trabajos"
                # The end of the last gallery-container is `</div>\n            </div>\n\n            <section class="section section-height-3 bg-primary-darken`
                # Let's just find the last `</div>` of the gallery.
                insertion_point = content.rfind('</div>\n            </div>\n\n            <section class="section section-height-3 bg-primary-darken')
                if insertion_point != -1:
                    content = content[:insertion_point] + '</div>' + old_imgs_html + '\n            </div>\n\n            <section class="section section-height-3 bg-primary-darken' + content[insertion_point + len('</div>\n            </div>\n\n            <section class="section section-height-3 bg-primary-darken'):]
        
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)

    print("Success")

if __name__ == '__main__':
    main()
