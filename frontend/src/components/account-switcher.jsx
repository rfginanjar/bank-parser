import { useState, useEffect, useRef } from 'react';

export default function AccountSwitcher({ accounts, selectedAccountId, onSelect }) {
  const [open, setOpen] = useState(false);
  const [filter, setFilter] = useState('');
  const containerRef = useRef(null);

  const filtered = accounts.filter(acc =>
    (acc.bank_name + ' ' + acc.account_name + ' ' + acc.account_number).toLowerCase().includes(filter.toLowerCase())
  );

  const selected = accounts.find(a => a.id === selectedAccountId);

  // Close on outside click or escape
  useEffect(() => {
    function handleClick(e) {
      if (containerRef.current && !containerRef.current.contains(e.target)) setOpen(false);
    }
    function handleKey(e) {
      if (e.key === 'Escape') setOpen(false);
    }
    document.addEventListener('mousedown', handleClick);
    document.addEventListener('keydown', handleKey);
    return () => {
      document.removeEventListener('mousedown', handleClick);
      document.removeEventListener('keydown', handleKey);
    };
  }, []);

  return (
    <div ref={containerRef} style={{ position: 'relative', marginBottom: '1rem' }}>
      <button onClick={() => setOpen(!open)} aria-haspopup="listbox" aria-expanded={open}>
        {selected ? `${selected.bank_name} (${selected.account_number})` : 'Select Account'} ▼
      </button>
      {open && (
        <div role="listbox" style={{ position: 'absolute', top: '100%', left: 0, background: 'white', border: '1px solid #ccc', zIndex: 1000, width: '300px', maxHeight: '300px', overflowY: 'auto' }}>
          <input
            type="text"
            placeholder="Search..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            autoFocus
            style={{ width: '100%', boxSizing: 'border-box', padding: '4px' }}
          />
          {filtered.map(acc => (
            <div
              key={acc.id}
              role="option"
              aria-selected={acc.id === selectedAccountId}
              onClick={() => {
                onSelect(acc.id);
                setOpen(false);
                setFilter('');
              }}
              style={{ padding: '8px', cursor: 'pointer', background: acc.id === selectedAccountId ? '#e0e0e0' : 'white' }}
            >
              {acc.bank_name} - {acc.account_name} ({acc.account_number})
            </div>
          ))}
          {filtered.length === 0 && <div style={{ padding: '8px', color: '#666' }}>No accounts</div>}
        </div>
      )}
    </div>
  );
}
