import os
import re

def rebuild_colocaciones():
    with open('colocaciones.html', 'r', encoding='utf-8') as f:
        col_html = f.read()

    start_str = '<div class="container py-5 my-5">'
    end_str = '<section class="section section-height-3 bg-primary-darken'
    
    start_idx = col_html.find(start_str)
    end_idx = col_html.find(end_str)
    
    # We need to find the last </div> before end_idx
    last_div = col_html.rfind('</div>', start_idx, end_idx)
    # Actually wait, the container closes with a </div>. Let's just replace everything inside the container.
    # The structure in colocaciones.html currently has `<div class="container py-5 my-5">` followed by `<div id="trabajos"...`
    # The container ends exactly before `<section class="section section-height-3 bg-primary-darken`.
    
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

    gallery_html += '            </div>\n\n            '

    new_html = col_html[:start_idx] + gallery_html + col_html[end_idx:]

    with open('colocaciones.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Gallery rebuilt.")

if __name__ == '__main__':
    rebuild_colocaciones()
