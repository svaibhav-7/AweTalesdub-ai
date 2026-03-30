import React, { useState } from 'react';

const FloatingInput = ({ label, type = "text", required = false }) => {
    const [focused, setFocused] = useState(false);
    const [val, setVal] = useState('');

    return (
        <div style={{ position: 'relative', marginBottom: '1.5rem' }}>
            <label style={{
                position: 'absolute',
                top: focused || val ? '-10px' : '15px',
                left: '15px',
                background: focused || val ? 'var(--bg-primary)' : 'transparent',
                padding: '0 5px',
                fontSize: focused || val ? '0.75rem' : '1rem',
                color: focused ? 'var(--accent-purple)' : 'var(--text-muted)',
                transition: 'var(--transition)',
                pointerEvents: 'none',
                zIndex: 1
            }}>
                {label} {required && '*'}
            </label>
            <input
                type={type}
                required={required}
                value={val}
                onChange={(e) => setVal(e.target.value)}
                onFocus={() => setFocused(true)}
                onBlur={() => setFocused(false)}
                style={{ width: '100%', background: 'transparent' }}
            />
        </div>
    );
};

const Contact = () => {
    return (
        <div className="page-container fadeIn">
            <header className="page-header center-content" style={{ marginTop: '4rem' }}>
                <h1 style={{ fontSize: '4.5rem' }}>Get in touch</h1>
                <p style={{ fontSize: '1.25rem', color: 'var(--text-muted)' }}>Enterprise scale deployment? Custom LLM tuning? We're here.</p>
            </header>

            <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '4rem', marginBottom: '8rem' }}>

                <div className="card" style={{ padding: '3rem' }}>
                    <h2 style={{ fontSize: '2rem', marginBottom: '2rem' }}>Send us a message</h2>
                    <form onSubmit={(e) => { e.preventDefault(); alert("Form validated successfully."); }}>
                        <FloatingInput label="Full Name" required />
                        <FloatingInput label="Corporate Email" type="email" required />
                        <FloatingInput label="Subject / Purpose" required />
                        <div style={{ position: 'relative', marginBottom: '2rem' }}>
                            <textarea placeholder="Describe your structural needs..." rows="5" required style={{ width: '100%', background: 'transparent' }}></textarea>
                        </div>
                        <button type="submit" className="btn btn-primary w-full large">Submit Inquiry</button>
                    </form>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                    <div className="card" style={{ background: 'linear-gradient(135deg, var(--bg-card), rgba(0,240,255,0.05))', borderColor: 'rgba(0,240,255,0.2)' }}>
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Direct Support Inbox</h3>
                        <div style={{ fontSize: '1.25rem', fontFamily: 'var(--font-mono)', color: 'var(--accent-cyan)', marginBottom: '1rem' }}>support@dubsmart.ai</div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                            <span style={{ width: '10px', height: '10px', background: 'var(--success)', borderRadius: '50%', display: 'inline-block', boxShadow: '0 0 10px var(--success)' }}></span>
                            <span className="text-muted">Average response time: 2 hours</span>
                        </div>
                    </div>

                    {/* CSS Art Map Placeholder */}
                    <div style={{ flex: 1, borderRadius: '24px', border: '1px solid var(--border)', overflow: 'hidden', position: 'relative', background: '#0A0A0A' }}>
                        {/* Pseudo-map styling */}
                        <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', background: 'radial-gradient(circle at 50% 50%, rgba(91,33,250,0.1), transparent 70%)' }}></div>
                        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                            <defs>
                                <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                                    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="1" />
                                </pattern>
                            </defs>
                            <rect width="100%" height="100%" fill="url(#grid)" />
                        </svg>
                        {/* Location Pin */}
                        <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', width: '20px', height: '20px', background: 'var(--accent-purple)', borderRadius: '50%', boxShadow: '0 0 30px var(--accent-purple), 0 0 0 10px rgba(91,33,250,0.2)', animation: 'pulse 2s infinite' }}></div>
                        <style>{`
                @keyframes pulse {
                  0% { box-shadow: 0 0 0 0 rgba(91,33,250, 0.4); }
                  70% { box-shadow: 0 0 0 20px rgba(91,33,250, 0); }
                  100% { box-shadow: 0 0 0 0 rgba(91,33,250, 0); }
                }
              `}</style>
                        <div style={{ position: 'absolute', bottom: '20px', left: '20px', background: 'rgba(0,0,0,0.8)', padding: '10px 15px', borderRadius: '8px', border: '1px solid var(--border)', fontSize: '0.9rem' }}>
                            DubSmart Headquarters
                        </div>
                    </div>
                </div>

            </section>

        </div>
    );
};

export default Contact;
