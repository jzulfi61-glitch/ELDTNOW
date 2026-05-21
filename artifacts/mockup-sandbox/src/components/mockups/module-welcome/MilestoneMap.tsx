
export function MilestoneMap() {
  const navy = "#0d1b2a";
  const navyMid = "#1a3a5c";
  const accent = "#f5c842";
  const bg = "#f7f9fb";
  const border = "#dde4ec";
  const muted = "#6b7a8d";

  const phases = [
    { id: 1, label: "Introduction", slides: ["Shifting: The Skill That Sets Professionals Apart", "Learning Objectives"], color: "#4a90d9" },
    { id: 2, label: "Controls & Tools", slides: ["Three Controls That Drive the Shift", "Your Shifting Gauges and Governor", "Most Tractor-Trailers Have 7 to 18 Gears"], color: "#27ae60" },
    { id: 3, label: "Shifting Technique", slides: ["Upshifting: Building Speed", "Downshifting: Engine Braking", "Hitting or Hunting a Gear", "Traits of a Skilled Shifter", "Why Smooth Shifting Matters"], color: "#e67e22" },
    { id: 4, label: "Shift Patterns", slides: ["Eaton Fuller Nine-Speed", "Eaton Fuller Super Ten", "Rockwell Ten-Speed", "Other Pattern Variants"], color: "#8e44ad" },
    { id: 5, label: "Other Transmissions", slides: ["Semiautomatic, Autoshift, and Automatic"], color: "#c0392b" },
  ];

  return (
    <div style={{ fontFamily: "'Barlow Condensed', 'Arial Narrow', sans-serif", background: bg, minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      {/* Header */}
      <header style={{ background: navy, color: "#fff", padding: "0 24px", display: "flex", alignItems: "center", justifyContent: "space-between", height: 52, flexShrink: 0, borderBottom: `3px solid ${accent}` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <span style={{ fontWeight: 700, fontSize: 17, letterSpacing: 2, textTransform: "uppercase" }}>ELDT NOW</span>
          <span style={{ width: 1, height: 22, background: "rgba(255,255,255,0.2)" }} />
          <span style={{ fontSize: 12, letterSpacing: 1.5, textTransform: "uppercase", color: "rgba(255,255,255,0.7)" }}>Entry-Level Driver Training</span>
          <span style={{ width: 1, height: 22, background: "rgba(255,255,255,0.2)" }} />
          <span style={{ fontSize: 12, letterSpacing: 1.5, textTransform: "uppercase", color: "rgba(255,255,255,0.7)" }}>Unit 1.1.5 · Shifting / Operating Transmissions</span>
        </div>
        <span style={{ background: accent, color: navy, fontWeight: 700, fontSize: 11, letterSpacing: 2, textTransform: "uppercase", padding: "3px 10px", borderRadius: 3 }}>Module 5 of 33</span>
      </header>

      {/* Body */}
      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
        {/* Sidebar — Journey Map */}
        <aside style={{ width: 260, background: "#fff", borderRight: `1px solid ${border}`, display: "flex", flexDirection: "column", overflowY: "auto" }}>
          <div style={{ padding: "14px 16px 8px", borderBottom: `1px solid ${border}` }}>
            <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: 2.5, textTransform: "uppercase", color: muted }}>Your Journey</div>
          </div>
          <div style={{ padding: "12px 14px", flex: 1 }}>
            {phases.map((phase, pi) => (
              <div key={phase.id} style={{ marginBottom: 18 }}>
                {/* Phase header */}
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
                  <div style={{ width: 22, height: 22, borderRadius: "50%", background: phase.color, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, fontWeight: 700, flexShrink: 0 }}>{phase.id}</div>
                  <span style={{ fontSize: 12, fontWeight: 700, letterSpacing: 1.2, textTransform: "uppercase", color: navy }}>{phase.label}</span>
                </div>
                {/* Slide nodes */}
                <div style={{ marginLeft: 11, borderLeft: `2px solid ${border}`, paddingLeft: 14 }}>
                  {phase.slides.map((slide, si) => (
                    <div key={si} style={{ position: "relative", padding: "5px 0", display: "flex", alignItems: "center", gap: 8 }}>
                      <div style={{ position: "absolute", left: -19, width: 8, height: 8, borderRadius: "50%", background: "#c8d6e5", border: `2px solid ${border}` }} />
                      <span style={{ fontSize: 11, color: "#a0adb8", letterSpacing: 0.3, lineHeight: 1.35 }}>{slide}</span>
                    </div>
                  ))}
                  {/* Quiz node */}
                  {pi === phases.length - 1 && (
                    <div style={{ position: "relative", padding: "8px 0 0", display: "flex", alignItems: "center", gap: 8, marginTop: 6 }}>
                      <div style={{ position: "absolute", left: -22, width: 14, height: 14, borderRadius: "50%", background: "#f0e4b0", border: `2px solid ${accent}` }} />
                      <span style={{ fontSize: 11, color: "#b38b00", fontWeight: 700, letterSpacing: 0.8 }}>⚡ Knowledge Check</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
          <div style={{ padding: "10px 14px", borderTop: `1px solid ${border}`, fontSize: 10, color: muted, letterSpacing: 0.5, textAlign: "center" }}>
            15 slides · ~45 min
          </div>
        </aside>

        {/* Main content */}
        <main style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center", padding: "40px 48px" }}>
          <div style={{ maxWidth: 620 }}>
            <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: 3, textTransform: "uppercase", color: muted, marginBottom: 10 }}>Module 5 · Unit 1.1.5</div>
            <h1 style={{ fontFamily: "'Source Serif 4', Georgia, serif", fontSize: 42, fontWeight: 700, color: navy, lineHeight: 1.12, margin: "0 0 24px" }}>Shifting &amp; Operating Transmissions</h1>
            <div style={{ width: 52, height: 4, background: accent, borderRadius: 2, marginBottom: 28 }} />
            <div style={{ background: "#fff", border: `1px solid ${border}`, borderRadius: 8, padding: "24px 28px", marginBottom: 32 }}>
              <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: 2.5, textTransform: "uppercase", color: muted, marginBottom: 14 }}>Learning Objectives</div>
              {[
                "Describe the key controls and instruments for shifting a manual transmission",
                "Identify basic shift patterns and procedures",
                "Explain how proper shifting improves vehicle control and fuel economy",
                "Recognize the characteristics of automatic, semiautomatic, and autoshift transmissions",
              ].map((obj, i) => (
                <div key={i} style={{ display: "flex", gap: 12, marginBottom: 10, alignItems: "flex-start" }}>
                  <span style={{ width: 20, height: 20, borderRadius: "50%", background: accent, color: navy, fontSize: 11, fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, marginTop: 1 }}>{i + 1}</span>
                  <span style={{ fontSize: 14, color: "#3a3a3a", lineHeight: 1.4 }}>{obj}</span>
                </div>
              ))}
            </div>
            <button style={{ background: navy, color: "#fff", border: "none", padding: "14px 40px", fontSize: 15, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", borderRadius: 6, cursor: "pointer", display: "flex", alignItems: "center", gap: 10 }}>
              Start Module <span style={{ fontSize: 18 }}>→</span>
            </button>
          </div>
        </main>
      </div>
    </div>
  );
}
