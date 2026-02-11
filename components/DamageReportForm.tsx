
import React, { useState } from 'react';
import { useNavigation } from '../App';
import { Screen } from '../types';


export const DamageReportForm = () => {
    const { goBack } = useNavigation();
    const [affectedCount, setAffectedCount] = useState(0);

    const handleCountChange = (amount: number) => {
        setAffectedCount(prev => Math.max(0, prev + amount));
    };

    return (
        <div className="w-full max-w-md mx-auto bg-background-light dark:bg-background-dark min-h-screen flex flex-col relative shadow-2xl overflow-hidden">
            <header className="bg-surface-light dark:bg-surface-dark px-6 pt-12 pb-4 shadow-sm z-10 sticky top-0 border-b border-primary/10">
                <div className="flex items-center justify-between">
                    <button onClick={goBack} aria-label="Atrás" className="p-2 -ml-2 rounded-full hover:bg-primary/10 transition-colors text-primary">
                        <span className="material-icons text-3xl">arrow_back</span>
                    </button>
                    <h1 className="text-xl font-bold text-center flex-grow text-slate-800 dark:text-white">Reporte de Daños</h1>
                    <div className="w-10"></div>
                </div>
            </header>

            <main className="flex-grow p-6 space-y-8 overflow-y-auto pb-32">
                <section>
                    <h2 className="text-lg font-semibold text-slate-600 dark:text-slate-300 mb-3 flex items-center gap-2">
                        <span className="material-icons text-primary text-xl">my_location</span>Ubicación Detectada
                    </h2>
                    <div className="bg-surface-light dark:bg-surface-dark p-4 rounded-xl border border-primary/20 shadow-sm flex items-start gap-4">
                        <div className="flex-shrink-0 w-16 h-16 rounded-lg overflow-hidden bg-slate-200 relative">
                            <div className="absolute inset-0 bg-cover bg-center" style={{ backgroundImage: `url('https://picsum.photos/seed/map/100/100')` }}></div>
                            <div className="absolute inset-0 bg-primary/10 flex items-center justify-center"><span className="material-icons text-primary text-3xl drop-shadow-md">location_on</span></div>
                        </div>
                        <div className="flex flex-col justify-center h-16">
                            <span className="text-primary font-bold text-lg leading-tight">El Danubio</span>
                            <span className="text-slate-500 dark:text-slate-400 text-base">Calle 7 #45-19</span>
                        </div>
                    </div>
                </section>

                <section className="space-y-6">
                    <div>
                        <label className="block text-lg font-semibold text-slate-700 dark:text-slate-200 mb-3" htmlFor="damage-type">Tipo de Evento</label>
                        <select className="w-full bg-surface-light dark:bg-surface-dark border border-slate-300 dark:border-slate-600 rounded-xl px-4 py-4 text-lg font-medium focus:ring-2 focus:ring-primary focus:border-primary transition-all text-slate-800 dark:text-white shadow-sm appearance-none cursor-pointer" id="damage-type">
                            <option disabled value="">Seleccionar tipo...</option>
                            <option value="inundacion">Inundación</option>
                            <option value="deslizamiento">Deslizamiento</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-lg font-semibold text-slate-700 dark:text-slate-200 mb-3">Severidad</label>
                        <div className="grid grid-cols-3 gap-3">
                            {['Leve', 'Moderado', 'Severo'].map((level, i) => (
                                <label key={level} className="cursor-pointer group">
                                    <input className="peer sr-only" name="severity" type="radio" value={level.toLowerCase()} />
                                    <div className={`h-16 flex flex-col items-center justify-center rounded-xl border-2 border-slate-200 dark:border-slate-700 bg-surface-light dark:bg-surface-dark text-slate-500 peer-checked:border-green-500 peer-checked:bg-green-50 dark:peer-checked:bg-green-900/20 peer-checked:text-green-700 dark:peer-checked:text-green-400 transition-all shadow-sm
                                        ${i === 1 && 'peer-checked:border-yellow-500 peer-checked:bg-yellow-50 dark:peer-checked:bg-yellow-900/20 peer-checked:text-yellow-700 dark:peer-checked:text-yellow-400'}
                                        ${i === 2 && 'peer-checked:border-red-500 peer-checked:bg-red-50 dark:peer-checked:bg-red-900/20 peer-checked:text-red-700 dark:peer-checked:text-red-400'}
                                    `}>
                                        <span className="material-icons text-2xl mb-1">{i === 0 ? 'sentiment_satisfied' : i === 1 ? 'warning' : 'error'}</span>
                                        <span className="text-sm font-bold">{level}</span>
                                    </div>
                                </label>
                            ))}
                        </div>
                    </div>
                    
                    <div>
                        <label className="block text-lg font-semibold text-slate-700 dark:text-slate-200 mb-3" htmlFor="affected-people">Personas Afectadas</label>
                        <div className="flex items-center bg-surface-light dark:bg-surface-dark rounded-xl border border-slate-300 dark:border-slate-600 p-2 shadow-sm">
                            <button className="w-14 h-14 rounded-lg bg-primary/10 hover:bg-primary/20 text-primary flex items-center justify-center transition-colors active:scale-95" onClick={() => handleCountChange(-1)} type="button"><span className="material-icons text-3xl">remove</span></button>
                            <input readOnly className="flex-1 text-center text-3xl font-bold bg-transparent border-none focus:ring-0 p-0 text-slate-800 dark:text-white" id="affected-people" value={affectedCount} />
                            <button className="w-14 h-14 rounded-lg bg-primary/10 hover:bg-primary/20 text-primary flex items-center justify-center transition-colors active:scale-95" onClick={() => handleCountChange(1)} type="button"><span className="material-icons text-3xl">add</span></button>
                        </div>
                    </div>

                     <div>
                        <h3 className="text-lg font-semibold text-slate-700 dark:text-slate-200 mb-3">Evidencia Fotográfica</h3>
                        <div className="grid grid-cols-2 gap-4">
                            <button className="aspect-square rounded-2xl border-2 border-dashed border-primary bg-primary/5 hover:bg-primary/10 flex flex-col items-center justify-center gap-2 transition-all active:scale-95 group" type="button">
                                <div className="w-16 h-16 rounded-full bg-primary text-white flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform"><span className="material-icons text-3xl">camera_alt</span></div>
                                <span className="font-medium text-primary text-lg">Tomar Foto</span>
                            </button>
                            <div className="aspect-square rounded-2xl overflow-hidden relative shadow-sm group">
                                <img alt="Flooded street corner with debris" className="w-full h-full object-cover" src="https://picsum.photos/seed/flood/200/200" />
                            </div>
                        </div>
                    </div>
                </section>
            </main>

            <div className="absolute bottom-0 left-0 w-full p-6 bg-gradient-to-t from-background-light via-background-light to-transparent dark:from-background-dark dark:via-background-dark pt-12">
                <button className="w-full bg-primary hover:bg-red-700 text-white font-bold text-xl py-5 rounded-2xl shadow-lg shadow-primary/30 active:scale-[0.98] transition-all flex items-center justify-center gap-3" type="button">
                    <span>ENVIAR REPORTE</span>
                    <span className="material-icons">send</span>
                </button>
            </div>
        </div>
    );
};
