import { useState } from 'react';
import { exportTransactionsCSV } from '../services/api.js';

export default function ExportCSVButton({ filters = {}, disabled }) {
  const [loading, setLoading] = useState(false);

  const handleExport = async () => {
    setLoading(true);
    try {
      const blob = await exportTransactionsCSV(filters);
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'transactions.csv';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert('Export failed: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleExport} disabled={disabled || loading}>
      {loading ? 'Exporting...' : 'Export CSV'}
    </button>
  );
}
  };

  // For now, this is a placeholder.
  return (
    <button onClick={handleExport} disabled={disabled || loading}>
      {loading ? 'Exporting...' : 'Export CSV'}
    </button>
  );
}
