import re

def main():
    with open('original_colocaciones.html', 'r', encoding='utf-8') as f:
        old_html = f.read()
    
    old_imgs = re.findall(r'<img[^>]+src="([^"]+img/products/[^"]+)"', old_html)
    old_imgs = list(dict.fromkeys(old_imgs))
    
    old_imgs_html = '''                <div class="row row-gutter-sm justify-content-center ">
                    <h4 class="text-color-black font-weight-extra-bold text-6 mb-4 appear-animation text-center mt-4" data-appear-animation="fadeInUpShorter" data-appear-animation-delay="200">
                        <em>Trabajos Anteriores</em>
                    </h4>
                    <div class="d-flex justify-content-center align-items-center flex-column w-100 gap-4">
'''
    for src in old_imgs:
        old_imgs_html += f'                        <img src="{src}" class="img-fluid" alt="Trabajo Anterior">\n'
    old_imgs_html += '                    </div>\n                </div>\n'

    with open('colocaciones.html', 'r', encoding='utf-8') as f:
        col_html = f.read()
        
    end_str = '            </div>\n\n            <section class="section section-height-3 bg-primary-darken'
    end_idx = col_html.find(end_str)
    
    if end_idx != -1:
        new_html = col_html[:end_idx] + old_imgs_html + col_html[end_idx:]
        with open('colocaciones.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        print("Injected old images successfully.")

if __name__ == '__main__':
    main()
