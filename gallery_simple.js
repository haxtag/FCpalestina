/**
 * Version simplifiée de la galerie pour éviter les erreurs
 */

// Configuration simple
const SIMPLE_CONFIG = {
    API_BASE_URL: '/data',
    IMAGES_BASE_URL: '/assets/images/jerseys',
    THUMBNAILS_BASE_URL: '/assets/images/thumbnails'
};

// Fonctions utilitaires simples
function simpleDebounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function simpleHandleError(error, context = 'Unknown') {
    console.error(`[${context}]`, error);
}

function simpleToggleLoading(show) {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.classList.toggle('active', show);
    }
}

// Classe de galerie simplifiée
class SimpleGallery {
    constructor() {
        this.galleryGrid = document.getElementById('gallery-grid');
        this.filterButtons = document.querySelectorAll('.filter-btn');
        this.searchInput = document.getElementById('search-input');
        this.currentCategory = 'all';
        this.currentSearch = '';
        
        this.init();
    }

    init() {
        console.log('🚀 Initialisation de la galerie simplifiée');
        this.bindEvents();
        this.loadJerseys();
    }

    bindEvents() {
        // Filtres
        this.filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.handleCategoryFilter(e.target.dataset.filter);
            });
        });

        // Recherche
        if (this.searchInput) {
            this.searchInput.addEventListener('input', 
                simpleDebounce((e) => {
                    this.handleSearch(e.target.value);
                }, 300)
            );
        }
    }

    handleCategoryFilter(category) {
        // Mettre à jour l'état actif des boutons
        this.filterButtons.forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.filter === category) {
                btn.classList.add('active');
            }
        });

        this.currentCategory = category;
        this.loadJerseys();
    }

    handleSearch(searchTerm) {
        this.currentSearch = searchTerm;
        this.loadJerseys();
    }

    async loadJerseys() {
        try {
            console.log('📡 Chargement des maillots...');
            simpleToggleLoading(true);

            const response = await fetch(`${SIMPLE_CONFIG.API_BASE_URL}/jerseys.json`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const jerseys = await response.json();
            console.log(`✅ ${jerseys.length} maillots chargés`);

            // Filtrer les maillots
            let filteredJerseys = jerseys;

            if (this.currentCategory !== 'all') {
                filteredJerseys = filteredJerseys.filter(jersey => 
                    jersey.category === this.currentCategory
                );
            }

            if (this.currentSearch) {
                const searchLower = this.currentSearch.toLowerCase();
                filteredJerseys = filteredJerseys.filter(jersey =>
                    jersey.title.toLowerCase().includes(searchLower) ||
                    jersey.description.toLowerCase().includes(searchLower)
                );
            }

            this.displayJerseys(filteredJerseys);

        } catch (error) {
            simpleHandleError(error, 'SimpleGallery.loadJerseys');
            this.showErrorMessage();
        } finally {
            simpleToggleLoading(false);
        }
    }

    displayJerseys(jerseys) {
        if (!this.galleryGrid) {
            console.error('❌ Élément gallery-grid non trouvé');
            return;
        }

        this.galleryGrid.innerHTML = '';

        if (!jerseys || jerseys.length === 0) {
            this.showNoResultsMessage();
            return;
        }

        jerseys.forEach((jersey, index) => {
            const jerseyElement = this.createJerseyElement(jersey);
            this.galleryGrid.appendChild(jerseyElement);
            
            // Animation d'apparition
            setTimeout(() => {
                jerseyElement.classList.add('fade-in-up');
            }, index * 100);
        });

        console.log(`✅ ${jerseys.length} maillots affichés`);
    }

    createJerseyElement(jersey) {
        const article = document.createElement('article');
        article.className = 'gallery-item';
        article.dataset.category = jersey.category;
        article.dataset.id = jersey.id;

    const imageUrl = jersey.thumbnail || (jersey.images && jersey.images[0]) || 'placeholder.jpg';
    const imagePath = /^https?:/i.test(imageUrl) ? imageUrl : `${SIMPLE_CONFIG.IMAGES_BASE_URL}/${imageUrl}`;

        article.innerHTML = `
            <div class="gallery-item-image">
                <img 
                    src="${imagePath}" 
                    alt="${jersey.title}"
                    loading="lazy"
                    onerror="this.style.display='none'"
                >
                <div class="gallery-item-overlay">
                    <i class="fas fa-search-plus"></i>
                </div>
            </div>
            <div class="gallery-item-content">
                <h3 class="gallery-item-title">${jersey.title || jersey.name || 'Maillot'}</h3>
                <p class="gallery-item-description">${jersey.description || ''}</p>
                <div class="gallery-item-meta">
                    <span class="gallery-item-category">${this.getCategoryDisplayName(jersey.category)}</span>
                    <span class="gallery-item-year">${jersey.year}</span>
                </div>
            </div>
        `;

        // Ajouter l'événement de clic pour la modal
        article.addEventListener('click', () => {
            this.openJerseyModal(jersey);
        });

        return article;
    }

    getCategoryDisplayName(category) {
        const names = {
            'home': 'Domicile',
            'away': 'Extérieur',
            'special': 'Spéciaux',
            'vintage': 'Vintage',
            'keeper': 'Gardien'
        };
        return names[category] || category;
    }

    openJerseyModal(jersey) {
        console.log('🖼️ Ouverture de la modal pour:', jersey.title);
        // Pour l'instant, juste un alert
        alert(`Maillot: ${jersey.title}\nCatégorie: ${jersey.category}\nAnnée: ${jersey.year}`);
    }

    showNoResultsMessage() {
        this.galleryGrid.innerHTML = `
            <div class="no-results">
                <i class="fas fa-search"></i>
                <h3>Aucun maillot trouvé</h3>
                <p>Essayez de modifier vos critères de recherche</p>
            </div>
        `;
    }

    showErrorMessage() {
        this.galleryGrid.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Erreur de chargement</h3>
                <p>Impossible de charger les maillots. Veuillez réessayer.</p>
                <button class="btn btn-primary" onclick="location.reload()">Recharger</button>
            </div>
        `;
    }
}

// Initialisation automatique
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initialisation de la galerie simplifiée...');
    
    // Attendre un peu que le DOM soit prêt
    setTimeout(() => {
        try {
            window.simpleGallery = new SimpleGallery();
            console.log('✅ Galerie simplifiée initialisée avec succès');
        } catch (error) {
            console.error('❌ Erreur initialisation galerie simplifiée:', error);
        }
    }, 100);
});
