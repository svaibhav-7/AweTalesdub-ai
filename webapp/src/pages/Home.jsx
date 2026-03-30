import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { PlayCircle, Globe, Video, Headphones, Star, ChevronRight } from 'lucide-react';

const Home = () => {
    const [scrollY, setScrollY] = useState(0);

    useEffect(() => {
        const handleScroll = () => setScrollY(window.scrollY);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <div className="home-wrapper" style={{ position: 'relative' }}>
            {/* Background Mesh */}
            <div className="mesh-glow"></div>

            {/* Hero Section */}
            <section className="hero-section center-content" style={{ minHeight: '90vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', paddingTop: '10vh' }}>
                <div className="page-container fadeIn" style={{ paddingBottom: '0' }}>

                    <div className="badge-pill delay-100" style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', background: 'rgba(91,33,250,0.15)', border: '1px solid rgba(91,33,250,0.4)', padding: '6px 16px', borderRadius: '999px', fontSize: '0.85rem', fontWeight: 600, color: 'var(--accent-cyan)', marginBottom: '2rem' }}>
                        <span style={{ display: 'inline-block', width: '8px', height: '8px', borderRadius: '50%', background: 'var(--accent-cyan)', boxShadow: '0 0 10px var(--accent-cyan)' }}></span>
                        DubSmart AI V2 is Live
                    </div>

                    <h1 className="hero-title delay-200" style={{ fontSize: 'min(5.5rem, 12vw)', maxWidth: '900px', margin: '0 auto 1.5rem', lineHeight: '1.05' }}>
                        Speak every language.<br />
                        <span style={{ background: 'linear-gradient(90deg, #5B21FA 0%, #00F0FF 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                            Keep your voice.
                        </span>
                    </h1>

                    <p className="hero-subtitle delay-200" style={{ fontSize: '1.25rem', color: 'var(--text-muted)', maxWidth: '650px', margin: '0 auto 3rem' }}>
                        The production-grade AI dubbing studio. Instantly translate your video & audio into 30+ languages with emotional continuity and ultra-realistic voice cloning.
                    </p>

                    <div className="hero-cta-group delay-200" style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginBottom: '4rem' }}>
                        <Link to="/signup" className="btn btn-primary large">Start for Free</Link>
                        <button className="btn btn-ghost large"><PlayCircle size={20} /> Watch Demo</button>
                    </div>

                    {/* Animated Studio Console Mockup */}
                    <div className="console-mockup delay-200" style={{
                        position: 'relative',
                        maxWidth: '1000px',
                        margin: '0 auto',
                        transform: `perspective(1000px) rotateX(${Math.max(0, 15 - scrollY * 0.05)}deg) translateY(${scrollY * 0.1}px)`,
                        transition: 'transform 0.1s ease-out',
                        boxShadow: '0 30px 60px rgba(0,0,0,0.6), 0 0 40px rgba(91,33,250,0.2)'
                    }}>
                        <div style={{ background: '#151515', border: '1px solid var(--border)', borderRadius: '16px', padding: '12px', overflow: 'hidden' }}>
                            {/* Fake Mac OS Header */}
                            <div style={{ display: 'flex', gap: '8px', marginBottom: '16px', paddingLeft: '8px' }}>
                                <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#EF4444' }}></div>
                                <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#F59E0B' }}></div>
                                <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#22C55E' }}></div>
                            </div>
                            {/* Studio UI Content */}
                            <div style={{ display: 'flex', gap: '16px', height: '400px' }}>
                                <div style={{ width: '250px', background: '#0A0A0A', borderRadius: '12px', border: '1px solid var(--border)', padding: '16px' }}>
                                    <div style={{ height: '30px', background: 'rgba(255,255,255,0.05)', borderRadius: '6px', marginBottom: '16px' }}></div>
                                    <div style={{ height: '40px', background: 'var(--accent-purple)', opacity: 0.2, borderRadius: '6px', marginBottom: '12px' }}></div>
                                    <div style={{ height: '40px', background: 'rgba(255,255,255,0.05)', borderRadius: '6px', marginBottom: '12px' }}></div>
                                    <div style={{ height: '40px', background: 'rgba(255,255,255,0.05)', borderRadius: '6px', marginBottom: '12px' }}></div>
                                </div>
                                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '16px' }}>
                                    <div style={{ flex: 1, background: '#0A0A0A', borderRadius: '12px', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative', overflow: 'hidden' }}>
                                        {/* SVG Animated Waveform inside Editor */}
                                        <svg width="100%" height="150" viewBox="0 0 800 150" preserveAspectRatio="none">
                                            <path d="M0,75 L50,60 L100,90 L150,40 L200,110 L250,50 L300,100 L350,30 L400,120 L450,40 L500,100 L550,60 L600,90 L650,40 L700,110 L750,50 L800,75" fill="none" stroke="var(--accent-cyan)" strokeWidth="3" opacity="0.8">
                                                <animate attributeName="d" dur="2s" repeatCount="indefinite" values="
                             M0,75 L50,60 L100,90 L150,40 L200,110 L250,50 L300,100 L350,30 L400,120 L450,40 L500,100 L550,60 L600,90 L650,40 L700,110 L750,50 L800,75;
                             M0,75 L50,90 L100,60 L150,110 L200,40 L250,100 L300,50 L350,120 L400,30 L450,100 L500,40 L550,90 L600,60 L650,110 L700,40 L750,90 L800,75;
                             M0,75 L50,60 L100,90 L150,40 L200,110 L250,50 L300,100 L350,30 L400,120 L450,40 L500,100 L550,60 L600,90 L650,40 L700,110 L750,50 L800,75" />
                                            </path>
                                            {/* Playhead line */}
                                            <rect x="300" y="0" width="2" height="150" fill="var(--accent-purple)">
                                                <animate attributeName="x" from="0" to="800" dur="5s" repeatCount="indefinite" />
                                            </rect>
                                        </svg>
                                    </div>
                                    <div style={{ height: '80px', background: '#0A0A0A', borderRadius: '12px', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', padding: '0 20px', gap: '15px' }}>
                                        <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--accent-purple)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}><PlayCircle size={20} color="white" /></div>
                                        <div style={{ flex: 1, height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px' }}>
                                            <div style={{ width: '40%', height: '100%', background: 'var(--accent-cyan)', borderRadius: '3px' }}></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Ticker Section */}
            <section style={{ borderTop: '1px solid var(--border)', borderBottom: '1px solid var(--border)', background: 'rgba(0,0,0,0.5)', padding: '2rem 0', overflow: 'hidden' }}>
                <div style={{ textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '1.5rem', fontWeight: 600 }}>
                    Trusted by top creators and studios globally
                </div>
                <div className="ticker-container" style={{ display: 'flex', whiteSpace: 'nowrap', opacity: 0.6, fontSize: '1.5rem', fontWeight: 800, fontFamily: 'var(--font-display)', color: 'var(--text-muted)' }}>
                    {/* Pure CSS Ticker logic: we use two identical blocks that slide */}
                    <div style={{ display: 'inline-flex', paddingRight: '50px', gap: '80px', animation: 'ticker 20s linear infinite' }}>
                        <span>NETFLIXX</span><span>DISNEY+</span><span>HBO</span><span>CREATOR STUDIO</span><span>YOUTUBE</span><span>PARAMOUNT</span>
                        <span>NETFLIXX</span><span>DISNEY+</span><span>HBO</span><span>CREATOR STUDIO</span><span>YOUTUBE</span><span>PARAMOUNT</span>
                    </div>
                    <style>{`
             @keyframes ticker {
               0% { transform: translateX(0); }
               100% { transform: translateX(-50%); }
             }
           `}</style>
                </div>
            </section>

            {/* Feature Highlight Grid */}
            <section className="page-container" style={{ padding: '8rem 2rem' }}>
                <div style={{ textAlign: 'center', marginBottom: '5rem' }}>
                    <h2 style={{ fontSize: '3rem', marginBottom: '1rem' }}>Engineered for <span style={{ color: 'var(--accent-purple)' }}>Perfection</span></h2>
                    <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem', maxWidth: '600px', margin: '0 auto' }}>Stop settling for robotic translations. Our proprietary AI preserves intonation, pacing, and emotional depth.</p>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '2rem' }}>
                    {/* Card 1 */}
                    <div className="card" style={{ padding: '3rem 2rem' }}>
                        <div style={{ width: '56px', height: '56px', borderRadius: '16px', background: 'rgba(91,33,250,0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '2rem', border: '1px solid rgba(91,33,250,0.2)' }}>
                            <Globe size={28} color="var(--accent-purple)" />
                        </div>
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Global Reach, Local Feel</h3>
                        <p style={{ color: 'var(--text-muted)' }}>Translate into 30+ languages automatically. Our engine adapts cultural nuances so your content resonates everywhere.</p>
                    </div>
                    {/* Card 2 */}
                    <div className="card" style={{ padding: '3rem 2rem', borderColor: 'rgba(0,240,255,0.2)', boxShadow: '0 0 30px rgba(0,240,255,0.05)' }}>
                        <div style={{ width: '56px', height: '56px', borderRadius: '16px', background: 'rgba(0,240,255,0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '2rem', border: '1px solid rgba(0,240,255,0.2)' }}>
                            <Headphones size={28} color="var(--accent-cyan)" />
                        </div>
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Zero-Shot Voice Cloning</h3>
                        <p style={{ color: 'var(--text-muted)' }}>Require only 3 seconds of reference audio. The AI reconstructs your exact vocal timbre in the target language.</p>
                    </div>
                    {/* Card 3 */}
                    <div className="card" style={{ padding: '3rem 2rem' }}>
                        <div style={{ width: '56px', height: '56px', borderRadius: '16px', background: 'rgba(255,255,255,0.05)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '2rem', border: '1px solid var(--border)' }}>
                            <Video size={28} color="var(--text-primary)" />
                        </div>
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Studio Synchronization</h3>
                        <p style={{ color: 'var(--text-muted)' }}>Automatically aligns generated audio with your original video timestamps, making the replacement totally seamless.</p>
                    </div>
                </div>
            </section>

            {/* How it Works - Timeline */}
            <section style={{ background: 'var(--bg-secondary)', borderTop: '1px solid var(--border)', borderBottom: '1px solid var(--border)', padding: '8rem 2rem' }}>
                <div className="page-container" style={{ padding: 0 }}>
                    <h2 style={{ fontSize: '3rem', textAlign: 'center', marginBottom: '5rem' }}>How It Works</h2>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '3rem', position: 'relative' }}>
                        {/* Desktop connecting line */}
                        <div style={{ position: 'absolute', top: '32px', left: '10%', right: '10%', height: '2px', background: 'var(--border)', zIndex: 0, display: window.innerWidth > 900 ? 'block' : 'none' }}></div>

                        <div style={{ position: 'relative', zIndex: 1, textAlign: 'center' }}>
                            <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'var(--bg-primary)', border: '2px solid var(--accent-purple)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem', fontWeight: 700, margin: '0 auto 2rem' }}>1</div>
                            <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Upload Media</h3>
                            <p style={{ color: 'var(--text-muted)' }}>Drag and drop your video or audio file. We support all major industry formats up to 4K resolution.</p>
                        </div>

                        <div style={{ position: 'relative', zIndex: 1, textAlign: 'center' }}>
                            <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'var(--bg-primary)', border: '2px solid var(--accent-cyan)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem', fontWeight: 700, margin: '0 auto 2rem' }}>2</div>
                            <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>AI Processing</h3>
                            <p style={{ color: 'var(--text-muted)' }}>Our proprietary engine analyzes the speech, translates it, and synthesizes the exact voice in the target language.</p>
                        </div>

                        <div style={{ position: 'relative', zIndex: 1, textAlign: 'center' }}>
                            <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'var(--bg-primary)', border: '2px solid var(--success)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem', fontWeight: 700, margin: '0 auto 2rem' }}>3</div>
                            <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Export & Publish</h3>
                            <p style={{ color: 'var(--text-muted)' }}>Review in the Studio Dashboard. Export synchronized audio splits or a freshly multiplexed video file instantly.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Social Proof / Testimonials */}
            <section className="page-container" style={{ padding: '8rem 2rem' }}>
                <h2 style={{ fontSize: '3rem', textAlign: 'center', marginBottom: '1rem' }}>Loved by Creators</h2>
                <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem', textAlign: 'center', marginBottom: '5rem' }}>Join thousands of professionals scaling their audience.</p>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
                    <div className="card">
                        <div style={{ display: 'flex', gap: '4px', color: 'var(--warning)', marginBottom: '1rem' }}>
                            <Star fill="currentColor" size={16} /><Star fill="currentColor" size={16} /><Star fill="currentColor" size={16} /><Star fill="currentColor" size={16} /><Star fill="currentColor" size={16} />
                        </div>
                        <p style={{ fontSize: '1.1rem', fontStyle: 'italic', marginBottom: '2rem' }}>"DubSmart completely changed our content strategy. We hit 1M subscribers in Spain using their 1-click dubbing, and nobody noticed it was AI."</p>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                            <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: '#333' }}></div>
                            <div>
                                <h4 style={{ fontWeight: 700 }}>Marques D.</h4>
                                <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Tech Reviewer, 5M Subs</div>
                            </div>
                        </div>
                    </div>

                    <div className="card">
                        <div style={{ display: 'flex', gap: '4px', color: 'var(--warning)', marginBottom: '1rem' }}>
                            <Star fill="currentColor" size={16} /><Star fill="currentColor" size={16} /><Star fill="currentColor" size={16} /><Star fill="currentColor" size={16} /><Star fill="currentColor" size={16} />
                        </div>
                        <p style={{ fontSize: '1.1rem', fontStyle: 'italic', marginBottom: '2rem' }}>"The API integration is flawless. We route all our corporate training videos through DubSmart Enterprise and it saves us $50k monthly."</p>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                            <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: '#333' }}></div>
                            <div>
                                <h4 style={{ fontWeight: 700 }}>Sarah J.</h4>
                                <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Director of Ops, FinTech Inc.</div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Final CTA Banner */}
            <section style={{ padding: '0 2rem 8rem' }}>
                <div style={{ maxWidth: '1000px', margin: '0 auto', background: 'linear-gradient(135deg, var(--bg-card) 0%, rgba(91,33,250,0.1) 100%)', border: '1px solid var(--accent-purple)', borderRadius: '24px', padding: '5rem 3rem', textAlign: 'center', position: 'relative', overflow: 'hidden' }}>
                    <div style={{ position: 'absolute', top: '-50%', left: '-20%', width: '100%', height: '200%', background: 'radial-gradient(circle, rgba(0,240,255,0.1) 0%, transparent 60%)', zIndex: 0, pointerEvents: 'none' }}></div>
                    <div style={{ position: 'relative', zIndex: 1 }}>
                        <h2 style={{ fontSize: '3rem', marginBottom: '1rem' }}>Ready to go global?</h2>
                        <p style={{ color: 'var(--text-muted)', fontSize: '1.25rem', marginBottom: '3rem', maxWidth: '500px', margin: '0 auto 3rem' }}>Get 10 free credits immediately upon signup. No credit card required.</p>
                        <Link to="/signup" className="btn btn-primary large" style={{ animation: 'pulse 2s infinite' }}>
                            Create Free Account <ChevronRight size={20} />
                        </Link>
                    </div>
                </div>
                <style>{`
          @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(91,33,250, 0.7); }
            70% { box-shadow: 0 0 0 20px rgba(91,33,250, 0); }
            100% { box-shadow: 0 0 0 0 rgba(91,33,250, 0); }
          }
        `}</style>
            </section>
        </div>
    );
};

export default Home;
