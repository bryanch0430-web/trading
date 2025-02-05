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
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '../store/authStore';
  
  export default {
    name: 'LoginPage',
    setup() {
      const username = ref('');
      const password = ref('');
      const errorMessage = ref('');
      const authStore = useAuthStore();
      const router = useRouter();
  
      const handleLogin = async () => {
        errorMessage.value = '';
        try {
          // Call the login action in your auth store
          await authStore.login(username.value, password.value);
          // After successful login, navigate to the Transactions page or any protected route
          router.push({ name: 'Transactions' });
        } catch (error) {
          errorMessage.value = 'Invalid username or password. Please try again.';
        }
      };
  
      return {
        username,
        password,
        errorMessage,
        handleLogin,
      };
    },
  };
  </script>
  
  <style scoped>
  .login-container {
    max-width: 400px;
    margin: 80px auto;
    padding: 2rem;
    border: 1px solid #cccccc;
    border-radius: 8px;
    background-color: #f9f9f9;
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
  input[type='password'] {
    width: 100%;
    padding: 0.6rem;
    border: 1px solid #cccccc;
    border-radius: 4px;
  }
  
  .btn {
    width: 100%;
    padding: 0.8rem;
    background-color: #007bff;
    border: none;
    color: white;
    font-size: 1rem;
    cursor: pointer;
    border-radius: 4px;
  }
  
  .btn:hover {
    background-color: #0056b3;
  }
  
  .error-message {
    color: red;
    margin-top: 1rem;
    text-align: center;
  }
  </style>
