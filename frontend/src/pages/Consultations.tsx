import { useState, useEffect, FormEvent } from 'react';
import api from '../services/api';

interface Consultation {
  id: string;
  doctor_name: string;
  summary: string;
  diagnoses: string[];
  medications_prescribed: string[];
  consultation_date: string;
}

export default function Consultations() {
  const [consultations, setConsultations] = useState<Consultation[]>([]);
  const [doctorName, setDoctorName] = useState('');
  const [summary, setSummary] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => { fetchAll(); }, []);

  async function fetchAll() {
    const { data } = await api.get('/consultations/');
    setConsultations(data);
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setMessage('');
    try {
      await api.post('/consultations/', { doctor_name: doctorName, summary });
      setMessage('✓ Consultation saved');
      setDoctorName(''); setSummary('');
      fetchAll();
    } catch (e: any) {
      setMessage(`✗ ${e.response?.data?.detail || 'Failed to save'}`);
    }
  }

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Consultations</h2>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <h3 className="font-semibold text-gray-700 mb-4">New Consultation</h3>
        <form onSubmit={handleSubmit} className="space-y-3">
          <input
            value={doctorName} onChange={(e) => setDoctorName(e.target.value)}
            required placeholder="Doctor's name"
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          />
          <textarea
            value={summary} onChange={(e) => setSummary(e.target.value)}
            required placeholder="Consultation summary / notes"
            rows={4}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none resize-none"
          />
          {message && (
            <p className={`text-sm ${message.startsWith('✓') ? 'text-green-600' : 'text-red-600'}`}>{message}</p>
          )}
          <button
            type="submit"
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700"
          >
            Save Consultation
          </button>
        </form>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="font-semibold text-gray-700 mb-4">History ({consultations.length})</h3>
        {consultations.length === 0 ? (
          <p className="text-gray-400 text-sm">No consultations recorded yet.</p>
        ) : (
          <div className="space-y-3">
            {consultations.map((c) => (
              <div key={c.id} className="p-4 bg-gray-50 rounded-lg border border-gray-100">
                <div className="flex justify-between items-start mb-1">
                  <p className="font-medium text-gray-700 text-sm">{c.doctor_name}</p>
                  <p className="text-xs text-gray-400">{new Date(c.consultation_date).toLocaleDateString()}</p>
                </div>
                <p className="text-sm text-gray-600">{c.summary}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
