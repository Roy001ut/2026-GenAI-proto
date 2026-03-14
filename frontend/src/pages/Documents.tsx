import { useState, useEffect } from 'react';
import api from '../services/api';
import FileUpload from '../components/FileUpload';

interface Doc {
  id: string;
  document_type: string;
  original_filename: string;
}

const DOC_TYPES = ['prescription', 'bill', 'lab_report', 'consultation', 'insurance_policy'];

export default function Documents() {
  const [docs, setDocs] = useState<Doc[]>([]);
  const [docType, setDocType] = useState('prescription');
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => { fetchDocs(); }, []);

  async function fetchDocs() {
    const { data } = await api.get('/documents/');
    setDocs(data);
  }

  async function handleFile(file: File) {
    setUploading(true);
    setMessage('');
    try {
      const form = new FormData();
      form.append('file', file);
      await api.post(`/documents/upload/${docType}`, form);
      setMessage(`✓ "${file.name}" uploaded successfully`);
      fetchDocs();
    } catch (err: any) {
      setMessage(`✗ ${err.response?.data?.detail || 'Upload failed'}`);
    } finally {
      setUploading(false);
    }
  }

  async function handleDelete(id: string) {
    await api.delete(`/documents/${id}`);
    setDocs((prev) => prev.filter((d) => d.id !== id));
  }

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Documents</h2>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <h3 className="font-semibold text-gray-700 mb-4">Upload Document</h3>
        <div className="mb-4">
          <label className="block text-sm text-gray-600 mb-1">Document Type</label>
          <select
            value={docType}
            onChange={(e) => setDocType(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          >
            {DOC_TYPES.map((t) => <option key={t} value={t}>{t.replace('_', ' ')}</option>)}
          </select>
        </div>
        <FileUpload onFile={handleFile} accept=".pdf,.jpg,.jpeg,.png" label="Upload PDF or image" />
        {uploading && <p className="text-sm text-indigo-600 mt-2">Uploading…</p>}
        {message && (
          <p className={`text-sm mt-2 ${message.startsWith('✓') ? 'text-green-600' : 'text-red-600'}`}>
            {message}
          </p>
        )}
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="font-semibold text-gray-700 mb-4">My Documents ({docs.length})</h3>
        {docs.length === 0 ? (
          <p className="text-gray-400 text-sm">No documents yet. Upload one above.</p>
        ) : (
          <div className="space-y-2">
            {docs.map((doc) => (
              <div key={doc.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="text-sm font-medium text-gray-700">{doc.original_filename}</p>
                  <p className="text-xs text-gray-400">{doc.document_type.replace('_', ' ')}</p>
                </div>
                <button
                  onClick={() => handleDelete(doc.id)}
                  className="text-red-400 hover:text-red-600 text-xs"
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
