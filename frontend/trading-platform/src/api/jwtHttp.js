
import jwtHttpInstanceFactory from "./jwtHttpInstanceFactory.js";

const backend_url = import.meta.env.VITE_BACKEND_URL;
const timeout = 30 * 1000;
const baseURL = backend_url;

const instance = jwtHttpInstanceFactory(baseURL, timeout);



export default instance;
