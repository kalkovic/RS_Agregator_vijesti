import { useState } from 'react';

function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Ovo je demo simulacija za: ${isLogin ? 'Prijava' : 'Registracija'} sa emailom: ${email}`);
  };

  return (
    <div className="max-w-md mx-auto mt-12">
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-200">
        <h2 className="text-2xl font-black text-center text-slate-800 mb-2">
          {isLogin ? 'Dobrodošli natrag' : 'Kreirajte račun'}
        </h2>
        <p className="text-slate-400 text-center text-sm mb-6">
          {isLogin ? 'Prijavite se za pristup administratorskim rutama' : 'Registrirajte novi administratorski profil'}
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <div>
              <label className="block text-xs font-bold uppercase text-slate-500 mb-1">Ime i prezime</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white text-slate-800 text-sm"
                placeholder="Ivan Horvat"
                required
              />
            </div>
          )}

          <div>
            <label className="block text-xs font-bold uppercase text-slate-500 mb-1">Email adresa</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white text-slate-800 text-sm"
              placeholder="admin@agregator.hr"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase text-slate-500 mb-1">Lozinka</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white text-slate-800 text-sm"
              placeholder="••••••••"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 rounded-lg transition-colors text-sm mt-2"
          >
            {isLogin ? 'Prijavi se' : 'Registriraj se'}
          </button>
        </form>

        <hr className="border-slate-100 my-6" />

        <div className="text-center text-sm">
          <span className="text-slate-500">
            {isLogin ? 'Nemate račun?' : 'Već imate račun?'}
          </span>{' '}
          <button
            onClick={() => setIsLogin(!isLogin)}
            className="text-indigo-600 hover:underline font-bold"
          >
            {isLogin ? 'Registriraj se' : 'Prijavi se'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default AuthPage;