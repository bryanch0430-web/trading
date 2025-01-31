<!-- src/App.vue -->
<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="nav-link">Transactions</router-link>
        <router-link to="/assets" class="nav-link">User Assets</router-link>
        <router-link to="/all-assets" class="nav-link">All Assets</router-link>
      </div>
    </nav>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
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
</style>