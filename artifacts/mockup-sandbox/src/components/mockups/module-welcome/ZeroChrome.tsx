
export function ZeroChrome() {
  const navy = "#0d1b2a";
  const accent = "#f5c842";
  const bg = "#f7f9fb";
  const border = "#dde4ec";
  const muted = "#6b7a8d";

  const objectives = [
    { icon: "⚙️", title: "Manual Controls", desc: "Key controls and instruments for shifting a manual transmission" },
    { icon: "📊", title: "Shift Patterns", desc: "Basic shift patterns for 7–18 gear configurations" },
    { icon: "⛽", title: "Economy & Control", desc: "How proper shifting improves fuel economy and vehicle control" },
    { icon: "🔄", title: "Transmission Types", desc: "Automatic, semiautomatic, and autoshift transmission differences" },
  ];

  return (
    <div style={{ fontFamily: "'Barlow Condensed', 'Arial Narrow', sans-serif", background: bg, minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      {/* Slim header — just branding */}
      <header style={{ background: navy, borderBottom: `3px solid ${accent}`, padding: "0 40px", height: 48, display: "flex", alignItems: "center", justifyContent: "space-between", flexShrink: 0 }}>
        <span style={{ fontWeight: 700, fontSize: 16, letterSpacing: 2.5, textTransform: "uppercase", color: "#fff" }}>ELDT NOW</span>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 11, letterSpacing: 1.5, textTransform: "uppercase", color: "rgba(255,255,255,0.55)" }}>Entry-Level Driver Training</span>
          <span style={{ background: accent, color: navy, fontWeight: 700, fontSize: 10, letterSpacing: 2, textTransform: "uppercase", padding: "2px 8px", borderRadius: 3 }}>5 of 33</span>
        </div>
      </header>

      {/* Immersive hero — full width */}
      <div style={{ background: `linear-gradient(135deg, ${navy} 0%, #1a3a5c 100%)`, color: "#fff", padding: "56px 80px 48px", flexShrink: 0 }}>
        <div style={{ maxWidth: 900, margin: "0 auto" }}>
          <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: 4, textTransform: "uppercase", color: "rgba(255,255,255,0.45)", marginBottom: 18 }}>Module 5 · Unit 1.1.5 · FMCSA Compliance</div>
          <h1 style={{ fontFamily: "'Source Serif 4', Georgia, serif", fontSize: 58, fontWeight: 700, lineHeight: 1.06, margin: "0 0 22px", letterSpacing: -0.5 }}>
            Shifting &amp;<br />Operating<br />Transmissions
          </h1>
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <div style={{ width: 64, height: 4, background: accent, borderRadius: 2 }} />
            <span style={{ fontSize: 13, letterSpacing: 1.5, textTransform: "uppercase", color: "rgba(255,255,255,0.5)" }}>15 slides · ~45 min · 80% to pass</span>
          </div>
        </div>
      </div>

      {/* Objectives — 2-column card grid */}
      <div style={{ flex: 1, padding: "44px 80px", background: bg }}>
        <div style={{ maxWidth: 900, margin: "0 auto" }}>
          <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: 3, textTransform: "uppercase", color: muted, marginBottom: 20 }}>What You'll Master</div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 40 }}>
            {objectives.map((obj, i) => (
              <div key={i} style={{ background: "#fff", border: `1px solid ${border}`, borderRadius: 10, padding: "22px 24px", display: "flex", gap: 18, alignItems: "flex-start" }}>
                <div style={{ fontSize: 28, flexShrink: 0, marginTop: 2 }}>{obj.icon}</div>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 700, letterSpacing: 1, textTransform: "uppercase", color: navy, marginBottom: 6 }}>{obj.title}</div>
                  <div style={{ fontSize: 13, color: "#555", lineHeight: 1.45 }}>{obj.desc}</div>
                </div>
              </div>
            ))}
          </div>
          {/* Full-width CTA */}
          <button style={{ width: "100%", background: navy, color: "#fff", border: "none", padding: "18px 40px", fontSize: 16, fontWeight: 700, letterSpacing: 2.5, textTransform: "uppercase", borderRadius: 8, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", gap: 14 }}>
            Begin Module 5
            <span style={{ background: accent, color: navy, borderRadius: "50%", width: 32, height: 32, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 18, fontWeight: 900 }}>→</span>
          </button>
          <p style={{ textAlign: "center", fontSize: 12, color: muted, marginTop: 14, letterSpacing: 0.5 }}>
            Course outline and slide-by-slide navigation available during the module
          </p>
        </div>
      </div>
    </div>
  );
}
