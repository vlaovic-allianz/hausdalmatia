/* Haus Dalmatia · Bewegung beim Scrollen mit GSAP 3.13 + ScrollTrigger
   Ergänzt die Effekte der Seite (Lenis, Einblenden, Tagesreise). Aus bei „Bewegung reduzieren“. */
(function(){
  if (!window.gsap || !window.ScrollTrigger || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger);
  document.documentElement.classList.add('hd-gsap');
  // Sanftes Scrollen (Lenis) und ScrollTrigger im Gleichschritt
  if (window.hdLenis) hdLenis.on('scroll', ScrollTrigger.update);

  // Titelbild: Text gleitet beim Hinunterscrollen leicht nach oben und blendet aus
  var kids = gsap.utils.toArray('.hero-content > *');
  if (kids.length) gsap.to(kids, {
    y: function(i){ return -24 - i * 14; }, opacity: 0, ease: 'none',
    scrollTrigger: {trigger: '.hero', start: 'top top', end: 'center top', scrub: true}
  });

  // Bildtiefe: Fotos wandern im Rahmen minimal gegen die Scrollrichtung
  gsap.utils.toArray('.apt-img, .xf-img, .mosaic .m').forEach(function(box){
    var img = box.querySelector('img'); if (!img) return;
    gsap.fromTo(img, {'--py': '-4%'}, {'--py': '4%', ease: 'none',
      scrollTrigger: {trigger: box, start: 'top bottom', end: 'bottom top', scrub: true}});
  });

  // Lichtschein folgt der Maus auf den Karten „Direkt buchen“
  if (matchMedia('(hover: hover) and (pointer: fine)').matches)
    document.querySelectorAll('.benefit').forEach(function(c){
      c.addEventListener('pointermove', function(e){
        var r = c.getBoundingClientRect();
        c.style.setProperty('--mx', (e.clientX - r.left) + 'px'); c.style.setProperty('--my', (e.clientY - r.top) + 'px');
        c.classList.add('lit');
      });
      c.addEventListener('pointerleave', function(){ c.classList.remove('lit'); });
    });

  // Maße neu berechnen, wenn Bilder und Schriften geladen sind
  addEventListener('load', function(){ ScrollTrigger.refresh(); });
  if (document.fonts) document.fonts.ready.then(function(){ ScrollTrigger.refresh(); });
})();
