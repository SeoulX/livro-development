var carousel = document.querySelector('.carousel');
var carouselInner = document.querySelector('.carousel-inner');
var images = carouselInner.querySelectorAll('img');

var currentImageIndex = 0;

function rotateImages() {
  currentImageIndex++;
  if (currentImageIndex >= images.length) {
    currentImageIndex = 0;
  }

  carouselInner.classList.remove('active');
  images[currentImageIndex].classList.add('active');

  setTimeout(rotateImages, 5000);
}

rotateImages();