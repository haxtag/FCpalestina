/**
 * Module API pour la gestion des données des maillots
 */

class JerseyAPI {
    constructor() {
        this.baseURL = '/data';
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }

    /**
     * Récupérer tous les maillots
     * @param {Object} options - Options de filtrage et pagination
     * @returns {Promise<Array>} - Liste des maillots
     */
    async getJerseys(options = {}) {
        const {
            page = 1,
            limit = 12,
            category = 'all',
            search = '',
            sortBy = 'date',
            sortOrder = 'desc'
        } = options;

        const cacheKey = `jerseys_${JSON.stringify(options)}`;
        
        // Vérifier le cache
        if (this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < this.cacheTimeout) {
                return cached.data;
            }
        }

        try {
            // Simuler un appel API (remplacer par un vrai appel)
            const response = await this.fetchJerseysFromFile();
            let filteredJerseys = response;

            // Appliquer les filtres
            if (category !== 'all') {
                filteredJerseys = filteredJerseys.filter(jersey => 
                    jersey.category === category
                );
            }

            if (search) {
                const searchLower = search.toLowerCase();
                filteredJerseys = filteredJerseys.filter(jersey =>
                    jersey.title.toLowerCase().includes(searchLower) ||
                    jersey.description.toLowerCase().includes(searchLower) ||
                    jersey.tags.some(tag => tag.toLowerCase().includes(searchLower))
                );
            }

            // Appliquer le tri
            filteredJerseys.sort((a, b) => {
                let aValue = a[sortBy];
                let bValue = b[sortBy];

                if (sortBy === 'date') {
                    aValue = new Date(aValue);
                    bValue = new Date(bValue);
                }

                if (sortOrder === 'asc') {
                    return aValue > bValue ? 1 : -1;
                } else {
                    return aValue < bValue ? 1 : -1;
                }
            });

            // Appliquer la pagination
            const startIndex = (page - 1) * limit;
            const endIndex = startIndex + limit;
            const paginatedJerseys = filteredJerseys.slice(startIndex, endIndex);

            const result = {
                jerseys: paginatedJerseys,
                pagination: {
                    currentPage: page,
                    totalPages: Math.ceil(filteredJerseys.length / limit),
                    totalItems: filteredJerseys.length,
                    hasNext: endIndex < filteredJerseys.length,
                    hasPrev: page > 1
                }
            };

            // Mettre en cache
            this.cache.set(cacheKey, {
                data: result,
                timestamp: Date.now()
            });

            return result;

        } catch (error) {
            handleError(error, 'JerseyAPI.getJerseys');
            throw error;
        }
    }

    /**
     * Récupérer un maillot par ID
     * @param {string} id - ID du maillot
     * @returns {Promise<Object>} - Données du maillot
     */
    async getJerseyById(id) {
        try {
            const response = await this.fetchJerseysFromFile();
            const jersey = response.find(j => j.id === id);
            
            if (!jersey) {
                throw new Error(`Maillot avec l'ID ${id} non trouvé`);
            }

            return jersey;
        } catch (error) {
            handleError(error, 'JerseyAPI.getJerseyById');
            throw error;
        }
    }

    /**
     * Récupérer les catégories disponibles
     * @returns {Promise<Array>} - Liste des catégories
     */
    async getCategories() {
        try {
            // Essayer d'abord de charger depuis le fichier des catégories
            const response = await fetch(`${this.baseURL}/categories.json`);
            if (response.ok) {
                const categories = await response.json();
                return categories.map(cat => ({
                    id: cat.id,
                    name: cat.name,
                    color: cat.color,
                    count: 0 // Sera calculé plus tard
                }));
            }
        } catch (error) {
            console.warn('Impossible de charger categories.json, fallback vers les maillots');
        }
        
        // Fallback : extraire les catégories des maillots
        try {
            const response = await this.fetchJerseysFromFile();
            const categories = [...new Set(response.map(jersey => jersey.category))];
            return categories.map(category => ({
                id: category,
                name: this.getCategoryDisplayName(category),
                color: '#8B1538',
                count: response.filter(jersey => jersey.category === category).length
            }));
        } catch (error) {
            handleError(error, 'JerseyAPI.getCategories');
            throw error;
        }
    }

    /**
     * Rechercher des maillots
     * @param {string} query - Terme de recherche
     * @returns {Promise<Array>} - Résultats de recherche
     */
    async searchJerseys(query) {
        if (!query.trim()) {
            return this.getJerseys();
        }

        return this.getJerseys({ search: query });
    }

    /**
     * Récupérer les maillots populaires
     * @param {number} limit - Nombre de maillots à retourner
     * @returns {Promise<Array>} - Maillots populaires
     */
    async getPopularJerseys(limit = 6) {
        try {
            const response = await this.fetchJerseysFromFile();
            return response
                .sort((a, b) => b.views - a.views)
                .slice(0, limit);
        } catch (error) {
            handleError(error, 'JerseyAPI.getPopularJerseys');
            throw error;
        }
    }

    /**
     * Récupérer les maillots récents
     * @param {number} limit - Nombre de maillots à retourner
     * @returns {Promise<Array>} - Maillots récents
     */
    async getRecentJerseys(limit = 6) {
        try {
            const response = await this.fetchJerseysFromFile();
            return response
                .sort((a, b) => new Date(b.date) - new Date(a.date))
                .slice(0, limit);
        } catch (error) {
            handleError(error, 'JerseyAPI.getRecentJerseys');
            throw error;
        }
    }

    /**
     * Charger les données depuis le fichier JSON
     * @returns {Promise<Array>} - Données des maillots
     */
    async fetchJerseysFromFile() {
        try {
            const response = await fetch(`${this.baseURL}/jerseys.json`);
            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            // Fallback avec des données de démonstration
            console.warn('Impossible de charger les données, utilisation des données de démonstration');
            return this.getDemoData();
        }
    }

    /**
     * Données de démonstration
     * @returns {Array} - Données de démonstration
     */
    getDemoData() {
        return [
            {
                id: 'jersey-1',
                title: 'Maillot Domicile 2024',
                description: 'Maillot officiel domicile FC Palestina saison 2024. Couleurs traditionnelles avec design moderne.',
                category: 'home',
                year: 2024,
                price: 89.99,
                images: [
                    'jersey-home-2024-1.jpg',
                    'jersey-home-2024-2.jpg',
                    'jersey-home-2024-3.jpg'
                ],
                thumbnail: 'jersey-home-2024-thumb.jpg',
                tags: ['domicile', '2024', 'officiel', 'moderne'],
                date: '2024-01-15',
                views: 1250,
                featured: true
            },
            {
                id: 'jersey-2',
                title: 'Maillot Extérieur 2024',
                description: 'Maillot officiel extérieur FC Palestina saison 2024. Design élégant pour les matchs à l\'extérieur.',
                category: 'away',
                year: 2024,
                price: 89.99,
                images: [
                    'jersey-away-2024-1.jpg',
                    'jersey-away-2024-2.jpg',
                    'jersey-away-2024-3.jpg'
                ],
                thumbnail: 'jersey-away-2024-thumb.jpg',
                tags: ['extérieur', '2024', 'officiel', 'élégant'],
                date: '2024-01-10',
                views: 980,
                featured: false
            },
            {
                id: 'jersey-3',
                title: 'Maillot Spécial Liberté',
                description: 'Maillot spécial édition limitée "Liberté" avec design unique et message de solidarité.',
                category: 'special',
                year: 2024,
                price: 129.99,
                images: [
                    'jersey-special-2024-1.jpg',
                    'jersey-special-2024-2.jpg',
                    'jersey-special-2024-3.jpg'
                ],
                thumbnail: 'jersey-special-2024-thumb.jpg',
                tags: ['spécial', 'liberté', 'édition limitée', 'solidarité'],
                date: '2024-02-01',
                views: 2100,
                featured: true
            },
            {
                id: 'jersey-4',
                title: 'Maillot Vintage 1990',
                description: 'Reproduction du maillot historique de 1990. Design rétro authentique.',
                category: 'vintage',
                year: 1990,
                price: 79.99,
                images: [
                    'jersey-vintage-1990-1.jpg',
                    'jersey-vintage-1990-2.jpg',
                    'jersey-vintage-1990-3.jpg'
                ],
                thumbnail: 'jersey-vintage-1990-thumb.jpg',
                tags: ['vintage', '1990', 'rétro', 'historique'],
                date: '2024-01-20',
                views: 750,
                featured: false
            },
            {
                id: 'jersey-5',
                title: 'Maillot Gardien 2024',
                description: 'Maillot officiel gardien de but FC Palestina saison 2024. Couleurs distinctives.',
                category: 'home',
                year: 2024,
                price: 99.99,
                images: [
                    'jersey-keeper-2024-1.jpg',
                    'jersey-keeper-2024-2.jpg',
                    'jersey-keeper-2024-3.jpg'
                ],
                thumbnail: 'jersey-keeper-2024-thumb.jpg',
                tags: ['gardien', '2024', 'officiel', 'distinctif'],
                date: '2024-01-25',
                views: 420,
                featured: false
            },
            {
                id: 'jersey-6',
                title: 'Maillot Célébration 2023',
                description: 'Maillot de célébration pour les victoires importantes de 2023. Design commémoratif.',
                category: 'special',
                year: 2023,
                price: 109.99,
                images: [
                    'jersey-celebration-2023-1.jpg',
                    'jersey-celebration-2023-2.jpg',
                    'jersey-celebration-2023-3.jpg'
                ],
                thumbnail: 'jersey-celebration-2023-thumb.jpg',
                tags: ['célébration', '2023', 'commémoratif', 'victoire'],
                date: '2023-12-15',
                views: 1680,
                featured: true
            }
        ];
    }

    /**
     * Obtenir le nom d'affichage d'une catégorie
     * @param {string} category - ID de la catégorie
     * @returns {string} - Nom d'affichage
     */
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

    /**
     * Vider le cache
     */
    clearCache() {
        this.cache.clear();
    }

    /**
     * Synchroniser avec Yupoo (à implémenter)
     * @returns {Promise<boolean>} - Succès de la synchronisation
     */
    async syncWithYupoo() {
        try {
            // TODO: Implémenter la synchronisation avec Yupoo
            showNotification('Synchronisation avec Yupoo en cours...', 'info');
            
            // Simulation d'une synchronisation
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            this.clearCache();
            showNotification('Synchronisation terminée !', 'success');
            return true;
        } catch (error) {
            handleError(error, 'JerseyAPI.syncWithYupoo');
            showNotification('Erreur lors de la synchronisation', 'error');
            return false;
        }
    }
}

// ===== INSTANCE GLOBALE =====
const jerseyAPI = new JerseyAPI();

// ===== EXPORT POUR UTILISATION MODULAIRE =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = JerseyAPI;
}
