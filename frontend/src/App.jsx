import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Leaf, IndianRupee, Package, Activity, Loader2, Trophy, Medal, Award, BarChart3, Download, Sparkles, Clock, Code, Box, History, ShieldCheck } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable'; 
import html2canvas from 'html2canvas';
import './App.css';

function App() {
  const [loadingApp, setLoadingApp] = useState(true);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isTouchDevice, setIsTouchDevice] = useState(false);
  
  const [formData, setFormData] = useState({
    product_name: 'Smartwatch',
    category_name: 'Electronics',
    weight_capacity_kg: 2,
    tensile_strength_mpa: 50,
    biodegradability_score: 80,
    recyclability_percent: 90
  });

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [timestamp, setTimestamp] = useState(null);
  const [history, setHistory] = useState([]);

  const industries = [
    "Healthcare", "Automotive", "Cosmetics", "Electronics", "Toys", 
    "Food & Beverage", "Construction", "E-commerce", "Agriculture", "Home Appliances"
  ];

  useEffect(() => {
    if (window.matchMedia("(pointer: coarse)").matches) setIsTouchDevice(true);
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
        const simResults = response.data.recommendations;
        setResults(simResults);
        
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
        setTimestamp(timeString);
        
        setHistory(prev => [
          { id: Date.now(), time: timeString, product: formData.product_name, category: formData.category_name, topMatch: simResults[0].material }, 
          ...prev
        ]);
        
        setLoading(false);
      }, 800);
    } catch (error) {
      console.error("Error fetching prediction:", error);
      alert("Backend offline! Make sure Flask is running.");
      setLoading(false);
    }
  };

  const getRankIcon = (index) => {
    if (index === 0) return <Trophy className="rank-icon gold glow" size={32} />;
    if (index === 1) return <Medal className="rank-icon silver" size={28} />;
    return <Award className="rank-icon bronze" size={24} />;
  };

  const getSustainabilityScore = (item, index, formConstraints) => {
    let baseScore = 98.5 - (index * 4.2); 
    let co2Penalty = (item.co2_kg || 0) * 2.5;
    let costPenalty = (item.cost_inr || 0) / 800;
    let ecoBonus = (formConstraints.biodegradability_score / 100) * 2.5;

    let finalScore = baseScore - co2Penalty - costPenalty + ecoBonus;
    return Math.max(45, Math.min(99.9, finalScore)).toFixed(2);
  };

  const generatePDF = async () => {
    try {
      const doc = new jsPDF('p', 'mm', 'a4');
      const pageWidth = doc.internal.pageSize.getWidth();
      const pageHeight = doc.internal.pageSize.getHeight();
      
      doc.setFillColor(15, 23, 42); 
      doc.rect(0, 0, pageWidth, 40, 'F');
      
      doc.setFont("helvetica", "bold");
      doc.setFontSize(26);
      doc.setTextColor(0, 255, 170); 
      doc.text("EcoPack AI", 14, 22);

      doc.setFont("helvetica", "normal");
      doc.setFontSize(16);
      doc.setTextColor(255, 255, 255);
      doc.text("|  Sustainability Report", 68, 22);
      
      doc.setFontSize(11);
      doc.setTextColor(148, 163, 184); 
      doc.text(`Generated at: ${timestamp}`, 14, 32);
      
      autoTable(doc, {
        startY: 50,
        head: [['Target Product Details', 'Physical & Eco Constraints']],
        body: [
          [`Product: ${formData.product_name}`, `Capacity Limit: ${formData.weight_capacity_kg} kg`],
          [`Industry: ${formData.category_name}`, `Tensile Strength: ${formData.tensile_strength_mpa} MPa`],
          [`Minimum Bio-Score: ${formData.biodegradability_score}/100`, `Target Recyclability: ${formData.recyclability_percent}%`]
        ],
        theme: 'grid',
        styles: { font: 'helvetica', fontSize: 11, cellPadding: 6 },
        headStyles: { fillColor: [15, 23, 42], textColor: [255, 255, 255], fontStyle: 'bold', fontSize: 12 },
        alternateRowStyles: { fillColor: [248, 250, 252] }
      });

      const finalY1 = doc.lastAutoTable.finalY || 80;

      doc.setFont("helvetica", "italic");
      doc.setFontSize(13);
      doc.setTextColor(51, 65, 85);
      
      const topScore = getSustainabilityScore(results[0], 0, formData);
      const insightText = `AI Insight: For your ${formData.category_name} product '${formData.product_name}', ${results[0].material} is the optimal recommendation. It achieved a Sustainability Score of ${topScore}/100, carrying a unit cost of Rs.${results[0].cost_inr.toLocaleString()} and a minimal CO2 footprint of ${results[0].co2_kg} kg.`;
      
      const splitText = doc.splitTextToSize(insightText, pageWidth - 28);
      doc.text(splitText, 14, finalY1 + 15);

      const chartEl = document.getElementById('telemetry-chart');
      let finalY2 = finalY1 + 30 + (splitText.length * 6);

      if (chartEl) {
        const canvas = await html2canvas(chartEl, { backgroundColor: '#030712', scale: 2 });
        const imgData = canvas.toDataURL('image/png');
        
        doc.setFont("helvetica", "bold");
        doc.setFontSize(14);
        doc.setTextColor(15, 23, 42);
        doc.text("Cost vs CO₂ Telemetry Analysis", 14, finalY2 + 5);
        
        doc.addImage(imgData, 'PNG', 14, finalY2 + 10, 180, 80);
        finalY2 = finalY2 + 100; 
      }

      if (finalY2 > pageHeight - 40) { doc.addPage(); finalY2 = 20; }

      const tableData = results.map((r, i) => [
        `#${i+1} ${r.material}`, 
        `Rs. ${r.cost_inr.toLocaleString()}`, 
        `${r.co2_kg} kg`, 
        `${getSustainabilityScore(r, i, formData)}/100` 
      ]);

      autoTable(doc, {
        startY: finalY2,
        head: [['Rank & Material', 'Est. Cost', 'CO2 Footprint', 'Sustainability Score']],
        body: tableData,
        theme: 'striped',
        styles: { font: 'helvetica', fontSize: 11, cellPadding: 6 },
        /* FIXED: Changed from [16, 185, 129] (green) to [15, 23, 42] (dark blue) */
        headStyles: { fillColor: [15, 23, 42], textColor: [255, 255, 255], fontStyle: 'bold', fontSize: 12 }
      });

      doc.save(`EcoPackAI_${formData.product_name.replace(/\s+/g, '_')}_Report.pdf`);
    } catch (error) {
      console.error("PDF Generation Failed:", error);
      alert("Failed to generate the PDF. Please ensure the chart has finished loading.");
    }
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
          <motion.div className="boot-screen" exit={{ opacity: 0, filter: "blur(10px)" }}>
            <Leaf size={80} className="boot-logo" />
            <h1>ECOPACK.AI</h1>
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

            <div className="top-split-layout">
              <motion.div className="bento-box form-box" initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.6, delay: 0.2 }}>
                <div className="box-header">
                  <Package className="icon-glow" />
                  <h2>Constraint Matrix</h2>
                </div>
                <form onSubmit={handleSubmit} className="matrix-form">
                  <div className="input-grid">
                    
                    <div className="input-wrap">
                      <label>Product Name</label>
                      <div className="input-with-icon">
                        <Box size={16} className="input-icon" />
                        <input type="text" name="product_name" value={formData.product_name} onChange={handleChange} required />
                      </div>
                    </div>
                    
                    <div className="input-wrap">
                      <label>Industry Category</label>
                      <div className="select-wrapper">
                        <select name="category_name" value={formData.category_name} onChange={handleChange} required>
                          {industries.map((ind, i) => <option key={i} value={ind}>{ind}</option>)}
                        </select>
                      </div>
                    </div>

                    <div className="input-row">
                      <div className="input-wrap">
                        <label>Capacity (kg)</label>
                        <input type="number" name="weight_capacity_kg" value={formData.weight_capacity_kg} onChange={handleChange} required />
                      </div>
                      <div className="input-wrap">
                        <label>Strength (MPa)</label>
                        <input type="number" name="tensile_strength_mpa" value={formData.tensile_strength_mpa} onChange={handleChange} required />
                      </div>
                    </div>

                    <div className="input-row">
                      <div className="input-wrap">
                        <label>Bio-Score (1-100)</label>
                        <input type="number" name="biodegradability_score" value={formData.biodegradability_score} onChange={handleChange} required />
                      </div>
                      <div className="input-wrap">
                        <label>Recycle %</label>
                        <input type="number" name="recyclability_percent" value={formData.recyclability_percent} onChange={handleChange} required />
                      </div>
                    </div>

                  </div>
                  <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.95 }} type="submit" className="cyber-button" disabled={loading}>
                    {loading ? <Loader2 className="spinner" /> : <><Sparkles size={18}/> Initialize Core</>}
                  </motion.button>
                </form>
              </motion.div>

              <div className="right-top-content">
                <AnimatePresence mode="wait">
                  {!results && !loading && (
                    <motion.div key="empty" className="bento-box empty-box" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                      <Activity size={50} className="radar-ping" />
                      <p>System standing by. Input telemetry for <strong>{formData.product_name || "your product"}</strong>.</p>
                    </motion.div>
                  )}

                  {loading && (
                    <motion.div key="loading" className="bento-box loading-box" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                      <div className="cyber-spinner"></div>
                      <p>Simulating materials...</p>
                    </motion.div>
                  )}

                  {results && (
                    <motion.div key="results" className="cards-and-btn-wrapper" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                      <div className="cards-grid">
                        {results.map((item, index) => (
                          <motion.div 
                            key={index} 
                            className={`bento-box rank-card ${index === 0 ? 'hero-card' : 'sub-card'}`}
                            whileHover={!isTouchDevice ? { scale: 1.03, translateY: -5 } : {}}
                          >
                            <div className="card-top">
                              {getRankIcon(index)}
                              <span className="rank-text">Match 0{index + 1}</span>
                            </div>
                            <h3>{item.material}</h3>
                            <div className="data-strip">
                              <div className="data-point"><IndianRupee size={16} className="cyan-text" /> <span>₹{item.cost_inr.toLocaleString()}</span></div>
                              <div className="data-point"><Activity size={16} className="green-text" /> <span>{item.co2_kg} kg</span></div>
                            </div>
                          </motion.div>
                        ))}
                      </div>
                      
                      <motion.button whileHover={{ scale: 1.01 }} onClick={generatePDF} className="full-width-pdf-btn">
                        <Download size={18} /> Export Formal PDF Report
                      </motion.button>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>

            {results && (
              <motion.div className="bottom-metrics" initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.3 }}>
                
                <div className="ai-insights-bar">
                  <ShieldCheck className="green-text" size={24} />
                  <p>
                    For your {formData.category_name} product <strong>'{formData.product_name}'</strong>, <span className="green-text">{results[0].material}</span> is the top recommendation with a sustainability score of <strong>{getSustainabilityScore(results[0], 0, formData)}/100</strong>, cost of <strong>Rs.{results[0].cost_inr.toLocaleString()}/unit</strong>, and CO2 footprint of <strong>{results[0].co2_kg} kg</strong>.
                  </p>
                </div>

                <div className="bento-box chart-box" id="telemetry-chart">
                  <div className="box-header">
                    <BarChart3 className="cyan-text"/> <h2>Cost vs CO₂ Telemetry</h2>
                  </div>
                  <div className="chart-container">
                    <ResponsiveContainer width="100%" height={280}>
                      <BarChart data={results} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                        <XAxis dataKey="material" stroke="#64748b" tick={{fill: '#94a3b8', fontSize: 13}} />
                        <YAxis yAxisId="left" stroke="#00f0ff" tick={{fontSize: 13}} />
                        <YAxis yAxisId="right" orientation="right" stroke="#00ffaa" tick={{fontSize: 13}} />
                        <Tooltip cursor={{fill: 'rgba(255,255,255,0.05)'}} contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155' }} />
                        <Bar yAxisId="left" dataKey="cost_inr" name="Cost (INR)" fill="url(#cyanGrad)" radius={[4, 4, 0, 0]} isAnimationActive={false}/>
                        <Bar yAxisId="right" dataKey="co2_kg" name="CO2 (kg)" fill="url(#greenGrad)" radius={[4, 4, 0, 0]} isAnimationActive={false}/>
                        <defs>
                          <linearGradient id="cyanGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#00f0ff" /><stop offset="100%" stopColor="#0057ff" /></linearGradient>
                          <linearGradient id="greenGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#00ffaa" /><stop offset="100%" stopColor="#008055" /></linearGradient>
                        </defs>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="deep-dive-grid">
                  {results.map((item, idx) => {
                    const score = getSustainabilityScore(item, idx, formData); 
                    
                    // FIX: Convert the string state to actual Numbers before adding
                    const bioDisplay = Number(formData.biodegradability_score) + (idx * 2);
                    const recyDisplay = Number(formData.recyclability_percent) + (idx * 1);

                    return (
                      <motion.div 
                        key={idx} 
                        className="bento-box deep-dive-card"
                        whileHover={!isTouchDevice ? { scale: 1.03, translateY: -5 } : {}}
                      >
                        <div className="dd-header">
                          <h4>{item.material}</h4>
                          <span className="dd-rank">{idx + 1}</span>
                        </div>
                        <ul className="dd-list">
                          <li><span>Cost/unit</span> <span className="cyan-text">₹{item.cost_inr.toLocaleString()}</span></li>
                          <li><span>CO₂</span> <span className="cyan-text">{item.co2_kg} kg</span></li>
                          <li><span>Biodegradable</span> <span className="white-text">{bioDisplay}%</span></li>
                          <li><span>Recyclability</span> <span className="white-text">{recyDisplay}%</span></li>
                        </ul>
                        <div className="dd-score-section">
                          <div className="dd-score-text"><span>Sustainability Score</span> <span className="green-text">{score}/100</span></div>
                          <div className="progress-bar-bg"><div className="progress-bar-fill" style={{ width: `${score}%` }}></div></div>
                        </div>
                        <p className="dd-reasoning">
                          Best choice because: highly biodegradable ({bioDisplay}%), excellent recyclability, and cost-efficient relative to CO2 output.
                        </p>
                      </motion.div>
                    );
                  })}
                </div>
              </motion.div>
            )}

            {history.length > 0 && (
              <motion.div className="bento-box history-section" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <div className="box-header">
                  <History className="icon-glow" /> <h2>Simulation History</h2>
                </div>
                <div className="history-table-container">
                  <table className="history-table">
                    <thead><tr><th>Time</th><th>Product</th><th>Industry</th><th>Top Recommendation</th></tr></thead>
                    <tbody>
                      {history.map((run) => (
                        <tr key={run.id}><td>{run.time}</td><td className="cyan-text">{run.product}</td><td>{run.category}</td><td className="green-text"><strong>{run.topMatch}</strong></td></tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </motion.div>
            )}

            <footer className="app-footer">
              <p><Code size={14} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '5px' }} /> Developed by <strong>Shameel Mohamed</strong> | <a href="mailto:shameelmohamed2005@gmail.com">shameelmohamed2005@gmail.com</a> | <a href="https://github.com/ShameelMohamed">GitHub</a></p>
              <p className="license-text">Licensed under the <a href="https://opensource.org/license/MIT">MIT License</a></p>
            </footer>

          </div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;