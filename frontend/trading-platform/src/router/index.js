import { createRouter, createWebHistory } from 'vue-router';
import TransactionPage from '../views/TransactionPage.vue';
import UserAssetPage from '../views/UserAssetPage.vue';
import AssetDisplayPage from '../views/AssetDisplayPage.vue';
import AllAssetsPage from '../views/AllAssetsPage.vue'; 

const routes = [
  {
    path: '/',
    name: 'Transactions',
    component: TransactionPage,
  },
  {
    path: '/assets',
    name: 'UserAssets',
    component: UserAssetPage,
  },
  {
    path: '/all-assets/:id',
    name: 'AssetDisplay',
    component: AssetDisplayPage,
  },
  {
    path: '/all-assets', // Define the new route path
    name: 'AllAssets',
    component: AllAssetsPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;