import { useState } from 'react';
import UploadButton from '../components/upload-button.jsx';
import { useAccount } from '../context/AccountContext.jsx'; // to be created

export default function UploadPage() {
  const { selectedAccountId } = useAccount();
  const [statementId, setStatementId] = useState(null);

  const handleSuccess = (id) => {
    setStatementId(id);
    // maybe navigate to validation?
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Upload Statement</h1>
      {selectedAccountId ? (
        <UploadButton accountId={selectedAccountId} onUploadSuccess={handleSuccess} />
      ) : (
        <p>Please select an account first.</p>
      )}
      {statementId && <p>Upload complete. Statement ID: {statementId}</p>}
    </div>
  );
}
