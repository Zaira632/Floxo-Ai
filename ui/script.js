document.addEventListener('DOMContentLoaded', () => {
  const elements = document.querySelectorAll('a[href^="#"]');
  elements.forEach((link) => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      const target = document.querySelector(link.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
});
