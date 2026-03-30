import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LayoutDashboard, Mic2, Settings, LogOut, Clock, PlayCircle, Plus } from 'lucide-react';

const DashboardLayout = ({ children, activeTab }) => {
    const { user, logout } = useAuth();

    return (
        <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--bg-primary)' }}>
            {/* Sidebar */}
            <aside style={{ width: '280px', background: 'var(--bg-card)', borderRight: '1px solid var(--border)', display: 'flex', flexDirection: 'column', padding: '2rem 1.5rem' }}>
                <div style={{ marginBottom: '3rem', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <div style={{ width: '36px', height: '36px', borderRadius: '8px', background: 'linear-gradient(135deg, var(--accent-purple), var(--accent-cyan))', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <Mic2 color="white" size={20} />
                    </div>
                    <span style={{ fontSize: '1.25rem', fontFamily: 'var(--font-display)', fontWeight: 800 }}>DubSmart Studio</span>
                </div>

                <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 1 }}>
                    <Link to="/dashboard" className={`btn-ghost ${activeTab === 'overview' ? 'active' : ''}`} style={{ justifyContent: 'flex-start', background: activeTab === 'overview' ? 'rgba(255,255,255,0.05)' : 'transparent', border: '1px solid transparent' }}>
                        <LayoutDashboard size={20} /> Overview
                    </Link>
                    <Link to="/studio" className={`btn-ghost ${activeTab === 'studio' ? 'active' : ''}`} style={{ justifyContent: 'flex-start', background: activeTab === 'studio' ? 'rgba(255,255,255,0.05)' : 'transparent', border: '1px solid transparent' }}>
                        <PlayCircle size={20} /> New Dubbing Job
                    </Link>
                    <Link to="/dashboard/settings" className={`btn-ghost ${activeTab === 'settings' ? 'active' : ''}`} style={{ justifyContent: 'flex-start', background: activeTab === 'settings' ? 'rgba(255,255,255,0.05)' : 'transparent', border: '1px solid transparent' }}>
                        <Settings size={20} /> Settings
                    </Link>
                    {user?.email === 'sasi@dubsmart.ai' && (
                        <Link to="/admin" className="btn-ghost" style={{ justifyContent: 'flex-start', color: 'var(--warning)', borderColor: 'rgba(245,158,11,0.2)' }}>
                            <Settings size={20} /> Super Admin Panel
                        </Link>
                    )}
                </nav>

                <div style={{ padding: '1.5rem', background: '#0A0A0A', borderRadius: '16px', border: '1px solid var(--border)', marginBottom: '1.5rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                        <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Available Credits</span>
                        <span style={{ fontWeight: 700, fontFamily: 'var(--font-mono)' }}>{user?.credits || 10}</span>
                    </div>
                    <div style={{ width: '100%', height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                        {/* Fixed 100 max width ratio for mock UI */}
                        <div style={{ width: `${Math.min(100, (user?.credits || 10) / 100 * 100)}%`, height: '100%', background: 'linear-gradient(90deg, var(--accent-purple), var(--accent-cyan))' }}></div>
                    </div>
                </div>

                <button onClick={logout} className="btn-ghost" style={{ justifyContent: 'flex-start', color: 'var(--text-muted)' }}><LogOut size={20} /> Log Out</button>
            </aside>

            {/* Main Content Area */}
            <main style={{ flex: 1, padding: '3rem 4rem', overflowY: 'auto' }}>
                {children}
            </main>
        </div>
    );
};

const DashboardOverview = () => {
    const { user } = useAuth();

    // Mock Data
    const recentJobs = [
        { id: 1, name: 'Q1_Marketing_Promo.mp4', lang: 'Spanish (ES)', status: 'Completed', date: '2 hours ago' },
        { id: 2, name: 'Sasi_Keynote_Speech.wav', lang: 'Japanese (JP)', status: 'Processing', date: '5 hours ago' },
        { id: 3, name: 'Customer_Testimonial.mp4', lang: 'French (FR)', status: 'Completed', date: '1 day ago' }
    ];

    return (
        <DashboardLayout activeTab="overview">
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
                <div>
                    <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Welcome, {user?.name || 'Creator'}</h1>
                    <p style={{ color: 'var(--text-muted)' }}>Here's an overview of your recent studio activity.</p>
                </div>
                <Link to="/studio" className="btn btn-primary"><Plus size={20} /> Create New Job</Link>
            </header>

            {/* Stats Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem', marginBottom: '4rem' }}>
                <div className="card" style={{ padding: '2rem' }}>
                    <h3 style={{ fontSize: '1rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '1rem' }}>Total Jobs Completed</h3>
                    <div style={{ fontSize: '3rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>124</div>
                </div>
                <div className="card" style={{ padding: '2rem' }}>
                    <h3 style={{ fontSize: '1rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '1rem' }}>Total Minutes Generated</h3>
                    <div style={{ fontSize: '3rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>542</div>
                </div>
                <div className="card" style={{ padding: '2rem', borderColor: 'var(--accent-purple)', background: 'linear-gradient(135deg, var(--bg-card), rgba(91,33,250,0.1))' }}>
                    <h3 style={{ fontSize: '1rem', color: 'var(--accent-purple)', textTransform: 'uppercase', marginBottom: '1rem', fontWeight: 700 }}>Credits Remaining</h3>
                    <div style={{ fontSize: '3rem', fontWeight: 800, fontFamily: 'var(--font-mono)', display: 'flex', alignItems: 'baseline', gap: '10px' }}>
                        {user?.credits || 10} <span style={{ fontSize: '1rem', color: 'var(--text-muted)', fontWeight: 400 }}>/ 100</span>
                    </div>
                </div>
            </div>

            {/* Recent Jobs Table */}
            <div>
                <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '10px' }}><Clock size={24} /> Recent Dubbing Activity</h2>
                <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                        <thead>
                            <tr style={{ background: 'rgba(255,255,255,0.02)', borderBottom: '1px solid var(--border)' }}>
                                <th style={{ padding: '1rem 1.5rem', color: 'var(--text-muted)', fontWeight: 500 }}>File Name</th>
                                <th style={{ padding: '1rem 1.5rem', color: 'var(--text-muted)', fontWeight: 500 }}>Target Language</th>
                                <th style={{ padding: '1rem 1.5rem', color: 'var(--text-muted)', fontWeight: 500 }}>Status</th>
                                <th style={{ padding: '1rem 1.5rem', color: 'var(--text-muted)', fontWeight: 500 }}>Date</th>
                                <th style={{ padding: '1rem 1.5rem', color: 'var(--text-muted)', fontWeight: 500 }}>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {recentJobs.map(job => (
                                <tr key={job.id} style={{ borderBottom: '1px solid var(--border)' }}>
                                    <td style={{ padding: '1rem 1.5rem', fontWeight: 600 }}>{job.name}</td>
                                    <td style={{ padding: '1rem 1.5rem' }}>{job.lang}</td>
                                    <td style={{ padding: '1rem 1.5rem' }}>
                                        <span style={{
                                            display: 'inline-block', padding: '4px 12px', borderRadius: '50px', fontSize: '0.85rem', fontWeight: 600,
                                            background: job.status === 'Completed' ? 'rgba(34,197,94,0.1)' : 'rgba(0,240,255,0.1)',
                                            color: job.status === 'Completed' ? 'var(--success)' : 'var(--accent-cyan)'
                                        }}>
                                            {job.status}
                                        </span>
                                    </td>
                                    <td style={{ padding: '1rem 1.5rem', color: 'var(--text-muted)' }}>{job.date}</td>
                                    <td style={{ padding: '1rem 1.5rem' }}>
                                        {job.status === 'Completed' ? (
                                            <button className="btn-ghost" style={{ padding: '6px 16px', fontSize: '0.85rem' }}>Download</button>
                                        ) : (
                                            <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Processing...</span>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

        </DashboardLayout>
    );
};

export default DashboardOverview;
export { DashboardLayout };
