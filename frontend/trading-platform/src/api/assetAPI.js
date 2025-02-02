import axios from "axios";

const API_BASE_URL = "http://localhost:8000";



async function ListAsset() {
    try {
      const requestUrl = `${API_BASE_URL}/assets/list_all_asset`;
  
      const response = await axios.get(requestUrl);
  
  
      return response
    } catch (error) {
      console.error("Error fetching transactions:", error);
      throw error; 
    }
  }


export{
    ListAsset,
    
}