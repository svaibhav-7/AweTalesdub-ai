import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, Globe, Mail, Link as LinkIcon, ArrowRight } from 'lucide-react';

const Footer = () => {
  return (
    <footer style={{ 
      background: '#040404', 
      borderTop: '1px solid var(--border)', 
      paddingTop: '6rem', 
      paddingBottom: '2rem',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Subtle background glow */}
      <div style={{ position: 'absolute', top: 0, left: '50%', transform: 'translate(-50%, -50%)', width: '80%', height: '300px', background: 'radial-gradient(circle, rgba(91,33,250,0.1) 0%, transparent 60%)', filter: 'blur(60px)', pointerEvents: 'none' }}></div>

      <div className="page-container" style={{ paddingTop: 0, paddingBottom: 0 }}>
        
        {/* Top Section: Newsletter & Branding */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '4rem', marginBottom: '6rem', alignItems: 'start' }}>
          
          <div style={{ flex: 1 }}>
            <Link to="/" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: '1.75rem', letterSpacing: '-0.04em', marginBottom: '1.5rem' }}>
              <Activity className="logo-icon" size={32} color="var(--accent-purple)" />
              <span style={{ background: 'linear-gradient(90deg, #fff 0%, var(--text-muted) 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                DubSmart
              </span> AI
            </Link>
            <p style={{ color: 'var(--text-muted)', fontSize: '1.05rem', lineHeight: '1.7', maxWidth: '400px', marginBottom: '2rem' }}>
              The enterprise standard for zero-shot neural voice cloning and emotional video transcription. Built for creators crossing international borders.
            </p>
            <div style={{ display: 'flex', gap: '1rem' }}>
               <a href="#" className="btn-icon" style={{ background: 'rgba(255,255,255,0.05)', color: 'var(--text-muted)', padding: '0.75rem' }}><Globe size={20} /></a>
               <a href="#" className="btn-icon" style={{ background: 'rgba(255,255,255,0.05)', color: 'var(--text-muted)', padding: '0.75rem' }}><LinkIcon size={20} /></a>
               <a href="#" className="btn-icon" style={{ background: 'rgba(255,255,255,0.05)', color: 'var(--text-muted)', padding: '0.75rem' }}><Mail size={20} /></a>
            </div>
          </div>

          <div className="card" style={{ background: 'rgba(255,255,255,0.02)', padding: '2.5rem', border: '1px solid rgba(255,255,255,0.05)' }}>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>Subscribe to our newsletter</h3>
            <p className="text-muted" style={{ marginBottom: '1.5rem', fontSize: '0.95rem' }}>Get the latest deep learning insights.</p>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
               <input type="email" placeholder="Email address" style={{ flex: 1, padding: '0.85rem 1rem', background: '#090909', border: '1px solid var(--border)', borderRadius: '8px', color: 'white' }} />
               <button className="btn btn-primary" style={{ padding: '0.85rem 1.5rem' }}>Subscribe</button>
            </div>
          </div>

        </div>

        {/* Middle Section: Directory Links */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '3rem', borderTop: '1px solid var(--border)', paddingTop: '4rem', paddingBottom: '4rem' }}>
           
           <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <h4 style={{ color: 'white', fontWeight: 600, marginBottom: '0.5rem', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Platform</h4>
              <Link to="/features" className="text-muted" style={{ fontSize: '0.95rem', transition: 'color 0.2s', ':hover': { color: 'white' } }}>Features</Link>
              <Link to="/pricing" className="text-muted" style={{ fontSize: '0.95rem' }}>Pricing</Link>
              <Link to="/studio" className="text-muted" style={{ fontSize: '0.95rem' }}>Dubbing Studio</Link>
              <a href="#" className="text-muted" style={{ fontSize: '0.95rem', display: 'flex', alignItems: 'center', gap: '5px' }}>API Access <ArrowRight size={14} color="var(--accent-cyan)" /></a>
           </div>

           <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <h4 style={{ color: 'white', fontWeight: 600, marginBottom: '0.5rem', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Company</h4>
              <Link to="/about" className="text-muted" style={{ fontSize: '0.95rem' }}>Our Story</Link>
              <a href="#" className="text-muted" style={{ fontSize: '0.95rem' }}>Careers</a>
              <a href="#" className="text-muted" style={{ fontSize: '0.95rem' }}>Press Kit</a>
              <Link to="/contact" className="text-muted" style={{ fontSize: '0.95rem' }}>Contact Sales</Link>
           </div>

           <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <h4 style={{ color: 'white', fontWeight: 600, marginBottom: '0.5rem', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Resources</h4>
              <a href="#" className="text-muted" style={{ fontSize: '0.95rem' }}>Documentation</a>
              <a href="#" className="text-muted" style={{ fontSize: '0.95rem' }}>Help Center</a>
              <a href="#" className="text-muted" style={{ fontSize: '0.95rem' }}>Community Discord</a>
              <a href="#" className="text-muted" style={{ fontSize: '0.95rem' }}>System Status</a>
           </div>

           <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <h4 style={{ color: 'white', fontWeight: 600, marginBottom: '0.5rem', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Legal</h4>
              <a href="#" className="text-muted" style={{ fontSize: '0.95rem' }}>Privacy Policy</a>
              <a href="#" className="text-muted" style={{ fontSize: '0.95rem' }}>Terms of Service</a>
              <a href="#" className="text-muted" style={{ fontSize: '0.95rem' }}>Cookie Usage</a>
              <a href="#" className="text-muted" style={{ fontSize: '0.95rem' }}>Security Trust Center</a>
           </div>

        </div>

        {/* Bottom Bar */}
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '2rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
           <p>© {new Date().getFullYear()} DubSmart AI, Inc. All rights reserved.</p>
           <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ width: '8px', height: '8px', background: 'var(--success)', borderRadius: '50%', boxShadow: '0 0 10px var(--success)' }}></span>
              All systems operational
           </div>
        </div>

      </div>
    </footer>
  );
};

export default Footer;
