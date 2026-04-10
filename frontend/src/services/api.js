const API_BASE = ''; // Same origin

function getAuthHeaders() {
  const token = localStorage.getItem('token');
  return token ? { 'Authorization': `Bearer ${token}` } : {};
}

export async function uploadStatement(file, account_id, onUploadProgress) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('account_id', account_id);
  const response = await fetch(`${API_BASE}/upload`, {
    method: 'POST',
    body: formData,
    headers: {
      ...getAuthHeaders(),
      // Content-Type will be set automatically by browser for FormData
    },
    // For progress, we'd need XHR; keep simple: no progress here
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || 'Upload failed');
  }
  return response.json();
}

export async function getDashboardStats(params) {
  const query = new URLSearchParams(params);
  const response = await fetch(`${API_BASE}/dashboard/stats?${query}`, {
    headers: getAuthHeaders()
  });
  if (!response.ok) throw new Error('Failed to fetch dashboard stats');
  return response.json();
}

export async function getAccounts(params = {}) {
  const query = new URLSearchParams(params);
  const response = await fetch(`${API_BASE}/accounts?${query}`, {
    headers: getAuthHeaders()
  });
  if (!response.ok) throw new Error('Failed to fetch accounts');
  return response.json();
}

export async function getTransactions(params = {}) {
  const query = new URLSearchParams(params);
  const response = await fetch(`${API_BASE}/transactions?${query}`, {
    headers: getAuthHeaders()
  });
  if (!response.ok) throw new Error('Failed to fetch transactions');
  return response.json();
}

export async function exportTransactionsCSV(params = {}) {
  const query = new URLSearchParams(params);
  const response = await fetch(`${API_BASE}/transactions/export/csv?${query}`, {
    headers: getAuthHeaders()
  });
  if (!response.ok) throw new Error('Failed to export CSV');
  const blob = await response.blob();
  return blob;
}

export async function getCategories() {
  const response = await fetch(`${API_BASE}/categories`, {
    headers: getAuthHeaders()
  });
  if (!response.ok) throw new Error('Failed to fetch categories');
  return response.json();
}

export async function createCategory(name, color) {
  const response = await fetch(`${API_BASE}/categories`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders()
    },
    body: JSON.stringify({ name, color })
  });
  if (!response.ok) throw new Error('Failed to create category');
  return response.json();
}

export async function updateCategory(category_id, name, color) {
  const response = await fetch(`${API_BASE}/categories/${category_id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders()
    },
    body: JSON.stringify({ name, color })
  });
  if (!response.ok) throw new Error('Failed to update category');
  return response.json();
}

export async function deleteCategory(category_id) {
  const response = await fetch(`${API_BASE}/categories/${category_id}`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  });
  if (!response.ok) throw new Error('Failed to delete category');
  return response.json();
}

export async function getPendingReviews() {
  const response = await fetch(`${API_BASE}/validation/pending-reviews`, {
    headers: getAuthHeaders()
  });
  if (!response.ok) throw new Error('Failed to fetch pending reviews');
  return response.json();
}

export async function validateReview(token, updates) {
  const response = await fetch(`${API_BASE}/validation/pending-reviews/${token}/validate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders()
    },
    body: JSON.stringify(updates)
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || 'Validation failed');
  }
  return response.json();
}
