import { useState } from 'react';
import { uploadStatement } from '../services/api.js';

export default function UploadButton({ accountId, onUploadSuccess, onUploadError }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) setFile(selected);
  };

  const handleUpload = async () => {
    if (!file || !accountId) return;
    setUploading(true);
    setError(null);
    try {
      const result = await uploadStatement(file, accountId);
      setFile(null);
      if (onUploadSuccess) onUploadSuccess(result.statement_id);
    } catch (err) {
      setError(err.message);
      if (onUploadError) onUploadError(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h3>Upload Statement</h3>
      <input type="file" accept=".pdf,.jpg,.jpeg,.png,.tiff" onChange={handleFileChange} disabled={uploading} />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {file && (
        <div>
          <p>Selected: {file.name}</p>
          <button onClick={handleUpload} disabled={uploading || !accountId}>
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      )}
    </div>
  );
}
