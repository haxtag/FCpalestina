/**
 * SOLUTION DE SECOURS - FORMULAIRE SIMPLE
 * Si FormSubmit ne fonctionne toujours pas, utilisez cette solution
 */

// Alternative 1: Ouvrir le client email avec mailto (marche toujours)
function sendEmailWithMailto() {
    const nom = document.querySelector('input[name="name"]').value;
    const email = document.querySelector('input[name="email"]').value;
    const message = document.querySelector('textarea[name="message"]').value;
    
    const subject = "Nouveau message depuis FC Palestina";
    const body = `Nom: ${nom}\nEmail: ${email}\n\nMessage:\n${message}`;
    
    const mailtoLink = `mailto:maillots.du.peuple91@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.location.href = mailtoLink;
}

// Alternative 2: EmailJS (gratuit, 200 emails/mois)
// 1. Créer compte sur https://www.emailjs.com/
// 2. Configurer service email (Gmail)
// 3. Remplacer les IDs ci-dessous

function initEmailJS() {
    // Script EmailJS
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js';
    script.onload = () => {
        emailjs.init("YOUR_PUBLIC_KEY"); // Remplacer par votre clé publique
    };
    document.head.appendChild(script);
}

function sendWithEmailJS(event) {
    event.preventDefault();
    
    const formData = {
        from_name: document.querySelector('input[name="name"]').value,
        from_email: document.querySelector('input[name="email"]').value,
        message: document.querySelector('textarea[name="message"]').value,
        to_email: "maillots.du.peuple91@gmail.com"
    };
    
    emailjs.send('YOUR_SERVICE_ID', 'YOUR_TEMPLATE_ID', formData)
        .then(() => {
            alert('Message envoyé avec succès ! 🎉');
            document.querySelector('.contact-form').reset();
        })
        .catch((error) => {
            console.error('Erreur:', error);
            alert('Erreur lors de l\'envoi. Réessayez plus tard.');
        });
}

// Alternative 3: Webhook simple (Zapier, Make.com)
function sendWithWebhook(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    fetch('https://hooks.zapier.com/hooks/catch/YOUR_WEBHOOK_ID/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(() => {
        alert('Message envoyé ! 📧');
        event.target.reset();
    })
    .catch(() => {
        // Fallback vers mailto si webhook ne marche pas
        sendEmailWithMailto();
    });
}

// POUR TESTER - Remplacer le formulaire par cette version si FormSubmit ne marche pas
const formBackupHTML = `
<form class="contact-form" onsubmit="sendEmailWithMailto(); return false;">
    <div class="form-group">
        <input type="text" name="name" placeholder="Votre nom" required>
    </div>
    <div class="form-group">
        <input type="email" name="email" placeholder="votre@email.com" required>
    </div>
    <div class="form-group">
        <textarea name="message" placeholder="Votre message" rows="5" required></textarea>
    </div>
    <button type="submit" class="btn btn-primary">📧 Ouvrir mon client email</button>
    <p style="font-size: 12px; color: #666; margin-top: 10px;">
        Cela ouvrira votre client email avec le message pré-rempli
    </p>
</form>
`;

console.log("🔧 Solutions de secours pour formulaire prêtes !");
console.log("📧 Pour utiliser mailto: remplacez le formulaire par formBackupHTML");
console.log("⚡ Pour EmailJS: configurez sur emailjs.com puis utilisez sendWithEmailJS");