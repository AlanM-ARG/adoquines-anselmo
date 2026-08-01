import os
import re

def fix_all_bugs():
    # ---------------------------------------------------------
    # 1. Consistencia del Header en TODAS las páginas
    # ---------------------------------------------------------
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_html = f.read()

    header_pattern = re.compile(r'(<header id="header".*?</header>)', re.DOTALL)
    header_match = header_pattern.search(idx_html)
    if not header_match:
        print("Header not found in index.html")
        return
    base_header = header_match.group(1)

    # Ensure phones are formatted with names in base_header
    # Looking for: href="tel:1170046534"... and href="tel:1135517563"...
    # Wait, the prompt says "los teléfonos deben decir: 11XXXXXXXX (Máximo) y 11XXXXXXXX (Anselmo)".
    # The header has a phone list at the top.
    
    # ---------------------------------------------------------
    # 2. Enlaces de WhatsApp (Link 6534)
    # ---------------------------------------------------------
    # We will replace all WA links in the header and all files
    # First, fix WA links in base_header
    base_header = re.sub(r'wa\.me/\d+', 'wa.me/5491170046534', base_header)

    # ---------------------------------------------------------
    # 3. Estado Activo en el Navbar (Negrita y href="#")
    # ---------------------------------------------------------
    def apply_active_nav(html_content, page_name):
        # page_name can be "INICIO", "COLOCACIONES", "CONTACTO"
        # 1. Remove active class/style from all links, and make href absolute
        nav_pattern = re.compile(r'<ul class="nav nav-pills" id="mainNav">.*?</ul>', re.DOTALL)
        nav_match = nav_pattern.search(html_content)
        if not nav_match:
            return html_content
        nav = nav_match.group(0)
        
        # Reset all
        nav = re.sub(r'class="nav-link[^"]*"', 'class="nav-link text-3"', nav)
        nav = re.sub(r'href="#"', 'href="index.html"', nav)
        nav = re.sub(r'href="[^"]*#(inicio|trabajos|nosotros)"', r'href="index.html#\1"', nav)
        
        # Determine the link to make active
        if page_name == 'index.html':
            target_text = 'INICIO'
        elif page_name == 'colocaciones.html':
            target_text = 'COLOCACIONES'
        elif page_name == 'contacto.html':
            target_text = 'CONTACTO'
        else:
            target_text = ''
            
        # Make the target active
        if target_text:
            # We look for <a href="..." class="..."> TARGET </a>
            active_regex = re.compile(r'(<a\s+href=")([^"]+)("\s+class="nav-link text-3"[^>]*>\s*' + target_text + r'\s*</a>)', re.DOTALL)
            nav = active_regex.sub(r'\1#\3', nav)
            # Add active and font-weight-bold
            nav = nav.replace('class="nav-link text-3"', 'class="nav-link text-3 active font-weight-bold"')
            
        html_content = nav_pattern.sub(nav, html_content)
        return html_content

    # ---------------------------------------------------------
    # Apply to all files
    # ---------------------------------------------------------
    pages = ['index.html', 'colocaciones.html', 'contacto.html']
    for page in pages:
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update Header
        if page != 'index.html':
            content = header_pattern.sub(base_header, content)
            
        # Apply Active Nav
        content = apply_active_nav(content, page)
        
        # Fix WA links in the whole page (for floating button, footer, etc.)
        content = re.sub(r'wa\.me/\d+', 'wa.me/5491170046534', content)
        
        # Write back
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)


    # ---------------------------------------------------------
    # 4. Restaurar Imágenes Previas en Colocaciones
    # ---------------------------------------------------------
    # Need to merge the old gallery with the new gallery in colocaciones.html
    # Let's read the current colocaciones.html (which has the new gallery only)
    # And we'll get the old gallery from git... wait, I can just write the HTML.
    # The old colocaciones had 4 sections: baldosas, disco, porfido, natural.
    # Instead of pulling from git, let's just append the old images HTML block to the gallery.
    # I'll create a script to get it from git if needed, or I'll just write it.
    
    # ---------------------------------------------------------
    # 5. Recuperar la Imagen de Fondo (Banner)
    # ---------------------------------------------------------
    # In colocaciones.html and contacto.html
    def fix_banner(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        banner_pattern = re.compile(r'(<section class="page-header[^>]*style="[^"]*)(\bbackground-image:[^;]+;|\bbackground:[^;]+;)([^"]*")')
        
        # Target style: background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('img/photo-ground-texture-pattern.jpg'); background-size: cover; background-position: center;
        def banner_repl(m):
            return m.group(1) + " background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('img/photo-ground-texture-pattern.jpg'); background-size: cover; background-position: center;" + m.group(3)
            
        new_content = banner_pattern.sub(banner_repl, content)
        
        # If it doesn't have a style attribute at all, we might need to add it, but it does.
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)

    fix_banner('colocaciones.html')
    fix_banner('contacto.html')
    
    print("Corrections applied.")

if __name__ == '__main__':
    fix_all_bugs()
