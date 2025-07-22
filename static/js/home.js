document.addEventListener('DOMContentLoaded', function() {
    // Slider for "WHAT OUR CLIENTS SAY"
    const reviewSlider = document.querySelector('.review-slider');
    const reviewItems = document.querySelectorAll('.review-item');
    const reviewPrev = document.createElement('button');
    const reviewNext = document.createElement('button');
    let reviewIndex = 0;

    reviewPrev.innerHTML = '&laquo;'; // Left arrow
    reviewNext.innerHTML = '&raquo;'; // Right arrow
    reviewPrev.className = 'slider-btn prev';
    reviewNext.className = 'slider-btn next';

    reviewSlider.parentElement.insertBefore(reviewPrev, reviewSlider);
    reviewSlider.parentElement.appendChild(reviewNext);

    function showReviewSlide(index) {
        reviewSlider.scrollLeft = reviewItems[index].offsetLeft - reviewSlider.offsetLeft;
    }

    reviewPrev.addEventListener('click', function() {
        reviewIndex = (reviewIndex > 0) ? reviewIndex - 1 : reviewItems.length - 1;
        showReviewSlide(reviewIndex);
    });

    reviewNext.addEventListener('click', function() {
        reviewIndex = (reviewIndex < reviewItems.length - 1) ? reviewIndex + 1 : 0;
        showReviewSlide(reviewIndex);
    });

    // Slider for "TOP HEALTH ARTICLES"
    const articleSlider = document.querySelector('.article-slider');
    const articleItems = document.querySelectorAll('.article-item');
    const articlePrev = document.createElement('button');
    const articleNext = document.createElement('button');
    let articleIndex = 0;

    articlePrev.innerHTML = '&laquo;'; // Left arrow
    articleNext.innerHTML = '&raquo;'; // Right arrow
    articlePrev.className = 'slider-btn prev';
    articleNext.className = 'slider-btn next';

    articleSlider.parentElement.insertBefore(articlePrev, articleSlider);
    articleSlider.parentElement.appendChild(articleNext);

    function showArticleSlide(index) {
        articleSlider.scrollLeft = articleItems[index].offsetLeft - articleSlider.offsetLeft;
    }

    articlePrev.addEventListener('click', function() {
        articleIndex = (articleIndex > 0) ? articleIndex - 1 : articleItems.length - 1;
        showArticleSlide(articleIndex);
    });

    articleNext.addEventListener('click', function() {
        articleIndex = (articleIndex < articleItems.length - 1) ? articleIndex + 1 : 0;
        showArticleSlide(articleIndex);
    });


    
});
document.addEventListener('DOMContentLoaded', () => {
    const reviews = document.querySelectorAll('.review-card');
    let activeIndex = 0;

    function updateCarousel() {
        reviews.forEach((review, index) => {
            review.classList.remove('active');
            if (index === activeIndex) {
                review.style.transform = 'scale(1.2)';
                review.style.opacity = '1';
                review.classList.add('active');
            } else {
                review.style.transform = 'scale(0.8)';
                review.style.opacity = '0.8';
            }
        });
    }

    document.getElementById('prevReview').addEventListener('click', () => {
        activeIndex = (activeIndex - 1 + reviews.length) % reviews.length;
        updateCarousel();
    });

    document.getElementById('nextReview').addEventListener('click', () => {
        activeIndex = (activeIndex + 1) % reviews.length;
        updateCarousel();
    });

    updateCarousel(); // Initialize the carousel
});
