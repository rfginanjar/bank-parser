import { createContext, useState, useContext } from 'react';

const AccountContext = createContext();

export function AccountProvider({ children }) {
  const [selectedAccountId, setSelectedAccountId] = useState(null);
  return (
    <AccountContext.Provider value={{ selectedAccountId, setSelectedAccountId }}>
      {children}
    </AccountContext.Provider>
  );
}

export function useAccount() {
  return useContext(AccountContext);
}
