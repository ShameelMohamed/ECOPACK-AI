import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Leaf, IndianRupee, Package, Activity, Loader2, Trophy, Medal, Award, BarChart3, Download, Sparkles, Clock, Code } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import html2pdf from 'html2pdf.js';
import './App.css';

function App() {
  const [loadingApp, setLoadingApp] = useState(true);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isTouchDevice, setIsTouchDevice] = useState(false);
  
  const [formData, setFormData] = useState({
    category_name: 'Healthcare',
    weight_capacity_kg: 800,
    tensile_strength_mpa: 400,
    biodegradability_score: 60,
    recyclability_percent: 80
  });

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [timestamp, setTimestamp] = useState(null);

  const industries = [
    "Healthcare", "Automotive", "Cosmetics", "Electronics", 
    "Food & Beverage", "Construction", "E-commerce", "Agriculture"
  ];

  useEffect(() => {
    if (window.matchMedia("(pointer: coarse)").matches) {
      setIsTouchDevice(true);
    }
    setTimeout(() => setLoadingApp(false), 2000);
    
    const updateMousePosition = (e) => {
      if (!isTouchDevice) setMousePosition({ x: e.clientX, y: e.clientY });
    };
    
    window.addEventListener('mousemove', updateMousePosition);
    return () => window.removeEventListener('mousemove', updateMousePosition);
  }, [isTouchDevice]);

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResults(null);
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/recommend', {
        ...formData,
        weight_capacity_kg: parseFloat(formData.weight_capacity_kg),
        tensile_strength_mpa: parseFloat(formData.tensile_strength_mpa),
        biodegradability_score: parseFloat(formData.biodegradability_score),
        recyclability_percent: parseFloat(formData.recyclability_percent)
      });
      setTimeout(() => {
        setResults(response.data.recommendations);
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
        setTimestamp(response.data.timestamp || timeString);
        setLoading(false);
      }, 800);
    } catch (error) {
      console.error("Error fetching prediction:", error);
      alert("Backend offline! Make sure Flask is running.");
      setLoading(false);
    }
  };

  const getRankIcon = (index) => {
    if (index === 0) return <Trophy className="rank-icon gold glow" size={36} />;
    if (index === 1) return <Medal className="rank-icon silver" size={30} />;
    return <Award className="rank-icon bronze" size={24} />;
  };

  const handlePrint = () => {
    const element = document.getElementById('pdf-content');
    const opt = {
      margin: [0.2, 0.2, 0.2, 0.2], // Top, Left, Bottom, Right margins
      filename: `EcoPackAI_Report_${new Date().getTime()}.pdf`,
      image: { type: 'jpeg', quality: 1 },
      html2canvas: { scale: 2, useCORS: true, backgroundColor: '#030712', windowWidth: 1200 }, // Forces desktop width for PDF
      jsPDF: { unit: 'in', format: 'a4', orientation: 'portrait' }
    };
    html2pdf().set(opt).from(element).save();
  };

  return (
    <div className="app-wrapper">
      {!isTouchDevice && (
        <motion.div 
          className="custom-cursor"
          animate={{ x: mousePosition.x - 150, y: mousePosition.y - 150 }}
          transition={{ type: 'spring', stiffness: 150, damping: 15, mass: 0.5 }}
        />
      )}

      <AnimatePresence>
        {loadingApp ? (
          <motion.div className="boot-screen" exit={{ opacity: 0, filter: "blur(10px)" }} transition={{ duration: 0.8 }}>
            <motion.div initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ duration: 1, repeat: Infinity, repeatType: "reverse" }}>
              <Leaf size={80} className="boot-logo" />
            </motion.div>
            <motion.h1 initial={{ letterSpacing: "0px" }} animate={{ letterSpacing: "8px" }} transition={{ duration: 2 }}>ECOPACK.AI</motion.h1>
            <div className="loading-bar"><motion.div className="loading-progress" initial={{ width: "0%" }} animate={{ width: "100%" }} transition={{ duration: 2 }} /></div>
          </motion.div>
        ) : (
          <div className="app-container">
            <motion.header initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}>
              <div className="logo-group">
                <Leaf className="main-logo" size={36} />
                <h1>EcoPack<span className="accent">AI</span></h1>
              </div>
              <p className="subtitle">Nexus Supply Chain Engine</p>
            </motion.header>

            {/* The PDF target container */}
            <div id="pdf-content">
              <div className="master-grid">
                
                {/* LEFT COLUMN: Form */}
                <motion.div className="sidebar" initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.6, delay: 0.2 }}>
                  <div className="bento-box form-box">
                    <div className="box-header">
                      <Package className="icon-glow" />
                      <h2>Constraint Matrix</h2>
                    </div>
                    <form onSubmit={handleSubmit} data-html2canvas-ignore="true">
                      <div className="input-grid">
                        <div className="input-wrap span-2">
                          <label>Industry Category</label>
                          <div className="select-wrapper">
                            <select name="category_name" value={formData.category_name} onChange={handleChange} required>
                              {industries.map((ind, i) => <option key={i} value={ind}>{ind}</option>)}
                            </select>
                          </div>
                        </div>
                        <div className="input-wrap">
                          <label>Capacity (kg)</label>
                          <input type="number" name="weight_capacity_kg" value={formData.weight_capacity_kg} onChange={handleChange} required />
                        </div>
                        <div className="input-wrap">
                          <label>Strength (MPa)</label>
                          <input type="number" name="tensile_strength_mpa" value={formData.tensile_strength_mpa} onChange={handleChange} required />
                        </div>
                        <div className="input-wrap">
                          <label>Bio-Score (1-100)</label>
                          <input type="number" name="biodegradability_score" value={formData.biodegradability_score} onChange={handleChange} required />
                        </div>
                        <div className="input-wrap">
                          <label>Recycle %</label>
                          <input type="number" name="recyclability_percent" value={formData.recyclability_percent} onChange={handleChange} required />
                        </div>
                      </div>
                      
                      <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.95 }} type="submit" className="cyber-button" disabled={loading}>
                        {loading ? <Loader2 className="spinner" /> : <><Sparkles size={18}/> Initialize Core</>}
                      </motion.button>
                    </form>
                  </div>
                </motion.div>

                {/* RIGHT COLUMN: Results */}
                <div className="main-content">
                  <AnimatePresence mode="wait">
                    {!results && !loading && (
                      <motion.div key="empty" className="bento-box empty-box" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                        <Activity size={50} className="radar-ping" />
                        <p>System standing by. Input telemetry to begin simulation.</p>
                      </motion.div>
                    )}

                    {loading && (
                      <motion.div key="loading" className="bento-box loading-box" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                        <div className="cyber-spinner"></div>
                        <p>Calculating Multidimensional Impact...</p>
                      </motion.div>
                    )}

                    {results && (
                      <motion.div key="results" className="dashboard-layout" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                        
                        <div className="mobile-timestamp" data-html2canvas-ignore="true">
                           <span className="timestamp-badge"><Clock size={14}/> Run at {timestamp}</span>
                        </div>
                        
                        {/* THE 3 CARDS GRID */}
                        <div className="cards-grid">
                          {results.map((item, index) => (
                            <motion.div 
                              key={index}
                              className={`bento-box rank-card ${index === 0 ? 'hero-card' : 'sub-card'}`}
                              initial={{ opacity: 0, y: 30 }}
                              animate={{ opacity: 1, y: 0 }}
                              transition={{ duration: 0.5, delay: index * 0.1 }}
                              whileHover={!isTouchDevice ? { scale: 1.02, translateY: -5 } : {}} 
                            >
                              <div className="card-top">
                                {getRankIcon(index)}
                                <span className="rank-text">Match 0{index + 1}</span>
                              </div>
                              <h3>{item.material}</h3>
                              <div className="data-strip">
                                <div className="data-point">
                                  <IndianRupee size={16} className="cyan-text" />
                                  <span>₹{item.cost_inr.toLocaleString()}</span>
                                </div>
                                <div className="data-point">
                                  <Activity size={16} className="green-text" />
                                  <span>{item.co2_kg} kg</span>
                                </div>
                              </div>
                            </motion.div>
                          ))}
                        </div>

                        {/* TELEMETRY CHART */}
                        <motion.div className="bento-box chart-box" initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.4 }}>
                          <div className="box-header flex-between">
                            <div className="left">
                              <BarChart3 className="cyan-text"/> 
                              <h2>Telemetry Chart</h2>
                            </div>
                            <div className="right-actions" data-html2canvas-ignore="true">
                              <span className="timestamp-badge desktop-only"><Clock size={14}/> {timestamp}</span>
                              <motion.button whileHover={{ scale: 1.1 }} onClick={handlePrint} className="icon-btn">
                                <Download size={20} />
                              </motion.button>
                            </div>
                          </div>
                          <div className="chart-container">
                            <ResponsiveContainer width="100%" height={260}>
                              <BarChart data={results} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                                <XAxis dataKey="material" stroke="#64748b" tick={{fill: '#94a3b8', fontSize: 11}} />
                                <YAxis yAxisId="left" stroke="#00f0ff" tick={{fontSize: 11}} />
                                <YAxis yAxisId="right" orientation="right" stroke="#00ffaa" tick={{fontSize: 11}} />
                                <Tooltip cursor={{fill: 'rgba(255,255,255,0.05)'}} contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }} />
                                {/* isAnimationActive={false} ensures the PDF captures the fully drawn bars */}
                                <Bar yAxisId="left" dataKey="cost_inr" fill="url(#cyanGrad)" radius={[4, 4, 0, 0]} isAnimationActive={false} />
                                <Bar yAxisId="right" dataKey="co2_kg" fill="url(#greenGrad)" radius={[4, 4, 0, 0]} isAnimationActive={false} />
                                <defs>
                                  <linearGradient id="cyanGrad" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="0%" stopColor="#00f0ff" />
                                    <stop offset="100%" stopColor="#0057ff" />
                                  </linearGradient>
                                  <linearGradient id="greenGrad" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="0%" stopColor="#00ffaa" />
                                    <stop offset="100%" stopColor="#008055" />
                                  </linearGradient>
                                </defs>
                              </BarChart>
                            </ResponsiveContainer>
                          </div>
                        </motion.div>

                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </div>
            </div>

            {/* CUSTOM FOOTER */}
            <footer className="app-footer">
              <p>
                <Code size={14} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '5px' }} />
                Developed by <strong>Shameel Mohamed</strong> |{' '}
                <a href="mailto:shameelmohamed2005@gmail.com" target="_blank" rel="noreferrer">shameelmohamed2005@gmail.com</a> |{' '}
                <a href="https://github.com/ShameelMohamed" target="_blank" rel="noreferrer">GitHub</a>
              </p>
              <p className="license-text">
                Licensed under the <a href="https://opensource.org/license/MIT" target="_blank" rel="noreferrer">MIT License</a>
              </p>
            </footer>

          </div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;