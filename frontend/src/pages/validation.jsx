import { useState, useEffect } from 'react';
import ValidationTable from '../components/validation-table.jsx';
import { getPendingReviews } from '../services/api.js';

export default function ValidationPage() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    async function load() {
      try {
        const data = await getPendingReviews();
        setReviews(data);
      } catch (err) {
        console.error(err);
      }
    }
    load();
  }, []);

  if (reviews.length === 0) return <div>No pending reviews.</div>;

  // For simplicity, use the first pending review. In real app, allow selection.
  const review = reviews[0];

  const handleSuccess = () => {
    // refresh or navigate
    window.location.reload();
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Validation</h1>
      <p>Account: {review.bank_name} - {review.account_name}</p>
      <ValidationTable
        token={review.token}
        initialTransactions={review.transactions}
        onSuccess={handleSuccess}
      />
    </div>
  );
}
