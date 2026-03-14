import { useState } from 'react';
import { useAuthStore } from '../../store/auth.store';
import UploadBox from '../Upload/UploadBox';
import PrescriptionsTab from '../Tabs/PrescriptionsTab';
import BillsTab from '../Tabs/BillsTab';
import HealthWalletTab from '../Tabs/HealthWalletTab';
import InsuranceTab from '../Tabs/InsuranceTab';
import SummaryTab from '../Tabs/SummaryTab';

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('summary');
  const { user, logout } = useAuthStore();

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-blue-600">MedAudit</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">Welcome, {user?.full_name}</span>
            <button
              onClick={logout}
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <UploadBox />

        <div className="mt-8 bg-white rounded-lg shadow">
          <div className="flex border-b overflow-x-auto">
            {[
              { id: 'summary', label: 'Summary' },
              { id: 'prescriptions', label: 'Prescriptions' },
              { id: 'bills', label: 'Bills' },
              { id: 'health-wallet', label: 'Health Wallet' },
              { id: 'insurance', label: 'Insurance' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-3 font-medium whitespace-nowrap ${
                  activeTab === tab.id
                    ? 'border-b-2 border-blue-600 text-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <div className="p-6">
            {activeTab === 'summary' && <SummaryTab />}
            {activeTab === 'prescriptions' && <PrescriptionsTab />}
            {activeTab === 'bills' && <BillsTab />}
            {activeTab === 'health-wallet' && <HealthWalletTab />}
            {activeTab === 'insurance' && <InsuranceTab />}
          </div>
        </div>
      </main>
    </div>
  );
}
