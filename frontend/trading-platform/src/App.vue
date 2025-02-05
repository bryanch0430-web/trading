<!-- src/App.vue -->
<template>
  <div id="app">
    <nav v-if="$route.name !== 'Login'" class="navbar">
      <div class="nav-container">
        <router-link to="/transacts" class="nav-link">Transactions</router-link>
        <router-link to="/assets" class="nav-link">User Assets</router-link>
        <router-link to="/all-assets" class="nav-link">All Assets</router-link>
        <button class="logout-btn" @click="handleLogout">Logout</button>

      </div>
    </nav>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>


<script>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from './store/authStore';

export default {
  name: 'App',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const authStore = useAuthStore();

    // Only show the navbar if the current route is not the Login page.
    const showNavbar = computed(() => route.name !== 'Login');

    // Logout handler that calls the store logout function and then redirects to the login page.
    const handleLogout = () => {
      authStore.logout(); // This should clear any tokens or user data
      router.push({ name: 'Login' });
    };

    return {
      showNavbar,
      handleLogout,
    };
  },
};
</script>

<style>
/* Reset some default styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Navbar Styles */
.navbar {
  position: fixed; /* Fixes the navbar to the top */
  top: 0;
  left: 0;
  width: 100%; /* Full width */
  background-color: var(--color-panel);
  padding: 16px 32px; /* Adjust padding as needed */
  display: flex;
  justify-content: center; /* Centers the nav content */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Optional: Adds a subtle shadow */
  z-index: 1000; /* Ensures the navbar stays above other elements */
}

.nav-container {
  display: flex;
  gap: 24px; /* Increased gap for better spacing */
}

/* Nav Link Styles */
.nav-link {
  color: var(--color-text);
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: var(--color-primary-light); /* Optional: Change color on hover */
}

.router-link-active {
  color: var(--color-primary);
  border-bottom: 2px solid var(--color-primary); /* Optional: Adds an underline to active link */
}

/* Main Content Styles */
.content {
  flex: 1;
  padding: 80px 32px 32px; /* Top padding accounts for the fixed navbar height */
  background-color: var(--color-background); /* Optional: Set a background color */
}

/* Responsive Design (Optional) */
@media (max-width: 768px) {
  .navbar {
    padding: 12px 16px;
  }

  .nav-container {
    gap: 16px;
  }

  .content {
    padding: 72px 16px 16px;
  }
}


.logout-btn {
  background-color: #BB86FC;
  color: #fff;
  border: none;
  padding: 8px 16px;
  cursor: pointer;
  border-radius: 4px;
}

.logout-btn:hover {
  background-color: #fff;
}
</style>

