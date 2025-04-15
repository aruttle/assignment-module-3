document.addEventListener('DOMContentLoaded', function () {
    const swiper = new Swiper('.mySwiper', {
      loop: true,
      slidesPerView: 1,
      spaceBetween: 30,
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
    });
  });
  