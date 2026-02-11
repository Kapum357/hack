
import React, { useState } from 'react';
import { useNavigation } from '../App';
import { Screen } from '../types';

export const EvacuationRouteSelection = () => {
    const { navigateTo, goBack } = useNavigation();
    const [selectedRoute, setSelectedRoute] = useState('A');

    return (
        <div className="bg-background-light dark:bg-background-dark text-slate-900 dark:text-white h-screen flex flex-col overflow-hidden max-w-md mx-auto shadow-2xl relative">
            <header className="bg-white dark:bg-slate-900 px-4 py-3 flex items-center justify-between border-b border-slate-200 dark:border-slate-800 z-20 shrink-0">
                <div className="flex items-center gap-2">
                    <button onClick={goBack} className="p-2 -ml-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500 dark:text-slate-400"><span className="material-icons-round">arrow_back</span></button>
                    <div>
                        <h1 className="font-display font-bold text-lg leading-tight">Activar Evacuación</h1>
                        <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">Paso 1 de 3: Selección de Ruta</p>
                    </div>
                </div>
                <button onClick={goBack} className="text-alert font-bold text-sm bg-red-100/80 dark:bg-red-900/20 px-3 py-1.5 rounded-full hover:bg-red-100 transition-colors">CANCELAR</button>
            </header>

            <main className="flex-1 overflow-y-auto hide-scrollbar pb-32 bg-background-light dark:bg-background-dark">
                <div className="bg-red-500 text-white px-4 py-3 shadow-sm">
                    <div className="flex items-start gap-3">
                        <span className="material-icons-round mt-0.5 animate-pulse">warning</span>
                        <div>
                            <h2 className="font-bold text-sm uppercase tracking-wide">Alerta Activa: Inundación Súbita</h2>
                            <p className="text-sm opacity-90 mt-0.5">Nivel del río subiendo rápidamente en El Danubio.</p>
                        </div>
                    </div>
                </div>

                <div className="relative w-full h-64 bg-slate-200">
                    <img alt="Map of Soacha" className="w-full h-full object-cover opacity-80 mix-blend-multiply" src="https://picsum.photos/seed/mapview/400/300" />
                    <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-background-light dark:to-background-dark/90"></div>
                </div>

                <div className="px-4 -mt-6 relative z-10 space-y-4">
                    <h3 className="font-display font-bold text-slate-800 dark:text-white text-lg pl-1">Seleccionar Ruta Segura</h3>
                    {/* Route Options */}
                    <div onClick={() => setSelectedRoute('A')} className={`group relative bg-white dark:bg-slate-800 rounded-xl shadow-lg border-2 ${selectedRoute === 'A' ? 'border-primary' : 'border-transparent'} overflow-hidden transition-all transform active:scale-[0.99] cursor-pointer`}>
                        <div className="absolute top-0 right-0 bg-primary text-white px-3 py-1 rounded-bl-xl text-xs font-bold uppercase tracking-wider flex items-center gap-1"><span className="material-icons-round text-sm">verified</span> Recomendada</div>
                        <div className="p-4 flex flex-row gap-4 items-center">
                            <div className="w-14 h-14 rounded-lg bg-primary/10 flex items-center justify-center shrink-0 text-primary"><span className="material-icons-round text-3xl">directions_walk</span></div>
                            <div className="flex-1">
                                <h4 className="font-bold text-xl text-slate-900 dark:text-white leading-tight">Ruta A</h4>
                                <p className="text-sm text-slate-500 dark:text-slate-400 font-medium mb-2">Destino: Escuela La Esperanza</p>
                            </div>
                        </div>
                        {selectedRoute === 'A' && <div className="bg-primary/5 p-2 flex items-center justify-center gap-2 border-t border-primary/10"><span className="w-5 h-5 rounded-full bg-primary flex items-center justify-center text-white"><span className="material-icons-round text-sm font-bold">check</span></span><span className="text-primary font-bold text-sm">Seleccionada</span></div>}
                    </div>

                     <div onClick={() => setSelectedRoute('B')} className={`relative bg-white dark:bg-slate-800 rounded-xl shadow-sm border ${selectedRoute === 'B' ? 'border-primary' : 'border-slate-200 dark:border-slate-700'} opacity-80 hover:opacity-100 transition-opacity cursor-pointer`}>
                        <div className="p-4 flex flex-row gap-4 items-center">
                            <div className="w-14 h-14 rounded-lg bg-slate-100 dark:bg-slate-700 flex items-center justify-center shrink-0 text-slate-500 dark:text-slate-400"><span className="material-icons-round text-3xl">kayaking</span></div>
                             <div className="flex-1">
                                <div className="flex justify-between items-center mb-1">
                                    <h4 className="font-bold text-lg text-slate-700 dark:text-slate-200">Ruta B (Río)</h4>
                                    <span className="text-xs font-bold text-orange-500 bg-orange-50 dark:bg-orange-900/30 px-2 py-0.5 rounded">Riesgo Medio</span>
                                </div>
                            </div>
                        </div>
                        {selectedRoute === 'B' && <div className="bg-primary/5 p-2 flex items-center justify-center gap-2 border-t border-primary/10"><span className="w-5 h-5 rounded-full bg-primary flex items-center justify-center text-white"><span className="material-icons-round text-sm font-bold">check</span></span><span className="text-primary font-bold text-sm">Seleccionada</span></div>}
                    </div>
                </div>
            </main>

            <div className="absolute bottom-0 left-0 right-0 p-4 bg-white/95 dark:bg-slate-900/95 backdrop-blur border-t border-slate-200 dark:border-slate-800 z-30 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)]">
                 <div className="flex flex-col gap-3">
                    <button onClick={() => navigateTo(Screen.EvacuationConfirmation)} className="w-full bg-primary hover:bg-red-700 text-white font-display font-extrabold text-lg py-4 rounded-xl shadow-lg shadow-primary/30 active:translate-y-0.5 transition-all flex items-center justify-center gap-3">
                        CONTINUAR CON RUTA {selectedRoute}
                        <span className="material-icons-round">arrow_forward</span>
                    </button>
                </div>
            </div>
        </div>
    );
};
