import http from "./jwtHttp.js";


async function ListUserAsset(userid) {
    try {
      const requestUrl = `/users/${userid}/assets`;
      const response = await http.get(requestUrl);
      console.log(response.data)
      return response.data
    } catch (error) {
      console.error("Error fetching transactions:", error);
      throw error; 
    }
  }


  export{
    ListUserAsset
    
}


