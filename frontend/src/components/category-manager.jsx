import { useState, useEffect } from 'react';
import { getCategories, createCategory, updateCategory, deleteCategory } from '../services/api.js';

export default function CategoryManager() {
  const [categories, setCategories] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [editName, setEditName] = useState('');
  const [editColor, setEditColor] = useState('#000000');
  const [adding, setAdding] = useState(false);
  const [newName, setNewName] = useState('');
  const [newColor, setNewColor] = useState('#000000');
  const [error, setError] = useState(null);

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      const data = await getCategories();
      setCategories(data);
    } catch (err) {
      setError(err.message);
    }
  };

  const startEdit = (cat) => {
    setEditingId(cat.id);
    setEditName(cat.name);
    setEditColor(cat.color);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditName('');
    setEditColor('#000000');
  };

  const saveEdit = async () => {
    try {
      await updateCategory(editingId, editName, editColor);
      // optimistic update already reflected
      setEditingId(null);
      // reload to ensure consistency
      loadCategories();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id, is_default) => {
    if (is_default) {
      alert('Cannot delete default category');
      return;
    }
    if (!window.confirm('Delete this category?')) return;
    try {
      await deleteCategory(id);
      setCategories(categories.filter(c => c.id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  const handleAdd = async () => {
    if (!newName.trim()) return;
    try {
      const cat = await createCategory(newName, newColor);
      setCategories([...categories, cat]);
      setAdding(false);
      setNewName('');
      setNewColor('#000000');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ padding: '1rem' }}>
      <h2>Categories</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button onClick={() => setAdding(true)} disabled={adding}>Add New Category</button>
      {adding && (
        <div style={{ marginTop: '1rem', border: '1px solid #ccc', padding: '1rem' }}>
          <input placeholder="Name" value={newName} onChange={e => setNewName(e.target.value)} />
          <input type="color" value={newColor} onChange={e => setNewColor(e.target.value)} />
          <button onClick={handleAdd}>Save</button>
          <button onClick={() => setAdding(false)}>Cancel</button>
        </div>
      )}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {categories.map(cat => (
          <li key={cat.id} style={{ display: 'flex', alignItems: 'center', margin: '0.5rem 0' }}>
            <span style={{ display: 'inline-block', width: '16px', height: '16px', backgroundColor: cat.color, marginRight: '8px', border: '1px solid #000' }}></span>
            {editingId === cat.id ? (
              <>
                <input value={editName} onChange={e => setEditName(e.target.value)} />
                <input type="color" value={editColor} onChange={e => setEditColor(e.target.value)} />
                <button onClick={saveEdit}>Save</button>
                <button onClick={cancelEdit}>Cancel</button>
              </>
            ) : (
              <>
                <span style={{ marginRight: '8px' }}>{cat.name} {cat.is_default && '(default)'}</span>
                {!cat.is_default && (
                  <>
                    <button onClick={() => startEdit(cat)}>Edit</button>
                    <button onClick={() => handleDelete(cat.id, cat.is_default)}>Delete</button>
                  </>
                )}
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
