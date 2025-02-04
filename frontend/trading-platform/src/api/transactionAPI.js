import http from "./jwtHttp.js";

async function fetchTransactions(user_id, skip = 0, limit = 25) {
    try {
      const requestUrl = `/transactions/transactions?user_id=${user_id}&skip=${skip}&limit=${limit}`;
  
      const response = await http.get(requestUrl);
  
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
