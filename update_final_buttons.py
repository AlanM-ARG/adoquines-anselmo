import os
import re

# 1. Add CSS rules strictly as requested
css_addition = """
/* ESTILOS OBLIGATORIOS PARA BOTONES */
.btn-custom-dark {
    background-color: #353535 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    box-shadow: none !important;
    transition: background-color 0.3s ease !important;
    text-decoration: none !important;
}

.btn-custom-dark:hover {
    background-color: #454545 !important;
    color: #ffffff !important;
}

.btn-custom-red {
    background-color: #c9302c !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    box-shadow: 0 6px 12px rgba(0,0,0,0.2) !important;
    transition: background-color 0.3s ease, transform 0.3s ease !important;
    text-decoration: none !important;
}

.btn-custom-red:hover {
    background-color: #ac2925 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 16px rgba(0,0,0,0.3) !important;
    color: #ffffff !important;
}
"""

with open('css/index.css', 'a', encoding='utf-8') as f:
    f.write(css_addition)


html_files = ['index.html', 'colocaciones.html', 'contacto.html']

for file in html_files:
    if not os.path.exists(file):
        continue
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Header Button
    # Find any li containing the header button and replace the whole <li> block
    # It might be: <li class="d-flex align-items-center ms-lg-3 mt-3 mt-lg-0"> ... </li>
    # Or <li class="d-none d-lg-flex align-items-center ms-3"> ... </li>
    header_li_pattern = r'<li class="[^"]*align-items-center[^"]*">\s*<a href="https://wa\.me/5491135517563"[^>]*>\s*Solicitar Presupuesto\s*</a>\s*</li>'
    
    new_header_li = '''<li class="d-flex align-items-center ms-lg-3 mt-3 mt-lg-0">
                                                    <a href="https://wa.me/5491135517563" class="btn btn-custom-dark font-weight-bold text-3-5 px-4 py-3 rounded">
                                                        Solicitar Presupuesto
                                                    </a>
                                                </li>'''
    
    html = re.sub(header_li_pattern, new_header_li, html, flags=re.DOTALL)


    # 2. Update Trabajos Button (The ONLY Red Button)
    # The Trabajos button has the icon and says Solicitar Presupuesto. It is near "NUESTROS TRABAJOS".
    # Pattern: <a ...><i ...></i> Solicitar Presupuesto</a>
    red_btn_pattern = r'<a href="https://wa\.me/5491135517563"[^>]*>\s*<i class="fas fa-clipboard-list me-2"></i>\s*Solicitar Presupuesto\s*</a>'
    
    new_red_btn = '''<a href="https://wa.me/5491135517563" class="btn btn-custom-red font-weight-bold text-3-5 px-4 py-3 rounded appear-animation" data-appear-animation="fadeInUpShorter" data-appear-animation-delay="300">
                        <i class="fas fa-clipboard-list me-2"></i> Solicitar Presupuesto
                    </a>'''
    
    html = re.sub(red_btn_pattern, new_red_btn, html, flags=re.DOTALL)


    # 3. Update Hero Buttons
    # Pattern: <a href="#trabajos" ...> Ver nuestros trabajos </a>
    hero_btn_pattern = r'<a href="#trabajos"[^>]*>\s*Ver nuestros trabajos\s*</a>'
    
    # Needs to be dynamically rebuilt to keep appear-animations if they vary, or we can just replace the class string.
    # The user says: Asegúrate de que este botón también use la clase .btn-custom-dark y rounded. NO debe ser rojo.
    # Currently they might be class="btn btn-custom-red ..."
    
    def replace_hero_class(match):
        full_a = match.group(0)
        # Change btn-custom-red to btn-custom-dark
        full_a = full_a.replace('btn-custom-red', 'btn-custom-dark')
        # Add rounded if not present
        if 'rounded' not in full_a:
            full_a = full_a.replace('px-4 py-3', 'px-4 py-3 rounded')
        return full_a
    
    html = re.sub(hero_btn_pattern, replace_hero_class, html, flags=re.DOTALL)
    
    # Just to be completely sure, replace ANY btn-custom-red that doesn't have the clipboard icon with btn-custom-dark.
    # (Since there should be NO other red buttons)
    # However, the above step should catch all Hero buttons.
    # What about Footer buttons or anything else?
    # Let's do a broad sweep: any 'btn-custom-red' without the exact red button string.
    # Better to just stick to the precise replacements.

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)
