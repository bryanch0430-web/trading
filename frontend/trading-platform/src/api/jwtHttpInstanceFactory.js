import axios from "axios";

function jwtHttpInstanceFactory(baseURL, timeout) {
  const instance = axios.create({
    baseURL: baseURL,
    timeout: timeout,
  });

  // Request interceptor (without adding Authorization header)
  instance.interceptors.request.use(
    (config) => {
      // You can add other request modifications here if needed
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response interceptor (without handling 401 errors)
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
      // Forward the error to the caller without handling 401 errors
      return Promise.reject(error);
    }
  );

  return instance;
}

export default jwtHttpInstanceFactory;
