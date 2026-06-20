import { useState, useEffect } from 'react';
import axios from 'axios';
import Header from './components/Header';
import Footer from './components/Footer';

function App() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/events')
      .then(response => {
        setEvents(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Greška pri dohvaćanju događaja:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <Header />
      <main className="flex-grow container mx-auto p-4 mt-6">
        <h2 className="text-2xl font-bold mb-6 text-slate-800">Agregirani događaji</h2>
        
        {loading ? (
          <p>Učitavanje...</p>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {events.map((event) => (
              <div key={event.id} className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
                <h3 className="font-semibold text-lg mb-2">{event.title}</h3>
                <p className="text-sm text-blue-600 mb-2">{event.category}</p>
                <div className="text-xs text-slate-400 font-mono bg-slate-100 p-2 rounded truncate">
                  ID: {event.id}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}

export default App;