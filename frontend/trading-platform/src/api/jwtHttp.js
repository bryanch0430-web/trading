
import jwtHttpInstanceFactory from "./jwtHttpInstanceFactory.js";

const backend_url = "http://localhost:8000";
const timeout = 30 * 1000;
const baseURL = backend_url;

const instance = jwtHttpInstanceFactory(baseURL, timeout);



export default instance;
