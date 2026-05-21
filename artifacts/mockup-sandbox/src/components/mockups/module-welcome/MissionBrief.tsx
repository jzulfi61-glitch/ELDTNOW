
export function MissionBrief() {
  const navy = "#0d1b2a";
  const navyMid = "#1a3a5c";
  const accent = "#f5c842";
  const bg = "#f7f9fb";
  const border = "#dde4ec";
  const muted = "#6b7a8d";

  const stats = [
    { label: "Slides", value: "15", icon: "📋" },
    { label: "Est. Time", value: "~45 min", icon: "⏱" },
    { label: "Passing Score", value: "80%", icon: "🎯" },
    { label: "CDL Class", value: "A / B", icon: "🚛" },
  ];

  const stakes = [
    "Improper shifting damages drivetrain components worth $15,000+",
    "Gear grinding on curves or slippery roads can cause loss of control",
    "Fuel waste from running in the wrong gear adds up to thousands per year",
    "Employers test shifting proficiency in CDL road exams and post-hire evaluations",
  ];

  const objectives = [
    "Describe key controls and instruments for shifting",
    "Identify basic shift patterns and procedures",
    "Explain how shifting affects fuel economy and vehicle control",
    "Recognize automatic, semiautomatic, and autoshift transmissions",
  ];

  return (
    <div style={{ fontFamily: "'Barlow Condensed', 'Arial Narrow', sans-serif", background: bg, minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      {/* Header */}
      <header style={{ background: navy, borderBottom: `3px solid ${accent}`, padding: "0 24px", height: 52, display: "flex", alignItems: "center", justifyContent: "space-between", flexShrink: 0 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <span style={{ fontWeight: 700, fontSize: 17, letterSpacing: 2, textTransform: "uppercase", color: "#fff" }}>ELDT NOW</span>
          <span style={{ width: 1, height: 22, background: "rgba(255,255,255,0.2)" }} />
          <span style={{ fontSize: 12, letterSpacing: 1.5, textTransform: "uppercase", color: "rgba(255,255,255,0.65)" }}>Entry-Level Driver Training</span>
          <span style={{ width: 1, height: 22, background: "rgba(255,255,255,0.2)" }} />
          <span style={{ fontSize: 12, letterSpacing: 1.5, textTransform: "uppercase", color: "rgba(255,255,255,0.65)" }}>Unit 1.1.5 · Shifting / Operating Transmissions</span>
        </div>
        <span style={{ background: accent, color: navy, fontWeight: 700, fontSize: 11, letterSpacing: 2, textTransform: "uppercase", padding: "3px 10px", borderRadius: 3 }}>Module 5 of 33</span>
      </header>

      {/* Mission stat strip */}
      <div style={{ background: navyMid, borderBottom: `1px solid rgba(255,255,255,0.08)` }}>
        <div style={{ display: "flex", padding: "0 32px" }}>
          {stats.map((s, i) => (
            <div key={i} style={{ padding: "12px 28px 12px 0", display: "flex", alignItems: "center", gap: 10, borderRight: i < stats.length - 1 ? "1px solid rgba(255,255,255,0.12)" : "none", marginRight: i < stats.length - 1 ? 28 : 0 }}>
              <span style={{ fontSize: 16 }}>{s.icon}</span>
              <div>
                <div style={{ fontSize: 16, fontWeight: 700, color: "#fff", lineHeight: 1, letterSpacing: 0.5 }}>{s.value}</div>
                <div style={{ fontSize: 10, letterSpacing: 1.5, textTransform: "uppercase", color: "rgba(255,255,255,0.45)", marginTop: 2 }}>{s.label}</div>
              </div>
            </div>
          ))}
          <div style={{ flex: 1 }} />
          <div style={{ display: "flex", alignItems: "center", gap: 8, padding: "12px 0" }}>
            <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#27ae60" }} />
            <span style={{ fontSize: 11, letterSpacing: 1.5, textTransform: "uppercase", color: "rgba(255,255,255,0.55)" }}>FMCSA 380.503 Compliant</span>
          </div>
        </div>
      </div>

      {/* Body: 2-col dashboard */}
      <div style={{ flex: 1, padding: "36px 32px", display: "flex", gap: 28 }}>
        {/* Left — Why This Matters */}
        <div style={{ flex: "0 0 340px" }}>
          <div style={{ background: "#fff", border: `1px solid ${border}`, borderRadius: 10, overflow: "hidden", height: "100%" }}>
            <div style={{ background: navy, padding: "16px 20px", display: "flex", alignItems: "center", gap: 10 }}>
              <div style={{ width: 6, height: 6, borderRadius: "50%", background: "#e74c3c" }} />
              <div style={{ width: 6, height: 6, borderRadius: "50%", background: "#f39c12" }} />
              <div style={{ width: 6, height: 6, borderRadius: "50%", background: "#27ae60" }} />
              <span style={{ marginLeft: 6, fontSize: 11, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", color: "rgba(255,255,255,0.7)" }}>Mission Brief</span>
            </div>
            <div style={{ padding: "24px 22px" }}>
              <div style={{ fontSize: 12, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", color: muted, marginBottom: 16 }}>Why This Matters in the Field</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                {stakes.map((stake, i) => (
                  <div key={i} style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
                    <div style={{ width: 22, height: 22, borderRadius: 4, background: "#fff3cd", border: `1px solid ${accent}`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, flexShrink: 0, marginTop: 1 }}>⚠</div>
                    <span style={{ fontSize: 13, color: "#3a3a3a", lineHeight: 1.45 }}>{stake}</span>
                  </div>
                ))}
              </div>
              <div style={{ marginTop: 22, padding: "14px 16px", background: "#f0f8ff", border: "1px solid #b8d9f0", borderRadius: 6 }}>
                <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", color: "#1a6a9a", marginBottom: 6 }}>FMCSA Requirement</div>
                <p style={{ fontSize: 12, color: "#2c5f7e", lineHeight: 1.5, margin: 0 }}>This unit satisfies 49 CFR Part 380 Subpart F requirements for Shifting and Operating Transmissions (Theory).</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right — Module launch card */}
        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 20 }}>
          {/* Title + objectives */}
          <div style={{ background: "#fff", border: `1px solid ${border}`, borderRadius: 10, padding: "28px 30px" }}>
            <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: 3, textTransform: "uppercase", color: muted, marginBottom: 12 }}>Module 5 · Unit 1.1.5</div>
            <h1 style={{ fontFamily: "'Source Serif 4', Georgia, serif", fontSize: 36, fontWeight: 700, color: navy, lineHeight: 1.1, margin: "0 0 20px" }}>Shifting &amp; Operating<br />Transmissions</h1>
            <div style={{ width: 40, height: 3, background: accent, borderRadius: 2, marginBottom: 22 }} />
            <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: 2.5, textTransform: "uppercase", color: muted, marginBottom: 14 }}>Learning Objectives</div>
            {objectives.map((obj, i) => (
              <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: 10, marginBottom: 10 }}>
                <svg width="16" height="16" viewBox="0 0 16 16" style={{ flexShrink: 0, marginTop: 2 }}>
                  <circle cx="8" cy="8" r="7" fill={navy} />
                  <polyline points="4.5,8.5 7,11 11.5,5.5" fill="none" stroke={accent} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                <span style={{ fontSize: 13, color: "#333", lineHeight: 1.4 }}>{obj}</span>
              </div>
            ))}
          </div>

          {/* Launch button */}
          <button style={{ background: navy, color: "#fff", border: "none", borderRadius: 8, padding: "16px 32px", fontSize: 15, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <span>Start Module 5</span>
            <span style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 13, color: "rgba(255,255,255,0.55)", fontWeight: 400, letterSpacing: 0.5 }}>
              <span>15 slides · ~45 min</span>
              <span style={{ background: accent, color: navy, fontWeight: 700, borderRadius: "50%", width: 28, height: 28, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16 }}>→</span>
            </span>
          </button>
        </div>
      </div>
    </div>
  );
}
