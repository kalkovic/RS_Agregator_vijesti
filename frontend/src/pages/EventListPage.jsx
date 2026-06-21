import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { newsApi } from '../api'; 

function EventListPage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');

  useEffect(() => {
    newsApi.get('/api/events')
      .then(response => {
        const data = Array.isArray(response.data) ? response.data : response.data.events || [];
        setEvents(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Greška pri dohvaćanju događaja:", error);
        setLoading(false);
      });
  }, []);

  const filteredEvents = events.filter(event => {
    const matchesSearch = event.title?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === '' || event.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const categories = [...new Set(events.map(e => e.category).filter(Boolean))];

  return (
    <div>
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-4">
        <h2 className="text-2xl font-bold text-slate-800">Agregirani događaji</h2>
        
        <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
          <input
            type="text"
            placeholder="Pretraži vijesti..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-full sm:w-64 bg-white text-slate-800"
          />
          
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-slate-800"
          >
            <option value="">Sve kategorije</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full mb-2"></div>
          <p className="text-slate-500 font-medium">Učitavanje vijesti...</p>
        </div>
      ) : filteredEvents.length === 0 ? (
        <p className="text-center text-slate-500 py-12">Nema pronađenih događaja za odabrane kriterije.</p>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredEvents.map((event) => (
            <div key={event.id} className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow flex flex-col justify-between">
              <div>
                <span className="text-xs font-semibold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full">
                  {event.category || 'Vijesti'}
                </span>
                <h3 className="font-bold text-lg text-slate-800 mt-3 mb-2 line-clamp-2">
                  {event.title}
                </h3>
              </div>
              
              <div className="mt-4">
                <div className="text-xs text-slate-400 font-mono bg-slate-50 p-2 rounded truncate mb-3">
                  ID: {event.id}
                </div>
                <Link 
                  to={`/event/${event.id}`} 
                  className="block text-center w-full bg-slate-100 hover:bg-blue-600 hover:text-white text-slate-700 font-medium py-2 rounded-lg transition-colors text-sm"
                >
                  Pogledaj detalje & Verifikaciju
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default EventListPage;