const body = document.body;
const slides = document.querySelectorAll('.slide');
const leftBtn = document.getElementById('left');
const rightBtn = document.getElementById('right');

let activeSlide = 0;
let activeImageSrc = '';

rightBtn.addEventListener('click', () => {
  activeSlide++;

  if (activeSlide > slides.length - 1) {
    activeSlide = 0;
  }

  setActiveSlide();
});

leftBtn.addEventListener('click', () => {
  activeSlide--;

  if (activeSlide < 0) {
    activeSlide = slides.length - 1;
  }

  setActiveSlide();
});

function setActiveSlide() {
  slides.forEach((slide) => {
    slide.classList.remove('active');
    slide.querySelector('.slide-image').classList.remove('active-image');
  });

  const activeSlideElement = slides[activeSlide];
  activeSlideElement.classList.add('active');
  activeSlideElement
    .querySelector('.slide-image')
    .classList.add('active-image');

  activeImageSrc = activeSlideElement
    .querySelector('.slide-image img')
    .getAttribute('src');
}
