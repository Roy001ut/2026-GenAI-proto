import { useAuthStore } from '../store/auth';

type Page = 'home' | 'documents' | 'analysis' | 'health' | 'consultations';

interface Props {
  current: Page;
  onChange: (page: Page) => void;
}

const navItems: { id: Page; label: string; icon: string }[] = [
  { id: 'home',          label: 'Dashboard',     icon: '🏠' },
  { id: 'documents',     label: 'Documents',     icon: '📄' },
  { id: 'analysis',      label: 'Analysis',      icon: '🔬' },
  { id: 'health',        label: 'Health Wallet', icon: '💊' },
  { id: 'consultations', label: 'Consultations', icon: '👨‍⚕️' },
];

export default function Navigation({ current, onChange }: Props) {
  const { user, logout } = useAuthStore();

  return (
    <aside className="w-56 bg-indigo-700 text-white flex flex-col min-h-screen">
      <div className="px-5 py-6 border-b border-indigo-600">
        <h1 className="text-xl font-bold">MedAudit</h1>
        <p className="text-indigo-300 text-xs mt-1 truncate">{user?.email}</p>
      </div>

      <nav className="flex-1 py-4 space-y-1 px-2">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onChange(item.id)}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
              current === item.id
                ? 'bg-indigo-800 text-white'
                : 'text-indigo-200 hover:bg-indigo-600 hover:text-white'
            }`}
          >
            <span>{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>

      <div className="px-4 py-4 border-t border-indigo-600">
        <p className="text-indigo-300 text-xs mb-2 truncate">{user?.full_name}</p>
        <button
          onClick={logout}
          className="w-full text-left text-sm text-indigo-300 hover:text-white transition-colors"
        >
          Sign out →
        </button>
      </div>
    </aside>
  );
}
