// Toggle password visibility
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

// Show alert
function showAlert(message, type = 'error') {
    const alert = document.getElementById('alert');
    alert.textContent = message;
    alert.className = `alert alert-${type}`;
    alert.style.display = 'block';
    
    setTimeout(() => {
        alert.style.display = 'none';
    }, 5000);
}

// Form submission
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const loginBtn = document.getElementById('loginBtn');
    const btnText = document.getElementById('btnText');
    const loadingSpinner = document.querySelector('.loading-spinner');
    
    // Disable button and show loading
    loginBtn.disabled = true;
    btnText.style.display = 'none';
    loadingSpinner.style.display = 'block';
    
    try {
        const response = await fetch('http://localhost:8001/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // Important pour les cookies de session
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Stocker uniquement le username (la session est gérée par cookie)
            localStorage.setItem('adminUser', username);
            
            showAlert('Connexion réussie! Redirection...', 'success');
            
            setTimeout(() => {
                window.location.href = 'admin_production.html';
            }, 1000);
        } else {
            showAlert(data.error || 'Identifiants incorrects');
            loginBtn.disabled = false;
            btnText.style.display = 'block';
            loadingSpinner.style.display = 'none';
        }
    } catch (error) {
        console.error('Login error:', error);
        showAlert('Erreur de connexion au serveur. Vérifiez que le backend est démarré.');
        loginBtn.disabled = false;
        btnText.style.display = 'block';
        loadingSpinner.style.display = 'none';
    }
});

// Check if already logged in
window.addEventListener('DOMContentLoaded', () => {
    // Vérifier la session avec le backend (via cookies)
    fetch('http://localhost:8001/api/auth/status', {
        credentials: 'include' // Important pour inclure les cookies de session
    })
    .then(response => response.json())
    .then(data => {
        if (data.authenticated) {
            window.location.href = 'admin_production.html';
        }
    })
    .catch(err => console.log('Session check failed'));
});

// Enter key support
document.getElementById('username').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('password').focus();
    }
});
