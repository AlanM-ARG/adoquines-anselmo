import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    start_str = '<div class="owl-carousel-wrapper"'
    # find the end of the owl-carousel-wrapper
    # it ends with `</div>\n            </div>\n\n            <div class="container"` or something similar.
    end_str = '</header>'
    
    # Let's extract the wrapper precisely
    start_idx = html.find(start_str)
    
    # We want to replace everything inside `<div class="owl-carousel-wrapper" ...> ... </div>` completely.
    # We can do this by finding the next major section:
    # After the carousel wrapper, there is usually something like `<div class="container py-4">` or similar.
    # Let's search for `<!-- Carousel Slides -->` and the end of the carousel.
    # Actually, the best way is to use regex or string methods.
    
    # Let's find the closing tag of owl-carousel-wrapper
    # The structure is:
    # <div class="owl-carousel-wrapper" style="height: 845px;">
    #   <div class="owl-carousel ...">
    #     ... slides ...
    #   </div>
    # </div>
    # <div class="container py-4">
    
    # To be safe, let's find the exact block using regex.
    # The block starts at `start_idx`. The end is right before the next `<div class="container`
    end_idx = html.find('<div id="home-intro"', start_idx)
    if end_idx == -1:
        end_idx = html.find('<section id="materiales"', start_idx)
        
    if end_idx == -1:
        # Just find the 2nd </div> after the last slide
        pass

    new_carousel = '''<div class="owl-carousel-wrapper position-relative" style="height: 845px;">
                <!-- NEW OVERLAY TEXT CONTAINER -->
                <div id="carousel-text-overlay" class="position-absolute top-50 start-50 translate-middle z-index-3 text-center w-100" style="pointer-events: none;">
                    <div class="container">
                        <div class="row justify-content-center">
                            <div class="col-lg-10 text-center" style="pointer-events: auto;">
                                <h1 id="carousel-title" class="text-color-light font-weight-bold line-height-1 text-7 text-md-10 positive-ls-1 mb-5" style="text-shadow: 0 2px 10px rgba(0,0,0,0.5); transition: opacity 0.5s ease-in-out;">
                                    Colocadores de piedra con más de 30 años de experiencia.
                                </h1>
                                <a href="index.html#trabajos"
                                    class="btn btn-custom-dark font-weight-bold text-3-5 px-4 py-3 rounded">
                                    Ver nuestros trabajos
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="owl-carousel dots-inside dots-horizontal-center show-dots-hover show-dots-xs show-dots-sm
                         show-dots-md nav-style-1 nav-inside nav-inside-plus nav-light nav-lg nav-font-size-lg mb-0"
                    data-plugin-options="{'responsive': {'0': {'items': 1, 'dots': true, 'nav': true}, '479': {'items': 1, 'dots': true},
                         '768': {'items': 1, 'dots': true}, '979': {'items': 1}, '1199': {'items': 1}}, 'loop': true, 'autoHeight': false,
                         'margin': 0, 'dots': false, 'dotsVerticalOffset': '-235px', 'nav': true, 'navVerticalOffset': '70px', 'animateIn': 'fadeIn',
                         'animateOut': 'fadeOut', 'mouseDrag': false, 'touchDrag': false, 'pullDrag': false, 'autoplay': false,
                         'rewind': false}">

                    <!-- Slide 1 -->
                    <div class="position-relative overlay overlay-show overlay-op-3 overflow-hidden pt-4"
                        style="height: 845px;">
                        <div class="background-image-wrapper position-absolute top-0 left-0 right-0 bottom-0"
                            data-appear-animation="kenBurnsToLeft" data-appear-animation-duration="30s"
                            data-plugin-options="{'minWindowWidth': 0}" data-carousel-onchange-show=""
                            style="background-image: url(img/products/porfido-mixto-colocacion-1.jpg); background-size: cover; background-position: center; background-color: #000;">
                        </div>
                    </div>
                    
                    <!-- Slide 2 -->
                    <div class="position-relative overlay overlay-show overlay-op-3 overflow-hidden pt-4"
                        style="height: 845px;">
                        <div class="background-image-wrapper position-absolute top-0 left-0 right-0 bottom-0"
                            data-appear-animation="kenBurnsToLeft" data-appear-animation-duration="30s"
                            data-plugin-options="{'minWindowWidth': 0}" data-carousel-onchange-show=""
                            style="background-image: url(img/products/cortado-a-disco-porfido-mixto-colocacion-4.jpeg); background-size: cover; background-position: center; background-color: #000;">
                        </div>
                    </div>

                </div>
            </div>

            <!-- Custom Vanilla JS Script for Sync and Autoplay -->
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    const titles = [
                        "Colocadores de piedra con más de 30 años de experiencia.",
                        "Especialistas en colocación de Pórfido y Granitullo."
                    ];
                    const titleElement = document.getElementById('carousel-title');
                    
                    // The owl carousel is initialized automatically by theme.js.
                    // We can hook into it using jQuery since the theme uses it.
                    // If we MUST use vanilla JS for the hook, we can poll for the active item or use jQuery events.
                    // Since theme.js initializes it, jQuery is present. We will use it just for the hook.
                    
                    let intervalId = null;
                    const autoplayTime = 4000;
                    
                    function startAutoplay() {
                        clearInterval(intervalId);
                        intervalId = setInterval(function() {
                            $('.owl-carousel').trigger('next.owl.carousel');
                        }, autoplayTime);
                    }
                    
                    startAutoplay();

                    // Hook into changed event
                    $('.owl-carousel').on('changed.owl.carousel', function(event) {
                        const count = event.item.count;
                        if(count === 0) return;
                        
                        // calculate active index
                        // event.item.index is the current index including clones (loop: true).
                        // the easiest way is to use modulus.
                        let realIndex = event.item.index - event.relatedTarget._clones.length / 2;
                        if(realIndex >= count) { realIndex = realIndex % count; }
                        if(realIndex < 0) { realIndex = count + realIndex; }
                        
                        // Fade out
                        titleElement.style.opacity = 0;
                        setTimeout(() => {
                            titleElement.innerHTML = titles[realIndex];
                            titleElement.style.opacity = 1;
                        }, 500); // 500ms matches CSS transition
                    });

                    // Listen to manual clicks on next/prev buttons to restart autoplay
                    // The theme generates .owl-nav .owl-next and .owl-prev
                    $(document).on('click', '.owl-next, .owl-prev', function() {
                        startAutoplay();
                    });
                });
            </script>
'''

    # To be extremely precise, I will extract exactly what to replace.
    # The previous wrapper started at `start_idx`
    # Let's find the exact end of `<div class="owl-carousel-wrapper"` block.
    # I can use a simple script to count nested divs.
    
    if start_idx != -1:
        div_count = 0
        i = start_idx
        end_wrapper_idx = -1
        while i < len(html):
            if html[i:i+4] == '<div':
                div_count += 1
                i += 4
            elif html[i:i+6] == '</div>':
                div_count -= 1
                i += 6
                if div_count == 0:
                    end_wrapper_idx = i
                    break
            else:
                i += 1
        
        if end_wrapper_idx != -1:
            final_html = html[:start_idx] + new_carousel + html[end_wrapper_idx:]
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(final_html)
            print("Carousel refactored successfully.")
        else:
            print("Could not find end of carousel wrapper")
    else:
        print("Could not find start of carousel wrapper")

if __name__ == '__main__':
    main()
