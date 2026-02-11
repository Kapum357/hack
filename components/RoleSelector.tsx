
import React from 'react';
import { useNavigation } from '../App';
import { Screen, UserRole } from '../types';

const RoleCard = ({ role, icon, name, description, onClick }: { role: UserRole, icon: string, name: string, description: string, onClick: () => void }) => (
    <div onClick={onClick} className="bg-white dark:bg-surface-dark p-6 rounded-xl shadow-card border border-slate-100 dark:border-slate-700/50 cursor-pointer hover:border-primary transition-all hover:scale-105 transform">
        <div className="flex items-center space-x-4">
            <div className="p-3 bg-primary/10 rounded-lg">
                <span className="material-icons-round text-primary text-3xl">{icon}</span>
            </div>
            <div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">{name}</h3>
                <p className="text-sm text-slate-500 dark:text-slate-400">{description}</p>
            </div>
        </div>
    </div>
);

export const RoleSelector = () => {
    const { navigateTo } = useNavigation();

    const handleRoleSelect = (role: UserRole) => {
        switch (role) {
            case UserRole.Official:
                navigateTo(Screen.OfficialAnalyticsDashboard);
                break;
            case UserRole.Leader:
                navigateTo(Screen.LeaderRiskDashboard);
                break;
            case UserRole.Volunteer:
                navigateTo(Screen.VolunteerHome);
                break;
        }
    };

    return (
        <div className="h-full w-full flex flex-col items-center justify-center p-4 bg-background-light dark:bg-background-dark">
            <div className="text-center mb-10">
                 <span className="material-icons-round text-primary text-6xl">security</span>
                <h1 className="text-3xl font-bold mt-2">Soacha Resilience Hub</h1>
                <p className="text-slate-500 dark:text-slate-400 mt-2">Select your role to continue</p>
            </div>
            <div className="w-full max-w-sm space-y-4">
                <RoleCard role={UserRole.Official} icon="analytics" name="Official" description="View high-level analytics" onClick={() => handleRoleSelect(UserRole.Official)} />
                <RoleCard role={UserRole.Leader} icon="people" name="Community Leader" description="Manage local response" onClick={() => handleRoleSelect(UserRole.Leader)} />
                <RoleCard role={UserRole.Volunteer} icon="volunteer_activism" name="Volunteer" description="Access field tasks and reports" onClick={() => handleRoleSelect(UserRole.Volunteer)} />
            </div>
        </div>
    );
};
