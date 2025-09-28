/**
 * Module de gestion des avis clients
 */

class ReviewsManager {
    constructor() {
        this.reviews = [];
        this.reviewsPerPage = 6;
        this.currentPage = 1;
        this.totalPages = 1;
        
        // Éléments DOM
        this.reviewsGrid = document.getElementById('reviews-grid');
        this.reviewsPagination = document.getElementById('reviews-pagination');
        this.averageRating = document.getElementById('average-rating');
        this.averageStars = document.getElementById('average-stars');
        this.totalReviewsElement = document.getElementById('total-reviews');
        
        // Ticker d'avis pour la section About
        this.tickerReviews = [];
        this.tickerRefreshInterval = null;
        this.currentPanelIndex = 0;
        this.panelInterval = null;
        
        this.init();
    }
    
    async init() {
        try {
            await this.loadReviews();
            
            if (this.reviews.length === 0) {
                console.warn('Aucun avis trouvé - affichage désactivé');
                this.hideReviewsSection();
                return;
            }
            
            console.log(`✅ ${this.reviews.length} avis réels chargés`);
            this.updateStats();
            this.renderReviews();
            this.renderPagination();
            this.initCarousel();
        } catch (error) {
            console.error('Erreur initialisation reviews:', error);
            this.hideReviewsSection();
        }
    }
    
    async loadReviews() {
        try {
            const response = await fetch('data/reviews.json');
            if (!response.ok) throw new Error('Impossible de charger les avis');
            
            const data = await response.json();
            this.reviews = data.reviews || [];
            
            console.log(`${this.reviews.length} avis chargés`);
        } catch (error) {
            console.error('Erreur chargement avis:', error);
            throw error;
        }
    }
    
    hideReviewsSection() {
        // Masquer les sections d'avis si aucun avis réel n'est disponible
        const reviewsSection = document.getElementById('reviews');
        const tickerSection = document.querySelector('.reviews-ticker');
        
        if (reviewsSection) {
            reviewsSection.style.display = 'none';
            console.log('Section avis masquée - aucun avis réel disponible');
        }
        
        if (tickerSection) {
            tickerSection.style.display = 'none';
            console.log('Ticker avis masqué - aucun avis réel disponible');
        }
    }
    
    updateStats() {
        if (this.reviews.length === 0) return;
        
        // Calculer la moyenne des notes
        const totalRating = this.reviews.reduce((sum, review) => sum + review.rating, 0);
        const average = (totalRating / this.reviews.length).toFixed(1);
        
        // Mettre à jour l'affichage
        if (this.averageRating) {
            this.averageRating.textContent = average;
        }
        
        if (this.totalReviewsElement) {
            this.totalReviewsElement.textContent = this.reviews.length;
        }
        
        // Mettre à jour les étoiles
        if (this.averageStars) {
            this.updateStarsDisplay(this.averageStars, Math.round(parseFloat(average)));
        }
    }
    
    updateStarsDisplay(container, rating) {
        if (!container) return;
        
        const stars = container.querySelectorAll('i');
        stars.forEach((star, index) => {
            if (index < rating) {
                star.className = 'fas fa-star';
                star.style.color = '#ffc107';
            } else {
                star.className = 'far fa-star';
                star.style.color = '#ddd';
            }
        });
    }
    
    renderReviews() {
        if (!this.reviewsGrid) return;
        
        // Calculer les avis pour la page courante
        const startIndex = (this.currentPage - 1) * this.reviewsPerPage;
        const endIndex = startIndex + this.reviewsPerPage;
        const reviewsToShow = this.reviews.slice(startIndex, endIndex);
        
        // Générer le HTML
        this.reviewsGrid.innerHTML = reviewsToShow.map(review => `
            <div class="review-card" data-review-id="${review.id}">
                <div class="review-header">
                    <span class="review-author">${this.escapeHtml(review.username || review.author || 'Client')}</span>
                    <div class="review-rating">
                        ${this.generateStarsHtml(review.rating)}
                    </div>
                </div>
                <div class="review-text">
                    "${this.escapeHtml(review.comment || review.text || '')}"
                </div>
                <div class="review-date">
                    ${this.escapeHtml(review.date)}
                </div>
            </div>
        `).join('');
        
        // Animer l'apparition des cartes
        this.animateCards();
    }
    
    generateStarsHtml(rating) {
        const stars = [];
        for (let i = 1; i <= 5; i++) {
            if (i <= rating) {
                stars.push('<i class="fas fa-star"></i>');
            } else {
                stars.push('<i class="far fa-star"></i>');
            }
        }
        return stars.join('');
    }
    
    animateCards() {
        const cards = this.reviewsGrid.querySelectorAll('.review-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.5s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }
    
    renderPagination() {
        if (!this.reviewsPagination) return;
        
        this.totalPages = Math.ceil(this.reviews.length / this.reviewsPerPage);
        
        if (this.totalPages <= 1) {
            this.reviewsPagination.style.display = 'none';
            return;
        }
        
        this.reviewsPagination.style.display = 'flex';
        
        let paginationHtml = '';
        
        // Bouton précédent
        paginationHtml += `
            <button onclick="reviewsManager.goToPage(${this.currentPage - 1})" 
                    ${this.currentPage === 1 ? 'disabled' : ''}>
                <i class="fas fa-chevron-left"></i>
            </button>
        `;
        
        // Numéros de page
        for (let i = 1; i <= this.totalPages; i++) {
            paginationHtml += `
                <button onclick="reviewsManager.goToPage(${i})" 
                        class="${i === this.currentPage ? 'active' : ''}">
                    ${i}
                </button>
            `;
        }
        
        // Bouton suivant
        paginationHtml += `
            <button onclick="reviewsManager.goToPage(${this.currentPage + 1})" 
                    ${this.currentPage === this.totalPages ? 'disabled' : ''}>
                <i class="fas fa-chevron-right"></i>
            </button>
        `;
        
        this.reviewsPagination.innerHTML = paginationHtml;
    }
    
    goToPage(page) {
        if (page < 1 || page > this.totalPages) return;
        
        this.currentPage = page;
        this.renderReviews();
        this.renderPagination();
        
        // Scroll vers le haut de la section
        const reviewsSection = document.getElementById('reviews');
        if (reviewsSection) {
            reviewsSection.scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
    
    initCarousel() {
        // Trouver le container du ticker dans la section About
        const tickerContainer = document.getElementById('reviews-ticker-content');
        if (!tickerContainer) {
            console.log('Container ticker About non trouvé');
            return;
        }
        
        // Sélectionner des avis aléatoires pour le ticker
        this.tickerReviews = this.getRandomReviews(Math.min(this.reviews.length, 12));
        
        if (this.tickerReviews.length > 0) {
            this.renderTicker();
            this.startTickerAnimation();
        }
    }
    
    getRandomReviews(count) {
        const shuffled = [...this.reviews].sort(() => 0.5 - Math.random());
        return shuffled.slice(0, count);
    }
    
    renderTicker() {
        const tickerContainer = document.getElementById('reviews-ticker-content');
        if (!tickerContainer) return;
        
        // S'assurer qu'on a assez d'avis pour une boucle continue
        let reviewsToShow = [...this.tickerReviews];
        
        // Si moins de 6 avis, les dupliquer pour avoir assez de contenu
        while (reviewsToShow.length < 6) {
            reviewsToShow = [...reviewsToShow, ...this.tickerReviews];
        }
        
        // Quadrupler les avis pour une boucle parfaitement continue sans gap
        const quadrupleReviews = [
            ...reviewsToShow, 
            ...reviewsToShow, 
            ...reviewsToShow, 
            ...reviewsToShow
        ];
        
        // Créer le contenu HTML du ticker avec espacement optimisé
        tickerContainer.innerHTML = quadrupleReviews.map((review, index) => `
            <div class="ticker-review-item" data-index="${index}" style="margin-bottom: 25px;">
                <div class="ticker-review-text">
                    ${this.escapeHtml(review.comment || review.text || '')}
                </div>
                <div class="ticker-review-meta">
                    <span class="ticker-review-author">${this.escapeHtml(review.username || review.author || 'Client')}</span>
                    <div class="ticker-review-stars">
                        ${this.generateStarsHtml(review.rating)}
                    </div>
                </div>
            </div>
        `).join('');
        
        console.log(`🎢 Ticker rendu avec ${quadrupleReviews.length} avis (${this.tickerReviews.length} originaux x4)`);
    }
    
    startTickerAnimation() {
        // Le ticker défile automatiquement avec l'animation CSS
        // Pas besoin d'interval JavaScript, tout est géré par CSS
        console.log('🎬 Animation ticker démarrée (CSS)');
        
        // Randomiser les avis plus fréquemment pour éviter la monotonie
        this.tickerRefreshInterval = setInterval(() => {
            this.refreshTickerContent();
        }, 45000); // Changer le contenu toutes les 45 secondes (moins que l'animation de 55s)
    }
    
    refreshTickerContent() {
        // Mélanger à nouveau les avis pour plus de variété
        this.tickerReviews = this.getRandomReviews(Math.min(this.reviews.length, 12));
        this.renderTicker();
        console.log('🔄 Contenu du ticker rafraîchi');
    }
    
    stopCarousel() {
        if (this.tickerRefreshInterval) {
            clearInterval(this.tickerRefreshInterval);
            this.tickerRefreshInterval = null;
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Instance globale
let reviewsManager;

// Initialisation quand le DOM est prêt
document.addEventListener('DOMContentLoaded', () => {
    reviewsManager = new ReviewsManager();
});

// Export pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ReviewsManager;
}