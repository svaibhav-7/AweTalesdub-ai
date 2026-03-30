import React, { useState } from 'react';
import { DashboardLayout } from './Dashboard';
import { UploadCloud, Settings2, Globe, Sparkles, CheckCircle2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Studio = () => {
    const { user } = useAuth();
    const [file, setFile] = useState(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [success, setSuccess] = useState(false);

    const handleProcess = () => {
        setIsProcessing(true);
        // Mock the backend API delay
        setTimeout(() => {
            setIsProcessing(false);
            setSuccess(true);
        }, 4000);
    };

    return (
        <DashboardLayout activeTab="studio">
            <header style={{ marginBottom: '3rem' }}>
                <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Studio Pipeline</h1>
                <p style={{ color: 'var(--text-muted)' }}>Upload an asset, configure styles, and let the proprietary neural engine do the rest.</p>
            </header>

            {success ? (
                <div className="card center-content fadeIn" style={{ padding: '6rem 2rem', background: 'linear-gradient(135deg, var(--bg-card), rgba(34,197,94,0.1))', borderColor: 'var(--success)', maxWidth: '800px', margin: '0 auto' }}>
                    <CheckCircle2 color="var(--success)" size={64} style={{ margin: '0 auto 2rem' }} />
                    <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>Rendering Complete!</h2>
                    <p style={{ color: 'var(--text-muted)', marginBottom: '3rem', fontSize: '1.1rem' }}>Your video has been successfully synchronized and muxed with the new target language track.</p>
                    <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
                        <button className="btn btn-primary large">Download MP4 File</button>
                        <button className="btn btn-ghost large" onClick={() => setSuccess(false)}>Start New Job</button>
                    </div>
                </div>
            ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'minmax(400px, 2fr) 1fr', gap: '2rem' }}>

                    {/* Main Upload Zone */}
                    <div className="card" style={{ padding: '3rem', display: 'flex', flexDirection: 'column' }}>
                        <h3 style={{ fontSize: '1.25rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '10px' }}>
                            <UploadCloud size={20} color="var(--accent-cyan)" /> Asset Uploader
                        </h3>

                        <div style={{
                            flex: 1,
                            border: '2px dashed var(--border)',
                            borderRadius: '16px',
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            justifyContent: 'center',
                            background: 'rgba(255,255,255,0.02)',
                            cursor: 'pointer',
                            transition: 'var(--transition)',
                            padding: '4rem 2rem',
                            textAlign: 'center'
                        }}
                            onClick={() => document.getElementById('fileUpload').click()}
                            onMouseEnter={(e) => e.currentTarget.style.borderColor = 'var(--accent-purple)'}
                            onMouseLeave={(e) => e.currentTarget.style.borderColor = 'var(--border)'}>

                            <input type="file" id="fileUpload" style={{ display: 'none' }} onChange={(e) => setFile(e.target.files[0])} />

                            {file ? (
                                <>
                                    <div style={{ width: '60px', height: '60px', background: 'var(--accent-purple)', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.5rem' }}>
                                        <CheckCircle2 color="white" size={32} />
                                    </div>
                                    <h4 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>{file.name}</h4>
                                    <p className="text-muted">{(file.size / (1024 * 1024)).toFixed(2)} MB • Ready to analyze</p>
                                </>
                            ) : (
                                <>
                                    <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'rgba(91,33,250,0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem' }}>
                                        <UploadCloud color="var(--accent-purple)" size={32} />
                                    </div>
                                    <h4 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Drag & Drop or Browse</h4>
                                    <p className="text-muted">Supports MP4, MOV, WAV, MP3 max 2GB.</p>
                                </>
                            )}
                        </div>
                    </div>

                    {/* Configuration Panel */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>

                        <div className="card" style={{ padding: '2rem' }}>
                            <h3 style={{ fontSize: '1.25rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '10px' }}>
                                <Globe size={20} color="var(--accent-cyan)" /> Target Parameters
                            </h3>

                            <div className="form-group">
                                <label>Target Language</label>
                                <select>
                                    <option>Spanish (ES)</option>
                                    <option>French (FR)</option>
                                    <option>German (DE)</option>
                                    <option>Japanese (JP)</option>
                                    <option>Hindi (IN)</option>
                                </select>
                            </div>

                            <div className="form-group" style={{ marginBottom: 0 }}>
                                <label>Emotion Retention</label>
                                <select>
                                    <option>High (Cloned Strict)</option>
                                    <option>Medium (Balanced)</option>
                                    <option>Low (Flat/Narrator)</option>
                                </select>
                            </div>
                        </div>

                        <div className="card" style={{ padding: '2rem', background: 'linear-gradient(135deg, var(--bg-card), rgba(91,33,250,0.1))', borderColor: 'var(--accent-purple)' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem' }}>
                                <span className="text-muted">Cost</span>
                                <span style={{ fontWeight: 800 }}>1 Credit</span>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem' }}>
                                <span className="text-muted">Remaining Balance</span>
                                <span style={{ fontWeight: 800 }}>{user?.credits || 10} Credits</span>
                            </div>

                            <button
                                onClick={handleProcess}
                                disabled={!file || isProcessing}
                                className="btn btn-primary w-full large"
                                style={{
                                    opacity: (!file || isProcessing) ? 0.5 : 1,
                                    cursor: (!file || isProcessing) ? 'not-allowed' : 'pointer'
                                }}>
                                {isProcessing ? (
                                    <>Processing AI Engine...</>
                                ) : (
                                    <><Sparkles size={20} /> Generate</>
                                )}
                            </button>

                            {isProcessing && (
                                <div style={{ width: '100%', height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px', marginTop: '1rem', overflow: 'hidden' }}>
                                    <div style={{ width: '100%', height: '100%', background: 'var(--accent-cyan)', animation: 'indeterminate 1.5s infinite linear' }}></div>
                                    <style>{`
                           @keyframes indeterminate {
                             0% { transform: translateX(-100%); }
                             100% { transform: translateX(100%); }
                           }
                         `}</style>
                                </div>
                            )}
                        </div>

                    </div>

                </div>
            )}
        </DashboardLayout>
    );
};

export default Studio;
