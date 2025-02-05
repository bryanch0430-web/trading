import { defineStore } from 'pinia';
import authApi from "../api/authAPI.js";

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('access_token') || '',
    user: null,
    userName: '',
  }),
  actions: {
    async login(username, password) {
      try {
        const payload={
            username:username,
            password:password

        }
        const response = await authApi.getLoginToken(payload);
        this.token = response.access_token;
        localStorage.setItem('access_token', this.token);
        await this.fetchUser();
        return true;
      } catch (error) {
        console.error('Login failed:', error);
        throw error;
      }
    },
    logout() {
      this.token = '';
      this.user = null;
      localStorage.removeItem('access_token');
      localStorage.removeItem('userId');
      localStorage.removeItem('userName');

    },
    async fetchUser() {
      try {
        // const token = localStorage.getItem('access_token');
        const userResponse = await authApi.getUserProfile();
        this.user = userResponse;
        localStorage.setItem('userName', this.user.username);
        localStorage.setItem('userId', this.user.id);

      } catch (error) {
        console.error('Failed to fetch user:', error);
        this.logout();
      }
    },
    async register(username, email, password) {
      try {
        const payload = {
          username: username,
          email: email,
          password: password,
        };
        const response = await authApi.registerUser(payload);
        return response; 
      } catch (error) {
        console.error("Registration failed:", error);
        throw error;
      }
    },
  },
  getters: {
    isLoggedIn: (state) => !!state.token,
  }
});

export default useAuthStore;

