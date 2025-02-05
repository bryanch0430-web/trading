  import axios from "axios";
  import { useAuthStore } from '../store/authStore';

  function jwtHttpInstanceFactory(baseURL, timeout) {
    const instance = axios.create({
      baseURL: baseURL,
      timeout: timeout,
    });

  // Request interceptor to add the Authorization header
    instance.interceptors.request.use(
      (config) => {
        const authStore = useAuthStore();
        if (authStore.token) {
          config.headers.Authorization = `Bearer ${authStore.token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    instance.interceptors.response.use(
      function (response) {
        const isRequestSuccess =
          response.status === 200 || response.status === 201;
  
        if (isRequestSuccess) {
          return Promise.resolve(response.data); // Resolve with response data
        }
  
        return Promise.reject(response); // Reject the promise for non-successful responses
      },
      function (error) {
        if (error.response && error.response.status === 401) {
          const authStore = useAuthStore();
          authStore.logout();
          // Optionally, redirect to login page
          alert("Account information incorrect, please login again.");
          window.location.href = '/';
        }
        return Promise.reject(error); // Forward the error to the caller
      }
    );
  
    return instance;
  }

  export default jwtHttpInstanceFactory;



