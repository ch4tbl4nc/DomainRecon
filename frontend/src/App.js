
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [domain, setDomain] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await axios.post("http://localhost:8000/api/whois", { domain });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Erreur lors de la requête WHOIS.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: "90vh",
      background: "#fff",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontFamily: "'Segoe UI', 'Roboto', 'Arial', sans-serif"
    }}>
      <div style={{
        background: "#fff",
        borderRadius: 18,
        boxShadow: "0 8px 32px 0 rgba(31, 38, 135, 0.2)",
        padding: 36,
        minWidth: 500,
        maxWidth: 900,
        width: "100%",
        minHeight: 600,
        height: "auto"
      }}>
        <h1 style={{
          textAlign: "center",
          color: "#1e3c72",
          letterSpacing: 1,
          marginBottom: 24
        }}>WHOIS Tool</h1>
        <form onSubmit={handleSubmit} style={{ marginBottom: 24, display: "flex", gap: 8 }}>
          <input
            type="text"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            placeholder="Entrez un nom de domaine (ex: example.com)"
            style={{
              flex: 1,
              padding: "10px 14px",
              fontSize: 16,
              border: "1px solid #b0b8c1",
              borderRadius: 8,
              outline: "none",
              transition: "border 0.2s",
            }}
            required
          />
          <button
            type="submit"
            style={{
              padding: "10px 18px",
              fontSize: 16,
              background: loading ? "#b0b8c1" : "#2a5298",
              color: "#fff",
              border: "none",
              borderRadius: 8,
              cursor: loading ? "not-allowed" : "pointer",
              fontWeight: 600,
              boxShadow: loading ? "none" : "0 2px 8px 0 rgba(42,82,152,0.10)"
            }}
            disabled={loading}
          >
            {loading ? "Recherche..." : "Rechercher"}
          </button>
        </form>
        {error && <div style={{ color: "#d32f2f", marginBottom: 16, textAlign: "center" }}>{error}</div>}
        {result && (
          <div style={{
            background: "#f7fafd",
            padding: 24,
            borderRadius: 14,
            boxShadow: "0 2px 8px 0 rgba(42,82,152,0.07)",
            maxHeight: 500,
            overflowY: "auto"
          }}>
            <h2 style={{ color: "#2a5298", fontSize: 20, marginBottom: 18, textAlign: "center", letterSpacing: 1 }}>Résultat WHOIS</h2>
            <table style={{ width: "100%", borderCollapse: "separate", borderSpacing: 0 }}>
              <tbody>
                {Object.entries(result).map(([key, value]) => {
                  let displayValue = value;
                  if (key === "status" && Array.isArray(value)) {
                    displayValue = (
                      <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                        {value.filter(Boolean).map((v, i) => (
                          <span key={i} style={{
                            display: "inline-block",
                            background: "#e3e8ee",
                            color: "#2a5298",
                            borderRadius: 6,
                            padding: "2px 8px",
                            fontSize: 13,
                            marginBottom: 2,
                            fontWeight: 500
                          }}>{v}</span>
                        ))}
                      </div>
                    );
                  } else if (Array.isArray(value)) {
                    displayValue = value.filter(Boolean).join(", ");
                  } else if (typeof value === "string" && value.match(/^\d{4}-\d{2}-\d{2}/)) {
                    // Formatage simple des dates ISO
                    displayValue = new Date(value).toLocaleString();
                  } else if (value === null || value === undefined || value === "null") {
                    displayValue = <span style={{ color: "#b0b8c1" }}>–</span>;
                  }
                  return (
                    <tr key={key} style={{ borderBottom: "1.5px solid #e3e8ee", height: 38 }}>
                      <td style={{
                        fontWeight: 600,
                        color: "#1e3c72",
                        padding: "8px 12px 8px 0",
                        width: 160,
                        textTransform: "capitalize",
                        background: "#f0f4fa"
                      }}>{key.replace(/_/g, ' ')}</td>
                      <td style={{
                        color: "#222",
                        padding: "8px 0 8px 8px",
                        wordBreak: "break-all",
                        background: "#fff"
                      }}>{displayValue}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
