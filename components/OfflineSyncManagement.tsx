
import React from 'react';
import { useNavigation } from '../App';
import { Screen } from '../types';

export const OfflineSyncManagement = () => {
    const { goBack } = useNavigation();

    return (
        <div className="w-full max-w-md h-screen mx-auto flex flex-col relative bg-background-light dark:bg-background-dark overflow-hidden shadow-2xl">
            <header className="pt-12 pb-4 px-4 flex items-center justify-between z-10 bg-background-light dark:bg-background-dark/95 backdrop-blur-sm sticky top-0">
                <button onClick={goBack} aria-label="Volver" className="p-2 rounded-full hover:bg-slate-200 dark:hover:bg-surface-dark transition-colors">
                    <span className="material-icons-round text-2xl text-slate-600 dark:text-slate-300">arrow_back</span>
                </button>
                <h1 className="text-lg font-bold text-center flex-grow">Gestión de Datos</h1>
                <button aria-label="Configuración" className="p-2 rounded-full hover:bg-slate-200 dark:hover:bg-surface-dark transition-colors">
                    <span className="material-icons-round text-2xl text-slate-600 dark:text-slate-300">settings</span>
                </button>
            </header>

            <main className="flex-1 overflow-y-auto px-4 pb-24 scroll-smooth">
                <div className="w-full bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-4 mb-6 flex items-center justify-between shadow-sm">
                    <div className="flex items-center gap-3">
                        <div className="bg-yellow-500/20 p-2 rounded-full"><span className="material-icons-round text-yellow-500 text-xl">wifi_off</span></div>
                        <div>
                            <h2 className="font-bold text-yellow-600 dark:text-yellow-400 uppercase tracking-wide text-sm">Modo Offline</h2>
                            <p className="text-xs text-slate-500 dark:text-slate-400">Sin conexión a internet</p>
                        </div>
                    </div>
                    <div className="h-3 w-3 rounded-full bg-yellow-500 animate-pulse shadow-[0_0_8px_rgba(245,158,11,0.6)]"></div>
                </div>

                <div className="bg-white dark:bg-surface-dark rounded-2xl p-6 shadow-lg mb-6 border border-slate-100 dark:border-slate-800">
                    <div className="flex justify-between items-start mb-4">
                        <div>
                            <span className="block text-4xl font-bold text-slate-900 dark:text-white mb-1">4</span>
                            <span className="text-sm font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Reportes Pendientes</span>
                        </div>
                        <div className="bg-primary/10 dark:bg-primary/20 p-3 rounded-xl"><span className="material-icons-round text-primary text-2xl">cloud_queue</span></div>
                    </div>
                    <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2"><div className="bg-primary h-2 rounded-full w-[5%]"></div></div>
                </div>

                <div className="flex justify-between items-end mb-4 px-1">
                    <h3 className="font-bold text-lg">Cola de Sincronización</h3>
                    <span className="text-xs text-primary font-medium cursor-pointer hover:underline">Historial</span>
                </div>
                
                <div className="space-y-3">
                    <div className="group bg-white dark:bg-surface-dark border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm">
                        <div className="flex justify-between items-start">
                            <div className="flex gap-3">
                                <div className="mt-1 h-10 w-10 rounded-lg bg-red-500/10 flex items-center justify-center flex-shrink-0"><span className="material-icons-round text-red-500 text-xl">warning</span></div>
                                <div>
                                    <h4 className="font-bold text-sm text-slate-800 dark:text-slate-100">Reporte de Daños #102</h4>
                                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Hace 2 horas • Deslizamiento</p>
                                </div>
                            </div>
                            <span className="h-2 w-2 rounded-full bg-red-500 mt-2"></span>
                        </div>
                        <div className="mt-4 flex gap-3 pt-3 border-t border-slate-100 dark:border-slate-700">
                            <button className="flex-1 py-2 px-3 bg-slate-100 dark:bg-slate-700 rounded-lg text-xs font-bold text-slate-700 dark:text-slate-300 flex items-center justify-center gap-2">REINTENTAR</button>
                            <button className="flex-1 py-2 px-3 bg-primary/10 rounded-lg text-xs font-bold text-primary flex items-center justify-center gap-2">VER</button>
                        </div>
                    </div>
                </div>
            </main>

            <div className="absolute bottom-0 left-0 w-full p-4 bg-background-light dark:bg-background-dark border-t border-slate-200 dark:border-slate-800/50 backdrop-blur-md bg-opacity-95 dark:bg-opacity-95 z-20">
                <button className="w-full bg-primary hover:bg-red-700 text-white font-bold py-4 rounded-xl shadow-lg shadow-primary/30 active:scale-[0.98] transition-transform flex items-center justify-center gap-2">
                    <span className="material-icons-round">sync</span>
                    SINCRONIZAR TODO AHORA
                </button>
            </div>
        </div>
    );
};
