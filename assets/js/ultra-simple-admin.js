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
        this.apiBase = 'http://localhost:8001/api';
        this.apiMode = 'unknown'; // 'flask' (simple_backend) | 'http' (admin_server)
        
        console.log('🚀 Ultra Simple Admin initialisé');
        this.init();
    }

    async init() {
        await this.loadData();
        this.createAdminPanel();
        this.bindEvents();
    }

    async loadData() {
        try {
            console.log('📦 Chargement des données...');
            
            // Charger depuis les fichiers JSON directement
            const ts = Date.now();
            const noStore = { cache: 'no-store' };
            const [jerseysRes, categoriesRes, tagsRes] = await Promise.all([
                fetch(`/data/jerseys.json?t=${ts}`, noStore),
                fetch(`/data/categories.json?t=${ts}`, noStore),
                fetch(`/data/tags.json?t=${ts}`, noStore)
            ]);

            const expectJson = async (res, label) => {
                if (!res.ok) throw new Error(`${label} HTTP ${res.status}`);
                const ct = res.headers.get('content-type') || '';
                if (!ct.includes('application/json')) throw new Error(`${label} non JSON`);
                return res.json();
            };

            this.jerseys = await expectJson(jerseysRes, 'jerseys.json');
            this.categories = await expectJson(categoriesRes, 'categories.json');
            this.tags = await expectJson(tagsRes, 'tags.json');

            console.log('✅ Données chargées:', {
                jerseys: this.jerseys.length,
                categories: this.categories.length,
                tags: this.tags.length
            });
        } catch (error) {
            console.error('❌ Erreur chargement:', error);
            alert('Erreur: ' + error.message);
        }
    }

    createAdminPanel() {
        // Créer le panneau admin
        const adminPanel = document.createElement('div');
        adminPanel.id = 'ultra-admin-panel';
        adminPanel.innerHTML = `
            <div style="
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
                    <h2>🔧 ADMIN FC PALESTINA - VERSION ULTRA-SIMPLE <span id="api-status" style="font-size:14px; margin-left:10px; background:#6c757d; padding:3px 8px; border-radius:4px;">API: ...</span></h2>
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
                    <h3>📋 LISTE DES MAILLOTS</h3>
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
        // Check API backend status after panel exists
        this.checkBackend();
    }

    renderJerseys() {
        const container = document.getElementById('jerseys-list');
        if (!container) return;

        container.innerHTML = '';

        this.jerseys.forEach((jersey, index) => {
            const card = document.createElement('div');
            card.style.cssText = `
                border: 2px solid #ddd;
                border-radius: 10px;
                padding: 15px;
                background: #f9f9f9;
            `;

            card.innerHTML = `
                <div style="text-align: center; margin-bottom: 15px;">
                    <img src="${window.CONFIG.IMAGES_BASE_URL}/${jersey.thumbnail}" 
                         style="width: 100%; height: 200px; object-fit: cover; border-radius: 5px;">
                </div>
                
                <h4 style="margin: 10px 0; color: #8B1538;">${jersey.name || jersey.title || 'Sans nom'}</h4>
                
                <p><strong>Catégorie:</strong> ${this.getCategoryName(jersey.category)}</p>
                <p><strong>Année:</strong> ${jersey.year || 'N/A'}</p>
                <p><strong>Description:</strong> ${(jersey.description || '').substring(0, 100)}...</p>
                <p><strong>Tags:</strong> ${this.renderTagList(jersey.tags)}</p>
                
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
                    
                    <button onclick="window.ultraAdmin.changeCover(${index})" style="
                        background: #28a745;
                        color: white;
                        border: none;
                        padding: 8px 15px;
                        border-radius: 5px;
                        cursor: pointer;
                        flex: 1;
                    ">🖼️ COUVERTURE</button>
                </div>
            `;

            container.appendChild(card);
        });
    }

    renderTagList(tags) {
        if (!tags || tags.length === 0) return 'Aucun';
        const norm = (s) => (s || '').toString().normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase();
        const byId = new Map((this.tags || []).map(t => [norm(t.id), t.name]));
        const byName = new Map((this.tags || []).map(t => [norm(t.name), t.name]));
        const fallback = new Map([
            ['home','Domicile'],['away','Extérieur'],['special','Spéciaux'],['vintage','Vintage']
        ]);
        const seen = new Set();
        const names = [];
        (tags || []).forEach(raw => {
            const n = norm(raw);
            const display = byId.get(n) || byName.get(n) || fallback.get(n) || null;
            if (!display) return;
            const key = norm(display);
            if (seen.has(key)) return;
            seen.add(key);
            names.push(display);
        });
        return names.length ? names.join(', ') : 'Aucun';
    }

    getCategoryName(categoryId) {
        const category = this.categories.find(cat => cat.id === categoryId);
        return category ? category.name : categoryId;
    }

    editJersey(index) {
        this.currentJersey = this.jerseys[index];
        
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
            <div style="
                background: white;
                padding: 30px;
                border-radius: 10px;
                max-width: 500px;
                width: 100%;
                max-height: 80vh;
                overflow-y: auto;
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
                
                <div style="display: flex; gap: 10px; justify-content: flex-end;">
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" style="
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

    changeCover(index) {
        this.currentJersey = this.jerseys[index];
        
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
            <div style="
                background: white;
                padding: 30px;
                border-radius: 10px;
                max-width: 600px;
                width: 100%;
                max-height: 80vh;
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
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" style="
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
        this.currentJersey.category = document.getElementById('edit-category').value;

        // Sauvegarder
        await this.saveToFile();
        
        // Fermer le modal
        document.querySelector('[onclick="window.ultraAdmin.saveJersey()"]').closest('div').remove();
        
        // Recharger l'affichage
        this.renderJerseys();
        
        alert('✅ Maillot sauvegardé avec succès!');
    }

    async saveCover() {
        if (!this.currentJersey) return;

        // Sauvegarder
        await this.saveToFile();
        
        // Fermer le modal
        document.querySelector('[onclick="window.ultraAdmin.saveCover()"]').closest('div').remove();
        
        // Recharger l'affichage
        this.renderJerseys();
        
        alert('✅ Image de couverture sauvegardée!');
    }

    async saveToFile() {
        try {
            console.log('💾 Sauvegarde en cours...');
            
            let response, result;

            if (this.apiMode === 'http') {
                // admin_server.py style: PUT /api/jerseys with raw array
                response = await fetch(`${this.apiBase}/jerseys`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.jerseys)
                });
            } else {
                // flask simple_backend.py style: POST /api/jerseys with { jerseys }
                response = await fetch(`${this.apiBase}/jerseys`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ jerseys: this.jerseys })
                });
                // If POST not allowed, fallback to PUT format
                if (!response.ok && (response.status === 404 || response.status === 405)) {
                    response = await fetch(`${this.apiBase}/jerseys`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(this.jerseys)
                    });
                    this.apiMode = 'http';
                }
            }

            if (!response.ok) {
                const text = await response.text().catch(() => '');
                throw new Error(`Erreur ${response.status}: ${response.statusText} ${text}`);
            }
            result = await response.json().catch(() => ({}));
            console.log('✅ Sauvegarde réussie!', result);
            // Rafraîchir les données depuis disque pour éviter le cache
            await this.loadData();
            this.renderJerseys();

        } catch (error) {
            console.error('❌ Erreur sauvegarde:', error);
            alert('❌ Erreur: ' + error.message);
        }
    }

    async checkBackend() {
        const el = document.getElementById('api-status');
        if (!el) return;
        try {
            const res = await fetch(`${this.apiBase}/jerseys`, { cache: 'no-store' });
            const ct = res.headers.get('content-type') || '';
            if (!res.ok || !ct.includes('application/json')) throw new Error('API non disponible');
            // Detect admin_server (has /stats)
            try {
                const stats = await fetch(`${this.apiBase}/stats`, { cache: 'no-store' });
                this.apiMode = stats.ok ? 'http' : 'flask';
            } catch { this.apiMode = 'flask'; }
            el.textContent = this.apiMode === 'http' ? 'API: OK (admin)' : 'API: OK (flask)';
            el.style.background = '#28a745';
        } catch (e) {
            el.textContent = 'API: OFF';
            el.style.background = '#dc3545';
        }
    }

    open() {
        document.getElementById('ultra-admin-panel').style.display = 'block';
    }

    close() {
        document.getElementById('ultra-admin-panel').style.display = 'none';
    }

    async refresh() {
        await this.loadData();
        this.renderJerseys();
        alert('✅ Données rechargées!');
    }

    bindEvents() {
        // Pas besoin d'événements complexes
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
