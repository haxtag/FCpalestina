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
    DEBUG: false
};

// Exposer la configuration globalement
window.CONFIG = CONFIG;

// Tentative de surcharge dynamique depuis le backend (stockage externe)
// Cela permet de définir des URLs publiques externes sans re-bundler le front.
(async () => {
    try {
        const res = await fetch('/api/config-public', { credentials: 'include' });
        if (res.ok) {
            const pub = await res.json();
            if (pub && typeof pub === 'object') {
                if (pub.images_base_url) {
                    window.CONFIG.IMAGES_BASE_URL = pub.images_base_url;
                }
                if (pub.thumbnails_base_url) {
                    window.CONFIG.THUMBNAILS_BASE_URL = pub.thumbnails_base_url;
                }
                if (window.CONFIG.DEBUG) {
                    console.log('[CONFIG] Bases images appliquées:', window.CONFIG.IMAGES_BASE_URL, window.CONFIG.THUMBNAILS_BASE_URL);
                }
            }
        }
    } catch (e) {
        if (window.CONFIG && window.CONFIG.DEBUG) {
            console.warn('[CONFIG] Impossible de charger /api/config-public:', e);
        }
    }
})();
