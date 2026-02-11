
import React, { useState } from 'react';
import { useNavigation } from '../App';
import { Screen } from '../types';

export const CheckpointReporting = () => {
    const { goBack } = useNavigation();
    const [count, setCount] = useState(142);
    const [status, setStatus] = useState('open');
    
    return (
        <div className="bg-background-light dark:bg-background-dark font-display text-slate-800 dark:text-slate-100 min-h-screen flex flex-col antialiased max-w-md mx-auto">
            <header className="px-5 pt-12 pb-6 relative z-10">
                <button onClick={goBack} className="absolute top-4 left-2 p-2 rounded-full hover:bg-slate-100/50"><span className="material-icons">arrow_back</span></button>
                <div className="flex items-center gap-3 mb-2 opacity-70">
                    <span className="material-icons text-primary text-sm">location_on</span>
                    <span className="text-xs uppercase tracking-widest font-bold">Punto de Control</span>
                </div>
                <h1 className="text-3xl font-black leading-tight tracking-tight text-slate-900 dark:text-white">Escuela San Juan</h1>
                <p className="text-slate-500 dark:text-slate-400 text-sm mt-1 font-medium">Sector 4 • Soacha, Cundinamarca</p>
            </header>

            <main className="flex-1 flex flex-col px-5 pb-6 gap-6 overflow-y-auto">
                <section className="bg-white dark:bg-[#1A2632] rounded-2xl p-6 shadow-lg shadow-primary/5 border border-slate-200 dark:border-slate-800 flex flex-col items-center justify-center flex-1 min-h-[280px]">
                    <h2 className="text-xs uppercase tracking-widest font-bold text-slate-400 mb-6 text-center">Evacuados Registrados</h2>
                    <div className="flex items-center justify-between w-full gap-4 h-full">
                        <button onClick={() => setCount(c => Math.max(0, c - 1))} aria-label="Disminuir conteo" className="w-20 h-20 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 active:scale-95 transition-all flex items-center justify-center shadow-sm">
                            <span className="material-icons text-4xl">remove</span>
                        </button>
                        <div className="flex-1 flex flex-col items-center justify-center">
                            <span className="text-7xl font-black tracking-tighter text-slate-900 dark:text-white leading-none">{count}</span>
                            <span className="text-sm font-medium text-primary mt-2 flex items-center gap-1 bg-primary/10 px-3 py-1 rounded-full"><span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>En tiempo real</span>
                        </div>
                        <button onClick={() => setCount(c => c + 1)} aria-label="Aumentar conteo" className="w-20 h-20 rounded-2xl bg-primary text-white active:scale-95 transition-all flex items-center justify-center shadow-lg shadow-primary/30">
                            <span className="material-icons text-4xl">add</span>
                        </button>
                    </div>
                </section>

                <section className="grid grid-cols-1 gap-3">
                    <h2 className="text-xs uppercase tracking-widest font-bold text-slate-500 dark:text-slate-400 mb-1 ml-1">Estado del Punto</h2>
                    {[
                        { id: 'open', title: 'ABIERTO', subtitle: 'Flujo normal de personas', icon: 'check_circle', color: 'status-green' },
                        { id: 'slow', title: 'LENTO', subtitle: 'Cuello de botella detectado', icon: 'warning', color: 'status-yellow' },
                        { id: 'blocked', title: 'BLOQUEADO', subtitle: 'Emergencia / Paso cerrado', icon: 'block', color: 'status-red' }
                    ].map(({ id, title, subtitle, icon, color }) => (
                         <label key={id} className={`relative flex items-center p-4 rounded-xl border-2 cursor-pointer transition-all active:scale-[0.98] ${status === id ? `border-${color} bg-${color}/10` : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-[#1A2632] opacity-60 hover:opacity-100'}`}>
                            <input checked={status === id} onChange={() => setStatus(id)} className="peer sr-only" name="status" type="radio" value={id} />
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center text-white shadow-sm mr-4 ${status === id ? `bg-${color}` : `bg-${color}/20 text-${color}`}`}>
                                <span className="material-icons">{icon}</span>
                            </div>
                            <div className="flex-1">
                                <div className="font-bold text-lg dark:text-white">{title}</div>
                                <div className="text-xs text-slate-500 dark:text-slate-400 font-medium">{subtitle}</div>
                            </div>
                            <div className={`w-4 h-4 rounded-full border-2 ${status === id ? `border-${color} bg-${color}` : 'border-slate-300 dark:border-slate-600'}`}></div>
                        </label>
                    ))}
                </section>
            </main>

            <div className="sticky bottom-0 left-0 w-full p-5 bg-background-light dark:bg-background-dark/95 backdrop-blur-md border-t border-slate-200 dark:border-slate-800 z-50">
                <button className="w-full h-14 bg-slate-800 dark:bg-slate-700 hover:bg-slate-700 dark:hover:bg-slate-600 text-white rounded-xl font-bold text-lg flex items-center justify-center gap-3 shadow-lg active:scale-[0.98]">
                    <span className="material-icons text-primary">mic</span> Reportar Novedad
                </button>
            </div>
        </div>
    );
};
