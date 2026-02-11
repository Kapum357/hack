
import React from 'react';
import { useNavigation } from '../App';
import { Screen } from '../types';

export const LeaderRiskDashboard = () => {
    const { goBack, navigateTo } = useNavigation();

    return (
        <div className="bg-background-light dark:bg-background-dark font-display text-slate-800 dark:text-slate-100 antialiased h-screen overflow-hidden flex flex-col relative max-w-md mx-auto">
            <div className="bg-alert-orange text-white px-4 py-3 shadow-md z-50 flex items-start justify-between shrink-0">
                <div className="flex items-start gap-3">
                    <span className="material-icons text-white animate-pulse">warning</span>
                    <div>
                        <h2 className="font-bold text-sm uppercase tracking-wider">Alerta Naranja</h2>
                        <p className="text-xs font-medium mt-0.5">Zona 3: Riesgo de Inundación (Rio Soacha)</p>
                    </div>
                </div>
                <button className="bg-white/20 hover:bg-white/30 rounded-full p-1 transition-colors">
                    <span className="material-icons text-sm">close</span>
                </button>
            </div>

            <main className="flex-1 overflow-y-auto pb-24 hide-scrollbar">
                <header className="px-5 pt-5 pb-2 flex justify-between items-center">
                    <div>
                        <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide">Bienvenida, María</p>
                        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Panel de Control</h1>
                    </div>
                    <div className="flex flex-col items-end">
                        <span className="text-xs font-medium text-slate-400 dark:text-slate-500">Soacha, Cundinamarca</span>
                        <div className="flex items-center gap-1 text-primary">
                            <span className="material-icons text-sm">cloud</span>
                            <span className="text-xs font-bold">18°C</span>
                        </div>
                    </div>
                </header>

                <div className="px-5 mt-2">
                    <div className="relative w-full h-64 bg-slate-200 rounded-xl overflow-hidden shadow-sm border border-slate-200 dark:border-slate-700">
                        <div className="absolute inset-0 bg-cover bg-center opacity-80" style={{ backgroundImage: "url('https://picsum.photos/seed/soacha/400/300')", filter: 'grayscale(20%) contrast(110%)' }}></div>
                        <div className="absolute top-1/4 left-1/4 w-32 h-24 bg-red-500/30 border-2 border-red-500 rounded-full blur-sm transform -rotate-12"></div>
                        <div className="absolute bottom-4 right-1/4 w-28 h-20 bg-green-500/30 border-2 border-green-500 rounded-full blur-sm transform rotate-6"></div>
                        <div className="absolute top-[35%] left-[35%] cursor-pointer group">
                            <div className="relative flex items-center justify-center">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                                <div className="bg-primary text-white p-1.5 rounded-full shadow-lg z-10 border-2 border-white dark:border-slate-800"><span className="material-icons text-base">campaign</span></div>
                            </div>
                        </div>
                        <div className="absolute bottom-[20%] right-[30%] cursor-pointer">
                            <div className="bg-slate-700 text-white p-1.5 rounded-full shadow-lg z-10 border-2 border-white dark:border-slate-800"><span className="material-icons text-base">camera_alt</span></div>
                        </div>
                        <div className="absolute bottom-3 left-3 bg-white/90 dark:bg-slate-900/90 backdrop-blur-sm px-3 py-1.5 rounded-lg shadow-sm border border-slate-100 dark:border-slate-700 text-xs font-medium">
                            <div className="flex items-center gap-2 mb-1"><span className="w-2 h-2 rounded-full bg-risk-high"></span> Alto Riesgo</div>
                            <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-risk-low"></span> Estable</div>
                        </div>
                    </div>
                </div>

                <div className="px-5 mt-6 grid grid-cols-2 gap-4">
                    <div className="bg-white dark:bg-slate-800 p-4 rounded-xl shadow-sm border border-slate-100 dark:border-slate-700 flex flex-col items-start">
                        <div className="bg-primary/10 text-primary p-2 rounded-lg mb-2"><span className="material-icons text-xl">groups</span></div>
                        <span className="text-2xl font-bold text-slate-900 dark:text-white">15k</span>
                        <span className="text-xs text-slate-500 dark:text-slate-400">Personas Alcanzadas</span>
                    </div>
                    <div className="bg-white dark:bg-slate-800 p-4 rounded-xl shadow-sm border border-slate-100 dark:border-slate-700 flex flex-col items-start">
                        <div className="bg-alert-orange/10 text-alert-orange p-2 rounded-lg mb-2"><span className="material-icons text-xl">assignment_late</span></div>
                        <span className="text-2xl font-bold text-slate-900 dark:text-white">4</span>
                        <span className="text-xs text-slate-500 dark:text-slate-400">Reportes Activos</span>
                    </div>
                </div>

                <div className="px-5 mt-8">
                    <div className="flex justify-between items-end mb-4">
                        <h3 className="text-lg font-bold text-slate-900 dark:text-white">Estado de Zonas</h3>
                        <button className="text-sm font-medium text-primary hover:text-red-700">Ver Todo</button>
                    </div>
                    <div className="space-y-4">
                        <div className="bg-white dark:bg-slate-800 rounded-xl p-4 shadow-sm border-l-4 border-risk-high relative overflow-hidden">
                            <div className="flex justify-between items-start z-10 relative">
                                <div>
                                    <div className="flex items-center gap-2 mb-1">
                                        <h4 className="font-bold text-base text-slate-900 dark:text-white">El Danubio</h4>
                                        <span className="bg-risk-high/10 text-risk-high text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wide">Crítico</span>
                                    </div>
                                    <p className="text-xs text-slate-500 dark:text-slate-400 flex items-center gap-1"><span className="material-icons text-xs">home</span> 1,200 Familias</p>
                                </div>
                                <div className="text-right">
                                    <span className="block text-2xl font-black text-risk-high">78%</span>
                                    <span className="text-[10px] font-medium text-slate-400 uppercase">Nivel de Riesgo</span>
                                </div>
                            </div>
                            <div className="w-full bg-slate-100 dark:bg-slate-700 h-1.5 rounded-full mt-4">
                                <div className="bg-risk-high h-1.5 rounded-full" style={{ width: '78%' }}></div>
                            </div>
                        </div>
                        <div className="bg-white dark:bg-slate-800 rounded-xl p-4 shadow-sm border-l-4 border-risk-low relative overflow-hidden">
                            <div className="flex justify-between items-start z-10 relative">
                                <div>
                                    <h4 className="font-bold text-base text-slate-900 dark:text-white">La María</h4>
                                    <p className="text-xs text-slate-500 dark:text-slate-400 flex items-center gap-1"><span className="material-icons text-xs">home</span> 850 Familias</p>
                                </div>
                                <div className="text-right">
                                    <span className="block text-2xl font-black text-risk-low">22%</span>
                                    <span className="text-[10px] font-medium text-slate-400 uppercase">Nivel de Riesgo</span>
                                </div>
                            </div>
                            <div className="w-full bg-slate-100 dark:bg-slate-700 h-1.5 rounded-full mt-4">
                                <div className="bg-risk-low h-1.5 rounded-full" style={{ width: '22%' }}></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="h-24"></div>
            </main>

            <div className="absolute bottom-24 right-5 z-40">
                <button onClick={() => navigateTo(Screen.EvacuationRouteSelection)} className="bg-primary hover:bg-red-700 text-white rounded-full w-14 h-14 flex items-center justify-center shadow-lg shadow-primary/30 transition-transform active:scale-95">
                    <span className="material-icons text-2xl">add_alert</span>
                </button>
            </div>

            <nav className="bg-white dark:bg-background-dark border-t border-slate-200 dark:border-slate-800 px-6 py-3 flex justify-between items-center z-50 shrink-0 pb-6">
                <button onClick={goBack} className="flex flex-col items-center gap-1 text-primary">
                    <span className="material-icons">dashboard</span>
                    <span className="text-[10px] font-medium">Inicio</span>
                </button>
                <button className="flex flex-col items-center gap-1 text-slate-400 dark:text-slate-500"><span className="material-icons">map</span><span className="text-[10px] font-medium">Mapa</span></button>
                <button className="flex flex-col items-center gap-1 text-slate-400 dark:text-slate-500"><div className="relative"><span className="material-icons">description</span><span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-risk-high rounded-full border-2 border-white dark:border-background-dark"></span></div><span className="text-[10px] font-medium">Reportes</span></button>
                <button className="flex flex-col items-center gap-1 text-slate-400 dark:text-slate-500"><span className="material-icons">person</span><span className="text-[10px] font-medium">Perfil</span></button>
            </nav>
        </div>
    );
};
