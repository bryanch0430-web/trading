import axios from "axios";

const API_BASE_URL = "http://localhost:8000";



async function ListAsset() {
    try {
      const requestUrl = `${API_BASE_URL}/assets/list_all_asset`;
  
      const response = await axios.get(requestUrl);
  
  
      return response.data
    } catch (error) {
      console.error("Error fetching transactions:", error);
      throw error; 
    }
  }

  async function ListAssetPrice(assetId){
    try {
      const requestUrl = `${API_BASE_URL}/assets/get_asset_price/${assetId}`;
  
      const response = await axios.get(requestUrl);
  
      return response.data
    } catch (error) {
      console.error("Error fetching transactions:", error);
      throw error; 
    }
  }


  async function getUserAssets(userId) {
    try {
      const requestUrl = `${API_BASE_URL}/assets/get_user_asset?user_id=${userId}`;
      const response = await axios.get(requestUrl);
      return response.data;
    } catch (error) {
      console.error(`Error fetching assets for user ID ${userId}:`, error);
      throw error;
    }
  }
export{
    ListAsset,
    ListAssetPrice,
    getUserAssets
    
}


