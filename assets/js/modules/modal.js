/**
 * Module Modal pour l'affichage des détails des maillots
 */

class JerseyModal {
    constructor() {
        this.modal = document.getElementById('image-modal');
        this.modalImage = document.getElementById('modal-image');
        this.modalTitle = document.getElementById('modal-title');
        this.modalDescription = document.getElementById('modal-description');
        this.closeBtn = document.querySelector('.modal-close');
        this.currentJersey = null;
        this.currentImageIndex = 0;
        this.jerseys = [];
        
        this.init();
    }

    /**
     * Initialisation de la modal
     */
    init() {
        this.bindEvents();
        this.setupKeyboardNavigation();
    }

    /**
     * Liaison des événements
     */
    bindEvents() {
        // Fermeture de la modal
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => {
                this.close();
            });
        }

        // Fermeture en cliquant sur l'arrière-plan
        if (this.modal) {
            this.modal.addEventListener('click', (e) => {
                if (e.target === this.modal) {
                    this.close();
                }
            });
        }

        // Écouter l'événement personnalisé pour ouvrir la modal
        document.addEventListener('openJerseyModal', (e) => {
            // Vérifier si on est en mode admin
            const adminPanel = document.getElementById('admin-main-panel');
            if (adminPanel && adminPanel.style.display !== 'none') {
                console.log('🚫 Modal bloquée en mode admin');
                return; // Ne pas ouvrir le modal normal en mode admin
            }
            this.open(e.detail.jersey);
        });

        // Navigation au clavier
        document.addEventListener('keydown', (e) => {
            if (this.isOpen()) {
                this.handleKeyboard(e);
            }
        });
    }

    /**
     * Ouvrir la modal avec un maillot
     * @param {Object} jersey - Données du maillot
     */
    open(jersey) {
        console.log('🔍 Modal.open() appelé avec:', jersey);
        
        if (!jersey) {
            console.error('❌ Aucun maillot fourni à la modal');
            return;
        }

        this.currentJersey = jersey;
        this.currentImageIndex = 0;
        this.jerseys = this.getJerseysInCategory(jersey.category);
        
        console.log('📸 Images du maillot:', jersey.images);
        console.log('📸 Nombre d\'images:', jersey.images ? jersey.images.length : 0);
        
        this.updateModalContent();
        this.show();
        
        // Animation d'entrée
        this.modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        console.log('✅ Modal ouvert avec succès');
    }

    /**
     * Fermer la modal
     */
    close() {
        this.modal.classList.remove('active');
        document.body.style.overflow = '';
        
        // Nettoyer après l'animation
        setTimeout(() => {
            this.modal.style.display = 'none';
        }, 300);
    }

    /**
     * Afficher la modal
     */
    show() {
        this.modal.style.display = 'flex';
        // Forcer le reflow pour l'animation
        this.modal.offsetHeight;
    }

    /**
     * Vérifier si la modal est ouverte
     * @returns {boolean} - État de la modal
     */
    isOpen() {
        return this.modal.classList.contains('active');
    }

    /**
     * Mettre à jour le contenu de la modal
     */
    updateModalContent() {
        console.log('🔄 updateModalContent() appelé');
        console.log('📸 currentJersey:', this.currentJersey);
        console.log('📸 currentImageIndex:', this.currentImageIndex);
        
        if (!this.currentJersey) {
            console.error('❌ Aucun maillot actuel');
            return;
        }

        if (!this.currentJersey.images || this.currentJersey.images.length === 0) {
            console.error('❌ Aucune image dans le maillot');
            return;
        }

        const currentImage = this.currentJersey.images[this.currentImageIndex];
        const imagePath = `${window.CONFIG.IMAGES_BASE_URL}/${currentImage}`;

        console.log('🖼️ Image actuelle:', currentImage);
        console.log('🖼️ Chemin complet:', imagePath);

        // Mettre à jour l'image
        if (this.modalImage) {
            this.modalImage.src = imagePath;
            this.modalImage.alt = this.currentJersey.title;
            console.log('✅ Image mise à jour dans le modal');
        } else {
            console.error('❌ Élément modalImage non trouvé');
        }

        // Mettre à jour le titre
        if (this.modalTitle) {
            this.modalTitle.textContent = this.currentJersey.title;
        }

        // Mettre à jour la description
        if (this.modalDescription) {
            this.modalDescription.innerHTML = this.createDescriptionHTML();
        }

        // Mettre à jour la navigation
        this.updateNavigation();
        
        console.log('✅ updateModalContent() terminé');
    }

    /**
     * Créer le HTML de la description
     * @returns {string} - HTML de la description
     */
    createDescriptionHTML() {
        const jersey = this.currentJersey;
        
        return `
            <div class="jersey-details">
                <p class="jersey-description">${sanitizeHTML(jersey.description)}</p>
                
                <div class="jersey-info">
                    <div class="info-item">
                        <strong>Année:</strong> ${jersey.year}
                    </div>
                    <div class="info-item">
                        <strong>Catégorie:</strong> ${jerseyAPI.getCategoryDisplayName(jersey.category)}
                    </div>
                </div>

                <div class="jersey-tags">
                    <strong>Tags:</strong>
                    ${jersey.tags.map(tag => `<span class="tag">${sanitizeHTML(tag)}</span>`).join('')}
                </div>

                <div class="jersey-actions">
                    <button class="btn btn-primary" onclick="jerseyModal.shareJersey()">
                        <i class="fas fa-share"></i> Partager
                    </button>
                    <button class="btn btn-secondary" onclick="jerseyModal.downloadImage()">
                        <i class="fas fa-download"></i> Télécharger
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Mettre à jour la navigation
     */
    updateNavigation() {
        console.log('🧭 updateNavigation() appelé');
        
        // Supprimer l'ancienne navigation si elle existe
        const existingNav = this.modal.querySelector('.modal-nav');
        if (existingNav) {
            existingNav.remove();
            console.log('🗑️ Ancienne navigation supprimée');
        }

        // Créer la nouvelle navigation
        const nav = document.createElement('div');
        nav.className = 'modal-nav';
        
        const totalImages = this.currentJersey.images.length;
        const currentImage = this.currentImageIndex + 1;
        
        console.log('📊 Navigation - Total images:', totalImages, 'Image actuelle:', currentImage);
        
        nav.innerHTML = `
            <button class="modal-nav-btn" id="prev-image" ${this.currentImageIndex === 0 ? 'disabled' : ''}>
                <i class="fas fa-chevron-left"></i>
                Précédent
            </button>
            
            <span class="modal-counter">
                ${currentImage} / ${totalImages}
            </span>
            
            <button class="modal-nav-btn" id="next-image" ${this.currentImageIndex === totalImages - 1 ? 'disabled' : ''}>
                Suivant
                <i class="fas fa-chevron-right"></i>
            </button>
        `;

        // Ajouter la navigation à la modal
        const modalContent = this.modal.querySelector('.modal-content');
        if (modalContent) {
            modalContent.appendChild(nav);
            console.log('✅ Navigation ajoutée au modal');
        } else {
            console.error('❌ Élément .modal-content non trouvé');
        }

        // Créer les miniatures
        this.createThumbnails();

        // Liaison des événements de navigation
        const prevBtn = nav.querySelector('#prev-image');
        const nextBtn = nav.querySelector('#next-image');

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                console.log('⬅️ Bouton Précédent cliqué');
                this.previousImage();
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                console.log('➡️ Bouton Suivant cliqué');
                this.nextImage();
            });
        }
        
        console.log('✅ updateNavigation() terminé');
    }

    /**
     * Créer les miniatures pour la navigation
     */
    createThumbnails() {
        // Supprimer les anciennes miniatures
        const existingThumbs = this.modal.querySelector('.modal-thumbnails');
        if (existingThumbs) {
            existingThumbs.remove();
        }

        const totalImages = this.currentJersey.images.length;
        if (totalImages <= 1) return;

        // Créer le conteneur des miniatures
        const thumbnailsContainer = document.createElement('div');
        thumbnailsContainer.className = 'modal-thumbnails';
        
        // Créer les miniatures
        this.currentJersey.images.forEach((image, index) => {
            const thumbnail = document.createElement('div');
            thumbnail.className = `modal-thumbnail ${index === this.currentImageIndex ? 'active' : ''}`;
            
            const imagePath = `${window.CONFIG.IMAGES_BASE_URL}/${image}`;
            thumbnail.innerHTML = `
                <img src="${imagePath}" alt="Miniature ${index + 1}" loading="lazy">
                <div class="thumbnail-overlay">
                    <span class="thumbnail-number">${index + 1}</span>
                </div>
            `;
            
            // Événement de clic pour changer d'image
            thumbnail.addEventListener('click', () => {
                this.currentImageIndex = index;
                this.updateModalContent();
            });
            
            thumbnailsContainer.appendChild(thumbnail);
        });

        // Ajouter les miniatures à la modal
        this.modal.querySelector('.modal-content').appendChild(thumbnailsContainer);
    }

    /**
     * Image précédente
     */
    previousImage() {
        if (this.currentImageIndex > 0) {
            this.currentImageIndex--;
            this.updateModalContent();
        }
    }

    /**
     * Image suivante
     */
    nextImage() {
        const totalImages = this.currentJersey.images.length;
        if (this.currentImageIndex < totalImages - 1) {
            this.currentImageIndex++;
            this.updateModalContent();
        }
    }

    /**
     * Obtenir les maillots de la même catégorie
     * @param {string} category - Catégorie
     * @returns {Array} - Liste des maillots
     */
    getJerseysInCategory(category) {
        // Cette méthode devrait récupérer les maillots de la même catégorie
        // Pour l'instant, on retourne un tableau vide
        return [];
    }

    /**
     * Gestion de la navigation au clavier
     * @param {KeyboardEvent} e - Événement clavier
     */
    handleKeyboard(e) {
        switch (e.key) {
            case 'Escape':
                this.close();
                break;
            case 'ArrowLeft':
                e.preventDefault();
                this.previousImage();
                break;
            case 'ArrowRight':
                e.preventDefault();
                this.nextImage();
                break;
        }
    }

    /**
     * Configuration de la navigation au clavier
     */
    setupKeyboardNavigation() {
        // La navigation est déjà configurée dans bindEvents
    }

    /**
     * Partager le maillot
     */
    async shareJersey() {
        if (!this.currentJersey) return;

        const shareData = {
            title: this.currentJersey.title,
            text: this.currentJersey.description,
            url: window.location.href
        };

        try {
            if (navigator.share) {
                await navigator.share(shareData);
            } else {
                // Fallback: copier le lien
                await copyToClipboard(window.location.href);
            }
        } catch (error) {
            handleError(error, 'JerseyModal.shareJersey');
        }
    }

    /**
     * Télécharger l'image
     */
    downloadImage() {
        if (!this.currentJersey) return;

        const currentImage = this.currentJersey.images[this.currentImageIndex];
        const imagePath = `${window.CONFIG.IMAGES_BASE_URL}/${currentImage}`;
        
        // Créer un lien de téléchargement
        const link = document.createElement('a');
        link.href = imagePath;
        link.download = `${this.currentJersey.title}_${this.currentImageIndex + 1}.jpg`;
        link.click();
    }

    /**
     * Obtenir les informations de la modal
     * @returns {Object} - Informations de la modal
     */
    getInfo() {
        return {
            isOpen: this.isOpen(),
            currentJersey: this.currentJersey,
            currentImageIndex: this.currentImageIndex,
            totalImages: this.currentJersey ? this.currentJersey.images.length : 0
        };
    }
}

// ===== STYLES POUR LA MODAL =====
const modalStyles = `
    .jersey-details {
        margin-top: var(--spacing-lg);
    }

    .jersey-info {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: var(--spacing-md);
        margin: var(--spacing-lg) 0;
        padding: var(--spacing-lg);
        background: var(--light-gray);
        border-radius: var(--radius-md);
    }

    .info-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--spacing-sm) 0;
        border-bottom: 1px solid var(--border-color);
    }

    .info-item:last-child {
        border-bottom: none;
    }

    .info-item strong {
        color: var(--text-dark);
        font-weight: 600;
    }

    .jersey-tags {
        margin: var(--spacing-lg) 0;
    }

    .jersey-tags strong {
        display: block;
        margin-bottom: var(--spacing-sm);
        color: var(--text-dark);
    }

    .tag {
        display: inline-block;
        background: var(--primary-color);
        color: var(--white);
        padding: var(--spacing-xs) var(--spacing-sm);
        border-radius: var(--radius-sm);
        font-size: var(--font-size-sm);
        margin: var(--spacing-xs) var(--spacing-xs) var(--spacing-xs) 0;
    }

    .jersey-actions {
        display: flex;
        gap: var(--spacing-md);
        margin-top: var(--spacing-xl);
        flex-wrap: wrap;
    }

    .jersey-actions .btn {
        flex: 1;
        min-width: 150px;
    }

    .jersey-actions .btn i {
        margin-right: var(--spacing-sm);
    }

    @media (max-width: 768px) {
        .jersey-info {
            grid-template-columns: 1fr;
        }

        .jersey-actions {
            flex-direction: column;
        }

        .jersey-actions .btn {
            min-width: auto;
        }
    }
`;

// Ajouter les styles au document
const modalStyleSheet = document.createElement('style');
modalStyleSheet.textContent = modalStyles;
document.head.appendChild(modalStyleSheet);

// ===== INSTANCE GLOBALE =====
const jerseyModal = new JerseyModal();

// ===== EXPORT POUR UTILISATION MODULAIRE =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = JerseyModal;
}
