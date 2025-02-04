import http from "./jwtHttp.js";


async function ListUserAsset(userid) {
    try {
      const requestUrl = `/users/${userid}/assets`;
      const response = await http.get(requestUrl);
      return response
    } catch (error) {
      console.error("Error fetching transactions:", error);
      throw error; 
    }
  }


async function ShowUserValueTrend(userid) {
    try {
      const requestUrl = `/users/${userid}/value-history`;
      const response = await http.get(requestUrl);
      return response
    } catch (error) {
      console.error("Error fetching transactions:", error);
      throw error; 
    }
  }
export default {
    ListUserAsset,
    ShowUserValueTrend
    
}

