
import React from 'react';
import { useNavigation } from '../App';
import { Screen } from '../types';

const CheckpointCard = ({ name, detail, status }: { name: string, detail: string, status: 'Open' | 'Slow' | 'Blocked' }) => {
    const statusConfig = {
        Open: { icon: 'check_circle', text: 'Abierto', color: 'status-success', bg: 'bg-green-50 dark:bg-green-900/30', border: 'border-status-success' },
        Slow: { icon: 'warning', text: 'Lento', color: 'status-warning', bg: 'bg-amber-50 dark:bg-amber-900/30', border: 'border-status-warning' },
        Blocked: { icon: 'block', text: 'Bloqueado', color: 'status-danger', bg: 'bg-red-50 dark:bg-red-900/30', border: 'border-status-danger' },
    };
    const config = statusConfig[status];

    return (
        <div className={`bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border-l-4 ${config.border} flex items-center justify-between`}>
            <div>
                <h4 className="font-bold text-slate-900 dark:text-white">{name}</h4>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{detail}</p>
            </div>
            <div className={`flex items-center gap-1.5 px-2.5 py-1 ${config.bg} rounded text-${config.color} text-sm font-semibold`}>
                <span className="material-icons text-base">{config.icon}</span>
                {config.text}
            </div>
        </div>
    );
};

export const LiveEvacuationTracker = () => {
    const { goBack } = useNavigation();
    const progress = 22;
    const circumference = 2 * Math.PI * 42;
    const strokeDashoffset = circumference - (progress / 100) * circumference;

    return (
        <div className="w-full max-w-md mx-auto h-screen bg-white dark:bg-gray-900 flex flex-col relative shadow-2xl overflow-hidden">
            <header className="px-5 py-4 flex items-center justify-between bg-white dark:bg-gray-900 border-b border-gray-100 dark:border-gray-800 z-10 shrink-0">
                <div className="flex items-center gap-3">
                    <button onClick={goBack} className="p-2 -ml-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                        <span className="material-icons text-slate-600 dark:text-slate-300">arrow_back</span>
                    </button>
                    <h1 className="text-lg font-bold text-slate-900 dark:text-white">Monitoreo en Vivo</h1>
                </div>
                <button aria-label="Emergency SOS" className="flex items-center justify-center w-10 h-10 rounded-full bg-red-50 text-status-danger dark:bg-red-900/20 dark:text-red-400 hover:bg-red-100 transition-colors">
                    <span className="material-icons">sos</span>
                </button>
            </header>

            <main className="flex-1 overflow-y-auto hide-scrollbar pb-24">
                <section className="p-6 flex flex-col items-center justify-center bg-white dark:bg-gray-900">
                    <div className="relative w-48 h-48">
                        <svg className="w-full h-full" viewBox="0 0 100 100">
                            <circle className="text-gray-100 dark:text-gray-800" stroke="currentColor" cx="50" cy="50" fill="transparent" r="42" strokeWidth="8"></circle>
                            <circle className="text-primary" stroke="currentColor" cx="50" cy="50" fill="transparent" r="42" strokeDasharray={circumference} strokeDashoffset={strokeDashoffset} strokeLinecap="round" strokeWidth="8" style={{ transition: 'stroke-dashoffset 0.35s', transform: 'rotate(-90deg)', transformOrigin: '50% 50%' }}></circle>
                        </svg>
                        <div className="absolute inset-0 flex flex-col items-center justify-center">
                            <span className="text-3xl font-bold text-slate-900 dark:text-white">{progress}%</span>
                            <span className="text-xs font-medium text-slate-500 uppercase tracking-wide mt-1">Completado</span>
                        </div>
                    </div>
                    <div className="mt-4 text-center">
                        <h2 className="text-2xl font-bold text-slate-900 dark:text-white">720 <span className="text-slate-400 font-normal">/ 3,240</span></h2>
                        <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Residentes Evacuados</p>
                    </div>
                    <div className="mt-6 flex items-center gap-2 px-3 py-1 bg-green-50 dark:bg-green-900/20 rounded-full">
                        <span className="relative flex h-2 w-2"><span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-status-success opacity-75"></span><span className="relative inline-flex rounded-full h-2 w-2 bg-status-success"></span></span>
                        <span className="text-xs font-semibold text-status-success dark:text-green-400 uppercase tracking-wide">Actualizando en vivo</span>
                    </div>
                </section>
                
                <section className="px-5 py-4 bg-background-light dark:bg-background-dark/50 border-t border-gray-100 dark:border-gray-800">
                    <div className="flex justify-between items-end mb-3">
                        <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">Puntos de Control</h3>
                        <span className="text-xs text-primary font-medium cursor-pointer">Ver mapa completo</span>
                    </div>
                    <div className="grid gap-3">
                        <CheckpointCard name="Punto Escuela" detail="Capacidad: 85% libre" status="Open" />
                        <CheckpointCard name="Punto Calle 7" detail="Alto tráfico reportado" status="Slow" />
                        <CheckpointCard name="Puente Norte" detail="Deslizamiento menor" status="Blocked" />
                    </div>
                </section>
                
            </main>
            
            <div className="absolute bottom-0 left-0 right-0 p-5 bg-white/90 dark:bg-gray-900/90 backdrop-blur-md border-t border-gray-100 dark:border-gray-800 z-20">
                <button className="w-full bg-status-danger hover:bg-red-600 text-white font-bold py-4 px-6 rounded-xl shadow-lg shadow-red-500/30 active:transform active:scale-[0.98] transition-all flex items-center justify-center gap-2 group">
                    <span className="material-icons group-hover:scale-110 transition-transform">stop_circle</span>
                    FINALIZAR EVACUACIÓN
                </button>
                <p className="text-center text-[10px] text-slate-400 mt-2">Solo presione cuando la emergencia haya concluido totalmente.</p>
            </div>
        </div>
    );
};
