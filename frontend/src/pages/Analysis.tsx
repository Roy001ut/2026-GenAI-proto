import { useState } from 'react';
import api from '../services/api';

type Tab = 'drug' | 'bill' | 'insurance';

export default function Analysis() {
  const [tab, setTab] = useState<Tab>('drug');

  // Drug
  const [drugName, setDrugName] = useState('');
  const [dosage, setDosage] = useState('');
  const [drugResult, setDrugResult] = useState<any>(null);
  const [drugLoading, setDrugLoading] = useState(false);
  const [drugError, setDrugError] = useState('');

  // Bill / Insurance
  const [docId, setDocId] = useState('');
  const [diagnosis, setDiagnosis] = useState('');
  const [otherResult, setOtherResult] = useState<any>(null);
  const [otherLoading, setOtherLoading] = useState(false);
  const [otherError, setOtherError] = useState('');

  async function analyzeDrug() {
    setDrugLoading(true); setDrugError(''); setDrugResult(null);
    try {
      const { data } = await api.post('/analysis/drug', { drug_name: drugName, dosage });
      setDrugResult(data);
    } catch (e: any) {
      setDrugError(e.response?.data?.detail || 'Analysis failed');
    } finally {
      setDrugLoading(false);
    }
  }

  async function analyzeOther() {
    if (!docId.trim()) { setOtherError('Enter a document ID'); return; }
    setOtherLoading(true); setOtherError(''); setOtherResult(null);
    const endpoint = tab === 'bill' ? '/analysis/bill' : '/analysis/insurance';
    const payload = tab === 'bill'
      ? { document_id: docId, patient_diagnosis: diagnosis }
      : { document_id: docId };
    try {
      const { data } = await api.post(endpoint, payload);
      setOtherResult(data);
    } catch (e: any) {
      setOtherError(e.response?.data?.detail || 'Analysis failed');
    } finally {
      setOtherLoading(false);
    }
  }

  const tabs: Tab[] = ['drug', 'bill', 'insurance'];

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Analysis</h2>

      <div className="flex gap-2 mb-6">
        {tabs.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              tab === t ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        {tab === 'drug' ? (
          <>
            <h3 className="font-semibold text-gray-700 mb-4">Drug Analysis</h3>
            <div className="space-y-3 mb-4">
              <input
                value={drugName} onChange={(e) => setDrugName(e.target.value)}
                placeholder="Drug name (e.g. Metformin)"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              />
              <input
                value={dosage} onChange={(e) => setDosage(e.target.value)}
                placeholder="Dosage (e.g. 500mg twice daily)"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              />
            </div>
            {drugError && <p className="text-red-600 text-sm mb-2">{drugError}</p>}
            <button
              onClick={analyzeDrug} disabled={drugLoading || !drugName}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
            >
              {drugLoading ? 'Analyzing…' : 'Analyze Drug'}
            </button>
            {drugResult && (
              <pre className="mt-4 bg-gray-50 rounded-lg p-4 text-xs overflow-auto max-h-96">
                {JSON.stringify(drugResult, null, 2)}
              </pre>
            )}
          </>
        ) : (
          <>
            <h3 className="font-semibold text-gray-700 mb-4">
              {tab === 'bill' ? 'Bill Analysis' : 'Insurance Analysis'}
            </h3>
            <div className="space-y-3 mb-4">
              <input
                value={docId} onChange={(e) => setDocId(e.target.value)}
                placeholder="Document ID (from Documents page)"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              />
              {tab === 'bill' && (
                <input
                  value={diagnosis} onChange={(e) => setDiagnosis(e.target.value)}
                  placeholder="Patient diagnosis (optional)"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                />
              )}
            </div>
            {otherError && <p className="text-red-600 text-sm mb-2">{otherError}</p>}
            <button
              onClick={analyzeOther} disabled={otherLoading}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
            >
              {otherLoading ? 'Analyzing…' : 'Analyze'}
            </button>
            {otherResult && (
              <pre className="mt-4 bg-gray-50 rounded-lg p-4 text-xs overflow-auto max-h-96">
                {JSON.stringify(otherResult, null, 2)}
              </pre>
            )}
          </>
        )}
      </div>
    </div>
  );
}
