import React, { useState } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogIn, Eye, EyeOff, Mail } from 'lucide-react';

const Login = () => {
    const [searchParams] = useSearchParams();
    const isSignup = searchParams.get('signup') === 'true';
    const { login } = useAuth();
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [focusedInput, setFocusedInput] = useState(null);

    const handleSubmit = (e) => {
        e.preventDefault();
        login(email || 'sasi@dubsmart.ai');
        navigate('/dashboard');
    };

    return (
        <div className="page-container flex-center fadeIn" style={{ minHeight: 'calc(100vh - 80px)', paddingTop: '100px', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>

            <div className="mesh-glow" style={{ top: '50%', left: '50%', transform: 'translate(-50%, -50%)', opacity: 0.5 }}></div>

            <div className="card" style={{ width: '100%', maxWidth: '450px', padding: '3rem', background: 'rgba(15,15,15,0.7)', backdropFilter: 'var(--blur-strong)', zIndex: 10, borderColor: 'rgba(255,255,255,0.1)' }}>
                <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
                    <div style={{ width: '50px', height: '50px', background: 'linear-gradient(135deg, var(--accent-purple), var(--accent-cyan))', borderRadius: '12px', margin: '0 auto 1.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <LogIn size={24} color="white" />
                    </div>
                    <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem', fontFamily: 'var(--font-display)' }}>
                        {isSignup ? 'Create Account' : 'Welcome Back'}
                    </h2>
                    <p style={{ color: 'var(--text-muted)' }}>
                        {isSignup ? 'Start dubbing with 10 free credits instantly.' : 'Log in to your Studio Dashboard.'}
                    </p>
                </div>

                {/* Google Auth Mock */}
                <button className="btn btn-ghost w-full" style={{ marginBottom: '1.5rem', position: 'relative' }}>
                    <svg style={{ position: 'absolute', left: '1.5rem', width: '20px', height: '20px' }} viewBox="0 0 24 24">
                        <path fill="#EA4335" d="M5.26498 9.76453A8.959 8.959 0 0112 3c2.69 0 4.923.999 6.706 2.645l-2.43 2.378C15.225 7.027 13.784 6.5 12 6.5c-4.226 0-7.794 3.033-8.815 7.152L.789 11.832c1.084-3.21 3.86-5.83 7.09-6.307z" />
                        <path fill="#34A853" d="M16.04 18.013c-1.09.703-2.474 1.078-4.04 1.078-3.078 0-5.845-1.574-7.44-4.076l-2.39 1.847C4.192 19.98 7.785 22 12 22c2.81 0 5.176-.902 6.892-2.443l-2.852-1.544z" />
                        <path fill="#4A90E2" d="M23.5 12.28c0-.79-.07-1.54-.19-2.28h-11.3v4.51h6.47c-.29 1.48-1.14 2.73-2.4 3.58l2.85 1.55c1.66-1.53 2.57-3.83 2.57-6.36z" />
                        <path fill="#FBBC05" d="M3.185 14.86A8.96 8.96 0 012.5 12c0-.99.172-1.94.485-2.83L.605 7.323a11.96 11.96 0 000 9.354l2.58-1.817z" />
                    </svg>
                    Continue with Google
                </button>

                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1.5rem' }}>
                    <div style={{ flex: 1, height: '1px', background: 'var(--border)' }}></div>
                    OR CONTINUE WITH EMAIL
                    <div style={{ flex: 1, height: '1px', background: 'var(--border)' }}></div>
                </div>

                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

                    {/* Email Input */}
                    <div style={{ position: 'relative' }}>
                        <label style={{ position: 'absolute', top: focusedInput === 'email' || email ? '-10px' : '12px', left: '15px', background: focusedInput === 'email' || email ? 'var(--bg-primary)' : 'transparent', padding: '0 5px', fontSize: focusedInput === 'email' || email ? '0.75rem' : '1rem', color: focusedInput === 'email' ? 'var(--accent-purple)' : 'var(--text-muted)', transition: 'var(--transition)', pointerEvents: 'none', zIndex: 1 }}>
                            Email Address
                        </label>
                        <input
                            type="email"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            onFocus={() => setFocusedInput('email')}
                            onBlur={() => setFocusedInput(null)}
                            style={{ paddingRight: '40px' }}
                        />
                        <Mail style={{ position: 'absolute', right: '15px', top: '15px', color: 'var(--text-muted)' }} size={20} />
                    </div>

                    {/* Password Input */}
                    <div style={{ position: 'relative' }}>
                        <label style={{ position: 'absolute', top: focusedInput === 'password' || password ? '-10px' : '12px', left: '15px', background: focusedInput === 'password' || password ? 'var(--bg-primary)' : 'transparent', padding: '0 5px', fontSize: focusedInput === 'password' || password ? '0.75rem' : '1rem', color: focusedInput === 'password' ? 'var(--accent-purple)' : 'var(--text-muted)', transition: 'var(--transition)', pointerEvents: 'none', zIndex: 1 }}>
                            Password
                        </label>
                        <input
                            type={showPassword ? "text" : "password"}
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            onFocus={() => setFocusedInput('password')}
                            onBlur={() => setFocusedInput(null)}
                            style={{ paddingRight: '40px' }}
                        />
                        <button type="button" onClick={() => setShowPassword(!showPassword)} style={{ position: 'absolute', right: '15px', top: '15px', background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
                            {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                        </button>
                    </div>

                    {!isSignup && (
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', color: 'var(--text-muted)' }}>
                                <input type="checkbox" style={{ width: '16px', height: '16px', accentColor: 'var(--accent-purple)' }} />
                                Remember me
                            </label>
                            <a href="#" style={{ color: 'var(--accent-purple)' }}>Forgot Password?</a>
                        </div>
                    )}

                    <button type="submit" className="btn btn-primary w-full large" style={{ marginTop: '0.5rem' }}>
                        {isSignup ? 'Create Account' : 'Log In'}
                    </button>
                </form>

                <div style={{ textAlign: 'center', marginTop: '2rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                    {isSignup ? (
                        <>Already have an account? <Link to="/login" style={{ color: 'var(--accent-cyan)' }}>Sign In</Link></>
                    ) : (
                        <>New to DubSmart? <Link to="/login?signup=true" style={{ color: 'var(--accent-cyan)' }}>Sign Up</Link></>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Login;
