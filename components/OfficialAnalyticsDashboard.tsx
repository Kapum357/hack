
import React from 'react';
import { useNavigation } from '../App';

export const OfficialAnalyticsDashboard = () => {
  const { goBack } = useNavigation();

  return (
    <div className="bg-background-light dark:bg-background-dark font-display text-slate-900 dark:text-white antialiased h-screen flex flex-col overflow-hidden">
      <div className="h-12 w-full bg-background-light dark:bg-background-dark shrink-0"></div>
      <main className="flex-1 overflow-y-auto pb-24 px-5">
        <header className="flex justify-between items-center mb-6 pt-2">
          <div>
            <p className="text-sm text-slate-500 dark:text-slate-400 font-medium">Panel de Control • Soacha</p>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white mt-0.5">Hola, Dr. Andrés</h1>
          </div>
          <div className="relative">
            <div className="h-12 w-12 rounded-full overflow-hidden border-2 border-white dark:border-slate-700 shadow-subtle bg-primary/10">
              <img alt="Portrait of Dr. Andres" className="h-full w-full object-cover" src="https://picsum.photos/id/1005/100/100" />
            </div>
            <span className="absolute top-0 right-0 h-3 w-3 bg-red-500 rounded-full border-2 border-background-light dark:border-background-dark"></span>
          </div>
        </header>
        
        <section className="mb-8">
          <div className="flex space-x-4 overflow-x-auto hide-scrollbar pb-2 -mx-5 px-5 snap-x">
            <div className="snap-start shrink-0 w-40 bg-white dark:bg-surface-dark p-4 rounded-xl shadow-card border border-slate-100 dark:border-slate-700/50">
              <div className="flex items-center space-x-2 mb-3">
                <div className="p-1.5 bg-primary/10 rounded-lg"><span className="material-icons-round text-primary text-xl">people_alt</span></div>
                <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide">Cobertura</span>
              </div>
              <div className="text-3xl font-bold text-slate-900 dark:text-white">40.3%</div>
              <div className="mt-2 text-xs font-medium text-green-500 flex items-center"><span className="material-icons-round text-sm mr-0.5">arrow_upward</span><span>2.1% este mes</span></div>
            </div>
            <div className="snap-start shrink-0 w-40 bg-white dark:bg-surface-dark p-4 rounded-xl shadow-card border border-slate-100 dark:border-slate-700/50">
              <div className="flex items-center space-x-2 mb-3">
                <div className="p-1.5 bg-primary/10 rounded-lg"><span className="material-icons-round text-primary text-xl">shield</span></div>
                <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide">Protección</span>
              </div>
              <div className="text-3xl font-bold text-slate-900 dark:text-white">42%</div>
              <div className="mt-2 text-xs font-medium text-slate-500 dark:text-slate-400 flex items-center"><span className="material-icons-round text-sm mr-0.5">remove</span><span>Estable</span></div>
            </div>
            <div className="snap-start shrink-0 w-40 bg-white dark:bg-surface-dark p-4 rounded-xl shadow-card border border-slate-100 dark:border-slate-700/50">
              <div className="flex items-center space-x-2 mb-3">
                <div className="p-1.5 bg-primary/10 rounded-lg"><span className="material-icons-round text-primary text-xl">timer</span></div>
                <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide">Respuesta</span>
              </div>
              <div className="text-3xl font-bold text-slate-900 dark:text-white">+38%</div>
              <div className="mt-2 text-xs font-medium text-green-500 flex items-center"><span className="material-icons-round text-sm mr-0.5">trending_up</span><span>Mejora notable</span></div>
            </div>
          </div>
        </section>

        <section className="mb-6">
          <div className="bg-white dark:bg-surface-dark rounded-2xl p-5 shadow-card border border-slate-100 dark:border-slate-700/50">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h3 className="font-bold text-slate-900 dark:text-white text-lg">Tendencia de Alcance</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">Intervenciones activas (Últimos 6 meses)</p>
              </div>
              <button className="p-2 bg-background-light dark:bg-background-dark rounded-lg text-slate-500 hover:text-primary transition-colors"><span className="material-icons-round text-lg">filter_list</span></button>
            </div>
            <div className="relative h-48 w-full">
              <div className="absolute inset-0 flex flex-col justify-between text-xs text-slate-300 dark:text-slate-600">
                {[...new Array(5)].map((_, i) => <div key={i} className="border-b border-dashed border-slate-200 dark:border-slate-700 w-full h-0"></div>)}
              </div>
              <div className="absolute bottom-0 left-0 right-0 top-4 overflow-hidden">
                <div className="w-full h-full opacity-20 bg-gradient-to-t from-primary to-transparent" style={{clipPath: "polygon(0% 100%, 0% 70%, 20% 65%, 40% 40%, 60% 50%, 80% 20%, 100% 10%, 100% 100%)"}}></div>
                <svg width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="none" className="absolute inset-0">
                  <polyline points="0,70 20,65 40,40 60,50 80,20 100,10" fill="none" stroke="#F23545" strokeWidth="2" />
                </svg>
                <div className="absolute w-2.5 h-2.5 bg-white border-2 border-primary rounded-full top-[70%] left-[0%] transform -translate-x-1/2 -translate-y-1/2 shadow-sm z-10"></div>
                <div className="absolute w-2.5 h-2.5 bg-white border-2 border-primary rounded-full top-[65%] left-[20%] transform -translate-x-1/2 -translate-y-1/2 shadow-sm z-10"></div>
                <div className="absolute w-2.5 h-2.5 bg-white border-2 border-primary rounded-full top-[40%] left-[40%] transform -translate-x-1/2 -translate-y-1/2 shadow-sm z-10"></div>
                <div className="absolute w-2.5 h-2.5 bg-white border-2 border-primary rounded-full top-[50%] left-[60%] transform -translate-x-1/2 -translate-y-1/2 shadow-sm z-10"></div>
                <div className="absolute w-2.5 h-2.5 bg-white border-2 border-primary rounded-full top-[20%] left-[80%] transform -translate-x-1/2 -translate-y-1/2 shadow-sm z-10"></div>
                <div className="absolute top-[10%] left-[100%] transform -translate-x-full -translate-y-1/2 z-20">
                    <div className="bg-primary text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md mb-1 ml-[-10px]">1,240</div>
                    <div className="w-3 h-3 bg-primary rounded-full border-2 border-white shadow-md ml-auto mr-1"></div>
                </div>
              </div>
            </div>
            <div className="flex justify-between mt-2 text-xs text-slate-500 dark:text-slate-400 font-medium px-1">
              <span>ENE</span><span>FEB</span><span>MAR</span><span>ABR</span><span>MAY</span><span>JUN</span>
            </div>
          </div>
        </section>

        <section className="mb-24">
          <div className="bg-white dark:bg-surface-dark rounded-2xl p-5 shadow-card border border-slate-100 dark:border-slate-700/50">
            <h3 className="font-bold text-slate-900 dark:text-white text-lg mb-4">Tipos de Intervención</h3>
            <div className="flex items-center space-x-6">
              <div className="relative w-32 h-32 shrink-0">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                  <path className="text-slate-100 dark:text-slate-700" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3.8"></path>
                  <path className="text-primary" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeDasharray="45, 100" strokeWidth="3.8"></path>
                  <path className="text-red-500" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeDasharray="30, 100" strokeDashoffset="-45" strokeWidth="3.8"></path>
                  <path className="text-blue-300" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeDasharray="25, 100" strokeDashoffset="-75" strokeWidth="3.8"></path>
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Total</span>
                  <span className="text-lg font-bold text-slate-900 dark:text-white">856</span>
                </div>
              </div>
              <div className="flex-1 space-y-3">
                <div className="flex items-center justify-between"><div className="flex items-center"><span className="w-3 h-3 rounded-full bg-primary mr-2"></span><span className="text-sm font-medium text-slate-700 dark:text-slate-200">Salud Pública</span></div><span className="text-xs font-bold text-slate-500">45%</span></div>
                <div className="flex items-center justify-between"><div className="flex items-center"><span className="w-3 h-3 rounded-full bg-red-500 mr-2"></span><span className="text-sm font-medium text-slate-700 dark:text-slate-200">Riesgo</span></div><span className="text-xs font-bold text-slate-500">30%</span></div>
                <div className="flex items-center justify-between"><div className="flex items-center"><span className="w-3 h-3 rounded-full bg-blue-300 mr-2"></span><span className="text-sm font-medium text-slate-700 dark:text-slate-200">Cohesión</span></div><span className="text-xs font-bold text-slate-500">25%</span></div>
              </div>
            </div>
          </div>
        </section>
      </main>

      <div className="fixed bottom-[88px] left-0 right-0 px-5 z-20 pointer-events-none">
        <button className="w-full max-w-md mx-auto bg-primary hover:bg-red-700 text-white font-semibold py-4 rounded-xl shadow-float flex items-center justify-center space-x-2 transition-all active:scale-[0.98] pointer-events-auto"><span className="material-icons-round">picture_as_pdf</span><span>Generar Informe PDF</span></button>
      </div>

      <nav className="fixed bottom-0 w-full max-w-md mx-auto bg-white dark:bg-surface-dark border-t border-slate-200 dark:border-slate-800 pb-6 pt-3 px-6 z-30">
        <div className="flex justify-between items-center">
          <button onClick={goBack} className="flex flex-col items-center space-y-1 text-primary group">
            <div className="relative"><span className="material-icons-round text-2xl group-hover:scale-110 transition-transform">dashboard</span><span className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full"></span></div>
            <span className="text-[10px] font-medium">Panel</span>
          </button>
          <button className="flex flex-col items-center space-y-1 text-slate-400 dark:text-slate-500 hover:text-primary transition-colors"><span className="material-icons-round text-2xl">map</span><span className="text-[10px] font-medium">Mapa</span></button>
          <div className="w-8"></div>
          <button className="flex flex-col items-center space-y-1 text-slate-400 dark:text-slate-500 hover:text-primary transition-colors"><span className="material-icons-round text-2xl">folder_shared</span><span className="text-[10px] font-medium">Reportes</span></button>
          <button className="flex flex-col items-center space-y-1 text-slate-400 dark:text-slate-500 hover:text-primary transition-colors"><span className="material-icons-round text-2xl">settings</span><span className="text-[10px] font-medium">Ajustes</span></button>
        </div>
      </nav>
      <div className="fixed top-0 left-0 w-full h-64 bg-gradient-to-b from-primary/5 to-transparent -z-10 pointer-events-none"></div>
    </div>
  );
};
