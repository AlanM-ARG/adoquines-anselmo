import re

def main():
    pages = ['index.html', 'colocaciones.html', 'contacto.html']
    
    for page in pages:
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix 1: Formato exacto de Teléfonos en el Header y Enlace a WhatsApp
        # In the header there are phone links. Let's find them and replace accurately.
        # Máximo's phone: 1170046534 (Máximo) with href="https://wa.me/5491170046534"
        # Anselmo's phone: 1135517563 (Anselmo) with whatever href it had.
        
        # Replace Máximo link
        content = re.sub(r'<a href="[^"]*1170046534[^"]*"([^>]*)>\s*[^<]*\s*</a>', 
                         r'<a href="https://wa.me/5491170046534"\1>\n                                                1170046534 (Máximo)\n                                            </a>', content)
                         
        # Replace Anselmo link text
        content = re.sub(r'(<a href="tel:1135517563"[^>]*>)\s*[^<]*\s*(</a>)', 
                         r'\1\n                                                1135517563 (Anselmo)\n                                            \2', content)

        # Fix 2: Enlace del Logo en Inicio
        # Find logo: <a href="index.html">\n <img src="img/logo.webp"
        if page == 'index.html':
            content = re.sub(r'<a href="index\.html"([^>]*>\s*<img src="img/logo\.webp")', r'<a href="#"\1', content)
        else:
            content = re.sub(r'<a href="#"([^>]*>\s*<img src="img/logo\.webp")', r'<a href="index.html"\1', content)

        # Fix 3: Restaurar Imagen de Banner en Colocaciones y Contacto
        if page in ['colocaciones.html', 'contacto.html']:
            # Replace inline background styles in page-header
            # The current style might be:
            # style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('img/photo-ground-texture-pattern.jpg'); background-size: cover; background-position: center;"
            # We want to ensure it points to img/products/photo-ground-texture-pattern.jpg
            
            banner_pattern = re.compile(r'(<section class="page-header[^>]*style="[^"]*)(\bbackground-image:[^;]+;|\bbackground:[^;]+;)([^"]*")')
            def banner_repl(m):
                return m.group(1) + " background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('img/products/photo-ground-texture-pattern.jpg'); background-size: cover; background-position: center;" + m.group(3)
                
            if banner_pattern.search(content):
                content = banner_pattern.sub(banner_repl, content)
            else:
                # If there's no style with background, add it
                content = re.sub(r'(<section class="page-header[^>]*")>', 
                                 r'\1 style="background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url(\'img/products/photo-ground-texture-pattern.jpg\'); background-size: cover; background-position: center;">', content)

        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)

    print("Success")

if __name__ == '__main__':
    main()
