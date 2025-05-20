// API base URL - update this to your FastAPI server address
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const createUserSection = document.getElementById('createUserSection');
const accountDetailsSection = document.getElementById('accountDetailsSection');
const userNameInput = document.getElementById('userName');
const createUserBtn = document.getElementById('createUserBtn');
const createUserMessage = document.getElementById('createUserMessage');
const userNameDisplay = document.getElementById('userName-display');
const routingNumberDisplay = document.getElementById('routing-number');
const accountNumberDisplay = document.getElementById('account-number');
const accountBalanceDisplay = document.getElementById('account-balance');
const showDepositFormBtn = document.getElementById('showDepositFormBtn');
const depositForm = document.getElementById('depositForm');
const depositAmountInput = document.getElementById('depositAmount');
const submitDepositBtn = document.getElementById('submitDepositBtn');
const cancelDepositBtn = document.getElementById('cancelDepositBtn');
const depositMessage = document.getElementById('depositMessage');
const transactionList = document.getElementById('transaction-list');
const noTransactions = document.getElementById('noTransactions');
const refreshBtn = document.getElementById('refreshBtn');

// Initialize the Molecule Account Presenter for reactive state management
const { stateFlow: accountState, processor: accountProcessor } = Molecule.AccountPresenter.create();

// Authentication token from local storage
let authToken = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    // Check if user is authenticated with JWT
    authToken = localStorage.getItem('bankAuthToken');
    
    if (authToken) {
        // User is authenticated, get user info and load account
        getUserInfoAndLoadAccount();
    } else {
        // Redirect to login page if not authenticated
        window.location.href = 'login.html';
    }
    
    // Set up event listeners
    setupEventListeners();
    
    // Set up reactive UI with Molecule
    setupReactiveUI();
});

// Set up all event listeners
function setupEventListeners() {
    // Show deposit form button
    showDepositFormBtn.addEventListener('click', () => {
        depositForm.style.display = 'block';
        depositMessage.textContent = '';
    });
    
    // Cancel deposit button
    cancelDepositBtn.addEventListener('click', () => {
        depositForm.style.display = 'none';
        depositAmountInput.value = '';
        depositMessage.textContent = '';
    });
    
    // Submit deposit button
    submitDepositBtn.addEventListener('click', makeDeposit);
    
    // Refresh button
    refreshBtn.addEventListener('click', () => getUserInfoAndLoadAccount());
    
    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logOut);
    }
}

// Set up reactive UI with Molecule
function setupReactiveUI() {
    console.debug('[Account Debug] Setting up reactive UI');
    Molecule.connectView(accountState, (state) => {
        console.debug('[Account Debug] State updated:', state);
        // Update UI based on account state changes
        
        // Handle loading state
        if (state.isLoading) {
            // Show loading indicator
            accountDetailsSection.innerHTML = `
                <div class="col-md-12 text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="sr-only">Loading...</span>
                    </div>
                    <p>Loading your account details...</p>
                </div>
            `;
            return;
        }
        
        // Handle error state
        if (state.error) {
            // Create a more user-friendly error display
            accountDetailsSection.innerHTML = `
                <div class="col-md-12">
                    <div class="account-details">
                        <h3>Error Loading Account</h3>
                        <div class="alert alert-danger">
                            ${state.error}
                        </div>
                        <p>Please try again or create a new account.</p>
                        <button class="btn btn-primary" onclick="window.location.reload()">Retry</button>
                        <button class="btn btn-secondary" onclick="logOut()">Back to Login</button>
                    </div>
                </div>
            `;
            return;
        }
        
        // Restore the account section HTML if it was replaced with loading indicator
        if (!document.getElementById('userName-display') && document.getElementById('accountDetailsSection')) {
            // Reload the page to restore the HTML structure
            window.location.reload();
            return;
        }
        
        // Update user and account information if available
        if (state.user) {
            userNameDisplay.textContent = state.user.name || state.user.username;
        }
        
        if (state.account) {
            routingNumberDisplay.textContent = state.account.routing_number || 'N/A';
            accountNumberDisplay.textContent = state.account.account_number || 'N/A';
            accountBalanceDisplay.textContent = state.account.balance ? parseFloat(state.account.balance).toFixed(2) : '0.00';
        }
        
        // Update transactions list if available
        if (state.transactions && state.transactions.length > 0) {
            // Clear existing transactions
            transactionList.innerHTML = '';
            noTransactions.style.display = 'none';
            
            state.transactions.forEach(transaction => {
                const row = document.createElement('tr');
                
                // Format date
                const date = new Date(transaction.timestamp);
                const formattedDate = `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
                
                // Determine transaction type and add CSS class
                const amountClass = parseFloat(transaction.amount) >= 0 ? 'positive' : 'negative';
                const transactionType = parseFloat(transaction.amount) >= 0 ? 'Deposit' : 'Withdrawal';
                
                // Format amount with two decimal places and add $ sign
                const formattedAmount = '$' + Math.abs(parseFloat(transaction.amount)).toFixed(2);
                
                row.innerHTML = `
                    <td>${formattedDate}</td>
                    <td>${transactionType}</td>
                    <td class="${amountClass}">${formattedAmount}</td>
                `;
                
                transactionList.appendChild(row);
            });
        } else if (state.account) {
            // No transactions
            transactionList.innerHTML = '';
            noTransactions.style.display = 'block';
        }
    }, 'AccountView');
}

// Get authenticated user info and then load account
async function getUserInfoAndLoadAccount() {
    if (!authToken) {
        console.error('No auth token found');
        window.location.href = 'login.html';
        return;
    }
    
    try {
        // Set loading state
        accountProcessor.setLoading(true);
        
        const response = await fetch(`${API_BASE_URL}/auth/users/me`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`,
            }
        });
        
        if (!response.ok) {
            // Token might be expired or invalid
            if (response.status === 401) {
                localStorage.removeItem('bankAuthToken');
                window.location.href = 'login.html';
                return;
            }
            
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to get user information');
        }
        
        const userData = await response.json();
        console.log('User data received:', userData);
        
        // Update state with user data
        accountProcessor.setUser(userData);
        
        // Load the account details
        loadUserAccount();
    } catch (error) {
        console.error('Error getting user info:', error);
        accountProcessor.setError(error.message);
        // Handle error, potentially redirect to login
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 2000);
    }
}

// Load user account details
async function loadUserAccount() {
    if (!accountState.value.user || !authToken) {
        console.error('No authenticated user found');
        window.location.href = 'login.html';
        return;
    }
    
    try {
        console.log('Loading account for user:', accountState.value.user.username);
        
        // Set loading state
        accountProcessor.setLoading(true);
        
        // Show account section
        if (createUserSection) createUserSection.style.display = 'none';
        accountDetailsSection.style.display = 'block';
        // We already have user details from the initial load
        // Now we can skip directly to getting account details
        // Restore the account section HTML if it was replaced with loading indicator
        if (!document.getElementById('userName-display')) {
            // Reload the page to restore the HTML structure
            window.location.reload();
            return;
        }
        
        // User name will be updated by the reactive UI when state changes
        // Get account details with JWT authentication
        console.log('Fetching account details');
        const accountResponse = await fetch(`${API_BASE_URL}/users/me/account`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (!accountResponse.ok) {
            let errorMessage = 'Failed to load account details';
            try {
                const errorData = await accountResponse.json();
                errorMessage = errorData.detail || errorMessage;
            } catch (e) {
                console.error('Error parsing error response:', e);
                errorMessage = `Server error: ${accountResponse.status} ${accountResponse.statusText}`;
            }
            throw new Error(errorMessage);
        }
          let accountData;
        try {
            const responseText = await accountResponse.text();
            console.log('Account response:', responseText);
            try {
                accountData = JSON.parse(responseText);
            } catch (parseError) {
                console.error('JSON parse error:', parseError);
                throw new Error(`Failed to parse account data: ${responseText.substring(0, 100)}...`);
            }
        } catch (e) {
            console.error('Error processing account response:', e);
            throw new Error('Failed to process account data. See console for details.');
        }
        
        console.log('Account data received:', accountData);
        
        // Update account state in Molecule
        accountProcessor.setAccount(accountData);
          // Load transactions
        try {
            await loadTransactions(accountData.id);
        } catch (txError) {
            console.warn('Error loading transactions, but continuing:', txError);
            // Don't fail the whole account loading just because transactions failed
            document.getElementById('transaction-list').innerHTML = 
                `<tr><td colspan="3">Could not load transactions: ${txError.message}</td></tr>`;
        }
        
    } catch (error) {
        console.error('Error loading account:', error);
        
        // Update error state in Molecule
        accountProcessor.setError(error.message);
    }
}

// Load transaction history
async function loadTransactions(accountId) {
    try {
        const transactionsResponse = await fetch(`${API_BASE_URL}/accounts/${accountId}/transactions`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (!transactionsResponse.ok) {
            let errorMessage = 'Failed to load transactions';
            try {
                const errorData = await transactionsResponse.json();
                errorMessage = errorData.detail || errorMessage;
            } catch (e) {
                console.error('Error parsing error response:', e);
                errorMessage = `Server error: ${transactionsResponse.status} ${transactionsResponse.statusText}`;
            }
            throw new Error(errorMessage);
        }
        
        let transactions;
        try {
            transactions = await transactionsResponse.json();
        } catch (e) {
            console.error('Error parsing transactions response:', e);
            console.log('Response text:', await transactionsResponse.text());
            throw new Error('Failed to parse transaction data. See console for details.');
        }
        
        // Update transactions in Molecule state
        accountProcessor.setTransactions(transactions);
        
    } catch (error) {
        console.error('Error loading transactions:', error);
        throw error;
    }
}

// Make a deposit
async function makeDeposit() {
    if (!authToken || !accountState.value.account) return;
    
    const amount = parseFloat(depositAmountInput.value);
    
    if (isNaN(amount) || amount <= 0) {
        depositMessage.innerHTML = '<div class="error-message">Please enter a valid positive amount</div>';
        return;
    }
    
    try {
        depositMessage.innerHTML = '<div>Processing your deposit...</div>';
        
        const response = await fetch(`${API_BASE_URL}/accounts/${accountState.value.account.id}/deposit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                amount: amount,
                transfer_type: 'Standard',
                agree_terms: true
            }),
        });
        
        if (!response.ok) {
            let errorMessage = 'Failed to process deposit';
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorMessage;
            } catch (e) {
                console.error('Error parsing error response:', e);
                errorMessage = `Server error: ${response.status} ${response.statusText}`;
            }
            throw new Error(errorMessage);
        }
        
        let updatedAccount;
        try {
            updatedAccount = await response.json();
        } catch (e) {
            console.error('Error parsing deposit response:', e);
            console.log('Response text:', await response.text());
            throw new Error('Failed to parse deposit response. See console for details.');
        }
        
        // Update account state in Molecule
        accountProcessor.setAccount(updatedAccount);
        
        // Show success message
        depositMessage.innerHTML = '<div class="success-message">Deposit successful!</div>';
        
        // Reset deposit form
        depositAmountInput.value = '';
        
        // Reload transactions
        await loadTransactions(updatedAccount.id);
        
        // Hide deposit form after a delay
        setTimeout(() => {
            depositForm.style.display = 'none';
            depositMessage.textContent = '';
        }, 3000);
        
    } catch (error) {
        console.error('Error making deposit:', error);
        depositMessage.innerHTML = `<div class="error-message">${error.message}</div>`;
    }
}

// Log out
function logOut() {
    localStorage.removeItem('bankAuthToken');
    authToken = null;
    
    // Reset account state in Molecule
    accountProcessor.reset();
    
    // Clear any error messages
    depositMessage.innerHTML = '';
    
    // Redirect to login page
    window.location.href = 'login.html';
}
