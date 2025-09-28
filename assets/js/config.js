/**
 * Configuration globale du portfolio FC Palestina
 */

const CONFIG = {
    // URLs
    API_BASE_URL: '/data',
    IMAGES_BASE_URL: '/assets/images/jerseys',
    THUMBNAILS_BASE_URL: '/assets/images/thumbnails',
    
    // Pagination
    ITEMS_PER_PAGE: 12,
    
    // Animation
    ANIMATION_DELAY: 100,
    
    // Debug
    DEBUG: true
};

// Exposer la configuration globalement
window.CONFIG = CONFIG;
