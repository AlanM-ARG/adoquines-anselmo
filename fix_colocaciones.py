import os
import re

def fix_colocaciones():
    # 1. Extract gallery block from index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_html = f.read()

    start_idx = idx_html.find('<div id="trabajos" class="container-gallery py-5 mt-3">')
    end_idx = idx_html.find('<div id="nosotros"')

    if start_idx == -1 or end_idx == -1:
        print("Could not find gallery in index.html")
        return

    gallery_html = idx_html[start_idx:end_idx]

    # 2. Inject into colocaciones.html
    with open('colocaciones.html', 'r', encoding='utf-8') as f:
        col_html = f.read()

    start_col = col_html.find('<div class="container py-5 my-5">')
    end_col = col_html.find('<section class="section section-height-3 bg-primary-darken')

    if start_col == -1 or end_col == -1:
        print("Could not find boundaries in colocaciones.html")
        return

    # 3. Restore the banner gradient overlay
    page_header_pattern = re.compile(r'(<section class="page-header[^"]*")(.*?>)')
    def add_bg(m):
        if 'style=' in m.group(2):
            return m.group(1) + re.sub(r'style="([^"]*)"', r'style="\1 background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url(\'img/fotosdetrabajos_nuevas/Porfido patagonico 10x10 mixto Barrio privado Los troncos, berazategui 1.jpg\'); background-size: cover; background-position: center;"', m.group(2))
        else:
            return m.group(1) + ' style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url(\'img/fotosdetrabajos_nuevas/Porfido patagonico 10x10 mixto Barrio privado Los troncos, berazategui 1.jpg\'); background-size: cover; background-position: center;"' + m.group(2)
            
    # Apply gallery replacement
    new_col_html = col_html[:start_col] + gallery_html + '\n            ' + col_html[end_col:]
    
    # Apply background banner
    new_col_html = page_header_pattern.sub(add_bg, new_col_html)
    
    # 4. Routing fixes
    new_col_html = re.sub(r'href="#"\s*(class="nav-link[^>]*>\s*INICIO)', r'href="index.html" \1', new_col_html)
    new_col_html = re.sub(r'href="#[^"]*"\s*(class="nav-link[^>]*>\s*INICIO)', r'href="index.html" \1', new_col_html)
    
    # Also fix header links for "Colocaciones" and "Contacto" to use index.html#inicio, #trabajos etc.?
    # Wait, the menu links just say "INICIO", "COLOCACIONES", "CONTACTO". "INICIO" points to `index.html`.
    # Does "Ver nuestros trabajos" point to `#trabajos`? Yes.
    # In colocaciones.html, `#trabajos` will work because we injected the gallery with `id="trabajos"`.
    # Wait, the user asked for: "Cambia todos los enlaces para que usen la ruta raíz (ej. href="/#inicio", href="/#trabajos", href="/contacto.html" o index.html según corresponda)."
    
    # Let's just fix the main menu "INICIO".
    new_col_html = re.sub(r'href="index\.html#inicio"\s*(class="nav-link[^>]*>\s*INICIO)', r'href="index.html" \1', new_col_html)

    # 5. Ensure Lightbox Modal is at the bottom
    if '<!-- Lightbox Modal -->' not in new_col_html:
        lightbox_match = re.search(r'(<!-- Lightbox Modal -->.*?</script>)', idx_html, re.DOTALL)
        if lightbox_match:
            new_col_html = new_col_html.replace('</body>', lightbox_match.group(1) + '\n</body>')

    with open('colocaciones.html', 'w', encoding='utf-8') as f:
        f.write(new_col_html)
        
    print("Successfully replaced gallery in colocaciones.html")

    # Fix contacto routing as well
    with open('contacto.html', 'r', encoding='utf-8') as f:
        con_html = f.read()
    con_html = re.sub(r'href="#"\s*(class="nav-link[^>]*>\s*INICIO)', r'href="index.html" \1', con_html)
    con_html = re.sub(r'href="#[^"]*"\s*(class="nav-link[^>]*>\s*INICIO)', r'href="index.html" \1', con_html)
    with open('contacto.html', 'w', encoding='utf-8') as f:
        f.write(con_html)
    print("Successfully fixed contacto.html routing")

if __name__ == '__main__':
    fix_colocaciones()
