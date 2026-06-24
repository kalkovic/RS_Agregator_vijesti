import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { newsApi } from '../api';

function EventDetailPage() {
  const { id } = useParams(); 
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

 useEffect(() => {
    newsApi.get(`/api/events/${id}`)
      .then(response => {
        setEvent(response.data);
        setLoading(false);
                if (!response.data.blockchain_tx_hash) {
          newsApi.get(`/api/events/${id}/verify`)
            .then(verifyRes => {
              if (verifyRes.data.is_valid) {
                setEvent(prev => ({
                  ...prev,
                  blockchain_tx_hash: verifyRes.data.blockchain_hash 
                }));
              }
            })
            .catch(err => console.log("Blockchain verifikacija još nije spremna."));
        }
      })
      .catch(err => {
        console.error("Greška pri dohvaćanju detalja događaja:", err);
        setError("Nije moguće učitati detalje događaja.");
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin inline-block w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full mb-2"></div>
        <p className="text-slate-500 font-medium">Učitavanje detalja i provjera blockchaina...</p>
      </div>
    );
  }

  if (error || !event) {
    return (
      <div className="text-center py-12 max-w-md mx-auto">
        <div className="bg-red-50 text-red-800 p-4 rounded-xl border border-red-200 mb-4">
          {error || "Događaj nije pronađen."}
        </div>
        <Link to="/" className="text-indigo-600 hover:underline font-medium">← Povratak na naslovnicu</Link>
      </div>
    );
  }

  const isVerified = event.blockchain_tx_hash !== null && event.blockchain_tx_hash !== undefined;

  console.log("Stanje eventa:", event);
  console.log("Je li verificirano:", isVerified);

  return (
    <div className="max-w-4xl mx-auto">
      <Link to="/" className="inline-flex items-center text-sm font-medium text-slate-500 hover:text-indigo-600 mb-6 transition-colors">
        ← Natrag na sve vijesti
      </Link>

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 md:p-8 mb-8">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
          <span className="text-xs font-semibold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full">
            {event.category || 'Vijesti'}
          </span>
          
          {isVerified ? (
            <div className="inline-flex items-center space-x-1.5 bg-emerald-50 text-emerald-700 border border-emerald-200 px-3 py-1 rounded-full text-xs font-bold shadow-sm">
              <span className="flex h-2 w-2 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span>Verificirano na Blockchainu</span>
            </div>
          ) : (
            <div className="inline-flex items-center bg-amber-50 text-amber-700 border border-amber-200 px-3 py-1 rounded-full text-xs font-bold">
              ⚠️ Čeka se blockchain verifikacija
            </div>
          )}
        </div>

        <h1 className="text-2xl md:text-3xl font-black text-slate-900 mb-4 leading-snug">
          {event.title}
        </h1>

        {isVerified && (
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 mb-6 font-mono text-xs text-slate-600">
            <div className="font-bold text-slate-500 uppercase tracking-wider text-[10px] mb-1">Blockchain Tx Hash</div>
            <div className="break-all text-emerald-700 font-semibold">{event.blockchain_tx_hash}</div>
          </div>
        )}

        <hr className="border-slate-100 my-6" />

        <h2 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
          <span>📊</span> Analiza izvora i povezani članci ({event.articles?.length || 0})
        </h2>

        <div className="space-y-4">
          {event.articles && event.articles.length > 0 ? (
            event.articles.map((article, index) => (
              <div key={index} className="bg-slate-50 rounded-xl p-4 border border-slate-100 hover:border-slate-200 transition-colors flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-xs font-bold text-slate-700 bg-slate-200 px-2 py-0.5 rounded">
                      {article.source}
                    </span>
                    <span className="text-xs text-slate-400">
                      {article.published_at ? new Date(article.published_at).toLocaleString('hr-HR') : 'Nepoznat datum'}
                    </span>
                  </div>
                  <h4 className="text-sm font-semibold text-slate-800 line-clamp-2">
                    {article.title}
                  </h4>
                </div>
                
                <a 
                  href={article.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="inline-flex items-center justify-center bg-white text-slate-700 border border-slate-200 hover:bg-indigo-600 hover:text-white font-medium px-4 py-2 rounded-lg text-xs transition-all shadow-sm"
                >
                  Otvori izvornu vijest ↗
                </a>
              </div>
            ))
          ) : (
            <p className="text-sm text-slate-500 italic">Ovaj događaj nema dodatnih analiziranih izvora.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default EventDetailPage;