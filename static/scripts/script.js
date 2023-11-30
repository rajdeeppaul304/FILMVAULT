function generateStarRating(contForStar, rating) {
    const container = contForStar;
    container.innerHTML = '';

    // Ensure the rating is within the valid range (1 to 10)
    if (rating > 0) {
        
    } else{
        rating = 1
    }
    rating = Math.max(1, Math.min(10, rating));
    console.log(rating)
    // Calculate the number of full stars, half star, and empty stars
    const fullStars = Math.floor(rating / 2);
    const hasHalfStar = rating % 2 !== 0;

    // Create full stars
    for (let i = 0; i < fullStars; i++) {
    const star = document.createElement('span');
    star.className = 'fa fa-star checked';
    container.appendChild(star);
    }

    // Create half star if needed
    if (hasHalfStar) {
    const halfStar = document.createElement('span');
    halfStar.className = 'fa fa-star-half-o checked';
    container.appendChild(halfStar);
    }

    // Create empty stars
    const emptyStars = 5 - Math.ceil(rating / 2);
    for (let i = 0; i < emptyStars; i++) {
    const star = document.createElement('span');
    star.className = 'fa fa-star-o checked' ;
    container.appendChild(star);
    }
}
