import React from 'react';
import { Globe, Mail } from 'lucide-react';

const About = () => {
    return (
        <div className="page-container fadeIn" style={{ paddingTop: 0 }}>
            {/* Full bleed abstract waveform hero */}
            <section style={{ height: '70vh', width: '100vw', marginLeft: 'calc(-50vw + 50%)', position: 'relative', overflow: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#090909' }}>
                <svg width="100%" height="100%" viewBox="0 0 1000 400" preserveAspectRatio="none" style={{ position: 'absolute', top: 0, left: 0, opacity: 0.3 }}>
                    <path d="M0,200 Q150,50 300,200 T600,200 T900,200 T1000,200" fill="none" stroke="var(--accent-purple)" strokeWidth="1" />
                    <path d="M0,200 Q200,350 400,200 T800,200 T1000,200" fill="none" stroke="var(--accent-cyan)" strokeWidth="2" opacity="0.5" />
                    <path d="M0,200 C300,0 400,400 700,200 S900,0 1000,200" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="4" />
                </svg>
                <div style={{ position: 'relative', zIndex: 1, textAlign: 'center' }}>
                    <h1 style={{ fontSize: '5rem', marginBottom: '1rem', background: 'linear-gradient(135deg, #fff, #888)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Our Story</h1>
                    <p style={{ fontSize: '1.5rem', color: 'var(--text-muted)' }}>Breaking language barriers through deep learning.</p>
                </div>
            </section>

            {/* Editorial Mission */}
            <section style={{ maxWidth: '900px', margin: '8rem auto', textAlign: 'center' }}>
                <p style={{ fontFamily: 'var(--font-display)', fontSize: '2.5rem', lineHeight: '1.4', fontWeight: 600 }}>
                    "We believe that a masterpiece recorded in one language should resonate identically across all cultures, without compromising original emotion, pacing, or performance."
                </p>
            </section>

            {/* Founder Section */}
            <section className="card" style={{ maxWidth: '1000px', margin: '0 auto 8rem', display: 'flex', flexWrap: 'wrap', gap: '4rem', padding: '4rem' }}>
                <div style={{ flex: '1', minWidth: '300px' }}>
                    {/* Minimalist DP Placeholder */}
                    <div style={{ width: '100%', aspectRatio: '1/1', background: 'linear-gradient(135deg, var(--bg-primary) 0%, rgba(91,33,250,0.2) 100%)', borderRadius: '32px', border: '1px solid var(--accent-purple)', overflow: 'hidden', position: 'relative' }}>
                        <img src="https://via.placeholder.com/500/0A0A0A/5B21FA?text=SASI+VAIBHAV" alt="Sasi Vaibhav Background Shape" style={{ width: '100%', height: '100%', objectFit: 'cover', opacity: 0.8 }} />
                    </div>
                </div>
                <div style={{ flex: '1.5', minWidth: '350px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                    <h2 style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>Sasi Vaibhav</h2>
                    <div className="text-muted" style={{ fontSize: '1.25rem', marginBottom: '2rem', fontFamily: 'var(--font-mono)' }}>Founder & Super-Admin</div>
                    <p style={{ fontSize: '1.1rem', color: 'var(--text-muted)', marginBottom: '1.5rem', lineHeight: '1.8' }}>
                        As the architectural visionary behind DubSmart AI, Sasi recognized the severe limitations in current translation software—specifically the robotic loss of emotion and timing errors. Through iterative engineering and advanced neural rendering, he built a system that fundamentally preserves the artist's original soul.
                    </p>
                    <p style={{ fontSize: '1.1rem', color: 'var(--text-muted)', marginBottom: '2rem', lineHeight: '1.8' }}>
                        Leading a lean, hyper-focused team of ML researchers, Sasi scale DubSmart AI to serve enterprise clients and independent creators equally, handling millions of API calls effortlessly.
                    </p>
                    <div style={{ display: 'flex', gap: '1rem' }}>
                        <a href="#" className="btn-icon" style={{ background: 'rgba(255,255,255,0.05)', color: 'white', padding: '1rem' }}><Globe size={24} /></a>
                        <a href="#" className="btn-icon" style={{ background: 'rgba(255,255,255,0.05)', color: 'white', padding: '1rem' }}><Mail size={24} /></a>
                    </div>
                </div>
            </section>

            {/* Company Roadmap Timeline */}
            <section style={{ maxWidth: '800px', margin: '0 auto 8rem' }}>
                <h2 style={{ fontSize: '3rem', textAlign: 'center', marginBottom: '4rem' }}>The Journey</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '3rem', position: 'relative' }}>
                    <div style={{ position: 'absolute', top: 0, bottom: 0, left: '20px', width: '2px', background: 'var(--border)' }}></div>

                    <div style={{ display: 'flex', gap: '2rem', position: 'relative' }}>
                        <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--bg-primary)', border: '2px solid var(--accent-purple)', zIndex: 1, flexShrink: 0 }}></div>
                        <div>
                            <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Concept & Alpha</h3>
                            <p className="text-muted">Proved the initial Voice Cloning model on low-latency audio streams.</p>
                        </div>
                    </div>

                    <div style={{ display: 'flex', gap: '2rem', position: 'relative' }}>
                        <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--bg-primary)', border: '2px solid var(--accent-cyan)', zIndex: 1, flexShrink: 0 }}></div>
                        <div>
                            <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>V1 Launch</h3>
                            <p className="text-muted">Released basic API enabling translation of mp4 files via CLI bindings.</p>
                        </div>
                    </div>

                    <div style={{ display: 'flex', gap: '2rem', position: 'relative' }}>
                        <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--bg-primary)', border: '4px solid var(--success)', zIndex: 1, flexShrink: 0, boxShadow: '0 0 20px var(--success)' }}></div>
                        <div>
                            <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>V2 Series-A Overhaul</h3>
                            <p className="text-muted">Complete platform architectural remaster, UI overhaul, pricing implementation, and God-mode admin release.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Origin Badge */}
            <div style={{ textAlign: 'center', paddingBottom: '4rem' }}>
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: '10px', background: 'rgba(255,255,255,0.05)', padding: '1rem 2rem', borderRadius: '999px', fontSize: '1.1rem', fontWeight: 600, border: '1px solid var(--border)' }}>
                    Built with passion in India <span style={{ fontSize: '1.5rem' }}>🇮🇳</span>
                </span>
            </div>

        </div>
    );
};

export default About;
