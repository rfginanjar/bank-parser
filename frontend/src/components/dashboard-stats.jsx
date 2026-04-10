export default function DashboardStats({ stats }) {
  const { credit_total, debit_total, net_change, transaction_count } = stats;
  const fmt = (val) => val.toLocaleString('en-US', { style: 'currency', currency: 'USD' });

  return (
    <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
      <div style={{ border: '1px solid #ddd', padding: '1rem', borderRadius: '4px', flex: 1 }}>
        <h3>Income</h3>
        <p style={{ fontSize: '1.5rem', color: 'green' }}>{fmt(credit_total)}</p>
        <small>{transaction_count} transactions</small>
      </div>
      <div style={{ border: '1px solid #ddd', padding: '1rem', borderRadius: '4px', flex: 1 }}>
        <h3>Expenses</h3>
        <p style={{ fontSize: '1.5rem', color: 'red' }}>{fmt(debit_total)}</p>
      </div>
      <div style={{ border: '1px solid #ddd', padding: '1rem', borderRadius: '4px', flex: 1 }}>
        <h3>Net Change</h3>
        <p style={{ fontSize: '1.5rem', color: net_change >= 0 ? 'green' : 'red' }}>{fmt(net_change)}</p>
      </div>
    </div>
  );
}
