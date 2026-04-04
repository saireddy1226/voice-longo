// Authentication and User Management

class AuthManager {
    constructor() {
        this.currentUser = null;
        this.loadUserFromStorage();
    }

    async register(name, email, password, language = 'English') {
        try {
            const response = await fetch(`${CONFIG.SERVER_URL}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password,
                    language: language
                })
            });

            const data = await response.json();

            if (data.success) {
                this.currentUser = {
                    user_id: data.user_id,
                    name: name,
                    email: email,
                    language: language
                };
                this.saveUserToStorage();
                return { success: true, user: this.currentUser };
            } else {
                return { success: false, error: data.detail };
            }
        } catch (error) {
            console.error('Registration error:', error);
            return { success: false, error: error.message };
        }
    }

    async login(user_id, password) {
        try {
            const response = await fetch(`${CONFIG.SERVER_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: user_id,
                    password: password
                })
            });

            const data = await response.json();

            if (data.success) {
                this.currentUser = {
                    user_id: data.user.user_id,
                    name: data.user.name,
                    email: data.user.email,
                    language: data.user.language
                };
                this.saveUserToStorage();
                return { success: true, user: this.currentUser };
            } else {
                return { success: false, error: data.detail };
            }
        } catch (error) {
            console.error('Login error:', error);
            return { success: false, error: error.message };
        }
    }

    logout() {
        this.currentUser = null;
        localStorage.removeItem('currentUser');
    }

    saveUserToStorage() {
        localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
    }

    loadUserFromStorage() {
        const stored = localStorage.getItem('currentUser');
        if (stored) {
            this.currentUser = JSON.parse(stored);
        }
    }

    isLoggedIn() {
        return this.currentUser !== null;
    }

    getCurrentUser() {
        return this.currentUser;
    }
}

const authManager = new AuthManager();

async function checkUserId(id) {
    const res = await fetch(`${CONFIG.SERVER_URL}/check-userid/${id}`);
    const data = await res.json();
    if (data.available) {
        console.log("✔ Username available");
    } else {
        console.log("❌ Username already taken");
    }
}