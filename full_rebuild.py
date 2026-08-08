import os
import shutil
import re

def full_rebuild():
    # 1. Restore original colocaciones
    shutil.copy('original_colocaciones.html', 'colocaciones.html')

    # 2. Rebuild Gallery in colocaciones
    with open('colocaciones.html', 'r', encoding='utf-8') as f:
        col_html = f.read()

    start_str = '<div class="container py-5 my-5">'
    end_str = '<section class="section section-height-3 bg-primary-darken'
    
    start_idx = col_html.find(start_str)
    end_idx = col_html.find(end_str)

    if start_idx == -1 or end_idx == -1:
        print("Error finding boundaries")
        return

    # Old images extraction
    old_imgs = re.findall(r'<img[^>]+src="([^"]+img/products/[^"]+)"', col_html[start_idx:end_idx])
    old_imgs = list(dict.fromkeys(old_imgs))

    # New images
    files = os.listdir('img/fotosdetrabajos_nuevas')
    groups = {
        'Plota de Granitullo Mixto': [f for f in files if 'PLOTA DE GRANITULLO 10X10 MIXTO' in f],
        'Plota de Granitullo Gris': [f for f in files if 'Plota de granitullo gris 10x10' in f],
        'Pórfido Patagónico y Mixto': [f for f in files if 'Porfido' in f and 'Proceso' not in f],
        'Pisos de Pórfido': [f for f in files if 'Proceso de colocacion' in f],
    }

    gallery_html = '<div class="container py-5 my-5">\n'
    
    for category, images in groups.items():
        gallery_html += f'''                <div class="row row-gutter-sm justify-content-center ">
                    <h4 class="text-color-black font-weight-extra-bold text-6 mb-4 appear-animation text-center mt-4" data-appear-animation="fadeInUpShorter" data-appear-animation-delay="200">
                        <em>{category}</em>
                    </h4>
                    <div class="d-flex justify-content-center align-items-center flex-column w-100 gap-4">
'''
        for img in images:
            gallery_html += f'                        <img src="img/fotosdetrabajos_nuevas/{img}" class="img-fluid" alt="{category}">\n'
        gallery_html += '                    </div>\n                </div>\n'

    # Append old images
    gallery_html += '''                <div class="row row-gutter-sm justify-content-center ">
                    <h4 class="text-color-black font-weight-extra-bold text-6 mb-4 appear-animation text-center mt-4" data-appear-animation="fadeInUpShorter" data-appear-animation-delay="200">
                        <em>Trabajos Anteriores</em>
                    </h4>
                    <div class="d-flex justify-content-center align-items-center flex-column w-100 gap-4">
'''
    for src in old_imgs:
        gallery_html += f'                        <img src="{src}" class="img-fluid" alt="Trabajo Anterior">\n'
    gallery_html += '                    </div>\n                </div>\n'

    gallery_html += '            </div>\n\n            '

    # Assemble
    new_html = col_html[:start_idx] + gallery_html + col_html[end_idx:]
    with open('colocaciones.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

if __name__ == '__main__':
    full_rebuild()
