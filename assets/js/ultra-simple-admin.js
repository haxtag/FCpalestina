/**
 * ULTRA-SIMPLE ADMIN SYSTEM - VERSION FINALE
 * Ce système fonctionne à coup sûr !
 */

class UltraSimpleAdmin {
    constructor() {
        this.jerseys = [];
        this.categories = [];
        this.tags = [];
        this.currentJersey = null;
        
        // Pagination pour l'admin
        this.adminCurrentPage = 1;
        this.adminItemsPerPage = 12; // Affichage plus dense dans l'admin
        this.adminTotalPages = 0;
        
        console.log('🚀 Ultra Simple Admin initialisé');
        this.init();
    }

    async init() {
        await this.loadData();
        this.createAdminPanel();
        this.bindEvents();
        // Auto-open if admin=true present to ensure panel is visible
        try {
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('admin') === 'true') {
                this.open();
            }
        } catch { /* noop */ }
    }

    async loadData() {
        try {
            console.log('📦 Chargement des données...');
            
            // Charger depuis les fichiers JSON directement
            const [jerseysRes, categoriesRes, tagsRes] = await Promise.all([
                fetch('/data/jerseys.json'),
                fetch('/data/categories.json'),
                fetch('/data/tags.json')
            ]);

            this.jerseys = await jerseysRes.json();
            this.categories = await categoriesRes.json();
            this.tags = await tagsRes.json();

            console.log('✅ Données chargées:', {
                jerseys: this.jerseys.length,
                categories: this.categories.length,
                tags: this.tags.length
            });
        } catch (error) {
            console.error('❌ Erreur chargement:', error);
            const msg = (error && (error.message || error.toString())) || 'Erreur inconnue';
            if (typeof showNotification === 'function') {
                showNotification(`Erreur chargement admin: ${msg}`, 'error', 5000);
            } else {
                alert('Erreur: ' + msg);
            }
        }
    }

    createAdminPanel() {
        // Créer le panneau admin
        const adminPanel = document.createElement('div');
        adminPanel.id = 'ultra-admin-panel';
        adminPanel.innerHTML = `
            <div id="ultra-admin-overlay" style="
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.95);
                z-index: 99999;
                display: none;
                overflow-y: auto;
                padding: 20px;
            ">
                <div style="
                    background: #8B1538;
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                ">
<<<<<<< HEAD
                    <h2>🔧 ADMIN FC PALESTINA - VERSION ULTRA-SIMPLE</h2>
=======
                    <h2>🔧 ADMIN FC PALESTINA <span id="api-status" style="font-size:14px; margin-left:10px; background:#6c757d; padding:3px 8px; border-radius:4px;">API: ...</span></h2>
>>>>>>> 4e73183 (salam)
                    <div style="margin-top: 15px;">
                        <button onclick="window.ultraAdmin.close()" style="
                            background: #dc3545;
                            color: white;
                            border: none;
                            padding: 10px 20px;
                            border-radius: 5px;
                            cursor: pointer;
                            margin-right: 10px;
                        ">❌ FERMER</button>
                        <button onclick="window.ultraAdmin.refresh()" style="
                            background: #28a745;
                            color: white;
                            border: none;
                            padding: 10px 20px;
                            border-radius: 5px;
                            cursor: pointer;
                        ">🔄 RECHARGER</button>
                    </div>
                </div>

                <div id="admin-content" style="
                    background: white;
                    color: black;
                    padding: 20px;
                    border-radius: 10px;
                    min-height: 500px;
                ">
                    <h3 style="margin-top:0;">🧭 Gestion</h3>
                    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:12px; margin-bottom:18px;">
                        <div style="background:#f8f9fa; border:1px solid #eee; border-radius:8px; padding:12px;">
                            <h4 style="margin:0 0 8px 0; color:#8B1538;">📁 Créer une catégorie</h4>
                            <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
                                <input id="new-cat-name" type="text" placeholder="Nom de la catégorie" style="flex:1; min-width:140px; padding:8px; border:1px solid #ddd; border-radius:6px;">
                                <input id="new-cat-color" type="color" value="#8B1538" title="Couleur" style="width:42px; height:36px; border:1px solid #ddd; border-radius:6px; padding:0;">
                                <button onclick="window.ultraAdmin.createCategory()" style="background:#28a745; color:white; border:none; padding:8px 12px; border-radius:6px; cursor:pointer;">Créer</button>
                            </div>
                        </div>
                        <div style="background:#f8f9fa; border:1px solid #eee; border-radius:8px; padding:12px;">
                            <h4 style="margin:0 0 8px 0; color:#8B1538;">🏷️ Créer un tag</h4>
                            <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
                                <input id="new-tag-name" type="text" placeholder="Nom du tag" style="flex:1; min-width:140px; padding:8px; border:1px solid #ddd; border-radius:6px;">
                                <input id="new-tag-color" type="color" value="#17a2b8" title="Couleur" style="width:42px; height:36px; border:1px solid #ddd; border-radius:6px; padding:0;">
                                <button onclick="window.ultraAdmin.createTag()" style="background:#28a745; color:white; border:none; padding:8px 12px; border-radius:6px; cursor:pointer;">Créer</button>
                            </div>
                        </div>
                    </div>

                    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:16px; margin-bottom:24px;">
                        <div style="background:#fff; border:1px solid #dee2e6; border-radius:8px; padding:16px;">
                            <h4 style="margin:0 0 12px 0; color:#8B1538; display:flex; align-items:center; gap:8px;">📁 Catégories existantes</h4>
                            <div id="existing-categories" style="max-height:200px; overflow-y:auto;"></div>
                        </div>
                        <div style="background:#fff; border:1px solid #dee2e6; border-radius:8px; padding:16px;">
                            <h4 style="margin:0 0 12px 0; color:#8B1538; display:flex; align-items:center; gap:8px;">🏷️ Tags existants</h4>
                            <div id="existing-tags" style="max-height:200px; overflow-y:auto;"></div>
                        </div>
                    </div>
                    <h3>📋 Liste des maillots</h3>
                    <div id="jerseys-list" style="
                        display: grid;
                        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                        gap: 20px;
                        margin-top: 20px;
                    "></div>
                </div>
            </div>
        `;

        document.body.appendChild(adminPanel);
        this.renderJerseys();
    }

    renderJerseys() {
        const container = document.getElementById('jerseys-list');
        if (!container) return;

        // Calcul de la pagination
        this.adminTotalPages = Math.ceil(this.jerseys.length / this.adminItemsPerPage);
        const startIndex = (this.adminCurrentPage - 1) * this.adminItemsPerPage;
        const endIndex = startIndex + this.adminItemsPerPage;
        const pageJerseys = this.jerseys.slice(startIndex, endIndex);

        // Ajouter l'info de pagination
        let paginationInfo = '';
        if (this.jerseys.length > this.adminItemsPerPage) {
            paginationInfo = `
                <div style="background: #8B1538; color: white; padding: 10px; border-radius: 5px; margin-bottom: 15px; text-align: center;">
                    <strong>Page ${this.adminCurrentPage} sur ${this.adminTotalPages}</strong> 
                    (Affichage de ${pageJerseys.length} maillots sur ${this.jerseys.length} total)
                </div>
            `;
        }

        // Navigation pagination compacte
        let paginationControls = '';
        if (this.adminTotalPages > 1) {
            paginationControls = `
                <div style="display: flex; justify-content: center; align-items: center; gap: 6px; margin: 15px 0; flex-wrap: wrap; background: #f8f9fa; padding: 10px; border-radius: 6px; font-size: 11px;">
                    <button onclick="window.ultraAdmin.adminGoToPage(1)" 
                            ${this.adminCurrentPage === 1 ? 'disabled' : ''} 
                            style="padding: 6px 10px; border: none; border-radius: 4px; cursor: pointer; background: #6c757d; color: white; font-size: 10px; transition: all 0.2s ease; ${this.adminCurrentPage === 1 ? 'opacity: 0.5;' : ''}">
                        <i class="fas fa-angle-double-left"></i>
                    </button>
                    <button onclick="window.ultraAdmin.adminGoToPage(${this.adminCurrentPage - 1})" 
                            ${this.adminCurrentPage === 1 ? 'disabled' : ''} 
                            style="padding: 6px 10px; border: none; border-radius: 4px; cursor: pointer; background: #8B1538; color: white; transition: all 0.2s ease; ${this.adminCurrentPage === 1 ? 'opacity: 0.5;' : ''}">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <span style="padding: 6px 12px; background: white; border-radius: 4px; font-weight: bold; color: #8B1538; border: 1px solid #8B1538; font-size: 11px;">
                        ${this.adminCurrentPage} / ${this.adminTotalPages}
                    </span>
                    <button onclick="window.ultraAdmin.adminGoToPage(${this.adminCurrentPage + 1})" 
                            ${this.adminCurrentPage === this.adminTotalPages ? 'disabled' : ''} 
                            style="padding: 6px 10px; border: none; border-radius: 4px; cursor: pointer; background: #8B1538; color: white; transition: all 0.2s ease; ${this.adminCurrentPage === this.adminTotalPages ? 'opacity: 0.5;' : ''}">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                    <button onclick="window.ultraAdmin.adminGoToPage(${this.adminTotalPages})" 
                            ${this.adminCurrentPage === this.adminTotalPages ? 'disabled' : ''} 
                            style="padding: 6px 10px; border: none; border-radius: 4px; cursor: pointer; background: #6c757d; color: white; font-size: 10px; transition: all 0.2s ease; ${this.adminCurrentPage === this.adminTotalPages ? 'opacity: 0.5;' : ''}">
                        <i class="fas fa-angle-double-right"></i>
                    </button>
                    <span style="margin-left: 8px; color: #6c757d; font-size: 10px;">
                        ${this.jerseys.length} maillots
                    </span>
                </div>
            `;
        }

        container.innerHTML = paginationInfo + paginationControls;

        // Afficher les maillots de la page courante avec design compact
        pageJerseys.forEach((jersey, index) => {
            const actualIndex = startIndex + index; // Index réel dans la liste complète
            const card = document.createElement('div');
            card.style.cssText = `
                background: white;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 12px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
                transition: all 0.2s ease;
                position: relative;
            `;

            // Ajouter effet hover subtil
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-2px)';
                card.style.boxShadow = '0 4px 15px rgba(139, 21, 56, 0.1)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
                card.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.05)';
            });

            card.innerHTML = `
                <!-- Numéro compact repositionné -->
                <div style="position: absolute; top: 8px; left: 8px; background: #8B1538; color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold; z-index: 1;">
                    #${actualIndex + 1}
                </div>
                
<<<<<<< HEAD
                <h4 style="margin: 10px 0; color: #8B1538;">${jersey.name || jersey.title || 'Sans nom'}</h4>
                
                <p><strong>Catégorie:</strong> ${this.getCategoryName(jersey.category)}</p>
                <p><strong>Année:</strong> ${jersey.year || 'N/A'}</p>
                <p><strong>Description:</strong> ${(jersey.description || '').substring(0, 100)}...</p>
                <p><strong>Tags:</strong> ${(jersey.tags || []).join(', ')}</p>
                
                <div style="margin-top: 15px; display: flex; gap: 10px; flex-wrap: wrap;">
                    <button onclick="window.ultraAdmin.editJersey(${index})" style="
                        background: #007bff;
                        color: white;
                        border: none;
                        padding: 8px 15px;
                        border-radius: 5px;
                        cursor: pointer;
                        flex: 1;
                    ">✏️ MODIFIER</button>
=======
                <!-- Layout horizontal compact -->
                <div style="display: flex; gap: 12px; align-items: flex-start;">
                    <!-- Image miniature -->
                    <div style="flex-shrink: 0; width: 80px; height: 80px; border-radius: 6px; overflow: hidden; background: #f8f9fa;">
                        <img src="${window.CONFIG.IMAGES_BASE_URL}/${jersey.thumbnail}" 
                             style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
>>>>>>> 4e73183 (salam)
                    
                    <!-- Infos compactes -->
                    <div style="flex: 1; min-width: 0;">
                        <h4 style="margin: 0 0 6px 0; font-size: 14px; line-height: 1.3; color: #2d3748; font-weight: 600;">
                            ${jersey.name || jersey.title || 'Sans nom'}
                        </h4>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4px; font-size: 11px; margin-bottom: 8px;">
                            <div><span style="color: #8B1538; font-weight: 500;">Cat:</span> ${this.getCategoryName(jersey.category)}</div>
                            <div><span style="color: #8B1538; font-weight: 500;">Année:</span> ${jersey.year || 'N/A'}</div>
                        </div>
                        
                        <div style="font-size: 11px; color: #718096; margin-bottom: 8px;">
                            ${(jersey.description || '').substring(0, 60)}${jersey.description && jersey.description.length > 60 ? '...' : ''}
                        </div>
                        
                        <!-- Tags compacts -->
                        <div style="font-size: 10px; margin-bottom: 8px;">
                            <span style="color: #8B1538; font-weight: 500;">Tags:</span> 
                            <span style="color: #4a5568;">${this.renderTagList(jersey.tags)}</span>
                        </div>
                    </div>
                    
                    <!-- Actions compactes -->
                    <div style="flex-shrink: 0; display: flex; flex-direction: column; gap: 4px;">
                        <button onclick="window.ultraAdmin.editJersey(${actualIndex})" 
                                style="padding: 6px 10px; background: #4299e1; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 10px; font-weight: 500;"
                                title="Modifier ce maillot">
                            <i class="fas fa-edit"></i>
                        </button>
                        
                        <button onclick="window.ultraAdmin.changeCover(${actualIndex})" 
                                style="padding: 6px 10px; background: #48bb78; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 10px; font-weight: 500;"
                                title="Changer la couverture">
                            <i class="fas fa-image"></i>
                        </button>
                    </div>
                </div>
                
                <!-- Gestion catégories en bas, compacte -->
                <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #f1f3f4;">
                    <div style="display: flex; gap: 6px; align-items: center; font-size: 11px;">
                        <span style="color: #8B1538; font-weight: 500; font-size: 10px;">Gestion:</span>
                        <select id="quick-cat-${actualIndex}" style="flex: 1; padding: 4px 6px; border: 1px solid #cbd5e0; border-radius: 4px; font-size: 10px;">
                            ${this.categories.map(cat => `<option value="${cat.id}">${cat.name}</option>`).join('')}
                        </select>
                        <button onclick="window.ultraAdmin.quickAddCategory(${actualIndex})" 
                                style="padding: 4px 8px; background: #48bb78; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 9px;"
                                title="Ajouter catégorie">
                            +
                        </button>
                        <button onclick="window.ultraAdmin.quickRemoveCategory(${actualIndex})" 
                                style="padding: 4px 8px; background: #f56565; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 9px;"
                                title="Retirer catégorie">
                            -
                        </button>
                    </div>
                </div>
            `;

            container.appendChild(card);
        });
        
        // Ajouter les contrôles en bas aussi
        if (this.adminTotalPages > 1) {
            const bottomControls = document.createElement('div');
            bottomControls.innerHTML = paginationControls;
            container.appendChild(bottomControls);
        }
        
        // Rendre aussi les listes de gestion
        this.renderManagementLists();
    }

    getCategoryName(categoryId) {
        const category = this.categories.find(cat => cat.id === categoryId);
        return category ? category.name : categoryId;
    }

    editJersey(index) {
        // Fermer d'abord toute modal de détail ouverte
        const detailModal = document.getElementById('image-modal');
        if (detailModal && detailModal.classList.contains('active')) {
            detailModal.classList.remove('active');
            detailModal.style.display = 'none';
            document.body.style.overflow = 'auto';
            console.log('🧹 Modal de détail fermée avant ouverture admin');
        }

        this.currentJersey = this.jerseys[index];
        const norm = (s) => (s || '').toString().normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase();
        const tagsList = this.tags || [];
        const selectedSet = new Set((this.currentJersey.tags || []).map(t => norm(t)));
        
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.8);
            z-index: 100000;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        `;

        modal.innerHTML = `
            <div class="admin-modal-content" style="
                background: white;
                padding: 30px;
                border-radius: 10px;
                max-width: 500px;
                width: 100%;
                max-height: 80vh;
                overflow-y: auto;
                position: relative;
                margin: auto;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            ">
                <h3 style="color: #8B1538; margin-bottom: 20px;">✏️ MODIFIER LE MAILLOT</h3>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Nom:</label>
                    <input type="text" id="edit-name" value="${this.currentJersey.name || this.currentJersey.title || ''}" 
                           style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Description:</label>
                    <textarea id="edit-description" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; height: 100px;">${this.currentJersey.description || ''}</textarea>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Année:</label>
                    <input type="text" id="edit-year" value="${this.currentJersey.year || ''}" 
                           style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                </div>
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Catégorie:</label>
                    <select id="edit-category" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                        ${this.categories.map(cat => 
                            `<option value="${cat.id}" ${cat.id === this.currentJersey.category ? 'selected' : ''}>${cat.name}</option>`
                        ).join('')}
                    </select>
                </div>

                <div style="margin-bottom: 20px;">
                    <label style="display:block; margin-bottom:5px; font-weight:bold;">Catégories (multi):</label>
                    <div id="edit-categories" style="display:grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap:8px; max-height: 160px; overflow:auto; padding:8px; border:1px solid #eee; border-radius:6px;">
                        ${this.categories.map(cat => {
                            const selectedCats = new Set((this.currentJersey.categories || []).concat([this.currentJersey.category]).filter(Boolean));
                            const checked = selectedCats.has(cat.id);
                            const safeId = `cat-${cat.id}`.replace(/[^a-z0-9_-]/gi, '_');
                            return `
                                <label for="${safeId}" style="display:flex; align-items:center; gap:8px; background:#f8f9fa; padding:6px 8px; border-radius:6px;">
                                    <input type="checkbox" id="${safeId}" data-cat-id="${cat.id}" ${checked ? 'checked' : ''}>
                                    <span>${cat.name}</span>
                                </label>`;
                        }).join('')}
                    </div>
                    <small style="color:#666;">Choisissez une catégorie principale ci-dessus et plusieurs catégories ici.</small>
                </div>

                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Tags:</label>
                    <div id="edit-tags" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 8px; max-height: 160px; overflow: auto; padding: 8px; border: 1px solid #eee; border-radius: 6px;">
                        ${tagsList.map(tag => {
                            const checked = selectedSet.has(norm(tag.id)) || selectedSet.has(norm(tag.name));
                            const safeId = `tag-${tag.id}`.replace(/[^a-z0-9_-]/gi, '_');
                            return `
                                <label for="${safeId}" style="display:flex; align-items:center; gap:8px; background:#f8f9fa; padding:6px 8px; border-radius:6px;">
                                    <input type="checkbox" id="${safeId}" data-tag-id="${tag.id}" ${checked ? 'checked' : ''}>
                                    <span>${tag.name}</span>
                                </label>
                            `;
                        }).join('')}
                    </div>
                </div>
                
                <div style="display: flex; gap: 10px; justify-content: flex-end;">
                    <button onclick="window.ultraAdmin.closeModal()" style="
                        background: #6c757d;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                        cursor: pointer;
                    ">❌ ANNULER</button>
                    
                    <button onclick="window.ultraAdmin.saveJersey()" style="
                        background: #28a745;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                        cursor: pointer;
                    ">💾 SAUVEGARDER</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    /**
     * Fermer le modal actuel
     */
    closeModal() {
        // Fermer tous les modals admin
        const modals = document.querySelectorAll('.admin-modal-overlay');
        modals.forEach(modal => {
            modal.remove();
        });
        
        // S'assurer que le body overflow est restauré
        document.body.style.overflow = 'auto';
        
        console.log('✅ Tous les modals admin fermés');
    }

    changeCover(index) {
        // Fermer d'abord toute modal de détail ouverte
        const detailModal = document.getElementById('image-modal');
        if (detailModal && detailModal.classList.contains('active')) {
            detailModal.classList.remove('active');
            detailModal.style.display = 'none';
            document.body.style.overflow = 'auto';
            console.log('🧹 Modal de détail fermée avant changement couverture');
        }

        this.currentJersey = this.jerseys[index];
        
        const modal = document.createElement('div');
        modal.className = 'admin-modal-overlay';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0,0,0,0.8);
            z-index: 999999;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            box-sizing: border-box;
        `;

        modal.innerHTML = `
            <div class="admin-modal-content" style="
                background: white;
                padding: 30px;
                border-radius: 10px;
                max-width: 600px;
                width: 100%;
                max-height: 80vh;
                position: relative;
                margin: auto;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                overflow-y: auto;
            ">
                <h3 style="color: #8B1538; margin-bottom: 20px;">🖼️ CHANGER L'IMAGE DE COUVERTURE</h3>
                
                <p style="margin-bottom: 20px;">Sélectionnez une image pour la couverture:</p>
                
                <div style="
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
                    gap: 10px;
                    max-height: 300px;
                    overflow-y: auto;
                    margin-bottom: 20px;
                ">
                    ${this.currentJersey.images.map((img, imgIndex) => `
                        <img src="${window.CONFIG.IMAGES_BASE_URL}/${img}" 
                             class="cover-option ${img === this.currentJersey.thumbnail ? 'selected' : ''}"
                             data-image="${img}"
                             onclick="window.ultraAdmin.selectCoverImage('${img}')"
                             style="
                                width: 100px;
                                height: 100px;
                                object-fit: cover;
                                cursor: pointer;
                                border: 3px solid transparent;
                                border-radius: 5px;
                             ">
                    `).join('')}
                </div>
                
                <div style="display: flex; gap: 10px; justify-content: flex-end;">
                    <button onclick="window.ultraAdmin.closeModal()" style="
                        background: #6c757d;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                        cursor: pointer;
                    ">❌ ANNULER</button>
                    
                    <button onclick="window.ultraAdmin.saveCover()" style="
                        background: #28a745;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                        cursor: pointer;
                    ">💾 SAUVEGARDER</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    selectCoverImage(imageName) {
        // Retirer la sélection de toutes les images
        document.querySelectorAll('.cover-option').forEach(img => {
            img.style.border = '3px solid transparent';
            img.classList.remove('selected');
        });
        
        // Sélectionner la nouvelle image
        const selectedImg = document.querySelector(`[data-image="${imageName}"]`);
        if (selectedImg) {
            selectedImg.style.border = '3px solid #28a745';
            selectedImg.classList.add('selected');
            this.currentJersey.thumbnail = imageName;
        }
    }

    async saveJersey() {
        if (!this.currentJersey) return;

        // Mettre à jour les données
        this.currentJersey.name = document.getElementById('edit-name').value;
        this.currentJersey.title = this.currentJersey.name; // Garder la cohérence
        this.currentJersey.description = document.getElementById('edit-description').value;
        this.currentJersey.year = document.getElementById('edit-year').value;
        const primaryCat = document.getElementById('edit-category').value;
        // Catégories sélectionnées (multi)
        const catInputs = document.querySelectorAll('#edit-categories input[type="checkbox"]');
        let selectedCats = [];
        catInputs.forEach(inp => { if (inp.checked) selectedCats.push(inp.getAttribute('data-cat-id')); });
        // S'assurer que la catégorie principale est incluse
        if (primaryCat && !selectedCats.includes(primaryCat)) selectedCats.unshift(primaryCat);
        // Validation: au moins une catégorie
        const uniqueCats = Array.from(new Set(selectedCats));
        if (uniqueCats.length === 0) {
            if (typeof showNotification === 'function') showNotification('Sélectionnez au moins une catégorie', 'warning');
            return;
        }
        this.currentJersey.category = primaryCat || uniqueCats[0];
        this.currentJersey.categories = uniqueCats;

        // Tags sélectionnés
        const tagInputs = document.querySelectorAll('#edit-tags input[type="checkbox"]');
        const selectedTags = [];
        tagInputs.forEach(inp => { if (inp.checked) selectedTags.push(inp.getAttribute('data-tag-id')); });
        this.currentJersey.tags = selectedTags;

        // Sauvegarder
        await this.saveToFile();
        
        // Fermer le modal
        document.querySelector('[onclick="window.ultraAdmin.saveJersey()"]').closest('div').remove();
        
        // Recharger l'affichage
        this.renderJerseys();
        if (typeof showNotification === 'function') {
            showNotification('✅ Maillot sauvegardé avec succès', 'success', 3000);
        }
        // Notifier le site pour rafraîchir la galerie
        document.dispatchEvent(new CustomEvent('adminDataUpdated'));
        // Rafraîchir directement si la galerie est présente dans la même page
        try { if (window.gallery && typeof window.gallery.refresh === 'function') window.gallery.refresh(); } catch {}
        // Diffuser l'info aux autres onglets
        try { localStorage.setItem('fcp-admin-update', String(Date.now())); } catch {}
    }

    async saveCover() {
        if (!this.currentJersey) return;

        // Sauvegarder
        await this.saveToFile();
        
        // Fermer le modal
        document.querySelector('[onclick="window.ultraAdmin.saveCover()"]').closest('div').remove();
        
        // Recharger l'affichage
        this.renderJerseys();
        if (typeof showNotification === 'function') {
            showNotification('✅ Image de couverture sauvegardée', 'success', 3000);
        }
        document.dispatchEvent(new CustomEvent('adminDataUpdated'));
        // Rafraîchir directement si la galerie est présente dans la même page
        try { if (window.gallery && typeof window.gallery.refresh === 'function') window.gallery.refresh(); } catch {}
        // Diffuser l'info aux autres onglets
        try { localStorage.setItem('fcp-admin-update', String(Date.now())); } catch {}
    }

    async saveToFile() {
        try {
            console.log('💾 Sauvegarde en cours...');
            
            // Sauvegarder via l'API
            const response = await fetch('http://localhost:8001/api/jerseys', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    jerseys: this.jerseys
                })
            });

            if (!response.ok) {
                throw new Error(`Erreur ${response.status}: ${response.statusText}`);
            }

            console.log('✅ Sauvegarde réussie!');
            
            // Recharger la page principale
            setTimeout(() => {
                window.location.reload();
            }, 1000);

        } catch (error) {
            console.error('❌ Erreur sauvegarde:', error);
            const msg = (error && (error.message || error.toString())) || 'Erreur inconnue';
            if (typeof showNotification === 'function') {
                showNotification(`Erreur sauvegarde: ${msg}`, 'error', 6000);
            } else {
                alert('❌ Erreur: ' + msg);
            }
        }
    }

<<<<<<< HEAD
=======
    async checkBackend() {
        const el = document.getElementById('api-status');
        if (!el) return;
        try {
            const res = await fetch(`${this.apiBase}/jerseys`, { cache: 'no-store' });
            const ct = res.headers.get('content-type') || '';
            if (!res.ok || !ct.includes('application/json')) throw new Error('API non disponible');
            // Ne plus sonder /api/stats pour éviter les 404 inutiles avec Flask
            this.apiMode = 'flask';
            el.textContent = 'API: OK (flask)';
            el.style.background = '#28a745';
        } catch (e) {
            el.textContent = 'API: OFF';
            el.style.background = '#dc3545';
        }
    }

>>>>>>> 4e73183 (salam)
    open() {
        const overlay = document.getElementById('ultra-admin-overlay');
        if (overlay) overlay.style.display = 'block';
    }

    close() {
        const overlay = document.getElementById('ultra-admin-overlay');
        if (overlay) overlay.style.display = 'none';
    }

    async refresh() {
        await this.loadData();
        this.renderJerseys();
        alert('✅ Données rechargées!');
    }

    bindEvents() {
        // Pas besoin d'événements complexes
    }

    async createCategory() {
        const nameEl = document.getElementById('new-cat-name');
        const colorEl = document.getElementById('new-cat-color');
        const name = (nameEl?.value || '').trim();
        const color = colorEl?.value || '#8B1538';
        if (!name) {
            if (typeof showNotification === 'function') showNotification('Entrez un nom de catégorie', 'warning');
            return;
        }
        try {
            const res = await fetch(`${this.apiBase}/categories/create`, {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, color })
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            await this.loadData();
            this.renderJerseys();
            if (nameEl) nameEl.value = '';
            if (typeof showNotification === 'function') showNotification(`Catégorie "${name}" créée`, 'success');
            document.dispatchEvent(new CustomEvent('adminDataUpdated'));
            try { localStorage.setItem('fcp-admin-update', String(Date.now())); } catch {}
        } catch (e) {
            const msg = e?.message || e;
            if (typeof showNotification === 'function') showNotification(`Erreur création catégorie: ${msg}`, 'error');
        }
    }

    async createTag() {
        const nameEl = document.getElementById('new-tag-name');
        const colorEl = document.getElementById('new-tag-color');
        const name = (nameEl?.value || '').trim();
        const color = colorEl?.value || '#17a2b8';
        if (!name) {
            if (typeof showNotification === 'function') showNotification('Entrez un nom de tag', 'warning');
            return;
        }
        try {
            const res = await fetch(`${this.apiBase}/tags/create`, {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, color })
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            await this.loadData();
            this.renderJerseys();
            if (nameEl) nameEl.value = '';
            if (typeof showNotification === 'function') showNotification(`Tag "${name}" créé`, 'success');
            document.dispatchEvent(new CustomEvent('adminDataUpdated'));
            try { localStorage.setItem('fcp-admin-update', String(Date.now())); } catch {}
        } catch (e) {
            const msg = e?.message || e;
            if (typeof showNotification === 'function') showNotification(`Erreur création tag: ${msg}`, 'error');
        }
    }

    async quickAddCategory(index) {
        const jersey = this.jerseys[index];
        const select = document.getElementById(`quick-cat-${index}`);
        if (!jersey || !select) return;
        const catId = select.value;
        const set = new Set((jersey.categories || []).concat([jersey.category]).filter(Boolean));
        set.add(catId);
        const cats = Array.from(set);
        jersey.categories = cats;
        jersey.category = jersey.category || cats[0];
        await this.saveToFile();
        this.renderJerseys();
        if (typeof showNotification === 'function') showNotification('Catégorie ajoutée', 'success');
        document.dispatchEvent(new CustomEvent('adminDataUpdated'));
        try { if (window.gallery && typeof window.gallery.refresh === 'function') window.gallery.refresh(); } catch {}
        try { localStorage.setItem('fcp-admin-update', String(Date.now())); } catch {}
    }

    async quickRemoveCategory(index) {
        const jersey = this.jerseys[index];
        const select = document.getElementById(`quick-cat-${index}`);
        if (!jersey || !select) return;
        const catId = select.value;
        const list = (jersey.categories || []).filter(c => c !== catId);
        // Si on retire la catégorie principale, basculer sur une autre si possible
        const newPrimary = jersey.category === catId ? (list[0] || null) : jersey.category;
        jersey.categories = list;
        jersey.category = newPrimary || (list[0] || null);
        await this.saveToFile();
        this.renderJerseys();
        if (typeof showNotification === 'function') showNotification('Catégorie retirée', 'success');
        document.dispatchEvent(new CustomEvent('adminDataUpdated'));
        try { if (window.gallery && typeof window.gallery.refresh === 'function') window.gallery.refresh(); } catch {}
        try { localStorage.setItem('fcp-admin-update', String(Date.now())); } catch {}
    }

    renderManagementLists() {
        // Render existing categories
        const catContainer = document.getElementById('existing-categories');
        if (catContainer && this.categories) {
            catContainer.innerHTML = this.categories.map(cat => `
                <div style="display:flex; align-items:center; justify-content:space-between; padding:8px 12px; margin:4px 0; background:#f8f9fa; border-radius:6px; border-left:4px solid ${cat.color || '#8B1538'};">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <div style="width:12px; height:12px; background:${cat.color || '#8B1538'}; border-radius:50%;"></div>
                        <span style="font-weight:500;">${cat.name}</span>
                    </div>
                    <button onclick="window.ultraAdmin.deleteCategory('${cat.id}')" title="Supprimer ${cat.name}" style="background:#dc3545; color:white; border:none; padding:4px 8px; border-radius:4px; cursor:pointer; font-size:12px;">×</button>
                </div>
            `).join('');
        }
        
        // Render existing tags
        const tagContainer = document.getElementById('existing-tags');
        if (tagContainer && this.tags) {
            tagContainer.innerHTML = this.tags.map(tag => `
                <div style="display:flex; align-items:center; justify-content:space-between; padding:8px 12px; margin:4px 0; background:#f8f9fa; border-radius:6px; border-left:4px solid ${tag.color || '#6c757d'};">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <div style="width:12px; height:12px; background:${tag.color || '#6c757d'}; border-radius:50%;"></div>
                        <span style="font-weight:500;">${tag.name}</span>
                    </div>
                    <button onclick="window.ultraAdmin.deleteTag('${tag.id}')" title="Supprimer ${tag.name}" style="background:#dc3545; color:white; border:none; padding:4px 8px; border-radius:4px; cursor:pointer; font-size:12px;">×</button>
                </div>
            `).join('');
        }
    }

    async deleteCategory(categoryId) {
        if (!categoryId) return;
        
        const category = this.categories.find(c => c.id === categoryId);
        const categoryName = category ? category.name : categoryId;
        
        if (!confirm(`⚠️ Supprimer la catégorie "${categoryName}" ?\n\n⚠️ ATTENTION: Les maillots utilisant cette catégorie devront être remis à jour manuellement.`)) {
            return;
        }
        
        try {
            const res = await fetch(`${this.apiBase}/categories/delete`, {
                method: 'POST', 
                headers: { 'Content-Type': 'application/json' }, 
                body: JSON.stringify({ id: categoryId })
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            
            await this.loadData();
            this.renderJerseys();
            if (typeof showNotification === 'function') showNotification(`Catégorie "${categoryName}" supprimée`, 'success');
            document.dispatchEvent(new CustomEvent('adminDataUpdated'));
            try { localStorage.setItem('fcp-admin-update', String(Date.now())); } catch {}
        } catch (e) {
            const msg = e?.message || e;
            if (typeof showNotification === 'function') showNotification(`Erreur suppression catégorie: ${msg}`, 'error');
        }
    }

    async deleteTag(tagId) {
        if (!tagId) return;
        
        const tag = this.tags.find(t => t.id === tagId);
        const tagName = tag ? tag.name : tagId;
        
        if (!confirm(`⚠️ Supprimer le tag "${tagName}" ?\n\n⚠️ ATTENTION: Ce tag sera retiré de tous les maillots qui l'utilisent.`)) {
            return;
        }
        
        try {
            const res = await fetch(`${this.apiBase}/tags/delete`, {
                method: 'POST', 
                headers: { 'Content-Type': 'application/json' }, 
                body: JSON.stringify({ id: tagId })
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            
            await this.loadData();
            this.renderJerseys();
            if (typeof showNotification === 'function') showNotification(`Tag "${tagName}" supprimé`, 'success');
            document.dispatchEvent(new CustomEvent('adminDataUpdated'));
            try { localStorage.setItem('fcp-admin-update', String(Date.now())); } catch {}
        } catch (e) {
            const msg = e?.message || e;
            if (typeof showNotification === 'function') showNotification(`Erreur suppression tag: ${msg}`, 'error');
        }
    }
    
    /**
     * Navigation dans la pagination de l'admin
     * @param {number} page - Numéro de la page à afficher
     */
    adminGoToPage(page) {
        if (page < 1 || page > this.adminTotalPages || page === this.adminCurrentPage) {
            return;
        }
        
        this.adminCurrentPage = page;
        this.renderJerseys();
        
        // Scroll vers le haut de la liste des maillots
        const container = document.getElementById('jerseys-list');
        if (container) {
            container.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
}

// Fonctions globales
function openUltraAdmin() {
    if (!window.ultraAdmin) {
        window.ultraAdmin = new UltraSimpleAdmin();
    }
    window.ultraAdmin.open();
}

function closeUltraAdmin() {
    if (window.ultraAdmin) {
        window.ultraAdmin.close();
    }
}

// Auto-initialisation si on est en mode admin
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('admin') === 'true') {
        console.log('🔧 Mode admin détecté - Initialisation...');
        setTimeout(() => {
            openUltraAdmin();
        }, 1000);
    }
});
