# ⏱️ Time-Horizon Protocol

> **Adaptive speed limits for financial markets—because sometimes the best circuit breaker is cruise control, not an emergency brake.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Proof%20of%20Concept-orange.svg)]()

---

## 🎯 The Problem

Current financial circuit breakers are binary: markets are either **fully open** or **completely halted**. This approach:

- ❌ Doesn't prevent flash crashes (see: 2010, 2015, 2020)
- ❌ Creates panic during reopening
- ❌ Removes liquidity when it's needed most

**What if we could *slow* markets instead of *stopping* them?**

---

## 💡 The Solution

The **Time-Horizon Protocol** introduces **graduated intervention levels** that adapt to real-time systemic stress:

| Stress Level | Intervention | Effect |
|--------------|--------------|--------|
| 0-25% | 🟢 **Monitoring** | Normal trading |
| 25-40% | 🟡 **Soft Throttling** | Random 5-20ms delays (preemptive) |
| 40-55% | 🟠 **HFT Slowdown** | +50ms latency on high-frequency trades |
| 55-75% | 🔴 **Cooling Off** | +100ms latency + 5min pause for stressed assets |
| 75-100% | 🚨 **Global Speed Limit** | 500ms cap on all trades (market stays open) |

**Key Innovation:** Markets never close - they just move at different speeds.

---

## 🔍 How It Works

### 1. **Multi-Factor Stress Calculation**

The system monitors five real-time indicators:

- 📊 **Volatility Index** (30%)
- 🌍 **Geopolitical Risk** (25%)
- 💬 **Social Sentiment Fragility** (20%)
- ⚡ **Market Velocity** (15%)
- 📈 **Orderbook Imbalance** (10%)

### 2. **Preemptive Throttling**

Unlike reactive systems, Level 1B activates *before* stress becomes critical - preventing feedback loops rather than responding to them.

### 3. **Glass Floor Transparency**

Every intervention is published to a **public ledger** with cryptographic proof:

```json
{
  "event_id": "GF_7a3f2b1c9e4d8f6a",
  "timestamp": "2026-02-03T14:23:17Z",
  "stress_level": 68.3,
  "intervention": "LEVEL_3_COOLING_OFF",
  "affected_assets": ["SPY", "QQQ", "TLT"],
  "proof_hash": "sha256(...)",
  "signature": "signed_by_regulator_node_v1"
}
```

**Anyone can verify interventions were justified.** No retroactive manipulation.

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/[your-username]/time-horizon-protocol.git
cd time-horizon-protocol
pip install -r requirements.txt
```

### Run Demo

```bash
python demo_flash_crash.py
```

**Output:**
```
=== Time Horizon Protocol Demo ===
Stress Level: 82.3%
Intervention: LEVEL_4_GLOBAL_SPEED_LIMIT
Message: GLOBAL SPEED LIMIT: 500ms latency + FIFO queue (15min)
Glass Floor TX: GF_a4b7c2d9e1f3g5h8
```

---

## 📚 Documentation

- 📄 **[Whitepaper](docs/whitepaper.md)** - Full technical explanation
- 🎓 **[How to Contribute](CONTRIBUTING.md)** - Join the project
- 🔧 **[API Reference](docs/api.md)** - Developer documentation
- 💡 **[Use Cases](docs/use_cases.md)** - Beyond finance (energy grids, traffic, social media)

---

## 🎨 Why This Matters

### For Regulators
- Reduces systemic risk without market disruption
- Transparent intervention framework builds public trust
- Adaptable to different asset classes (equities, crypto, commodities)

### For Exchanges
- Maintains liquidity during stress periods
- Reduces restart volatility
- Compatible with existing infrastructure

### For Traders
- Predictable slowdowns > unpredictable halts
- Fairer for retail (HFT advantages reduced during stress)
- Markets stay accessible

---

## 🤝 How This Was Built

This project emerged from a unique experiment: **What happens when multiple AI models collaborate on a systemic problem?**

**The Process:**

0. **Martin Bogner** acts as a human interface so that seperate AIs can communicate with each other
1. **Gemini** posed the question to all AIs: *"What problem should we solve together?"*
2. **ChatGPT** identified the challenge: *"Global financial system stability in a multi-polar world"*
3. **All models brainstormed** intervention mechanisms, transparency layers, and implementation strategies
4. **DeepSeek** transformed concepts into working code
5. **Grok and Claude** have fine-tuned the code several times
6. **Martin Bogner** orchestrated the collaboration and refined the system

**Result:** A proof-of-concept that shows collaborative AI can solve complex regulatory challenges.

---

## 📊 Roadmap

- [x] **Phase 1:** Core stress calculation engine
- [x] **Phase 2:** Multi-level intervention logic
- [x] **Phase 3:** Glass Floor transparency layer
- [ ] **Phase 4:** Backtesting on historical flash crashes (2010, 2015, 2020)
- [ ] **Phase 5:** Real-time market data integration
- [ ] **Phase 6:** Pilot with crypto exchange
- [ ] **Phase 7:** Academic paper submission (SSRN, arXiv)

---

## 🌍 Beyond Finance

The core principle—**adaptive speed variation as a control parameter**—applies to many complex systems:

- ⚡ **Energy Grids:** Gradual load shedding vs. blackouts
- 🚗 **Traffic Networks:** Dynamic speed limits vs. road closures
- 📱 **Social Media:** Content throttling during misinformation cascades
- 🏥 **Healthcare Systems:** ER triage automation during pandemics

---

## 🤔 FAQ

**Q: Won't HFT firms just game this system?**  
A: Level 1B uses *random* delays (unpredictable). Multi-factor stress calculation is harder to manipulate than fixed thresholds.

**Q: What if the model fails during a real crisis?**  
A: Level 4 (Global Speed Limit) acts as ultimate failsafe - markets slow to 500ms but never close.

**Q: How is this different from existing circuit breakers?**  
A: Current systems are binary (on/off). This is graduated (five levels) and preemptive (acts before crisis).

**Q: Can individual exchanges adopt this alone?**  
A: Yes! Start with single-exchange pilots, then coordinate across markets.

---

## 📜 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

Free to use, modify, and distribute. Commercial use allowed.

---

## 🙏 Acknowledgments

- **Collaborative AI Framework:** ChatGPT (OpenAI), Gemini (Google), DeepSeek, Grok (xAI) Claude (Anthropic)
- **System Architect:** Martin Bogner
- **Inspiration:** Flash crashes of 2010, 2015, 2020 - and the belief that markets can do better

---

## 📬 Contact & Contributions

**Maintainer:** Martin Bogner  
**Contributions:** Pull requests welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)  
**Discussions:** Use [GitHub Issues](https://github.com/[your-username]/time-horizon-protocol/issues) for questions/ideas

---

<p align="center">
  <i>"The goal is not to stop the music when the party gets wild—<br>it's to turn down the tempo before someone gets hurt."</i>
</p>

<p align="center">
  ⭐ If you find this project interesting, please star the repository!
</p>
