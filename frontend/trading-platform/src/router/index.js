import { createRouter, createWebHistory } from 'vue-router';
import TransactionPage from '../views/TransactionPage.vue';
import UserAssetPage from '../views/UserAssetPage.vue';
import AssetDisplayPage from '../views/AssetDisplayPage.vue';
import AllAssetsPage from '../views/AllAssetsPage.vue';
import LoginPage from '../views/Login.vue';
import { useAuthStore } from '../store/authStore';

const routes = [
  {
    path: '/transacts',
    name: 'Transactions',
    component: TransactionPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/assets',
    name: 'UserAssets',
    component: UserAssetPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/all-assets/:id',
    name: 'AssetDisplay',
    component: AssetDisplayPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/all-assets',
    name: 'AllAssets',
    component: AllAssetsPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/',
    name: 'Login',
    component: LoginPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Global navigation guard to protect routes that require authentication
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  // If the route requires authentication and the user is not logged in
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next({ name: 'Login' });
  } else if (to.name === 'Login' && authStore.isLoggedIn) {
    // Optionally redirect already logged in users away from the login page
    next({ name: 'UserAssets' });
  } else {
    next();
  }
});

export default router;
