import React, { useState } from 'react';
import { Layers, Zap, Globe, Lock, Play, Pause, FastForward, CheckCircle2, XCircle } from 'lucide-react';

const Features = () => {
    const [isPlaying, setIsPlaying] = useState(false);

    return (
        <div className="page-container fadeIn">
            <div className="mesh-glow" style={{ top: '10%', right: '10%' }}></div>

            {/* Header */}
            <header className="page-header center-content" style={{ marginTop: '4rem' }}>
                <h1 style={{ fontSize: '4rem' }}>More than translation.<br />It's <span style={{ color: 'var(--accent-cyan)' }}>Vocal Replication.</span></h1>
                <p style={{ maxWidth: '700px', fontSize: '1.25rem', marginTop: '1.5rem' }}>The only pipeline that matches speaker emotion, background noise, and pacing in over 30 global languages.</p>
            </header>

            {/* Bento Grid Features */}
            <section style={{ marginBottom: '8rem' }}>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gridTemplateRows: 'auto auto', gap: '2rem', minHeight: '600px' }}>
                    {/* Bento 1: Large Span */}
                    <div className="card" style={{ gridColumn: 'span 2', display: 'flex', flexDirection: 'column', padding: '3rem' }}>
                        <h3 style={{ fontSize: '2rem', marginBottom: '1rem' }}>Zero-Shot Voice Cloning System</h3>
                        <p className="text-muted" style={{ fontSize: '1.1rem', marginBottom: '2rem', maxWidth: '400px' }}>Our fundamental ML architecture extracts the vocal print in just 3 seconds of audio without fine-tuning.</p>

                        {/* Interactive Waveform JS Demo Placeholder */}
                        <div style={{ flex: 1, background: '#0A0A0A', borderRadius: '16px', border: '1px solid var(--border)', display: 'flex', flexDirection: 'column', position: 'relative', overflow: 'hidden' }}>
                            <div style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '20px', borderBottom: '1px solid var(--border)', background: 'rgba(255,255,255,0.02)' }}>
                                <button onClick={() => setIsPlaying(!isPlaying)} className="btn-icon" style={{ background: 'var(--accent-purple)', color: 'white' }}>
                                    {isPlaying ? <Pause size={24} /> : <Play size={24} />}
                                </button>
                                <div style={{ fontSize: '0.9rem', color: 'var(--accent-cyan)' }}>Live Neural Rendering...</div>
                            </div>
                            <div style={{ flex: 1, display: 'flex', alignItems: 'center', padding: '0 20px', overflow: 'hidden' }}>
                                {/* Animated Bars Array JS simulation */}
                                <div style={{ display: 'flex', gap: '4px', alignItems: 'center', width: '100%' }}>
                                    {Array.from({ length: 40 }).map((_, i) => (
                                        <div key={i} style={{
                                            flex: 1,
                                            background: isPlaying ? 'var(--accent-cyan)' : 'var(--border)',
                                            height: isPlaying ? `${Math.max(10, Math.random() * 80)}%` : '20%',
                                            borderRadius: '2px',
                                            transition: 'height 0.2s ease'
                                        }}></div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Bento 2: Standard */}
                    <div className="card" style={{ display: 'flex', flexDirection: 'column', padding: '3rem' }}>
                        <Zap size={40} color="var(--accent-cyan)" style={{ marginBottom: '1.5rem' }} />
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Instant Multiplexing</h3>
                        <p className="text-muted">Once generated, audio is automatically synchronized and merged back into your MP4 container.</p>
                    </div>

                    {/* Bento 3: Standard */}
                    <div className="card" style={{ display: 'flex', flexDirection: 'column', padding: '3rem' }}>
                        <Globe size={40} color="var(--accent-purple)" style={{ marginBottom: '1.5rem' }} />
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Cultural Context</h3>
                        <p className="text-muted">Idioms and localized expressions are adapted appropriately by our highly trained LLM transcription layer.</p>
                    </div>

                    {/* Bento 4: Wide Span */}
                    <div className="card" style={{ gridColumn: 'span 2', display: 'flex', padding: '3rem', alignItems: 'center', gap: '3rem', background: 'linear-gradient(to right, var(--bg-card), rgba(91,33,250,0.1))', borderColor: 'rgba(91,33,250,0.3)' }}>
                        <div style={{ flex: 1 }}>
                            <Lock size={40} color="var(--success)" style={{ marginBottom: '1.5rem' }} />
                            <h3 style={{ fontSize: '2rem', marginBottom: '1rem' }}>Enterprise Grade Security</h3>
                            <p className="text-muted" style={{ fontSize: '1.1rem' }}>Your uploaded media is encrypted at rest. We never use your proprietary audio to train any public facing models or algorithms.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Comparison Table */}
            <section style={{ marginBottom: '8rem' }}>
                <h2 style={{ fontSize: '3rem', textAlign: 'center', marginBottom: '4rem' }}>The DubSmart Advantage</h2>
                <div style={{ overflowX: 'auto', background: 'var(--bg-card)', borderRadius: '24px', border: '1px solid var(--border)', padding: '2rem' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                        <thead>
                            <tr style={{ borderBottom: '1px solid var(--border)' }}>
                                <th style={{ padding: '1.5rem', fontSize: '1.1rem', color: 'var(--text-muted)' }}>Feature</th>
                                <th style={{ padding: '1.5rem', fontSize: '1.25rem', color: 'var(--accent-cyan)', background: 'rgba(0,240,255,0.05)', borderRadius: '12px 12px 0 0' }}>DubSmart AI V2</th>
                                <th style={{ padding: '1.5rem', fontSize: '1.1rem' }}>Other AI Tools</th>
                                <th style={{ padding: '1.5rem', fontSize: '1.1rem' }}>Manual Studio</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style={{ borderBottom: '1px solid var(--border)' }}>
                                <td style={{ padding: '1.5rem', fontWeight: 500 }}>Voice Cloning</td>
                                <td style={{ padding: '1.5rem', background: 'rgba(0,240,255,0.02)' }}><CheckCircle2 color="var(--success)" /></td>
                                <td style={{ padding: '1.5rem' }}><CheckCircle2 color="var(--warning)" /> (Requires Fine-Tuning)</td>
                                <td style={{ padding: '1.5rem' }}><XCircle color="var(--error)" /></td>
                            </tr>
                            <tr style={{ borderBottom: '1px solid var(--border)' }}>
                                <td style={{ padding: '1.5rem', fontWeight: 500 }}>Turnaround Time</td>
                                <td style={{ padding: '1.5rem', background: 'rgba(0,240,255,0.02)' }}>~2 Minutes</td>
                                <td style={{ padding: '1.5rem' }}>10-15 Minutes</td>
                                <td style={{ padding: '1.5rem' }}>Days / Weeks</td>
                            </tr>
                            <tr style={{ borderBottom: '1px solid var(--border)' }}>
                                <td style={{ padding: '1.5rem', fontWeight: 500 }}>Emotion Retention</td>
                                <td style={{ padding: '1.5rem', background: 'rgba(0,240,255,0.02)' }}><CheckCircle2 color="var(--success)" /></td>
                                <td style={{ padding: '1.5rem' }}><XCircle color="var(--error)" /> (Robotic tone)</td>
                                <td style={{ padding: '1.5rem' }}><CheckCircle2 color="var(--success)" /></td>
                            </tr>
                            <tr>
                                <td style={{ padding: '1.5rem', fontWeight: 500 }}>Cost per Minute</td>
                                <td style={{ padding: '1.5rem', background: 'rgba(0,240,255,0.02)' }}>$0.15 / min</td>
                                <td style={{ padding: '1.5rem' }}>$0.30 - $1.00 / min</td>
                                <td style={{ padding: '1.5rem' }}>$50+ / min</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            {/* Flowchart Demo */}
            <section style={{ marginBottom: '8rem', textAlign: 'center' }}>
                <h2 style={{ fontSize: '3rem', marginBottom: '4rem' }}>Under the Hood</h2>
                <div style={{ display: 'inline-flex', flexDirection: 'column', gap: '1rem', background: '#0A0A0A', border: '1px solid var(--border)', padding: '4rem', borderRadius: '32px' }}>
                    {/* Simple visual representation of flowchart */}
                    <div className="btn-ghost" style={{ padding: '1rem 3rem', cursor: 'default' }}>Source Audio (English)</div>
                    <div style={{ display: 'flex', justifyContent: 'center' }}><div style={{ width: '2px', height: '40px', background: 'var(--accent-purple)' }}></div></div>
                    <div className="btn-primary" style={{ padding: '1rem 3rem', cursor: 'default', background: 'var(--bg-secondary)', border: '1px solid var(--accent-purple)' }}>Sasi-Waveform Demuxer Model</div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', width: '400px', margin: '0 auto' }}>
                        <div style={{ width: '2px', height: '40px', background: 'var(--accent-purple)', marginLeft: '80px' }}></div>
                        <div style={{ width: '2px', height: '40px', background: 'var(--accent-purple)', marginRight: '80px' }}></div>
                    </div>
                    <div style={{ display: 'flex', gap: '2rem', justifyContent: 'center' }}>
                        <div className="btn-ghost" style={{ padding: '1rem', cursor: 'default' }}>Voice Print Extraction</div>
                        <div className="btn-ghost" style={{ padding: '1rem', cursor: 'default' }}>Text Alignment (Whisper)</div>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', width: '400px', margin: '0 auto' }}>
                        <div style={{ width: '2px', height: '40px', background: 'var(--accent-cyan)', marginLeft: '80px' }}></div>
                        <div style={{ width: '2px', height: '40px', background: 'var(--accent-cyan)', marginRight: '80px' }}></div>
                    </div>
                    <div className="btn-primary" style={{ padding: '1rem 3rem', cursor: 'default', background: 'var(--bg-secondary)', border: '1px solid var(--accent-cyan)' }}>Zero-Shot TTS Synthesizer</div>
                    <div style={{ display: 'flex', justifyContent: 'center' }}><div style={{ width: '2px', height: '40px', background: 'var(--accent-cyan)' }}></div></div>
                    <div className="btn-primary" style={{ padding: '1rem 3rem', cursor: 'default', boxShadow: '0 0 30px rgba(0,240,255,0.3)' }}>Target Output (Spanish)</div>
                </div>
            </section>

        </div>
    );
};

export default Features;
