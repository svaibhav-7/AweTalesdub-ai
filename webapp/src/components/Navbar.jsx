import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Activity } from 'lucide-react';

const Navbar = () => {
    const { user } = useAuth();
    const location = useLocation();
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const isDashboardOrAdmin = location.pathname.includes('/dashboard') || location.pathname.includes('/studio') || location.pathname.includes('/admin');
    if (isDashboardOrAdmin) return null; // These areas use their own structural sidebars

    return (
        <nav className="navbar" style={{
            background: scrolled ? 'rgba(9, 9, 9, 0.85)' : 'transparent',
            borderBottomColor: scrolled ? 'var(--border)' : 'transparent'
        }}>
            <div className="navbar-container">
                {/* Animated Wordmark */}
                <Link to="/" className="navbar-logo">
                    <Activity className="logo-icon" size={28} />
                    <span>DubSmart</span> AI
                </Link>

                {/* Links */}
                <div className="navbar-links" style={{ display: 'flex', gap: '2.5rem' }}>
                    <Link to="/" className={location.pathname === '/' ? 'active' : ''}>Home</Link>
                    <Link to="/features" className={location.pathname === '/features' ? 'active' : ''}>Features</Link>
                    <Link to="/pricing" className={location.pathname === '/pricing' ? 'active' : ''}>Pricing</Link>
                    <Link to="/about" className={location.pathname === '/about' ? 'active' : ''}>About</Link>
                    <Link to="/contact" className={location.pathname === '/contact' ? 'active' : ''}>Contact</Link>
                </div>

                {/* CTA Actions */}
                <div className="navbar-actions">
                    {user ? (
                        <Link to="/dashboard" className="btn btn-primary">Dashboard</Link>
                    ) : (
                        <>
                            <Link to="/login" className="btn btn-ghost">Log in</Link>
                            <Link to="/login?signup=true" className="btn btn-primary">Try for Free</Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
