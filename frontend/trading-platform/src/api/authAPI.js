import http from "./jwtHttp.js";

const getLoginToken = async (payload) => {
    const response = await http.post('/users/token', payload);
  return response;
};

const getUserProfile = async () => {
    const userResponse = await http.get('/users/me');
    return userResponse;
};


export default {
    getLoginToken,
    getUserProfile,
};
