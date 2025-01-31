// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import TransactionPage from '../views/TransactionPage.vue';
import UserAssetPage from '../views/UserAssetPage.vue';
import AssetDisplayPage from '../views/AssetDisplayPage.vue';

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
    path: '/asset/:id',
    name: 'AssetDisplay',
    component: AssetDisplayPage,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;