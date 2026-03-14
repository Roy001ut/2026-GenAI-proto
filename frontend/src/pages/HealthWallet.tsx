import { useState, useEffect, FormEvent } from 'react';
import api from '../services/api';

interface Report {
  id: string;
  test_value: number;
  unit: string;
  status: string;
  test_date: string;
}

export default function HealthWallet() {
  const [reports, setReports] = useState<Record<string, Report[]>>({});
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({
    test_name: '', test_value: '', unit: '',
    normal_range_min: '', normal_range_max: '', test_date: '',
  });
  const [message, setMessage] = useState('');

  useEffect(() => { fetchReports(); }, []);

  async function fetchReports() {
    try {
      const { data } = await api.get('/health-wallet/all-reports');
      setReports(data);
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setMessage('');
    try {
      await api.post('/health-wallet/lab-reports', {
        ...form,
        test_value: parseFloat(form.test_value),
        normal_range_min: parseFloat(form.normal_range_min),
        normal_range_max: parseFloat(form.normal_range_max),
      });
      setMessage('✓ Lab report added');
      setForm({ test_name: '', test_value: '', unit: '', normal_range_min: '', normal_range_max: '', test_date: '' });
      fetchReports();
    } catch (e: any) {
      setMessage(`✗ ${e.response?.data?.detail || 'Failed to add report'}`);
    }
  }

  const statusColor = (s: string) =>
    s === 'high' ? 'text-red-600 bg-red-50' : s === 'low' ? 'text-yellow-600 bg-yellow-50' : 'text-green-600 bg-green-50';

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Health Wallet</h2>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <h3 className="font-semibold text-gray-700 mb-4">Add Lab Report</h3>
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-3">
          {[
            ['test_name', 'Test Name', 'text', 'col-span-2'],
            ['test_value', 'Value', 'number'],
            ['unit', 'Unit (e.g. mg/dL)', 'text'],
            ['normal_range_min', 'Normal Min', 'number'],
            ['normal_range_max', 'Normal Max', 'number'],
            ['test_date', 'Test Date', 'date', 'col-span-2'],
          ].map(([key, label, type, cls]) => (
            <div key={key} className={cls}>
              <label className="block text-xs text-gray-600 mb-1">{label}</label>
              <input
                type={type}
                required
                value={(form as any)[key]}
                onChange={(e) => setForm((f) => ({ ...f, [key]: e.target.value }))}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                step={type === 'number' ? 'any' : undefined}
              />
            </div>
          ))}
          {message && (
            <p className={`col-span-2 text-sm ${message.startsWith('✓') ? 'text-green-600' : 'text-red-600'}`}>
              {message}
            </p>
          )}
          <button
            type="submit"
            className="col-span-2 bg-indigo-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-indigo-700"
          >
            Add Report
          </button>
        </form>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="font-semibold text-gray-700 mb-4">My Lab Reports</h3>
        {loading ? (
          <p className="text-gray-400 text-sm">Loading…</p>
        ) : Object.keys(reports).length === 0 ? (
          <p className="text-gray-400 text-sm">No lab reports yet.</p>
        ) : (
          <div className="space-y-4">
            {Object.entries(reports).map(([name, entries]) => (
              <div key={name}>
                <h4 className="text-sm font-semibold text-gray-600 mb-2">{name}</h4>
                <div className="space-y-1">
                  {entries.map((r) => (
                    <div key={r.id} className="flex justify-between items-center p-2 bg-gray-50 rounded-lg text-sm">
                      <span className="text-gray-600">{r.test_date}</span>
                      <span className="font-medium">{r.test_value} {r.unit}</span>
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(r.status)}`}>
                        {r.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
