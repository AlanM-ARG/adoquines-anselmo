import os
import re

def rebuild_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    # 1. Routing fixes
    html = re.sub(r'href="#"\s*(class="nav-link[^>]*>\s*INICIO)', r'href="index.html" \1', html)
    
    # 2. Rebuild Gallery
    img_dir = os.path.join('img', 'fotosdetrabajos_nuevas')
    categories = {
        'Plota de Granitullo Mixto': [],
        'Plota de Granitullo Gris': [],
        'Pórfido Patagónico y Mixto': [],
        'Pisos de Pórfido': []
    }
    
    files = sorted(os.listdir(img_dir))
    for filename in files:
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')): continue
        name = filename.lower()
        if 'granitullo gris' in name: categories['Plota de Granitullo Gris'].append(filename)
        elif 'granitullo' in name: categories['Plota de Granitullo Mixto'].append(filename)
        elif 'proceso' in name: categories['Pisos de Pórfido'].append(filename)
        elif 'porfido' in name: categories['Pórfido Patagónico y Mixto'].append(filename)
        else: categories['Pórfido Patagónico y Mixto'].append(filename)

    gallery_html = '''
            <div id="trabajos" class="container-gallery py-5 mt-3">
                <div class="d-flex flex-column flex-md-row justify-content-md-between align-items-center mb-5 text-center text-md-start">
                    <h2 class="text-color-dark font-weight-extra-bold text-10 mb-3 mb-md-0 appear-animation"
                        data-appear-animation="fadeInUpShorter" data-appear-animation-delay="200">
                        NUESTROS TRABAJOS
                    </h2>
                    <a href="https://wa.me/5491170046534" class="btn btn-custom-red font-weight-bold text-3-5 px-4 py-3 rounded appear-animation btn-mobile-centered mt-4" data-appear-animation="fadeInUpShorter" data-appear-animation-delay="300">
                        <i class="fas fa-clipboard-list me-2"></i> Solicitar Presupuesto
                    </a>
                </div>
    '''
    
    for cat_name, items in categories.items():
        if not items: continue
        gallery_html += f'''
                <div class="col-12 mt-5 mb-4">
                    <h3 class="font-weight-bold text-7 text-color-dark">{cat_name}</h3>
                </div>
                <div class="row row-cols-1 row-cols-md-2 row-cols-lg-2 g-4 mb-5 gallery-container">'''
        for filename in items:
            gallery_html += f'''
                    <div class="col">
                        <img src="img/fotosdetrabajos_nuevas/{filename}" class="img-fluid lightbox-trigger w-100" alt="{cat_name} - Colocación de adoquines" style="aspect-ratio: 16/9; object-fit: cover;">
                    </div>'''
        gallery_html += '''
                </div>'''

    gallery_html += '''
            </div>
    '''
    
    # Precise extraction for gallery
    start_trabajos = html.find('<div id="trabajos" class="container py-5 mt-3">')
    end_trabajos = html.find('<div id="nosotros"')
    
    if start_trabajos != -1 and end_trabajos != -1:
        html = html[:start_trabajos] + gallery_html + '\n            ' + html[end_trabajos:]
    
    # 3. Add Lightbox Modal HTML at bottom
    lightbox_html = '''
    <!-- Lightbox Modal -->
    <div id="custom-lightbox" class="lightbox-modal">
        <span class="lightbox-close" id="lightbox-close">&times;</span>
        <img class="lightbox-content" id="lightbox-img">
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var modal = document.getElementById('custom-lightbox');
            var modalImg = document.getElementById('lightbox-img');
            var closeBtn = document.getElementById('lightbox-close');
            document.body.addEventListener('click', function(e) {
                if (e.target.classList.contains('lightbox-trigger')) {
                    modal.classList.add('show');
                    modalImg.src = e.target.src;
                }
            });
            closeBtn.addEventListener('click', function() {
                modal.classList.remove('show');
            });
            modal.addEventListener('click', function(e) {
                if (e.target !== modalImg) {
                    modal.classList.remove('show');
                }
            });
        });
    </script>
'''
    if '<!-- Lightbox Modal -->' not in html:
        html = html.replace('</body>', lightbox_html + '\n</body>')

    # 4. Carousel Fixes (nav: true, remove hover)
    html = html.replace('show-nav-hover', '') 
    html = html.replace("'0': {'items': 1, 'dots': true, 'nav': false}", "'0': {'items': 1, 'dots': true, 'nav': true}") 
    
    # 5. Inject 16 images into carousel
    slides_html = ""
    images = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    for i, img in enumerate(images):
        title = "Colocadores de piedra con más de 30 años de experiencia." if i == 0 else "Especialistas en colocación de Pórfido y Granitullo."
        slides_html += f'''
                    <!-- Carousel Slide {i+1} -->
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
                                    <a href="index.html#trabajos" class="btn btn-custom-dark font-weight-bold text-3-5 px-4 py-3 rounded appear-animation" data-appear-animation="fadeInUpShorterPlus" data-appear-animation-delay="200">
                                        Ver nuestros trabajos
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>'''

    start_carousel = html.find('<!-- Carousel Slide 1 -->')
    end_carousel = html.find('<div id="trabajos"')
    
    if start_carousel != -1 and end_carousel != -1:
        # We need to preserve the closing divs of the carousel wrapper
        closing_divs = '\n                </div>\n            </div>\n\n            '
        html = html[:start_carousel] + '<!-- Carousel Slides -->\n' + slides_html + closing_divs + html[end_carousel:]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Rebuild index.html successful")

if __name__ == '__main__':
    rebuild_index()
