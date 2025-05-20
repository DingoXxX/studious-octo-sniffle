import React, { useEffect, useState } from 'react';
import { fetchAccounts } from './api';

export default function AccountsList() {
  const [accounts, setAccounts] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAccounts()
      .then(data => {
        setAccounts(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading accounts...</div>;
  if (error) return <div style={{color:'red'}}>Error: {error}</div>;
  if (!accounts.length) return <div>No accounts found.</div>;

  return (
    <div>
      <h2>Accounts</h2>
      <ul>
        {accounts.map(acc => (
          <li key={acc.id || acc.account_number}>
            {acc.name || acc.owner}: {acc.balance} {acc.currency || ''}
          </li>
        ))}
      </ul>
    </div>
  );
}
