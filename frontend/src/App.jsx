import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/dashboard.jsx'
import UploadPage from './pages/upload.jsx'
import ValidationPage from './pages/validation.jsx'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/validation" element={<ValidationPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App