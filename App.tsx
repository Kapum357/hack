
import React, { useState, createContext, useContext, ReactNode } from 'react';

import { RoleSelector } from './components/RoleSelector';
import { LiveEvacuationTracker } from './components/LiveEvacuationTracker';
import { OfficialAnalyticsDashboard } from './components/OfficialAnalyticsDashboard';
import { LeaderRiskDashboard } from './components/LeaderRiskDashboard';
import { DamageReportForm } from './components/DamageReportForm';
import { EvacuationRouteSelection } from './components/EvacuationRouteSelection';
import { EvacuationConfirmation } from './components/EvacuationConfirmation';
import { VolunteerHome } from './components/VolunteerHome';
import { CheckpointReporting } from './components/CheckpointReporting';
import { OfflineSyncManagement } from './components/OfflineSyncManagement';
import { Screen } from './types';


interface NavigationContextType {
    screen: Screen;
    navigateTo: (screen: Screen) => void;
    goBack: () => void;
}

const NavigationContext = createContext<NavigationContextType | undefined>(undefined);

export const useNavigation = () => {
    const context = useContext(NavigationContext);
    if (!context) {
        throw new Error('useNavigation must be used within a NavigationProvider');
    }
    return context;
};

const NavigationProvider = ({ children }: { children: ReactNode }) => {
    const [history, setHistory] = useState<Screen[]>([Screen.RoleSelector]);

    const navigateTo = (screen: Screen) => {
        setHistory(prev => [...prev, screen]);
    };
    
    const goBack = () => {
        setHistory(prev => prev.length > 1 ? prev.slice(0, -1) : prev);
    };

    const screen = history[history.length - 1];

    return (
        <NavigationContext.Provider value={{ screen, navigateTo, goBack }}>
            {children}
        </NavigationContext.Provider>
    );
};

const AppContent = () => {
    const { screen } = useNavigation();

    const renderScreen = () => {
        switch (screen) {
            case Screen.RoleSelector:
                return <RoleSelector />;
            case Screen.OfficialAnalyticsDashboard:
                return <OfficialAnalyticsDashboard />;
            case Screen.LeaderRiskDashboard:
                return <LeaderRiskDashboard />;
            case Screen.VolunteerHome:
                return <VolunteerHome />;
            case Screen.LiveEvacuationTracker:
                return <LiveEvacuationTracker />;
            case Screen.DamageReportForm:
                return <DamageReportForm />;
            case Screen.EvacuationRouteSelection:
                return <EvacuationRouteSelection />;
            case Screen.EvacuationConfirmation:
                return <EvacuationConfirmation />;
            case Screen.CheckpointReporting:
                return <CheckpointReporting />;
            case Screen.OfflineSyncManagement:
                return <OfflineSyncManagement />;
            default:
                return <RoleSelector />;
        }
    };

    return (
        <div className="h-screen w-screen bg-background-light dark:bg-background-dark font-display text-slate-800 dark:text-slate-100">
            {renderScreen()}
        </div>
    );
};

const App = () => {
    return (
        <NavigationProvider>
            <AppContent />
        </NavigationProvider>
    );
};

export default App;
