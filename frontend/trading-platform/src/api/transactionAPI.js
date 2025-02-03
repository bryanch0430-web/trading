import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

async function fetchTransactions(user_id, skip = 0, limit = 25) {
    try {
      const requestUrl = `${API_BASE_URL}/transactions/transactions?user_id=${user_id}&skip=${skip}&limit=${limit}`;
  
      const response = await axios.get(requestUrl);
  
      console.log("Response Data:", response.data);
  
      return response
    } catch (error) {
      console.error("Error fetching transactions:", error);
      throw error; 
    }
  }




export{
    fetchTransactions,
    
}