import { useState } from 'react';
import Navigation from '../components/Navigation';
import Documents from './Documents';
import Analysis from './Analysis';
import HealthWallet from './HealthWallet';
import Consultations from './Consultations';
import { useAuthStore } from '../store/auth';

type Page = 'home' | 'documents' | 'analysis' | 'health' | 'consultations';

function Home() {
  const { user } = useAuthStore();
  const cards = [
    { icon: '📄', title: 'Documents', desc: 'Upload and manage medical documents' },
    { icon: '🔬', title: 'Analysis',  desc: 'AI-powered drug, bill & insurance analysis' },
    { icon: '💊', title: 'Health Wallet', desc: 'Track lab results over time' },
    { icon: '👨‍⚕️', title: 'Consultations', desc: 'Record doctor visit notes' },
  ];
  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-1">
        Welcome back, {user?.full_name?.split(' ')[0]} 👋
      </h2>
      <p className="text-gray-500 mb-8">Here's what you can do with MedAudit.</p>
      <div className="grid grid-cols-2 gap-4">
        {cards.map((c) => (
          <div key={c.title} className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm hover:shadow-md transition-shadow">
            <div className="text-3xl mb-3">{c.icon}</div>
            <h3 className="font-semibold text-gray-700">{c.title}</h3>
            <p className="text-sm text-gray-400 mt-1">{c.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [page, setPage] = useState<Page>('home');

  const content: Record<Page, JSX.Element> = {
    home: <Home />,
    documents: <Documents />,
    analysis: <Analysis />,
    health: <HealthWallet />,
    consultations: <Consultations />,
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Navigation current={page} onChange={setPage} />
      <main className="flex-1 overflow-y-auto">{content[page]}</main>
    </div>
  );
}
