import os
import re
import glob

def main():
    img_dir = os.path.join('img', 'fotosdetrabajos_nuevas')
    images = [f for f in sorted(os.listdir(img_dir)) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    
    # 1. FIX NAVBAR LINKS IN ALL HTML FILES
    html_files = ['index.html', 'colocaciones.html', 'contacto.html']
    
    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # Replace href="#" for INICIO with href="index.html#inicio" (or just index.html)
        html = re.sub(r'href="#"\s*(class="nav-link[^>]*>\s*INICIO)', r'href="index.html" \1', html)
        html = re.sub(r'href="#inicio"\s*(class="nav-link[^>]*>\s*INICIO)', r'href="index.html" \1', html)
        
        # In Colocaciones and Contacto, INICIO should definitely go to index.html
        if filename != 'index.html':
            html = re.sub(r'href="#[^"]*"\s*(class="nav-link[^>]*>\s*INICIO)', r'href="index.html" \1', html)
            
        # Write back
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
            
    # 2. UPDATE CAROUSEL IN index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Generate new slides HTML
    slides_html = ""
    for i, img in enumerate(images):
        title = "Colocadores de piedra con más de 30 años de experiencia." if i == 0 else "Especialistas en colocación de Pórfido y Granitullo."
        
        # Add a dark gradient overlay dynamically on the wrapper or slide
        slides_html += f'''
                    <div id="slide{i}" class="position-relative overlay overlay-show overlay-op-3 overflow-hidden pt-4"
                        data-dynamic-height="['845px','845px','845px','750px','750px']" style="height: 845px; background-image: url('img/fotosdetrabajos_nuevas/{img}'); background-size: cover; background-position: center;">
                        <div class="background-image-wrapper position-absolute top-0 left-0 right-0 bottom-0"
                            data-appear-animation="kenBurnsToLeft" data-appear-animation-duration="30s"
                            data-plugin-options="{{'minWindowWidth': 0}}" data-carousel-onchange-show="" style="background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4));">
                        </div>
                        <div class="container position-relative z-index-3 pb-5 h-100">
                            <div class="row justify-content-center align-items-center pb-5 h-100">
                                <div class="col-lg-10 text-center pb-5 mb-5">
                                    <h1 class="text-color-light font-weight-bold line-height-1 text-7 text-md-10 positive-ls-1 mb-5 appear-animation"
                                        data-appear-animation="blurIn" data-appear-animation-delay="200"
                                        data-plugin-options="{{'minWindowWidth': 0}}" style="text-shadow: 0 2px 10px rgba(0,0,0,0.5);">
                                        {title}
                                    </h1>
                                    <a href="#trabajos" class="btn btn-custom-dark font-weight-bold text-3-5 px-4 py-3 rounded appear-animation" data-appear-animation="fadeInUpShorterPlus" data-appear-animation-delay="200">
                                        Ver nuestros trabajos
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>'''

    # Find the carousel slides block and replace
    carousel_pattern = re.compile(r'<!-- Carousel Slide 1 -->.*?</div>\s*</div>\s*</div>\s*</section>', re.DOTALL)
    replacement = "<!-- Carousel Slides -->\n" + slides_html + "\n                </div>\n            </div>\n        </div>\n    </section>"
    html = carousel_pattern.sub(replacement, html)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    # 3. UPDATE colocaciones.html HERO AND GALLERY
    with open('colocaciones.html', 'r', encoding='utf-8') as f:
        col_html = f.read()
        
    # Hero/Banner
    col_html = col_html.replace('overlay overlay-show overlay-op-9', 'overlay overlay-show overlay-op-9')
    # Let's just find the section and inject the gradient
    # Previously I removed `overlay overlay-show overlay-op-9`. Let's restore it with the gradient.
    page_header_pattern = re.compile(r'(<section class="page-header[^"]*")(.*?>)')
    def add_bg(m):
        if 'style=' in m.group(2):
            return m.group(1) + re.sub(r'style="([^"]*)"', r'style="\1 background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url(\'img/fotosdetrabajos_nuevas/Porfido patagonico 10x10 mixto Barrio privado Los troncos, berazategui 1.jpg\'); background-size: cover; background-position: center;"', m.group(2))
        else:
            return m.group(1) + ' style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url(\'img/fotosdetrabajos_nuevas/Porfido patagonico 10x10 mixto Barrio privado Los troncos, berazategui 1.jpg\'); background-size: cover; background-position: center;"' + m.group(2)
            
    col_html = page_header_pattern.sub(add_bg, col_html)
    
    # Copy the gallery from index.html to colocaciones.html
    # Find gallery in index
    gallery_match = re.search(r'(<div id="trabajos" class="container-gallery.*?</div>\s*</div>\s*</div>\s*</div>)', html, re.DOTALL)
    if gallery_match:
        gallery_code = gallery_match.group(1)
        # Find where to put it in colocaciones
        # Colocaciones has <div class="container py-5 mt-3"> or similar
        old_col_gallery_pattern = re.compile(r'<div class="container py-5 mt-3">.*?</div>\s*</div>\s*</div>\s*</div>', re.DOTALL)
        if old_col_gallery_pattern.search(col_html):
            col_html = old_col_gallery_pattern.sub(gallery_code, col_html)
        else:
            # Maybe it uses a different class now since I didn't update it yet
            pass

    # Ensure lightbox JS and HTML is at the bottom of colocaciones.html
    if '<!-- Lightbox Modal -->' not in col_html:
        lightbox_match = re.search(r'(<!-- Lightbox Modal -->.*?</script>)', html, re.DOTALL)
        if lightbox_match:
            col_html = col_html.replace('</body>', lightbox_match.group(1) + '\n</body>')

    with open('colocaciones.html', 'w', encoding='utf-8') as f:
        f.write(col_html)

if __name__ == '__main__':
    main()
