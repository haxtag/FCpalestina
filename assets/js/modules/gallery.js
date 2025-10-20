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
        this.itemsPerPage = 12; // 12 maillots par page pour meilleur affichage
        this.totalPages = 0;
        this.totalItems = 0;
        // Définition des tags (chargée au premier fetch)
        this.tagsDef = null;
    // Définition des catégories (chargée au premier fetch)
    this.categoriesDef = null;
        
        this.galleryGrid = document.getElementById('gallery-grid');
        this.filterButtons = document.querySelectorAll('.filter-btn');
        this.searchInput = document.getElementById('search-input');
        this.loadMoreBtn = document.getElementById('load-more');
        this.paginationContainer = document.getElementById('pagination-container');
        
        this.init();
    }

    /**
     * Initialisation de la galerie
     */
    init() {
        this.bindEvents();
        this.loadJerseys();
        this.updateFilterButtons(); // Mettre à jour les boutons avec couleurs
        
        // Écouter les événements de mise à jour de l'admin
        document.addEventListener('forceReloadGallery', (event) => {
            console.log('🔄 Événement de rechargement reçu, mise à jour de la galerie...');
            this.loadJerseys();
        });
        
        document.addEventListener('adminDataUpdated', (event) => {
            console.log('🔄 Données admin mises à jour, synchronisation...');
            this.loadJerseys();
        });

        // Réagir aux mises à jour provenant d'autres onglets (localStorage)
        window.addEventListener('storage', (e) => {
            if (e.key === 'fcp-admin-update') {
                console.log('🛰️ Signal admin reçu depuis un autre onglet, rafraîchissement...');
                this.refresh();
            }
        });
    }

    /**
     * Mettre à jour les boutons de filtre avec les couleurs des catégories
     */
    async updateFilterButtons() {
        try {
            // Charger les catégories avec leurs couleurs
            const ts = Date.now();
            const response = await fetch(`/data/categories.json?t=${ts}`, { cache: 'no-store' });
            if (response.ok) {
                const categories = await response.json();
                
                // Mettre à jour chaque bouton de filtre
                this.filterButtons.forEach(btn => {
                    const filter = btn.dataset.filter;
                    if (filter === 'all') {
                        // Bouton "Tous" avec dégradé spécial
                        btn.style.cssText += `
                            background: linear-gradient(135deg, #8B1538, #A61E47) !important;
                            color: white !important;
                            border: 2px solid #8B1538 !important;
                            position: relative;
                            overflow: hidden;
                        `;
                        return;
                    }
                    
                    // Trouver la catégorie correspondante
                    const category = categories.find(cat => cat.id === filter);
                    if (category && category.color) {
                        // Appliquer la couleur de la catégorie
                        btn.style.cssText += `
                            --category-color: ${category.color};
                            background: white !important;
                            color: ${category.color} !important;
                            border: 2px solid ${category.color} !important;
                            position: relative;
                            overflow: hidden;
                            transition: all 0.3s ease !important;
                        `;
                        
                        // Ajouter un pseudo-élément de couleur
                        btn.addEventListener('mouseenter', () => {
                            btn.style.background = category.color + ' !important';
                            btn.style.color = 'white !important';
                        });
                        
                        btn.addEventListener('mouseleave', () => {
                            if (!btn.classList.contains('active')) {
                                btn.style.background = 'white !important';
                                btn.style.color = category.color + ' !important';
                            }
                        });
                        
                        // Mettre à jour l'état actif
                        if (btn.classList.contains('active')) {
                            btn.style.background = category.color + ' !important';
                            btn.style.color = 'white !important';
                        }
                    }
                });
            }
        } catch (error) {
            console.warn('⚠️ Impossible de charger les couleurs des catégories:', error);
        }
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
        // Mettre à jour l'état actif des boutons avec maintien des couleurs
        this.filterButtons.forEach(btn => {
            btn.classList.remove('active');
            const filter = btn.dataset.filter;
            
            if (filter === category) {
                btn.classList.add('active');
                // Maintenir la couleur active
                if (filter === 'all') {
                    btn.style.background = 'linear-gradient(135deg, #8B1538, #A61E47) !important';
                    btn.style.color = 'white !important';
                } else {
                    const categoryColor = btn.style.getPropertyValue('--category-color') || '#8B1538';
                    btn.style.background = categoryColor + ' !important';
                    btn.style.color = 'white !important';
                }
            } else {
                // Restaurer l'état inactif
                if (filter === 'all') {
                    btn.style.background = 'linear-gradient(135deg, #8B1538, #A61E47) !important';
                    btn.style.color = 'white !important';
                } else {
                    const categoryColor = btn.style.getPropertyValue('--category-color') || '#8B1538';
                    btn.style.background = 'white !important';
                    btn.style.color = categoryColor + ' !important';
                }
            }
        });

        // Réinitialiser et charger
        this.currentCategory = category;
        this.currentPage = 1;
        this.totalPages = 0;
        this.totalItems = 0;
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
                    const ts = Date.now();
                    const tagsRes = await fetch(`/data/tags.json?t=${ts}`, { cache: 'no-store' });
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

            // Charger la définition des catégories une seule fois
            if (!this.categoriesDef) {
                try {
                    const ts = Date.now();
                    const catRes = await fetch(`/data/categories.json?t=${ts}`, { cache: 'no-store' });
                    if (catRes.ok) {
                        const ct = catRes.headers.get('content-type') || '';
                        if (ct.includes('application/json')) {
                            this.categoriesDef = await catRes.json();
                        }
                    }
                } catch (e) {
                    console.warn('⚠️ Impossible de charger categories.json');
                }
            }

            // Charger directement depuis le fichier JSON pour avoir les données les plus récentes
            const tsNow = Date.now();
            const response = await fetch(`/data/jerseys.json?t=${tsNow}`, { cache: 'no-store' });
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
            
            // Pagination - calculer le nombre total de pages
            this.totalItems = filteredJerseys.length;
            this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage);
            
            const startIndex = (this.currentPage - 1) * this.itemsPerPage;
            const endIndex = startIndex + this.itemsPerPage;
            const pageJerseys = filteredJerseys.slice(startIndex, endIndex);
            
            if (append) {
                this.appendJerseys(pageJerseys);
            } else {
                this.displayJerseys(pageJerseys);
            }

            // Mettre à jour les contrôles de pagination
            this.updatePagination();
            this.updateLoadMoreButton({
                hasNext: this.currentPage < this.totalPages,
                total: this.totalItems,
                current: this.currentPage,
                totalPages: this.totalPages
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

    // Tous les maillots doivent avoir une thumbnail valide
    const imageUrl = jersey.thumbnail || (jersey.images && jersey.images[0]);
    
    // Si pas d'image, on ne devrait jamais arriver ici (données nettoyées)
    if (!imageUrl) {
        console.error('Maillot sans image détecté:', jersey);
        return; // Ne pas créer la carte
    }
    
    // Si l'URL commence déjà par http, on la garde telle quelle, sinon on prepend le dossier local
    const imagePath = /^https?:/i.test(imageUrl) ? imageUrl : `${window.CONFIG.IMAGES_BASE_URL}/${imageUrl}`;

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
                <h3 class="gallery-item-title">${sanitizeHTML(jersey.title || jersey.name || 'Maillot')}</h3>
                <p class="gallery-item-description">${sanitizeHTML(jersey.description || '')}</p>
                <div class="gallery-item-meta">
                    <span class="gallery-item-category">${this.getCategoryName(jersey.category)}</span>
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
        const byId = new Map((this.tagsDef || []).map(t => [norm(t.id), { name: t.name, color: t.color || '#6c757d' }]));
        const byName = new Map((this.tagsDef || []).map(t => [norm(t.name), { name: t.name, color: t.color || '#6c757d' }]));
        const fallback = new Map([
            ['home', { name: 'Domicile', color: '#8B1538' }],
            ['away', { name: 'Extérieur', color: '#000000' }],
            ['special', { name: 'Spéciaux', color: '#FFD700' }],
            ['vintage', { name: 'Vintage', color: '#8B4513' }],
            ['limited', { name: 'Édition limitée', color: '#FF6B6B' }],
            ['fcpalestina', { name: 'Maillots Du Peuple', color: '#8B1538' }],
            ['nouveau', { name: 'Nouveau', color: '#28a745' }],
            ['selection', { name: 'Sélection', color: '#17a2b8' }],
            ['domicile', { name: 'Domicile', color: '#8B1538' }],
            ['exterieur', { name: 'Extérieur', color: '#000000' }],
            ['pasbeau', { name: 'PASBEAU', color: '#dc3545' }]
        ]);
        const seen = new Set();
        const pills = [];
        (tags || []).forEach(raw => {
            const n = norm(raw);
            const info = byId.get(n) || byName.get(n) || fallback.get(n) || null;
            if (!info) return;
            const key = norm(info.name);
            if (seen.has(key)) return;
            seen.add(key);
            pills.push(`<span class="tag" style="background-color: ${info.color}; color: white; border: 1px solid ${info.color};">${sanitizeHTML(info.name)}</span>`);
        });
        return pills.join('');
    }

    // Nom de catégorie depuis categories.json si dispo, sinon fallback jerseyAPI
    getCategoryName(catId) {
        if (!catId) return 'Non spécifiée';
        try {
            const list = this.categoriesDef || [];
            const found = list.find(c => c.id === catId);
            if (found && found.name) return found.name;
            const fallback = { 'home': 'Domicile', 'away': 'Extérieur', 'special': 'Spéciaux', 'vintage': 'Vintage', 'keeper': 'Gardien' };
            const jerseyApiName = (typeof jerseyAPI?.getCategoryDisplayName === 'function') ? jerseyAPI.getCategoryDisplayName(catId) : null;
            return fallback[catId] || jerseyApiName || `Catégorie supprimée (${catId})`;
        } catch (e) {
            console.warn('⚠️ Erreur getCategoryName:', e);
            return 'Catégorie inconnue';
        }
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
        this.totalPages = 0;
        this.totalItems = 0;
        this.galleryGrid.innerHTML = '';
        this.loadJerseys();
    }

    /**
     * Mettre à jour les contrôles de pagination
     */
    updatePagination() {
        if (!this.paginationContainer) return;

        // Si on a moins de 2 pages, cacher la pagination
        if (this.totalPages <= 1) {
            this.paginationContainer.innerHTML = '';
            this.paginationContainer.style.display = 'none';
            return;
        }

        this.paginationContainer.style.display = 'block';

        let paginationHTML = '<div class="pagination-controls">';
        
        // Bouton Précédent
        paginationHTML += `<button class="pagination-btn" onclick="gallery.goToPage(${this.currentPage - 1})" ${this.currentPage <= 1 ? 'disabled' : ''}>
            <i class="fas fa-chevron-left"></i>
        </button>`;

        // Pages - logique d'affichage intelligente
        const maxVisiblePages = 7;
        let startPage = Math.max(1, this.currentPage - Math.floor(maxVisiblePages / 2));
        let endPage = Math.min(this.totalPages, startPage + maxVisiblePages - 1);

        // Ajuster si on est près de la fin
        if (endPage - startPage < maxVisiblePages - 1) {
            startPage = Math.max(1, endPage - maxVisiblePages + 1);
        }

        // Première page si nécessaire
        if (startPage > 1) {
            paginationHTML += `<button class="pagination-btn" onclick="gallery.goToPage(1)">1</button>`;
            if (startPage > 2) {
                paginationHTML += `<span class="pagination-ellipsis">...</span>`;
            }
        }

        // Pages visibles
        for (let i = startPage; i <= endPage; i++) {
            paginationHTML += `<button class="pagination-btn ${i === this.currentPage ? 'active' : ''}" onclick="gallery.goToPage(${i})">${i}</button>`;
        }

        // Dernière page si nécessaire
        if (endPage < this.totalPages) {
            if (endPage < this.totalPages - 1) {
                paginationHTML += `<span class="pagination-ellipsis">...</span>`;
            }
            paginationHTML += `<button class="pagination-btn" onclick="gallery.goToPage(${this.totalPages})">${this.totalPages}</button>`;
        }

        // Bouton Suivant
        paginationHTML += `<button class="pagination-btn" onclick="gallery.goToPage(${this.currentPage + 1})" ${this.currentPage >= this.totalPages ? 'disabled' : ''}>
            <i class="fas fa-chevron-right"></i>
        </button>`;

        // Info pagination
        paginationHTML += `<div class="pagination-info">
            Page ${this.currentPage} sur ${this.totalPages} (${this.totalItems} maillots)
        </div>`;

        paginationHTML += '</div>';
        
        this.paginationContainer.innerHTML = paginationHTML;
    }

    /**
     * Aller à une page spécifique
     * @param {number} page - Numéro de la page
     */
    goToPage(page) {
        if (page < 1 || page > this.totalPages || page === this.currentPage) return;
        
        this.currentPage = page;
        this.loadJerseys(false);
        
        // Scroll vers le haut de la galerie
        this.galleryGrid.scrollIntoView({ behavior: 'smooth', block: 'start' });
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
        background: linear-gradient(45deg, rgba(219, 112, 147, 0.8), rgba(255, 192, 203, 0.6));
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

    /* Styles pour la pagination */
    .pagination-controls {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: var(--spacing-sm);
        margin: var(--spacing-xl) 0;
        flex-wrap: wrap;
    }

    .pagination-btn {
        padding: var(--spacing-sm) var(--spacing-md);
        border: 2px solid var(--primary);
        background: var(--white);
        color: var(--primary);
        border-radius: var(--border-radius);
        cursor: pointer;
        transition: all var(--transition-normal);
        font-weight: 600;
        min-width: 40px;
        text-align: center;
    }

    .pagination-btn:hover:not(:disabled) {
        background: var(--primary);
        color: var(--white);
        transform: translateY(-2px);
    }

    .pagination-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        transform: none;
    }

    .pagination-btn.active {
        background: var(--primary);
        color: var(--white);
    }

    .pagination-info {
        margin: 0 var(--spacing-md);
        font-weight: 600;
        color: var(--text-dark);
    }

    @media (max-width: 768px) {
        .pagination-controls {
            gap: var(--spacing-xs);
        }
        
        .pagination-btn {
            padding: var(--spacing-xs) var(--spacing-sm);
            min-width: 35px;
            font-size: var(--font-size-sm);
        }
        
        .pagination-info {
            font-size: var(--font-size-sm);
            margin: 0 var(--spacing-sm);
        }
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
