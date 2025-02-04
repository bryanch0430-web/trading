import http from "./jwtHttp.js";


async function ListAsset() {
    try {
      const requestUrl = `/assets/list_all_asset`;
  
      const response = await http.get(requestUrl);
  
  
      return response
    } catch (error) {
      console.error("Error fetching transactions:", error);
      throw error; 
    }
  }

  async function ListAssetPrice(assetId){
    try {
      const requestUrl = `/assets/get_asset_price/${assetId}`;
  
      const response = await http.get(requestUrl);
  
      return response
    } catch (error) {
      console.error("Error fetching transactions:", error);
      throw error; 
    }
  }


  async function getUserAssets(userId) {
    try {
      const requestUrl = `/assets/get_user_asset?user_id=${userId}`;
      const response = await http.get(requestUrl);
      return response;
    } catch (error) {
      console.error(`Error fetching assets for user ID ${userId}:`, error);
      throw error;
    }
  }

async function calculateUserAsset(userId) {
    try {
      const requestUrl = `/assets/calculate_asset_type_distribution/${userId}`;
      const response = await http.get(requestUrl);
      return response;
    } catch (error) {
      console.error(`Error fetching assets for user ID ${userId}:`, error);
      throw error;
    }
  }

export default {
    ListAsset,
    ListAssetPrice,
    getUserAssets,
    calculateUserAsset
    
}




