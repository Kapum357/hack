
import React, { useState } from 'react';
import { useNavigation } from '../App';
import { Screen } from '../types';

export const EvacuationConfirmation = () => {
    const { navigateTo, goBack } = useNavigation();
    const [notifyVolunteers, setNotifyVolunteers] = useState(true);
    
    const activateEvacuation = () => {
        // Here you would typically make an API call
        // For now, we'll navigate to the live tracker
        navigateTo(Screen.LiveEvacuationTracker);
    };

    return (
        <div className="w-full max-w-md mx-auto bg-white dark:bg-[#2a1515] shadow-2xl rounded-2xl overflow-hidden relative min-h-[800px] flex flex-col my-auto">
            <header className="bg-white dark:bg-[#2a1515] p-4 flex items-center justify-between border-b border-gray-100 dark:border-white/10 sticky top-0 z-10">
                <button onClick={goBack} className="p-2 -ml-2 text-slate-500 dark:text-slate-400 hover:text-primary transition-colors">
                    <span className="material-icons">chevron_left</span>
                </button>
                <div className="text-center">
                    <h1 className="text-lg font-bold text-slate-900 dark:text-white">Confirmar Evacuación</h1>
                    <p className="text-xs text-primary font-medium tracking-wide uppercase">Paso 2 de 2</p>
                </div>
                <div className="w-8"></div>
            </header>

            <main className="flex-1 p-6 space-y-6 overflow-y-auto pb-32">
                <div className="bg-primary/10 border border-primary/20 rounded-lg p-3 flex items-start gap-3">
                    <span className="material-icons text-primary mt-0.5">warning</span>
                    <p className="text-sm text-slate-700 dark:text-slate-200">
                        Estás a punto de activar una alerta real para el sector de <strong>Altos de la Florida</strong>.
                    </p>
                </div>

                <section className="grid grid-cols-2 gap-4">
                    <div className="bg-slate-50 dark:bg-white/5 p-4 rounded-xl border border-slate-100 dark:border-white/5 flex flex-col items-center justify-center text-center shadow-sm">
                        <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center mb-2"><span className="material-icons text-primary">groups</span></div>
                        <span className="text-xs text-slate-500 dark:text-slate-400 font-medium">Población en Riesgo</span>
                        <span className="text-xl font-bold text-slate-900 dark:text-white mt-1">3,240</span>
                    </div>
                    <div className="bg-slate-50 dark:bg-white/5 p-4 rounded-xl border border-slate-100 dark:border-white/5 flex flex-col items-center justify-center text-center shadow-sm">
                        <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center mb-2"><span className="material-icons text-primary">security</span></div>
                        <span className="text-xs text-slate-500 dark:text-slate-400 font-medium">Destino Seguro</span>
                        <span className="text-xl font-bold text-slate-900 dark:text-white mt-1 leading-tight">Escuela Secundaria</span>
                    </div>
                </section>
                
                <section className="space-y-2">
                    <label className="text-sm font-semibold text-slate-900 dark:text-white flex items-center gap-2">
                        <span className="material-icons text-slate-400 text-sm">sms</span>
                        Mensaje de Alerta (SMS)
                    </label>
                    <textarea className="w-full bg-white dark:bg-[#1a0c0c] border border-slate-200 dark:border-white/10 rounded-lg p-4 text-slate-800 dark:text-slate-200 text-base leading-relaxed focus:ring-2 focus:ring-primary focus:border-primary transition-all resize-none shadow-sm" rows="4" defaultValue="ALERTA SOACHA: Evacuación iniciada por riesgo de deslizamiento en Altos de la Florida. Diríjase a la Escuela Secundaria inmediatamente."></textarea>
                </section>

                <section className="bg-white dark:bg-[#1a0c0c] p-4 rounded-xl border border-slate-100 dark:border-white/5 shadow-sm flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-orange-100 dark:bg-orange-900/30 flex items-center justify-center text-orange-600 dark:text-orange-400"><span className="material-icons">volunteer_activism</span></div>
                        <div>
                            <h3 className="text-sm font-semibold text-slate-900 dark:text-white">Notificar voluntarios</h3>
                            <p className="text-xs text-slate-500 dark:text-slate-400">Alertar al equipo de respuesta</p>
                        </div>
                    </div>
                    <div className="relative inline-block w-12 mr-2 align-middle select-none">
                        <input checked={notifyVolunteers} onChange={() => setNotifyVolunteers(!notifyVolunteers)} className="peer absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer checked:right-0 checked:border-primary transition-all duration-300 top-0 left-0" id="toggle" name="toggle" type="checkbox"/>
                        <label className="block overflow-hidden h-6 rounded-full bg-gray-300 dark:bg-gray-600 cursor-pointer peer-checked:bg-primary transition-colors" htmlFor="toggle"></label>
                    </div>
                </section>
            </main>

            <div className="absolute bottom-0 left-0 right-0 bg-white/90 dark:bg-[#2a1515]/90 backdrop-blur-md border-t border-slate-100 dark:border-white/5 p-6 z-20">
                <button onClick={activateEvacuation} className="group w-full bg-primary hover:bg-red-700 text-white font-bold py-4 px-6 rounded-xl shadow-lg shadow-primary/30 transition-all transform active:scale-[0.98]">
                    <div className="flex items-center justify-center gap-3">
                        <span className="material-icons text-2xl animate-pulse">campaign</span>
                        <span className="tracking-wide">ACTIVAR EVACUACIÓN AHORA</span>
                    </div>
                </button>
            </div>
        </div>
    );
};
