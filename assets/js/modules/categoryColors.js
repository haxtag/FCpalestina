/**
 * Module de gestion dynamique des couleurs de catégories
 * Charge les couleurs depuis categories.json et les applique aux boutons filtres
 */

class CategoryColorManager {
    constructor() {
        this.categories = [];
        this.styleElement = null;
    }

    /**
     * Initialisation - charge les catégories et applique les couleurs
     */
    async init() {
        await this.loadCategories();
        this.applyColors();
    }

    /**
     * Charge les catégories depuis le fichier JSON
     */
    async loadCategories() {
        try {
            const response = await fetch('/data/categories.json?t=' + Date.now());
            if (response.ok) {
                this.categories = await response.json();
                console.log('✅ Catégories chargées:', this.categories);
            } else {
                console.warn('⚠️ Impossible de charger categories.json');
            }
        } catch (error) {
            console.error('❌ Erreur lors du chargement des catégories:', error);
        }
    }

    /**
     * Applique les couleurs dynamiquement via CSS
     */
    applyColors() {
        // Créer ou réutiliser l'élément style
        if (!this.styleElement) {
            this.styleElement = document.createElement('style');
            this.styleElement.id = 'dynamic-category-colors';
            document.head.appendChild(this.styleElement);
        }

        // Générer le CSS dynamique
        let css = '';

        // Bouton "Tous" - toujours bordeaux
        css += `
.filter-btn[data-filter="all"] {
    border-color: #8B1538 !important;
    color: #8B1538 !important;
    background: transparent !important;
}

.filter-btn[data-filter="all"].active {
    background: #8B1538 !important;
    color: #ffffff !important;
    border-color: #8B1538 !important;
}
`;

        // Générer le CSS pour chaque catégorie
        this.categories.forEach(category => {
            const { id, color } = category;
            
            // Style pour l'état non actif (contour + texte coloré, fond transparent)
            css += `
.filter-btn[data-filter="${id}"] {
    border-color: ${color} !important;
    color: ${color} !important;
    background: transparent !important;
}

`;
            
            // Style pour l'état actif (fond coloré + texte blanc)
            css += `
.filter-btn[data-filter="${id}"].active {
    background: ${color} !important;
    color: #ffffff !important;
    border-color: ${color} !important;
}

`;
        });

        // Appliquer le CSS généré
        this.styleElement.textContent = css;
        console.log('✅ Couleurs dynamiques appliquées pour', this.categories.length, 'catégories');
    }

    /**
     * Rafraîchir les couleurs (utile si categories.json est modifié)
     */
    async refresh() {
        await this.loadCategories();
        this.applyColors();
    }
}

// Créer et initialiser le gestionnaire de couleurs au chargement de la page
const categoryColorManager = new CategoryColorManager();

// Initialiser dès que le DOM est prêt
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => categoryColorManager.init());
} else {
    categoryColorManager.init();
}

// Exposer globalement pour permettre un refresh manuel si besoin
window.categoryColorManager = categoryColorManager;
