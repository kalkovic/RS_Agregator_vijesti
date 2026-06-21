import { useState, useEffect } from 'react';
import { analyticsApi } from '../api';

function AnalyticsDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    analyticsApi.get('/api/analytics/metrics')
      .then(response => {
        setMetrics(response.data.metrics);
        setLoading(false);
      })
      .catch(error => {
        console.error("Greška pri dohvaćanju analitike:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin inline-block w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full mb-2"></div>
        <p className="text-slate-500 font-medium">Učitavanje analitičkih podataka...</p>
      </div>
    );
  }

  if (!metrics) {
    return (
      <div className="bg-red-50 text-red-800 p-4 rounded-xl text-center border border-red-100 max-w-md mx-auto">
        Nije moguće učitati analitiku. Provjerite radi li analytics-service na portu 8092.
      </div>
    );
  }

  const getMaxValues = (obj) => Math.max(...Object.values(obj || { a: 1 }));
  const maxCategoryValue = getMaxValues(metrics.broj_vijesti_po_kategorijama);
  const maxSourceValue = getMaxValues(metrics.broj_clanaka_po_izvorima);

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-black text-slate-850">Analitički Dashboard</h2>
        <p className="text-slate-500 text-sm mt-1">Pregled agregiranih podataka i aktivnosti izvora u realnom vremenu.</p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <div className="text-sm font-bold text-slate-400 uppercase tracking-wider">Ukupno zapisa u bazi</div>
          <div className="text-4xl font-black text-slate-800 mt-2">{metrics.ukupno_zapisa_u_bazi}</div>
          <div className="text-xs text-indigo-500 font-medium mt-1">Raw entiteti iz scrape-era</div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <div className="text-sm font-bold text-slate-400 uppercase tracking-wider">Grupirani događaji</div>
          <div className="text-4xl font-black text-emerald-600 mt-2">{metrics.ukupno_grupiranih_dogadjaja}</div>
          <div className="text-xs text-emerald-500 font-medium mt-1">Konsolidirane jedinstvene vijesti</div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm sm:col-span-2 lg:col-span-1">
          <div className="text-sm font-bold text-slate-400 uppercase tracking-wider">Analizirani članci</div>
          <div className="text-4xl font-black text-blue-600 mt-2">{metrics.ukupno_analiziranih_clanaka}</div>
          <div className="text-xs text-blue-500 font-medium mt-1">Pojedinačni linkovi kroz izvore</div>
        </div>
      </div>

      <div className="grid gap-8 md:grid-cols-2">
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
            <span>🏷️</span> Distribucija po kategorijama
          </h3>
          <div className="space-y-3 max-h-[350px] overflow-y-auto pr-2">
            {Object.entries(metrics.broj_vijesti_po_kategorijama || {})
              .sort((a, b) => b[1] - a[1])
              .map(([cat, count]) => {
                const percentage = (count / maxCategoryValue) * 100;
                return (
                  <div key={cat} className="space-y-1">
                    <div className="flex justify-between text-xs font-semibold text-slate-600">
                      <span>{cat}</span>
                      <span className="text-slate-400">{count} vijesti</span>
                    </div>
                    <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                      <div className="bg-indigo-600 h-full rounded-full transition-all duration-500" style={{ width: `${percentage}%` }}></div>
                    </div>
                  </div>
                );
              })}
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
              <span>📰</span> Zastupljenost izvora informacija
            </h3>
            <div className="space-y-4">
              {Object.entries(metrics.broj_clanaka_po_izvorima || {}).map(([source, count]) => {
                const percentage = (count / maxSourceValue) * 100;
                return (
                  <div key={source} className="space-y-1.5">
                    <div className="flex justify-between text-sm font-bold text-slate-700">
                      <span className="font-mono text-xs uppercase tracking-wider bg-slate-100 px-2 py-0.5 rounded text-slate-600">{source}</span>
                      <span className="text-xs text-slate-500">{count} članaka</span>
                    </div>
                    <div className="w-full bg-slate-100 h-4 rounded-lg overflow-hidden">
                      <div className="bg-blue-500 h-full rounded-lg transition-all duration-500" style={{ width: `${percentage}%` }}></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
          
          <div className="bg-blue-50 border border-blue-100 text-blue-800 p-4 rounded-xl text-xs font-medium mt-6">
            💡 <strong>Zanimljivost:</strong> Index.hr trenutno drži najveći udio u prikupljenim podacima unutar baze.
          </div>
        </div>
      </div>
    </div>
  );
}

export default AnalyticsDashboard;