import React, { useState } from 'react';
import { Shield, Users, Database, Zap, ArrowRight, AlertTriangle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const AdminDashboard = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [overrideTarget, setOverrideTarget] = useState('');
    const [overrideValue, setOverrideValue] = useState('');

    // Fallback check if rendering on frontend, though Router guards it as well
    if (user?.email !== 'sasi@dubsmart.ai') {
        return (
            <div className="center-content page-container" style={{ padding: '8rem 2rem' }}>
                <AlertTriangle size={64} color="var(--error)" style={{ margin: '0 auto 2rem' }} />
                <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>Unauthorized Access</h1>
                <p className="text-muted">You require God-Mode Super Admin privileges to view this area.</p>
            </div>
        );
    }

    return (
        <div style={{ minHeight: '100vh', background: 'var(--bg-primary)' }}>
            {/* Admin Navbar */}
            <nav style={{ background: '#000', borderBottom: '1px solid var(--error)', padding: '1rem 3rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                    <div style={{ width: '40px', height: '40px', background: 'var(--error)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <Shield color="white" size={20} />
                    </div>
                    <div style={{ fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: '1.25rem', letterSpacing: '0.05em' }}>
                        <span style={{ color: 'var(--error)' }}>GOD-MODE</span> <span className="text-muted">/ OMNISCIENCE PANEL</span>
                    </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Welcome, Sasi Vaibhav.</span>
                    <button onClick={() => navigate('/dashboard')} className="btn-ghost" style={{ padding: '8px 16px', fontSize: '0.85rem' }}>Exit God-Mode</button>
                </div>
            </nav>

            <main style={{ padding: '4rem 3rem', maxWidth: '1400px', margin: '0 auto' }}>

                {/* Metric Cards */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.5rem', marginBottom: '4rem' }}>
                    <div className="card" style={{ borderColor: 'var(--border)' }}>
                        <h3 className="text-muted" style={{ textTransform: 'uppercase', fontSize: '0.85rem', marginBottom: '1rem' }}>Total Platform Users</h3>
                        <div style={{ fontSize: '2.5rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>14,295</div>
                    </div>
                    <div className="card" style={{ borderColor: 'var(--border)' }}>
                        <h3 className="text-muted" style={{ textTransform: 'uppercase', fontSize: '0.85rem', marginBottom: '1rem' }}>SaaS Monthly Recurring (MRR)</h3>
                        <div style={{ fontSize: '2.5rem', fontWeight: 800, fontFamily: 'var(--font-mono)', color: 'var(--success)' }}>$142,500</div>
                    </div>
                    <div className="card" style={{ borderColor: 'var(--border)' }}>
                        <h3 className="text-muted" style={{ textTransform: 'uppercase', fontSize: '0.85rem', marginBottom: '1rem' }}>Total Dubbing Jobs</h3>
                        <div style={{ fontSize: '2.5rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>853,101</div>
                    </div>
                    <div className="card" style={{ borderColor: 'var(--error)', background: 'linear-gradient(135deg, var(--bg-card), rgba(239, 68, 68, 0.1))' }}>
                        <h3 className="text-muted" style={{ textTransform: 'uppercase', fontSize: '0.85rem', marginBottom: '1rem' }}>System Load Avg.</h3>
                        <div style={{ fontSize: '2.5rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>42%</div>
                    </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>

                    {/* User Management Table */}
                    <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
                        <div style={{ padding: '1.5rem 2rem', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <h2 style={{ fontSize: '1.25rem', display: 'flex', alignItems: 'center', gap: '10px' }}><Users size={20} color="var(--accent-cyan)" /> Live User Directory</h2>
                            <input type="text" placeholder="Search by email..." style={{ padding: '0.5rem 1rem', background: '#0A0A0A', border: '1px solid var(--border)', borderRadius: '8px', color: 'white' }} />
                        </div>
                        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                            <thead>
                                <tr style={{ background: 'rgba(255,255,255,0.02)', borderBottom: '1px solid var(--border)' }}>
                                    <th style={{ padding: '1rem 2rem', color: 'var(--text-muted)', fontWeight: 500, fontSize: '0.85rem' }}>USER / EMAIL</th>
                                    <th style={{ padding: '1rem 2rem', color: 'var(--text-muted)', fontWeight: 500, fontSize: '0.85rem' }}>PLAN</th>
                                    <th style={{ padding: '1rem 2rem', color: 'var(--text-muted)', fontWeight: 500, fontSize: '0.85rem' }}>CREDIT BALANCE</th>
                                    <th style={{ padding: '1rem 2rem' }}></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr style={{ borderBottom: '1px solid var(--border)' }}>
                                    <td style={{ padding: '1rem 2rem' }}>
                                        <div style={{ fontWeight: 600 }}>Test Account 1</div>
                                        <div className="text-muted" style={{ fontSize: '0.85rem' }}>test1@example.com</div>
                                    </td>
                                    <td style={{ padding: '1rem 2rem' }}><span style={{ color: 'var(--accent-purple)' }}>Pro ($9.99)</span></td>
                                    <td style={{ padding: '1rem 2rem', fontFamily: 'var(--font-mono)' }}>85 / 100</td>
                                    <td style={{ padding: '1rem 2rem', textAlign: 'right' }}><button className="btn-ghost" style={{ padding: '6px 12px', fontSize: '0.75rem' }}>Manage Data</button></td>
                                </tr>
                                <tr style={{ borderBottom: '1px solid var(--border)' }}>
                                    <td style={{ padding: '1rem 2rem' }}>
                                        <div style={{ fontWeight: 600 }}>Agency LLC</div>
                                        <div className="text-muted" style={{ fontSize: '0.85rem' }}>admin@agency.co</div>
                                    </td>
                                    <td style={{ padding: '1rem 2rem' }}><span style={{ color: 'var(--accent-cyan)' }}>Enterprise ($29.99)</span></td>
                                    <td style={{ padding: '1rem 2rem', fontFamily: 'var(--font-mono)' }}>5 / 500</td>
                                    <td style={{ padding: '1rem 2rem', textAlign: 'right' }}><button className="btn-ghost" style={{ padding: '6px 12px', fontSize: '0.75rem' }}>Manage Data</button></td>
                                </tr>
                                <tr style={{ borderBottom: '1px solid var(--border)' }}>
                                    <td style={{ padding: '1rem 2rem' }}>
                                        <div style={{ fontWeight: 600 }}>Free Signer</div>
                                        <div className="text-muted" style={{ fontSize: '0.85rem' }}>free@gmail.com</div>
                                    </td>
                                    <td style={{ padding: '1rem 2rem' }}><span style={{ color: 'var(--text-muted)' }}>Free</span></td>
                                    <td style={{ padding: '1rem 2rem', fontFamily: 'var(--font-mono)' }}>0 / 10</td>
                                    <td style={{ padding: '1rem 2rem', textAlign: 'right' }}><button className="btn-ghost" style={{ padding: '6px 12px', fontSize: '0.75rem' }}>Manage Data</button></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>

                        {/* Credit Injector Override */}
                        <div className="card" style={{ borderColor: 'var(--error)' }}>
                            <h3 style={{ fontSize: '1.25rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '10px' }}>
                                <Zap size={20} color="var(--error)" /> Credit Injector
                            </h3>
                            <p className="text-muted" style={{ fontSize: '0.85rem', marginBottom: '1.5rem' }}>Force override credit balance for any user immediately without Stripe verification.</p>
                            <div className="form-group">
                                <label>Target User Email</label>
                                <input type="text" placeholder="user@domain.com" value={overrideTarget} onChange={(e) => setOverrideTarget(e.target.value)} />
                            </div>
                            <div className="form-group">
                                <label>New Absolute Credit Value</label>
                                <input type="number" placeholder="500" value={overrideValue} onChange={(e) => setOverrideValue(e.target.value)} />
                            </div>
                            <button className="btn w-full large" style={{ background: 'var(--error)', color: 'white', border: 'none' }} onClick={() => alert(`Injected ${overrideValue} credits to ${overrideTarget}`)}>
                                EXECUTE OVERRIDE
                            </button>
                        </div>

                        {/* System Announcer */}
                        <div className="card">
                            <h3 style={{ fontSize: '1.25rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '10px' }}>
                                <Database size={20} color="var(--accent-purple)" /> Global Broadcaster
                            </h3>
                            <div className="form-group">
                                <label>Announcement Headline</label>
                                <input type="text" placeholder="e.g., Scheduled Maintenance" />
                            </div>
                            <div className="form-group">
                                <label>Message Body</label>
                                <textarea rows="3" placeholder="Inform entire userbase..."></textarea>
                            </div>
                            <button className="btn btn-primary w-full">Broadcast Note <ArrowRight size={16} /></button>
                        </div>

                    </div>
                </div>
            </main>
        </div>
    );
};

export default AdminDashboard;
