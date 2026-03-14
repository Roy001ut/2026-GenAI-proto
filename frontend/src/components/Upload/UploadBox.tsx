import { useState } from 'react';
import api from '../../services/api';

export default function UploadBox() {
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>, type: string) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await api.post(`/documents/upload/${type}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setMessage(`✅ ${file.name} uploaded successfully`);
      setTimeout(() => setMessage(''), 3000);
    } catch (error: any) {
      setMessage(`❌ Error: ${error.response?.data?.detail || 'Upload failed'}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-blue-50 rounded-lg p-6 border-2 border-dashed border-blue-200">
      <h2 className="text-2xl font-bold text-blue-900 mb-4">Upload Documents</h2>

      {message && <div className="mb-4 p-3 bg-blue-100 text-blue-800 rounded">{message}</div>}

      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {[
          { type: 'prescription', label: '💊 Prescription' },
          { type: 'bill', label: '📋 Bill' },
          { type: 'lab_report', label: '📊 Lab Report' },
          { type: 'insurance_policy', label: '📄 Insurance' },
          { type: 'consultation', label: '🎙️ Consultation' },
        ].map((item) => (
          <label key={item.type} className="cursor-pointer">
            <input
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              onChange={(e) => handleFileUpload(e, item.type)}
              disabled={uploading}
              className="hidden"
            />
            <div className="p-4 bg-white border border-blue-300 rounded hover:bg-blue-100 transition text-center">
              <div className="text-2xl mb-1">{item.label.split(' ')[0]}</div>
              <div className="text-xs font-semibold">{item.label.split(' ')[1]}</div>
            </div>
          </label>
        ))}
      </div>
    </div>
  );
}
