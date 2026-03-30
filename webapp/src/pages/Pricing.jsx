import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Check, Plus, Minus } from 'lucide-react';

const FAQItem = ({ question, answer }) => {
    const [isOpen, setIsOpen] = useState(false);
    return (
        <div style={{ borderBottom: '1px solid var(--border)', padding: '1.5rem 0' }}>
            <button onClick={() => setIsOpen(!isOpen)} style={{ width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'none', border: 'none', color: 'var(--text-primary)', fontSize: '1.25rem', fontFamily: 'var(--font-display)', cursor: 'pointer', textAlign: 'left' }}>
                {question}
                {isOpen ? <Minus size={20} color="var(--accent-cyan)" /> : <Plus size={20} color="var(--accent-purple)" />}
            </button>
            {isOpen && (
                <p style={{ marginTop: '1rem', color: 'var(--text-muted)', lineHeight: '1.6' }} className="fadeIn">{answer}</p>
            )}
        </div>
    );
};

const Pricing = () => {
    const [annual, setAnnual] = useState(false);

    return (
        <div className="page-container fadeIn">
            <div className="mesh-glow" style={{ left: '50%', transform: 'translateX(-50%)', top: '0' }}></div>

            <header className="page-header center-content" style={{ marginTop: '4rem' }}>
                <h1 style={{ fontSize: '4.5rem' }}>Simple, transparent pricing</h1>
                <p style={{ maxWidth: '800px', margin: '1.5rem auto 3rem', fontSize: '1.25rem' }}>1 Credit = 1 Dubbing Job. No hidden fees. Credits reset monthly.</p>

                {/* Toggle */}
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: '1rem', background: 'rgba(255,255,255,0.05)', padding: '0.5rem', borderRadius: '999px', border: '1px solid var(--border)' }}>
                    <button onClick={() => setAnnual(false)} style={{ background: annual ? 'transparent' : 'var(--bg-card)', color: annual ? 'var(--text-muted)' : 'white', border: annual ? 'none' : '1px solid var(--border)', padding: '0.75rem 1.5rem', borderRadius: '999px', cursor: 'pointer', transition: 'var(--transition)', fontWeight: 600 }}>Monthly</button>
                    <button onClick={() => setAnnual(true)} style={{ background: annual ? 'var(--bg-card)' : 'transparent', color: annual ? 'white' : 'var(--text-muted)', border: annual ? '1px solid var(--border)' : 'none', padding: '0.75rem 1.5rem', borderRadius: '999px', cursor: 'pointer', transition: 'var(--transition)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        Annually <span style={{ background: 'rgba(34,197,94,0.1)', color: 'var(--success)', fontSize: '0.75rem', padding: '2px 8px', borderRadius: '10px' }}>Save 20%</span>
                    </button>
                </div>
            </header>

            {/* Pricing Cards */}
            <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '2rem', marginBottom: '8rem', alignItems: 'start' }}>

                {/* Free Plan */}
                <div className="card" style={{ padding: '3rem', borderTop: '4px solid var(--text-muted)' }}>
                    <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Free</h3>
                    <p className="text-muted" style={{ marginBottom: '2rem' }}>Perfect to test the platform.</p>
                    <div style={{ fontSize: '3rem', fontWeight: 800, marginBottom: '2rem', fontFamily: 'var(--font-mono)' }}>$0</div>
                    <Link to="/signup" className="btn btn-ghost w-full block center-content" style={{ marginBottom: '2rem' }}>Sign Up</Link>
                    <ul style={{ display: 'flex', flexDirection: 'column', gap: '1rem', color: 'var(--text-muted)' }}>
                        <li style={{ display: 'flex', gap: '0.75rem' }}><Check size={20} color="var(--success)" /> 10 starting credits</li>
                        <li style={{ display: 'flex', gap: '0.75rem' }}><Check size={20} color="var(--success)" /> Max 3 usage attempts</li>
                        <li style={{ display: 'flex', gap: '0.75rem' }}><Check size={20} color="var(--success)" /> Standard Quality (Watermarked)</li>
                    </ul>
                </div>

                {/* Pro Plan */}
                <div className="card" style={{ padding: '3rem', border: '1px solid var(--accent-purple)', boxShadow: '0 0 40px rgba(91,33,250,0.15)', transform: 'scale(1.05)', position: 'relative' }}>
                    <div style={{ position: 'absolute', top: 0, left: '50%', transform: 'translate(-50%, -50%)', background: 'var(--primary-gradient)', padding: '0.5rem 1.5rem', borderRadius: '20px', fontSize: '0.9rem', fontWeight: 700 }}>Most Popular</div>
                    <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Pro</h3>
                    <p className="text-muted" style={{ marginBottom: '2rem' }}>For active content creators.</p>
                    <div style={{ fontSize: '3.5rem', fontWeight: 800, marginBottom: '2rem', fontFamily: 'var(--font-mono)', display: 'flex', alignItems: 'baseline' }}>
                        {annual ? '$7.99' : '$9.99'} <span style={{ fontSize: '1rem', color: 'var(--text-muted)', fontWeight: 400 }}>/mo</span>
                    </div>
                    <Link to="/signup" className="btn btn-primary w-full block center-content" style={{ marginBottom: '2rem' }}>Get Started</Link>
                    <ul style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        <li style={{ display: 'flex', gap: '0.75rem' }}><Check size={20} color="var(--accent-cyan)" /> <strong>100 credits / month</strong></li>
                        <li style={{ display: 'flex', gap: '0.75rem' }}><Check size={20} color="var(--accent-cyan)" /> Unlimited dubbing attempts</li>
                        <li style={{ display: 'flex', gap: '0.75rem' }}><Check size={20} color="var(--accent-cyan)" /> No watermark</li>
                        <li style={{ display: 'flex', gap: '0.75rem' }}><Check size={20} color="var(--accent-cyan)" /> Priority processing queue</li>
                        <li style={{ display: 'flex', gap: '0.75rem' }}><Check size={20} color="var(--accent-cyan)" /> Download MP3 & WAV</li>
                    </ul>
                </div>

                {/* Enterprise Plan */}
                <div className="card" style={{ padding: '3rem', borderTop: '4px solid var(--accent-cyan)' }}>
                    <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Enterprise</h3>
                    <p className="text-muted" style={{ marginBottom: '2rem' }}>For agencies & high volume.</p>
                    <div style={{ fontSize: '3rem', fontWeight: 800, marginBottom: '2rem', fontFamily: 'var(--font-mono)', display: 'flex', alignItems: 'baseline' }}>
                        {annual ? '$23.99' : '$29.99'} <span style={{ fontSize: '1rem', color: 'var(--text-muted)', fontWeight: 400 }}>/mo</span>
                    </div>
                    <Link to="/signup" className="btn btn-ghost w-full block center-content" style={{ marginBottom: '2rem' }}>Subscribe</Link>
                    <ul style={{ display: 'flex', flexDirection: 'column', gap: '1rem', color: 'var(--text-muted)' }}>
                        <li style={{ display: 'flex', gap: '0.75rem' }}><Check size={20} color="var(--success)" /> <strong>500 credits / month</strong></li>
                        <li style={{ display: 'flex', gap: '0.75rem' }}><Check size={20} color="var(--success)" /> REST API Access</li>
                        <li style={{ display: 'flex', gap: '0.75rem' }}><Check size={20} color="var(--success)" /> Dedicated Priority Support</li>
                        <li style={{ display: 'flex', gap: '0.75rem' }}><Check size={20} color="var(--success)" /> White-label video generation</li>
                        <li style={{ display: 'flex', gap: '0.75rem' }}><Check size={20} color="var(--success)" /> Team Seats (Up to 5)</li>
                    </ul>
                </div>
            </section>

            {/* Credit Gauge Explainer */}
            <section style={{ background: '#0A0A0A', padding: '4rem', borderRadius: '24px', border: '1px solid var(--border)', marginBottom: '8rem', display: 'flex', alignItems: 'center', gap: '4rem', flexWrap: 'wrap' }}>
                <div style={{ flex: 1, minWidth: '300px' }}>
                    <h2 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>How does billing work?</h2>
                    <p className="text-muted" style={{ fontSize: '1.2rem', marginBottom: '2rem' }}>DubSmart AI operates on a simple, transparent credit system.</p>
                    <ul style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><div style={{ width: '8px', height: '8px', background: 'var(--accent-purple)', borderRadius: '50%' }}></div> 1 Dubbing Generation = 1 Credit Consumed</li>
                        <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><div style={{ width: '8px', height: '8px', background: 'var(--warning)', borderRadius: '50%' }}></div> Unused credits do not roll over</li>
                        <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><div style={{ width: '8px', height: '8px', background: 'var(--success)', borderRadius: '50%' }}></div> Instant topups available automatically</li>
                    </ul>
                </div>
                {/* Simple SVG Circular Gauge mockup */}
                <div style={{ width: '250px', height: '250px', position: 'relative' }}>
                    <svg viewBox="0 0 100 100" style={{ width: '100%', height: '100%', transform: 'rotate(-90deg)' }}>
                        <circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="10" />
                        <circle cx="50" cy="50" r="40" fill="none" stroke="url(#gv)" strokeWidth="10" strokeDasharray="251" strokeDashoffset="50" strokeLinecap="round" style={{ transition: 'stroke-dashoffset 2s ease' }} />
                        <defs>
                            <linearGradient id="gv" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stopColor="var(--accent-purple)" />
                                <stop offset="100%" stopColor="var(--accent-cyan)" />
                            </linearGradient>
                        </defs>
                    </svg>
                    <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                        <span style={{ fontSize: '2.5rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>80</span>
                        <span className="text-muted" style={{ fontSize: '0.85rem', textTransform: 'uppercase' }}>Credits Left</span>
                    </div>
                </div>
            </section>

            {/* FAQ Accordion */}
            <section style={{ maxWidth: '800px', margin: '0 auto 8rem' }}>
                <h2 style={{ fontSize: '3rem', textAlign: 'center', marginBottom: '4rem' }}>Frequently Asked Questions</h2>
                <FAQItem question="Can I cancel my subscription at any time?" answer="Yes, you can cancel your subscription from your dashboard at any point. You will retain access to your plan features until the end of the billing cycle." />
                <FAQItem question="What happens if I run out of credits mid-month?" answer="You will receive a notification when you are at 20% remaining credits. You can purchase top-up packs directly from your dashboard inside the Studio interface." />
                <FAQItem question="Is the Free Tier really free forever?" answer="Yes! The free tier provides 10 starting credits to try out the software. However, usage is limited and the outputs are watermarked to prevent commercial exploitation." />
                <FAQItem question="Can I manually override my plan settings?" answer="Only the system administrator Sasi Vaibhav can manually bypass credit boundaries through the internal Super Admin portal." />
                <FAQItem question="What payment methods do you accept?" answer="We currently process all payments securely through Razorpay and Stripe. This supports all major credit/debit cards, UPI (in India), and internationally recognized wallets." />
            </section>
        </div>
    );
};

export default Pricing;
