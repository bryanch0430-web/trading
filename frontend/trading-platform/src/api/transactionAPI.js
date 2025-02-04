import http from "./jwtHttp.js";

async function fetchTransactions(user_id, skip = 0, limit = 25) {
    try {
      const requestUrl = `/transactions/transactions?user_id=${user_id}&skip=${skip}&limit=${limit}`;
  
      const response = await http.get(requestUrl);
  
  
      return response
    } catch (error) {
      console.error("Error fetching transactions:", error);
      throw error; 
    }
  }


// Deposit Transaction
async function depositTransaction(depositData) {
  try {
    const response = await http.post("/transactions/deposit", depositData);
    return response; // assuming the successful response returns the transaction data
  } catch (error) {
    console.error("Error during deposit transaction:", error);
    throw error;
  }
}

// Withdraw Transaction
async function withdrawTransaction(withdrawData) {
  try {
    const response = await http.post("/transactions/withdraw", withdrawData);
    return response;
  } catch (error) {
    console.error("Error during withdraw transaction:", error);
    throw error;
  }
}

// Buy Transaction
async function buyTransaction(buyData) {
  try {
    const response = await http.post("/transactions/buy", buyData);
    return response;
  } catch (error) {
    console.error("Error during buy transaction:", error);
    throw error;
  }
}

// Sell Transaction
async function sellTransaction(sellData) {
  try {
    const response = await http.post("/transactions/sell", sellData);
    return response;
  } catch (error) {
    console.error("Error during sell transaction:", error);
    throw error;
  }
}

export default {
  fetchTransactions,
  depositTransaction,
  withdrawTransaction,
  buyTransaction,
  sellTransaction,
};


