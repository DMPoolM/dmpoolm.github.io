// Navigation remains fully functional without JavaScript.
// Mark the current section for assistive technology as the reader scrolls.
const sectionLinks = [...document.querySelectorAll('nav a')];
const sections = [...document.querySelectorAll('main > section[id]')];
if ('IntersectionObserver' in window && sections.length) {
  const observer = new IntersectionObserver(entries => {
    const current = entries.find(entry => entry.isIntersecting);
    if (!current) return;
    sectionLinks.forEach(link => {
      if (link.hash === `#${current.target.id}`) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }, { rootMargin: '-15% 0px -60% 0px', threshold: 0 });
  sections.forEach(section => observer.observe(section));
}
