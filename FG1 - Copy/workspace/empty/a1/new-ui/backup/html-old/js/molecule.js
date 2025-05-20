/**
 * Molecule Integration for Banking App
 * Based on CashApp's Molecule library principles
 * 
 * This is a custom implementation inspired by the cashapp/molecule library
 * that brings reactive state management to our vanilla JS application.
 */

// State container - inspired by Molecule's StateFlow pattern
class StateFlow {
  constructor(initialValue) {
    this._value = initialValue;
    this._subscribers = new Set();
  }

  get value() {
    return this._value;
  }
  set value(newValue) {
    if (JSON.stringify(this._value) !== JSON.stringify(newValue)) {
      console.debug('[Molecule Debug] State changed:', {
        previous: this._value,
        new: newValue,
        changes: this._findChanges(this._value, newValue)
      });
      this._value = newValue;
      this._notifySubscribers();
    }
  }
  
  _findChanges(oldValue, newValue) {
    const changes = {};
    if (!oldValue || !newValue) return { oldValue, newValue };
    
    // Find changed keys
    Object.keys({ ...oldValue, ...newValue }).forEach(key => {
      if (JSON.stringify(oldValue[key]) !== JSON.stringify(newValue[key])) {
        changes[key] = {
          from: oldValue[key],
          to: newValue[key]
        };
      }
    });
    
    return changes;
  }

  subscribe(callback) {
    this._subscribers.add(callback);
    // Initial update with current value
    callback(this._value);
    
    // Return unsubscribe function
    return () => {
      this._subscribers.delete(callback);
    };
  }

  _notifySubscribers() {
    this._subscribers.forEach(callback => callback(this._value));
  }
}

/**
 * Creates a reactive presenter that manages state and emits updates
 * Similar to Molecule's launchMolecule function
 */
function launchMolecule(initialState, stateProcessor) {
  const stateFlow = new StateFlow(initialState);
  
  // Setup processing logic
  const processor = stateProcessor(stateFlow);
  
  // Return the state flow and processor controls
  return {
    stateFlow,
    processor
  };
}

/**
 * Connect a StateFlow to DOM updates
 * Abstracts the rendering logic from the state management
 */
function connectView(stateFlow, renderFunction, debugName = 'unnamed') {
  console.debug(`[Molecule Debug] Connecting view: ${debugName}`);
  return stateFlow.subscribe(state => {
    console.debug(`[Molecule Debug] Rendering view: ${debugName}`, state);
    try {
      renderFunction(state);
    } catch(error) {
      console.error(`[Molecule Error] Error rendering view ${debugName}:`, error);
    }
  });
}

// Banking app specific presenters
const AccountPresenter = {
  // Create account state management
  create: function() {
    // Initial state
    const initialState = {
      user: null,
      account: null,
      transactions: [],
      isLoading: false,
      error: null
    };
    
    // Create the molecule
    return launchMolecule(initialState, (stateFlow) => {
      return {
        // Set loading state
        setLoading(isLoading) {
          stateFlow.value = {
            ...stateFlow.value,
            isLoading
          };
        },
        
        // Set error state
        setError(error) {
          stateFlow.value = {
            ...stateFlow.value,
            error,
            isLoading: false
          };
        },
        
        // Update user data
        setUser(userData) {
          stateFlow.value = {
            ...stateFlow.value,
            user: userData,
            error: null
          };
        },
        
        // Update account data
        setAccount(accountData) {
          stateFlow.value = {
            ...stateFlow.value,
            account: accountData,
            isLoading: false,
            error: null
          };
        },
        
        // Update transactions
        setTransactions(transactionData) {
          stateFlow.value = {
            ...stateFlow.value,
            transactions: transactionData,
            isLoading: false,
            error: null
          };
        },
        
        // Load full state (user + account + transactions)
        loadFullState(userData, accountData, transactionData) {
          stateFlow.value = {
            user: userData,
            account: accountData,
            transactions: transactionData,
            isLoading: false,
            error: null
          };
        },
        
        // Reset state
        reset() {
          stateFlow.value = initialState;
        }
      };
    });
  }
};

const AuthPresenter = {
  // Create authentication state management
  create: function() {
    // Initial state
    const initialState = {
      isAuthenticated: false,
      authToken: null,
      tempToken: null,
      twoFARequired: false,
      twoFASecret: null,
      user: null,
      isLoading: false,
      error: null,
      currentView: 'login' // 'login', 'register', 'twofa-setup', 'twofa-verify'
    };
    
    // Create the molecule
    return launchMolecule(initialState, (stateFlow) => {
      return {
        // Set loading state
        setLoading(isLoading) {
          stateFlow.value = {
            ...stateFlow.value,
            isLoading
          };
        },
        
        // Set error state
        setError(error) {
          stateFlow.value = {
            ...stateFlow.value,
            error,
            isLoading: false
          };
        },
        
        // Set authentication state
        setAuthenticated(token, userData = null) {
          stateFlow.value = {
            ...stateFlow.value,
            isAuthenticated: true,
            authToken: token,
            user: userData,
            isLoading: false,
            error: null
          };
        },
        
        // Set 2FA required state
        set2FARequired(tempToken, secret) {
          stateFlow.value = {
            ...stateFlow.value,
            twoFARequired: true,
            tempToken: tempToken,
            twoFASecret: secret,
            currentView: 'twofa-setup',
            isLoading: false,
            error: null
          };
        },
        
        // Set current view
        setView(viewName) {
          stateFlow.value = {
            ...stateFlow.value,
            currentView: viewName,
            error: null
          };
        },
        
        // Logout
        logout() {
          stateFlow.value = {
            ...initialState,
            currentView: 'login'
          };
        }
      };
    });
  }
};

// Export the modules for use in other files
window.Molecule = {
  StateFlow,
  launchMolecule,
  connectView,
  AccountPresenter,
  AuthPresenter
};
