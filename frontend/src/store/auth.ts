import { create } from 'zustand';

interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
}

interface AuthState {
  token: string | null;
  user: User | null;
  setAuth: (token: string, user: User) => void;
  setUser: (user: User) => void;
  logout: () => void;
}

console.log('[auth store] module loaded — localStorage token:', localStorage.getItem('token'));

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('token'),
  user: null,
  setAuth: (token, user) => {
    console.log('[auth store] setAuth called — token:', token, '| user:', user);
    localStorage.setItem('token', token);
    set({ token, user });
    console.log('[auth store] setAuth complete — state updated');
  },
  setUser: (user) => {
    console.log('[auth store] setUser called — user:', user);
    set({ user });
  },
  logout: () => {
    console.log('[auth store] logout called — wiping token & user');
    localStorage.removeItem('token');
    set({ token: null, user: null });
  },
}));
