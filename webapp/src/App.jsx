import React, { useState, useEffect } from 'react';
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [srcLang, setSrcLang] = useState('auto');
  const [tgtLang, setTgtLang] = useState('hi');
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('Ready to dub your audio');
  const [result, setResult] = useState(null);
  const [metadata, setMetadata] = useState(null);

  const handleUpload = (e) => {
    const uploadedFile = e.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      setStatus(`Selected file: ${uploadedFile.name}`);
    }
  };

  const startDubbing = async () => {
    if (!file) return;

    setIsProcessing(true);
    setResult(null);
    setMetadata(null);
    setProgress(5);
    setStatus('Uploading and initializing pipeline...');

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('src_lang', srcLang);
      formData.append('tgt_lang', tgtLang);

      const response = await fetch('http://localhost:8001/dub', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Failed to start dubbing');

      const { job_id } = await response.json();

      // Start polling
      const pollInterval = setInterval(async () => {
        try {
          const statusRes = await fetch(`http://localhost:8001/status/${job_id}`);
          const statusData = await statusRes.json();

          setProgress(statusData.progress || 10);
          setStatus(statusData.message || 'Processing...');
          setMetadata(statusData.metadata || null);

          if (statusData.status === 'completed') {
            clearInterval(pollInterval);
            setIsProcessing(false);
            setResult(`http://localhost:8001/download/${job_id}`);
            setStatus('Dubbing complete!');
          } else if (statusData.status === 'failed') {
            clearInterval(pollInterval);
            setIsProcessing(false);
            setStatus(`Error: ${statusData.message}`);
          }
        } catch (err) {
          console.error("Polling error:", err);
        }
      }, 3000);

    } catch (err) {
      console.error("Upload error:", err);
      setIsProcessing(false);
      setStatus(`Failed to connect: ${err.message}`);
    }
  };

  return (
    <div className="app-container">
      <header>
        <div className="logo">DUBSMART AI</div>
        <div className="status-badge">API Online</div>
      </header>

      <section className="hero">
        <h1>Your Dubbing Partner</h1>
        <p>AI-powered dubbing for your audio content</p>
      </section>

      <main className="main-card">
        <div className="upload-zone" onClick={() => document.getElementById('file-input').click()}>
          <div className="upload-icon">🎙️</div>
          <h3>{file ? file.name : "Drop your audio here or click to browse"}</h3>
          <p>Supports WAV, MP3, and AAC up to 50MB</p>
          <input
            id="file-input"
            type="file"
            hidden
            accept="audio/*"
            onChange={handleUpload}
          />
        </div>

        <div className="controls-grid">
          <div className="control-group">
            <label>Source Language</label>
            <select value={srcLang} onChange={(e) => setSrcLang(e.target.value)}>
              <option value="auto">Auto-detect</option>
              <option value="en">English</option>
              <option value="hi">Hindi</option>
              <option value="te">Telugu</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
              <option value="it">Italian</option>
              <option value="pt">Portuguese</option>
              <option value="pl">Polish</option>
              <option value="tr">Turkish</option>
              <option value="ru">Russian</option>
              <option value="nl">Dutch</option>
              <option value="cs">Czech</option>
              <option value="ar">Arabic</option>
              <option value="zh-cn">Chinese</option>
              <option value="ja">Japanese</option>
              <option value="ko">Korean</option>
            </select>
          </div>
          <div className="control-group">
            <label>Target Language</label>
            <select value={tgtLang} onChange={(e) => setTgtLang(e.target.value)}>
              <option value="hi">Hindi</option>
              <option value="en">English</option>
              <option value="te">Telugu</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
              <option value="it">Italian</option>
              <option value="pt">Portuguese</option>
              <option value="pl">Polish</option>
              <option value="tr">Turkish</option>
              <option value="ru">Russian</option>
              <option value="nl">Dutch</option>
              <option value="cs">Czech</option>
              <option value="ar">Arabic</option>
              <option value="zh-cn">Chinese</option>
              <option value="ja">Japanese</option>
              <option value="ko">Korean</option>
            </select>
          </div>
        </div>

        <button
          className="btn-primary"
          disabled={!file || isProcessing}
          onClick={startDubbing}
        >
          {isProcessing ? "Processing..." : "Start Dubbing Pipeline"}
        </button>

        {(isProcessing || progress > 0) && (
          <div className="progress-container">
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${progress}%` }}></div>
            </div>
            <div className="status-text">{status}</div>
          </div>
        )}

        {metadata && (metadata.detected_gender || metadata.selected_voice) && (
          <div className="metadata-section fadeIn" style={{ marginTop: '1rem', padding: '1rem', background: '#f8f9fa', borderRadius: '8px', border: '1px solid #e9ecef' }}>
            <h4 style={{ margin: '0 0 0.5rem 0', color: '#495057' }}>Processing Details</h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem' }}>
              {metadata.detected_language && (
                <div>
                  <small style={{ color: '#6c757d', display: 'block' }}>Detected Language</small>
                  <strong>{metadata.detected_language.toUpperCase()}</strong>
                </div>
              )}
              {metadata.detected_gender && (
                <div>
                  <small style={{ color: '#6c757d', display: 'block' }}>Detected Gender</small>
                  <strong>{metadata.detected_gender === 'female' ? '♀️ Female' : '♂️ Male'}</strong>
                  <span style={{ marginLeft: '0.5rem', fontSize: '0.7em', background: '#28a745', color: 'white', padding: '2px 6px', borderRadius: '4px' }}>Smart Match</span>
                </div>
              )}
              {metadata.selected_voice && (
                 <div>
                  <small style={{ color: '#6c757d', display: 'block' }}>Selected Voice</small>
                  <code style={{ fontSize: '0.9em' }}>{metadata.selected_voice}</code>
                </div>
              )}
            </div>
          </div>
        )}

        {result && (
          <div className="result-section fadeIn">
            <hr style={{ margin: '2rem 0', opacity: 0.1 }} />
            <h3>Result Ready!</h3>
            <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <audio controls src={result} style={{ flexGrow: 1 }} />
              <a href={result} download className="btn-secondary" style={{ textDecoration: 'none', color: 'white', padding: '0.5rem 1rem', border: '1px solid var(--border-color)', borderRadius: '8px' }}>
                Download
              </a>
            </div>
          </div>
        )}
      </main>

      <footer style={{ textAlign: 'center', opacity: 0.5, fontSize: '0.8rem' }}>
        © 2026 Dubsmart AI. Built for the future of multilingual content.
      </footer>
    </div>
  );
}

export default App;
