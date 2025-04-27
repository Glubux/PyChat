document.getElementById('username').addEventListener('input', function() {
    checkUsername();
});
  
document.getElementById('password').addEventListener('input', function() {
    checkPassword();
});
  
document.getElementById('confirm-password').addEventListener('input', function() {
    checkPasswordMatch();
});
  
// Prüft, ob der Benutzername korrekt ist
function checkUsername() {
    const username = document.getElementById('username').value;
    const usernameInput = document.getElementById('username');
    const usernameError = document.getElementById('username-error');
  
    // Fehlerhinweise als Liste
    let errors = [];
    if (username.length < 3) {
        errors.push("Benutzername muss mindestens 3 Zeichen lang sein.");
    }
    
    if (errors.length > 0) {
        usernameInput.classList.add('invalid');
        usernameInput.classList.remove('valid');
        usernameError.innerHTML = "<ul>" + errors.map(error => `<li>${error}</li>`).join('') + "</ul>";
    } else {
        usernameInput.classList.add('valid');
        usernameInput.classList.remove('invalid');
        usernameError.innerHTML = "";  // Fehlerhinweis entfernen
    }
}
  
// Prüft, ob das Passwort den Kriterien entspricht
function checkPassword() {
    const password = document.getElementById('password').value;
    const passwordInput = document.getElementById('password');
    const passwordError = document.getElementById('password-error');
    
    const minLength = 6;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
  
    // Fehlerhinweise als Liste
    let errors = [];
  
    if (password.length < minLength) {
        errors.push("6 Zeichen");
    }
    if (!hasUpperCase) {
        errors.push("Großbuchstaben");
    }
    if (!hasLowerCase) {
        errors.push("Kleinbuchstaben");
    }
    if (!hasNumber) {
        errors.push("Zahlen");
    }
    if (!hasSpecialChar) {
        errors.push("Sonderzeichen");
    }
  
    if (errors.length > 0) {
        passwordError.innerHTML = "<ul>" + errors.map(error => `<li>${error}</li>`).join('') + "</ul>";
        passwordInput.classList.add('invalid');
        passwordInput.classList.remove('valid');
    } else {
        passwordError.innerHTML = "";  // Fehlerhinweis entfernen
        passwordInput.classList.add('valid');
        passwordInput.classList.remove('invalid');
    }
}
  
// Prüft, ob das Passwort und die Bestätigung übereinstimmen
function checkPasswordMatch() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const confirmPasswordInput = document.getElementById('confirm-password');
    const confirmPasswordError = document.getElementById('confirm-password-error');
  
    // Fehlerhinweise als Liste
    if (password !== confirmPassword) {
        confirmPasswordError.innerHTML = "<ul><li>Die Passwörter stimmen nicht überein.</li></ul>";
        confirmPasswordInput.classList.add('invalid');
        confirmPasswordInput.classList.remove('valid');
    } else {
        confirmPasswordError.innerHTML = "";  // Fehlerhinweis entfernen
        confirmPasswordInput.classList.add('valid');
        confirmPasswordInput.classList.remove('invalid');
    }
}
