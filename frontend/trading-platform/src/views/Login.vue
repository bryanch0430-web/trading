<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">Username:</label>
        <input
          type="text"
          id="username"
          v-model="username"
          required
          placeholder="Enter username"
        />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          v-model="password"
          required
          placeholder="Enter password"
        />
      </div>
      <button type="submit" class="btn">Login</button>
    </form>
    <p v-if="loginError" class="error-message">{{ loginError }}</p>
    <p class="register-link">
      Don't have an account? 
      <button @click="openRegisterModal" class="register-btn">Register</button>
    </p>

    <!-- Registration Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2>Register</h2>
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label for="reg-username">Username:</label>
            <input
              type="text"
              id="reg-username"
              v-model="regUsername"
              required
              placeholder="Enter username"
            />
          </div>
          <div class="form-group">
            <label for="email">Email:</label>
            <input
              type="email"
              id="email"
              v-model="regEmail"
              required
              placeholder="Enter email"
            />
          </div>
          <div class="form-group">
            <label for="reg-password">Password:</label>
            <input
              type="password"
              id="reg-password"
              v-model="regPassword"
              required
              placeholder="Enter password"
            />
          </div>
          <div class="button-group">
            <button type="submit" class="btn">Register</button>
            <button type="button" class="btn cancel-btn" @click="closeModal">Cancel</button>
          </div>
        </form>
        <p v-if="regSuccess" class="success-message">{{ regSuccess }}</p>
        <p v-if="regError" class="error-message">{{ regError }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/authStore';

const username = ref('');
const password = ref('');
const loginError = ref('');
const showModal = ref(false);

const regUsername = ref('');
const regEmail = ref('');
const regPassword = ref('');
const regError = ref('');
const regSuccess = ref('');

const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  loginError.value = '';
  try {
    await authStore.login(username.value, password.value);
    // Navigate to a protected route after successful login
    router.push({ name: 'UserAssets' }); // Adjust the route name as needed.
  } catch (error) {
    loginError.value = 'Invalid username or password. Please try again.';
  }
};

const handleRegister = async () => {
  regError.value = '';
  regSuccess.value = '';
  try {
    await authStore.register(regUsername.value, regEmail.value, regPassword.value);
    regSuccess.value = 'Registration successful! You can now log in.';
    // Reset registration form after a brief delay or close modal directly.
    setTimeout(() => {
      closeModal();
      // Optionally, clear the registration fields
      regUsername.value = '';
      regEmail.value = '';
      regPassword.value = '';
      regSuccess.value = '';
    }, 1500);
  } catch (error) {
    regError.value = 'Registration failed. Please check your input and try again.';
  }
};

const openRegisterModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  // Clear state on close
  regError.value = '';
  regSuccess.value = '';
};
</script>

<style scoped>
/* Login container styles */
.login-container {
  background-color: var(--color-panel);
  max-width: 400px;
  margin: 80px auto;
  padding: 2rem;
  border-radius: 8px;
}

h1 {
  text-align: center;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.2rem;
}

label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: bold;
}

input[type='text'],
input[type='password'],
input[type='email'] {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #cccccc;
  border-radius: 4px;
}

.btn {
  width: 100%;
  padding: 0.8rem;
  background-color: #BB86FC;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 4px;
  margin-top: 0.5rem;
}

.btn:hover {
  background-color: #0056b3;
}

.cancel-btn {
  background-color: #6c757d;
}

.cancel-btn:hover {
  background-color: #565e64;
}

.error-message {
  color: red;
  margin-top: 1rem;
  text-align: center;
}

.success-message {
  color: green;
  margin-top: 1rem;
  text-align: center;
}

/* Style for the register link */
.register-link {
  margin-top: 1rem;
  text-align: center;
}

.register-btn {
  background: none;
  border: none;
  color: #BB86FC;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
  font-size: 1rem;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
   background-color: rgba(0, 0, 0, 0.5); 
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background-color: var(--color-panel);
  padding: 24px;
  border-radius: var(--border-radius);
  width: 90%;
  max-width: 400px;
}

.button-group {
  display: flex;
  gap: 16px;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .modal {
    width: 95%;
  }
}
</style>

