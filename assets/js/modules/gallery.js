/**
 * Module Gallery pour la gestion de la galerie de maillots
 */

class Gallery {
    constructor() {
        this.currentPage = 1;
        this.currentCategory = 'all';
        this.currentSearch = '';
        this.currentSort = 'date';
        this.currentOrder = 'desc';
        this.isLoading = false;
        this.hasMoreItems = true;
        // Définition des tags (chargée au premier fetch)
        this.tagsDef = null;
        
        this.galleryGrid = document.getElementById('gallery-grid');
        this.filterButtons = document.querySelectorAll('.filter-btn');
        this.searchInput = document.getElementById('search-input');
        this.loadMoreBtn = document.getElementById('load-more');
        
        this.init();
    }

    /**
     * Initialisation de la galerie
     */
    init() {
        this.bindEvents();
        this.loadJerseys();
        
        // Écouter les événements de mise à jour de l'admin
        document.addEventListener('forceReloadGallery', (event) => {
            console.log('🔄 Événement de rechargement reçu, mise à jour de la galerie...');
            this.loadJerseys();
        });
        
        document.addEventListener('adminDataUpdated', (event) => {
            console.log('🔄 Données admin mises à jour, synchronisation...');
            this.loadJerseys();
        });
    }

    /**
     * Liaison des événements
     */
    bindEvents() {
        // Filtres par catégorie
        this.filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.handleCategoryFilter(e.target.dataset.filter);
            });
        });

        // Recherche
        if (this.searchInput) {
            this.searchInput.addEventListener('input', 
                debounce((e) => {
                    this.handleSearch(e.target.value);
                }, 300)
            );
        }

        // Bouton "Charger plus"
        if (this.loadMoreBtn) {
            this.loadMoreBtn.addEventListener('click', () => {
                this.loadMoreJerseys();
            });
        }

        // Scroll infini (optionnel)
        this.setupInfiniteScroll();
    }

    /**
     * Gestion du filtre par catégorie
     * @param {string} category - Catégorie sélectionnée
     */
    handleCategoryFilter(category) {
        // Mettre à jour l'état actif des boutons
        this.filterButtons.forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.filter === category) {
                btn.classList.add('active');
            }
        });

        // Réinitialiser et charger
        this.currentCategory = category;
        this.currentPage = 1;
        this.hasMoreItems = true;
        this.galleryGrid.innerHTML = '';
        
        this.loadJerseys();
    }

    /**
     * Gestion de la recherche
     * @param {string} searchTerm - Terme de recherche
     */
    handleSearch(searchTerm) {
        this.currentSearch = searchTerm;
        this.currentPage = 1;
        this.hasMoreItems = true;
        this.galleryGrid.innerHTML = '';
        
        this.loadJerseys();
    }

    /**
     * Charger les maillots
     * @param {boolean} append - Ajouter aux maillots existants
     */
    async loadJerseys(append = false) {
        if (this.isLoading) return;

        this.isLoading = true;
        toggleLoading(true);

        try {
            console.log('🔄 Chargement des maillots...');
            
            // Charger la définition des tags une seule fois
            if (!this.tagsDef) {
                try {
                    const tagsRes = await fetch('/data/tags.json');
                    if (tagsRes.ok) {
                        const ct = tagsRes.headers.get('content-type') || '';
                        if (ct.includes('application/json')) {
                            this.tagsDef = await tagsRes.json();
                        }
                    }
                } catch (e) {
                    console.warn('⚠️ Impossible de charger tags.json');
                }
            }

            // Charger directement depuis le fichier JSON pour avoir les données les plus récentes
            const response = await fetch('/data/jerseys.json');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            const ct = response.headers.get('content-type') || '';
            if (!ct.includes('application/json')) {
                throw new Error('jerseys.json ne renvoie pas du JSON');
            }
            const allJerseys = await response.json();
            
            console.log('📦 Maillots chargés:', allJerseys.length);
            
            // Appliquer les filtres localement
            let filteredJerseys = allJerseys;
            
            // Filtrer par catégorie
            if (this.currentCategory !== 'all') {
                filteredJerseys = filteredJerseys.filter(jersey => 
                    jersey.category === this.currentCategory || 
                    (jersey.categories && jersey.categories.includes(this.currentCategory))
                );
            }
            
            // Filtrer par recherche
            if (this.currentSearch) {
                const searchTerm = this.currentSearch.toLowerCase();
                filteredJerseys = filteredJerseys.filter(jersey => 
                    (jersey.name && jersey.name.toLowerCase().includes(searchTerm)) ||
                    (jersey.title && jersey.title.toLowerCase().includes(searchTerm)) ||
                    (jersey.description && jersey.description.toLowerCase().includes(searchTerm)) ||
                    (jersey.tags && jersey.tags.some(tag => tag.toLowerCase().includes(searchTerm)))
                );
            }
            
            // Trier
            filteredJerseys.sort((a, b) => {
                let aValue, bValue;
                
                switch (this.currentSort) {
                    case 'date':
                        aValue = new Date(a.created_at || a.updated_at || 0);
                        bValue = new Date(b.created_at || b.updated_at || 0);
                        break;
                    case 'name':
                        aValue = (a.name || a.title || '').toLowerCase();
                        bValue = (b.name || b.title || '').toLowerCase();
                        break;
                    case 'year':
                        aValue = parseInt(a.year) || 0;
                        bValue = parseInt(b.year) || 0;
                        break;
                    default:
                        aValue = 0;
                        bValue = 0;
                }
                
                if (this.currentOrder === 'asc') {
                    return aValue > bValue ? 1 : -1;
                } else {
                    return aValue < bValue ? 1 : -1;
                }
            });
            
            // Pagination
            const startIndex = (this.currentPage - 1) * 12;
            const endIndex = startIndex + 12;
            const pageJerseys = filteredJerseys.slice(startIndex, endIndex);
            
            if (append) {
                this.appendJerseys(pageJerseys);
            } else {
                this.displayJerseys(pageJerseys);
            }

            // Mettre à jour l'état de pagination
            this.hasMoreItems = endIndex < filteredJerseys.length;
            this.updateLoadMoreButton({
                hasNext: this.hasMoreItems,
                total: filteredJerseys.length,
                current: this.currentPage
            });

        } catch (error) {
            console.error('❌ Erreur lors du chargement des maillots:', error);
            this.showErrorMessage();
        } finally {
            this.isLoading = false;
            toggleLoading(false);
        }
    }

    /**
     * Charger plus de maillots
     */
    async loadMoreJerseys() {
        if (!this.hasMoreItems || this.isLoading) return;

        this.currentPage++;
        await this.loadJerseys(true);
    }

    /**
     * Afficher les maillots
     * @param {Array} jerseys - Liste des maillots
     */
    displayJerseys(jerseys) {
        this.galleryGrid.innerHTML = '';
        this.appendJerseys(jerseys);
    }

    /**
     * Ajouter des maillots à la galerie
     * @param {Array} jerseys - Liste des maillots
     */
    appendJerseys(jerseys) {
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

        // Lazy loading des images
        this.setupLazyLoading();
    }

    /**
     * Créer un élément de maillot
     * @param {Object} jersey - Données du maillot
     * @returns {HTMLElement} - Élément DOM
     */
    createJerseyElement(jersey) {
        const article = document.createElement('article');
        article.className = 'gallery-item jersey-card';
        article.dataset.category = jersey.category;
        article.dataset.id = jersey.id;
        article.dataset.jerseyId = jersey.id;

        const imageUrl = jersey.thumbnail || jersey.images[0];
        const imagePath = `${window.CONFIG.IMAGES_BASE_URL}/${imageUrl}`;

        article.innerHTML = `
            <div class="gallery-item-image">
                <img 
                    src="${imagePath}" 
                    alt="${sanitizeHTML(jersey.title)}"
                    loading="lazy"
                    onerror="this.style.display='none'; this.parentElement.innerHTML='<div style=\\'background: linear-gradient(45deg, #2c5530, #4a7c59); color: white; display: flex; align-items: center; justify-content: center; height: 100%; border-radius: 8px;\\'>${sanitizeHTML(jersey.title)}</div>'"
                >
                <div class="gallery-item-overlay">
                    <i class="fas fa-search-plus"></i>
                </div>
            </div>
            <div class="gallery-item-content">
                <h3 class="gallery-item-title">${sanitizeHTML(jersey.title)}</h3>
                <p class="gallery-item-description">${sanitizeHTML(jersey.description)}</p>
                <div class="gallery-item-meta">
                    <span class="gallery-item-category">${jerseyAPI.getCategoryDisplayName(jersey.category)}</span>
                    <span class="gallery-item-year">${jersey.year}</span>
                </div>
                <div class="gallery-item-tags">${this.renderTags(jersey.tags)}</div>
                <!-- Debug: ${JSON.stringify(jersey.tags)} -->
            </div>
        `;

        // Ajouter l'événement de clic pour la modal
        article.addEventListener('click', () => {
            this.openJerseyModal(jersey);
        });

        return article;
    }

    // Rendu des tags basé sur la définition (id -> name) et dédoublonnage; ignore les tags inconnus
    renderTags(tags) {
        if (!tags || tags.length === 0) return '';
        const norm = (s) => (s || '').toString().normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase();
        const byId = new Map((this.tagsDef || []).map(t => [norm(t.id), t.name]));
        const byName = new Map((this.tagsDef || []).map(t => [norm(t.name), t.name]));
        const fallback = new Map([
            ['home','Domicile'],['away','Extérieur'],['special','Spéciaux'],['vintage','Vintage']
        ]);
        const seen = new Set();
        const pills = [];
        (tags || []).forEach(raw => {
            const n = norm(raw);
            const display = byId.get(n) || byName.get(n) || fallback.get(n) || null;
            if (!display) return;
            const key = norm(display);
            if (seen.has(key)) return;
            seen.add(key);
            pills.push(`<span class="tag">${sanitizeHTML(display)}</span>`);
        });
        return pills.join('');
    }

    /**
     * Ouvrir la modal d'un maillot
     * @param {Object} jersey - Données du maillot
     */
    openJerseyModal(jersey) {
        // Déclencher l'événement personnalisé pour la modal
        const event = new CustomEvent('openJerseyModal', {
            detail: { jersey }
        });
        document.dispatchEvent(event);
    }

    /**
     * Mettre à jour le bouton "Charger plus"
     * @param {Object} pagination - Informations de pagination
     */
    updateLoadMoreButton(pagination) {
        if (!this.loadMoreBtn) return;

        if (pagination.hasNext) {
            this.loadMoreBtn.style.display = 'block';
            this.loadMoreBtn.textContent = 'Charger Plus';
            this.loadMoreBtn.disabled = false;
        } else {
            this.loadMoreBtn.style.display = 'none';
        }
    }

    /**
     * Afficher le message "Aucun résultat"
     */
    showNoResultsMessage() {
        this.galleryGrid.innerHTML = `
            <div class="no-results">
                <i class="fas fa-search"></i>
                <h3>Aucun maillot trouvé</h3>
                <p>Essayez de modifier vos critères de recherche</p>
            </div>
        `;
    }

    /**
     * Afficher le message d'erreur
     */
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

    /**
     * Configuration du scroll infini
     */
    setupInfiniteScroll() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && this.hasMoreItems && !this.isLoading) {
                    this.loadMoreJerseys();
                }
            });
        }, {
            rootMargin: '100px'
        });

        // Observer le bouton "Charger plus"
        if (this.loadMoreBtn) {
            observer.observe(this.loadMoreBtn);
        }
    }

    /**
     * Configuration du lazy loading
     */
    setupLazyLoading() {
        const lazyImages = this.galleryGrid.querySelectorAll('img.lazy');
        lazyLoadImages(lazyImages);
    }

    /**
     * Rafraîchir la galerie
     */
    refresh() {
        this.currentPage = 1;
        this.hasMoreItems = true;
        this.galleryGrid.innerHTML = '';
        this.loadJerseys();
    }

    /**
     * Changer le tri
     * @param {string} sortBy - Champ de tri
     * @param {string} order - Ordre (asc/desc)
     */
    changeSort(sortBy, order = 'desc') {
        this.currentSort = sortBy;
        this.currentOrder = order;
        this.refresh();
    }

    /**
     * Obtenir les statistiques de la galerie
     * @returns {Object} - Statistiques
     */
    getStats() {
        const items = this.galleryGrid.querySelectorAll('.gallery-item');
        const categories = {};
        
        items.forEach(item => {
            const category = item.dataset.category;
            categories[category] = (categories[category] || 0) + 1;
        });

        return {
            totalItems: items.length,
            categories: categories,
            currentPage: this.currentPage,
            hasMore: this.hasMoreItems
        };
    }
}

// ===== STYLES POUR LES MESSAGES =====
const galleryStyles = `
    .no-results,
    .error-message {
        grid-column: 1 / -1;
        text-align: center;
        padding: var(--spacing-3xl);
        color: var(--text-light);
    }

    .no-results i,
    .error-message i {
        font-size: var(--font-size-5xl);
        color: var(--text-light);
        margin-bottom: var(--spacing-lg);
    }

    .no-results h3,
    .error-message h3 {
        font-size: var(--font-size-2xl);
        margin-bottom: var(--spacing-md);
        color: var(--text-dark);
    }

    .no-results p,
    .error-message p {
        font-size: var(--font-size-lg);
        margin-bottom: var(--spacing-xl);
    }

    .gallery-item {
        transition: all var(--transition-normal);
    }

    .gallery-item:hover {
        transform: translateY(-5px);
    }

    .gallery-item-image {
        position: relative;
        overflow: hidden;
    }

    .gallery-item-image img {
        transition: transform var(--transition-normal);
    }

    .gallery-item:hover .gallery-item-image img {
        transform: scale(1.05);
    }

    .gallery-item-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(44, 85, 48, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity var(--transition-normal);
    }

    .gallery-item:hover .gallery-item-overlay {
        opacity: 1;
    }

    .gallery-item-overlay i {
        color: var(--white);
        font-size: var(--font-size-3xl);
    }
`;

// Ajouter les styles au document
const styleSheet = document.createElement('style');
styleSheet.textContent = galleryStyles;
document.head.appendChild(styleSheet);

// ===== EXPORT POUR UTILISATION MODULAIRE =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Gallery;
}
