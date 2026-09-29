/**
 * Nym Privacy Hub Lovelace Custom Card
 * State-of-the-Art Mixnet Dashboard Card for Home Assistant
 */

class NymPrivacyHubCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._copied = false;
  }

  setConfig(config) {
    this._config = Object.assign({
      title: 'Nym Privacy Hub',
      entity_status: 'sensor.nym_mixnet_status',
      entity_latency: 'sensor.nym_mixnet_latenz',
      entity_proxy: 'sensor.nym_proxy_endpunkt',
      entity_ai: 'switch.ki_voice_privacy',
      entity_geo: 'switch.wetter_geodaten_schutz',
      entity_cover: 'switch.anti_einbruchs_schutz_cover_traffic',
    }, config);
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  toggleEntity(entityId) {
    if (!this._hass || !entityId) return;
    const stateObj = this._hass.states[entityId];
    const service = stateObj && stateObj.state === 'on' ? 'turn_off' : 'turn_on';
    this._hass.callService('switch', service, { entity_id: entityId });
  }

  triggerRefresh() {
    if (!this._hass) return;
    this._hass.callService('nym_privacy_hub', 'test_connection', {});
    this.showToast('Mixnet Ping & Verbindungstest ausgelöst...');
  }

  copyProxy(url) {
    navigator.clipboard.writeText(url).then(() => {
      this._copied = true;
      this.render();
      setTimeout(() => {
        this._copied = false;
        this.render();
      }, 2500);
    });
  }

  showToast(msg) {
    const toast = this.shadowRoot.getElementById('toast');
    if (toast) {
      toast.textContent = msg;
      toast.className = 'toast show';
      setTimeout(() => {
        toast.className = 'toast';
      }, 3000);
    }
  }

  render() {
    if (!this._hass) return;

    const statusState = this._hass.states[this._config.entity_status]?.state || 'connected';
    const latencyVal = this._hass.states[this._config.entity_latency]?.state || '450';
    const proxyUrl = this._hass.states[this._config.entity_proxy]?.state || 'socks5://127.0.0.1:1080';
    
    const aiState = this._hass.states[this._config.entity_ai]?.state === 'on';
    const geoState = this._hass.states[this._config.entity_geo]?.state === 'on';
    const coverState = this._hass.states[this._config.entity_cover]?.state === 'on';

    const isConnected = statusState !== 'unavailable' && statusState !== 'disconnected';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          --card-bg: var(--ha-card-background, #111827);
          --card-border: rgba(0, 245, 160, 0.2);
          --cyan: #00f5a0;
          --blue: #00d9f5;
          --purple: #8b5cf6;
          --text-main: #f9fafb;
          --text-muted: #9ca3af;
          --font-family: var(--paper-font-body1_-_font-family, 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif);
        }

        ha-card {
          background: linear-gradient(145deg, rgba(17, 24, 39, 0.95), rgba(15, 23, 42, 0.85));
          border-radius: 20px;
          border: 1px solid var(--card-border);
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), 0 0 20px rgba(0, 245, 160, 0.08);
          padding: 24px;
          color: var(--text-main);
          font-family: var(--font-family);
          position: relative;
          overflow: hidden;
        }

        ha-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 15%;
          right: 15%;
          height: 2px;
          background: linear-gradient(90deg, transparent, var(--cyan), var(--blue), transparent);
        }

        .header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 20px;
        }

        .brand {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .logo {
          width: 44px;
          height: 44px;
          border-radius: 12px;
          background: linear-gradient(135deg, var(--cyan), var(--blue));
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 22px;
          box-shadow: 0 4px 15px rgba(0, 245, 160, 0.3);
          color: #0b0f19;
        }

        .title-area h2 {
          margin: 0;
          font-size: 19px;
          font-weight: 700;
          background: linear-gradient(90deg, #fff, #a7f3d0);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .title-area p {
          margin: 2px 0 0;
          font-size: 12px;
          color: var(--text-muted);
        }

        .badge {
          display: flex;
          align-items: center;
          gap: 8px;
          background: rgba(0, 245, 160, 0.12);
          border: 1px solid var(--cyan);
          color: var(--cyan);
          padding: 6px 14px;
          border-radius: 999px;
          font-size: 13px;
          font-weight: 600;
        }

        .badge.off {
          background: rgba(239, 68, 68, 0.12);
          border-color: #ef4444;
          color: #ef4444;
        }

        .pulse {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: currentColor;
          box-shadow: 0 0 8px currentColor;
          animation: pulseAnim 2s infinite;
        }

        @keyframes pulseAnim {
          0%, 100% { transform: scale(1); opacity: 0.9; }
          50% { transform: scale(1.4); opacity: 1; }
        }

        .route-box {
          background: rgba(0, 0, 0, 0.3);
          border: 1px solid rgba(255, 255, 255, 0.05);
          border-radius: 14px;
          padding: 16px;
          margin-bottom: 20px;
        }

        .route-title {
          font-size: 11px;
          text-transform: uppercase;
          letter-spacing: 0.8px;
          color: var(--text-muted);
          margin-bottom: 12px;
          display: flex;
          justify-content: space-between;
        }

        .hops {
          display: flex;
          align-items: center;
          justify-content: space-between;
        }

        .hop {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 6px;
        }

        .hop-circle {
          width: 34px;
          height: 34px;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.06);
          border: 1px solid rgba(0, 245, 160, 0.3);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 14px;
          color: var(--cyan);
        }

        .hop span {
          font-size: 11px;
          color: var(--text-muted);
        }

        .hop-line {
          flex: 1;
          height: 2px;
          background: linear-gradient(90deg, var(--cyan), var(--blue));
          margin: 0 6px 16px;
          opacity: 0.5;
          position: relative;
        }

        .hop-line::after {
          content: '';
          position: absolute;
          top: -3px;
          left: 0;
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: #fff;
          box-shadow: 0 0 6px #fff;
          animation: hopFlow 2.5s linear infinite;
        }

        @keyframes hopFlow {
          0% { left: 0%; opacity: 0; }
          20% { opacity: 1; }
          80% { opacity: 1; }
          100% { left: 100%; opacity: 0; }
        }

        .proxy-wrapper {
          background: rgba(0, 0, 0, 0.4);
          border: 1px dashed rgba(0, 245, 160, 0.3);
          border-radius: 12px;
          padding: 12px 16px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 20px;
        }

        .proxy-text {
          font-family: monospace;
          color: var(--cyan);
          font-size: 13px;
        }

        .btn-copy {
          background: rgba(255, 255, 255, 0.08);
          border: 1px solid rgba(255, 255, 255, 0.15);
          color: #fff;
          border-radius: 8px;
          padding: 6px 12px;
          font-size: 12px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .btn-copy:hover {
          background: rgba(255, 255, 255, 0.2);
        }

        .toggle-group {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }

        .toggle-card {
          background: rgba(255, 255, 255, 0.03);
          border: 1px solid rgba(255, 255, 255, 0.06);
          border-radius: 12px;
          padding: 12px 16px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          cursor: pointer;
          transition: background 0.2s ease;
        }

        .toggle-card:hover {
          background: rgba(255, 255, 255, 0.06);
        }

        .toggle-left {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .toggle-icon {
          font-size: 20px;
        }

        .toggle-title {
          font-size: 14px;
          font-weight: 600;
        }

        .toggle-sub {
          font-size: 11px;
          color: var(--text-muted);
        }

        .switch-ui {
          width: 42px;
          height: 24px;
          background: rgba(255, 255, 255, 0.15);
          border-radius: 999px;
          position: relative;
          transition: background 0.25s ease;
        }

        .switch-ui.active {
          background: var(--cyan);
        }

        .switch-ui-handle {
          position: absolute;
          top: 2px;
          left: 2px;
          width: 20px;
          height: 20px;
          background: #fff;
          border-radius: 50%;
          transition: transform 0.25s ease;
        }

        .switch-ui.active .switch-ui-handle {
          transform: translateX(18px);
          background: #0b0f19;
        }

        .footer-actions {
          margin-top: 18px;
          display: flex;
          gap: 10px;
          justify-content: flex-end;
        }

        .btn-action {
          background: linear-gradient(135deg, var(--cyan), var(--blue));
          border: none;
          color: #0b0f19;
          font-weight: 700;
          font-size: 12px;
          padding: 8px 16px;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .btn-action:hover {
          box-shadow: 0 4px 15px rgba(0, 245, 160, 0.35);
          transform: translateY(-1px);
        }

        .toast {
          position: absolute;
          bottom: 15px;
          left: 50%;
          transform: translateX(-50%) translateY(50px);
          background: var(--cyan);
          color: #0b0f19;
          padding: 8px 16px;
          border-radius: 8px;
          font-size: 12px;
          font-weight: 600;
          opacity: 0;
          transition: all 0.3s ease;
          pointer-events: none;
        }

        .toast.show {
          transform: translateX(-50%) translateY(0);
          opacity: 1;
        }
      </style>

      <ha-card>
        <div class="header">
          <div class="brand">
            <div class="logo">🛡️</div>
            <div class="title-area">
              <h2>${this._config.title}</h2>
              <p>Mixnet Privatsphäre-Schild</p>
            </div>
          </div>
          <div class="badge ${isConnected ? '' : 'off'}">
            <span class="pulse"></span>
            <span>${isConnected ? `Aktiv • ${latencyVal} ms` : 'Getrennt'}</span>
          </div>
        </div>

        <div class="route-box">
          <div class="route-title">
            <span>Mixnet Route Topologie</span>
            <span style="color: var(--cyan);">3 Mix-Hops Anonymisiert</span>
          </div>
          <div class="hops">
            <div class="hop">
              <div class="hop-circle">🏠</div>
              <span>HA Node</span>
            </div>
            <div class="hop-line"></div>
            <div class="hop">
              <div class="hop-circle">🧅</div>
              <span>Layer 1</span>
            </div>
            <div class="hop-line"></div>
            <div class="hop">
              <div class="hop-circle">🧅</div>
              <span>Layer 2</span>
            </div>
            <div class="hop-line"></div>
            <div class="hop">
              <div class="hop-circle">🧅</div>
              <span>Layer 3</span>
            </div>
            <div class="hop-line"></div>
            <div class="hop">
              <div class="hop-circle">🌐</div>
              <span>Exit Gateway</span>
            </div>
          </div>
        </div>

        <div class="proxy-wrapper">
          <span class="proxy-text">${proxyUrl}</span>
          <button id="copyBtn" class="btn-copy">
            ${this._copied ? '✓ Kopiert!' : '📋 Kopieren'}
          </button>
        </div>

        <div class="toggle-group">
          <div class="toggle-card" id="toggleAiCard">
            <div class="toggle-left">
              <span class="toggle-icon">🤖</span>
              <div>
                <div class="toggle-title">KI & Voice Privacy</div>
                <div class="toggle-sub">OpenAI, Anthropic & Sprachassistenten über Mixnet</div>
              </div>
            </div>
            <div class="switch-ui ${aiState ? 'active' : ''}">
              <div class="switch-ui-handle"></div>
            </div>
          </div>

          <div class="toggle-card" id="toggleGeoCard">
            <div class="toggle-left">
              <span class="toggle-icon">🌦️</span>
              <div>
                <div class="toggle-title">Wetter & Geodaten Schutz</div>
                <div class="toggle-sub">Verschleiert genaue Standortkoordinaten</div>
              </div>
            </div>
            <div class="switch-ui ${geoState ? 'active' : ''}">
              <div class="switch-ui-handle"></div>
            </div>
          </div>

          <div class="toggle-card" id="toggleCoverCard">
            <div class="toggle-left">
              <span class="toggle-icon">🚨</span>
              <div>
                <div class="toggle-title">Anti-Einbruchs Cover Traffic</div>
                <div class="toggle-sub">Konstantes Grundrauschen gegen Router-Spione</div>
              </div>
            </div>
            <div class="switch-ui ${coverState ? 'active' : ''}">
              <div class="switch-ui-handle"></div>
            </div>
          </div>
        </div>

        <div class="footer-actions">
          <button class="btn-action" id="refreshBtn">⚡ Verbindungstest ausführen</button>
        </div>

        <div id="toast" class="toast"></div>
      </ha-card>
    `;

    this.shadowRoot.getElementById('copyBtn').onclick = () => this.copyProxy(proxyUrl);
    this.shadowRoot.getElementById('toggleAiCard').onclick = () => this.toggleEntity(this._config.entity_ai);
    this.shadowRoot.getElementById('toggleGeoCard').onclick = () => this.toggleEntity(this._config.entity_geo);
    this.shadowRoot.getElementById('toggleCoverCard').onclick = () => this.toggleEntity(this._config.entity_cover);
    this.shadowRoot.getElementById('refreshBtn').onclick = () => this.triggerRefresh();
  }

  getCardSize() {
    return 4;
  }
}

customElements.define('nym-privacy-hub-card', NymPrivacyHubCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: 'nym-privacy-hub-card',
  name: 'Nym Privacy Hub Karte',
  description: 'Echtzeit-Status, Mixnet-Topologie und Privatsphäre-Schalter für Home Assistant.',
  preview: true,
});
