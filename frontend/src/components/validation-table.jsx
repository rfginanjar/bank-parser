import { useState, useEffect } from 'react';
import { getCategories, validateReview } from '../services/api.js';

export default function ValidationTable({ token, initialTransactions, onSuccess }) {
  const [transactions, setTransactions] = useState(initialTransactions);
  const [categories, setCategories] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    getCategories().then(setCategories).catch(console.error);
  }, []);

  const handleChange = (index, field, value) => {
    const newTx = [...transactions];
    newTx[index] = { ...newTx[index], [field]: value };
    setTransactions(newTx);
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setError(null);
    try {
      const payload = transactions.map((tx) => ({
        date: tx.date,
        description: tx.description,
        mutation_amount: tx.mutation_amount,
        balance: tx.balance,
        type: tx.type,
        category: tx.category
      }));
      await validateReview(token, payload);
      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <h2>Review Transactions</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <table border="1" cellPadding="4" style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>Date</th>
            <th>Description</th>
            <th>Amount</th>
            <th>Type</th>
            <th>Balance</th>
            <th>Category</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((tx, i) => (
            <tr key={i}>
              <td><input type="date" value={tx.date} onChange={(e) => handleChange(i, 'date', e.target.value)} /></td>
              <td><input type="text" value={tx.description} onChange={(e) => handleChange(i, 'description', e.target.value)} /></td>
              <td><input type="number" step="0.01" value={tx.mutation_amount} onChange={(e) => handleChange(i, 'mutation_amount', parseFloat(e.target.value))} /></td>
              <td>
                <select value={tx.type} onChange={(e) => handleChange(i, 'type', e.target.value)}>
                  <option value="Debit">Debit</option>
                  <option value="Credit">Credit</option>
                </select>
              </td>
              <td><input type="number" step="0.01" value={tx.balance} onChange={(e) => handleChange(i, 'balance', parseFloat(e.target.value))} /></td>
              <td>
                <select value={tx.category || ''} onChange={(e) => handleChange(i, 'category', e.target.value)}>
                  <option value="">Select</option>
                  {categories.map(cat => (
                    <option key={cat.id} value={cat.name}>{cat.name}</option>
                  ))}
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={handleSubmit} disabled={submitting}>Submit Validation</button>
    </div>
  );
}
