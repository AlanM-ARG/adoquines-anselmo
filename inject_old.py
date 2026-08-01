import os
import re

def main():
    with open('original_colocaciones.html', 'r', encoding='utf-8') as f:
        old_html = f.read()
    
    old_imgs = re.findall(r'<img[^>]+src="([^"]+img/products/[^"]+)"', old_html)
    old_imgs = list(dict.fromkeys(old_imgs))
    
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

    with open('colocaciones.html', 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'Trabajos Anteriores' not in content:
        # Find the end of the gallery before the section
        # Look for the last '</div>' before '<section class="section section-height-3'
        insertion_point = content.find('<section class="section section-height-3')
        if insertion_point != -1:
            # We want to insert just before the last </div> before this section
            # The gallery container is `<div id="trabajos"...` and ends with `</div>`
            # Let's find the `</div>` that closes the gallery.
            last_div = content.rfind('</div>', 0, insertion_point)
            if last_div != -1:
                new_content = content[:last_div] + old_imgs_html + '\n            </div>\n' + content[last_div + 6:]
                with open('colocaciones.html', 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print("Injected old images successfully.")

if __name__ == '__main__':
    main()
