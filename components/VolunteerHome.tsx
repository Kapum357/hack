
import React from 'react';
import { useNavigation } from '../App';
import { Screen } from '../types';

export const VolunteerHome = () => {
    const { goBack, navigateTo } = useNavigation();

    return (
        <div className="bg-background-light dark:bg-background-dark font-display text-gray-900 dark:text-white min-h-screen flex flex-col relative overflow-hidden max-w-md mx-auto">
            <div className="bg-amber-400 text-amber-950 px-4 py-2 flex items-center justify-center font-bold text-sm shadow-sm z-50">
                <span className="material-icons-round mr-2 text-lg">wifi_off</span>
                Trabajando sin conexión
            </div>

            <header className="px-5 py-4 flex items-center justify-between bg-surface-light dark:bg-surface-dark shadow-subtle z-40">
                <div className="flex items-center gap-3">
                    <div className="relative">
                        <div className="w-10 h-10 rounded-full overflow-hidden border-2 border-primary/20"><img alt="Profile of Diego" className="w-full h-full object-cover" src="https://picsum.photos/id/1027/100/100" /></div>
                    </div>
                    <div>
                        <h1 className="text-sm text-gray-500 dark:text-gray-400 font-medium">Bienvenido,</h1>
                        <p className="text-lg font-bold leading-tight text-gray-900 dark:text-white">Diego</p>
                    </div>
                </div>
                <button onClick={() => navigateTo(Screen.OfflineSyncManagement)} className="rounded-full p-2 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-gray-600 dark:text-gray-300">
                    <span className="material-icons-round text-2xl">sync</span>
                </button>
            </header>

            <main className="flex-1 overflow-y-auto px-4 pb-32 pt-4">
                <div className="flex justify-between items-end mb-4 px-1">
                    <div>
                        <p className="text-xs font-semibold text-primary uppercase tracking-wider mb-1">Soacha, Cundinamarca</p>
                        <p className="text-2xl font-bold">Lunes, 14 Oct</p>
                    </div>
                    <div className="flex items-center gap-1 text-gray-600 dark:text-gray-300"><span className="material-icons-round">cloud_queue</span><span className="font-bold">18°C</span></div>
                </div>

                <div className="mb-6 rounded-xl overflow-hidden shadow-strong bg-white dark:bg-surface-dark border-l-8 border-orange-500 relative">
                    <div className="p-4 relative z-10">
                        <div className="flex items-start gap-3">
                             <div className="bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400 rounded-full p-2 mt-0.5"><span className="material-icons-round text-xl">warning</span></div>
                            <div className="flex-1">
                                <h2 className="text-lg font-bold text-orange-700 dark:text-orange-400 mb-1">ALERTA NARANJA</h2>
                                <p className="font-bold text-gray-900 dark:text-white mb-1">Sector El Danubio</p>
                                <p className="text-sm text-gray-700 dark:text-gray-300 leading-snug">Riesgo de deslizamiento por lluvias recientes.</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div className="flex items-center justify-between mb-3 px-1">
                    <h3 className="font-bold text-lg text-gray-900 dark:text-white flex items-center gap-2">MIS TAREAS <span className="bg-primary/10 text-primary text-xs px-2 py-0.5 rounded-full">3 Pendientes</span></h3>
                </div>
                
                <div className="space-y-3">
                    {/* Task items here */}
                    <div className="bg-white dark:bg-surface-dark p-4 rounded-xl shadow-sm flex items-start gap-4">
                        <input type="checkbox" className="mt-1 h-6 w-6 rounded border-gray-300 text-primary focus:ring-primary/50" />
                        <div className="flex-1"><h4 className="font-bold text-gray-900 dark:text-white text-lg">Limpieza de Drenaje</h4><p className="text-sm text-gray-500 dark:text-gray-400">Verificar obstrucciones.</p></div>
                    </div>
                    <div className="bg-white dark:bg-surface-dark p-4 rounded-xl shadow-sm flex items-start gap-4">
                        <input type="checkbox" className="mt-1 h-6 w-6 rounded border-gray-300 text-primary focus:ring-primary/50" />
                        <div className="flex-1"><h4 className="font-bold text-gray-900 dark:text-white text-lg">Censo de Familias</h4><p className="text-sm text-gray-500 dark:text-gray-400">Actualizar datos de 10 hogares.</p></div>
                    </div>
                    <div className="bg-gray-50 dark:bg-gray-800/50 p-4 rounded-xl shadow-sm flex items-start gap-4 opacity-60">
                        <input type="checkbox" checked readOnly className="mt-1 h-6 w-6 rounded border-gray-300 text-primary focus:ring-primary/50" />
                        <div className="flex-1"><h4 className="font-bold text-gray-900 dark:text-white text-lg line-through">Verificación Muros</h4></div>
                    </div>
                </div>

            </main>

            <div className="fixed bottom-0 left-0 right-0 z-50 pointer-events-none max-w-md mx-auto">
                 <div className="bg-background-light dark:bg-background-dark pt-2 px-4 pointer-events-auto shadow-nav pb-safe">
                    <button onClick={() => navigateTo(Screen.DamageReportForm)} className="w-full bg-primary hover:bg-red-700 text-white rounded-xl py-4 px-6 shadow-lg flex items-center justify-center gap-3 transition-transform transform active:scale-95">
                        <span className="material-icons-round text-3xl">add_a_photo</span>
                        <span className="font-bold text-xl tracking-wide">NUEVO REPORTE</span>
                    </button>
                    <div className="flex justify-around items-center mt-3 pb-2">
                        <button onClick={goBack} className="flex flex-col items-center text-primary"><span className="material-icons-round text-2xl">home</span><span className="text-[10px] font-bold mt-0.5">Inicio</span></button>
                        <button className="flex flex-col items-center text-gray-400"><span className="material-icons-round text-2xl">map</span><span className="text-[10px] font-medium mt-0.5">Mapa</span></button>
                        <button className="flex flex-col items-center text-gray-400"><span className="material-icons-round text-2xl">chat</span><span className="text-[10px] font-medium mt-0.5">Chat</span></button>
                        <button className="flex flex-col items-center text-gray-400"><span className="material-icons-round text-2xl">person</span><span className="text-[10px] font-medium mt-0.5">Perfil</span></button>
                    </div>
                </div>
            </div>
        </div>
    );
};
