import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

async function ListUserAsset(userid) {
    try {
      const requestUrl = `${API_BASE_URL}/users/${userid}/assets`;
      const response = await axios.get(requestUrl);
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


