import http.server
import socketserver
import json
import os
import sys
import webbrowser

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PORT = 8085
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(PROJECT_DIR, "nocodb_consolidated_data.json")

# Read Document files
def read_doc(filename):
    path = os.path.join(PROJECT_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Document non trouvé."

class NocoDBDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            else:
                self.wfile.write(json.dumps({"error": "Data file not found"}).encode("utf-8"))
            return

        if self.path == "/api/docs":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            docs = {
                "memorandum": read_doc("AIR_LIQUIDE_EURASIA_STRATEGIC_MEMORANDUM_2025_2030.md"),
                "playbook": read_doc("EIII_REGIONAL_INVESTMENT_INDEX_PLAYBOOK.md"),
                "montecarlo": read_doc("MONTE_CARLO_RISK_&_SANCTIONS_SIMULATION_REPORT.md")
            }
            self.wfile.write(json.dumps(docs, ensure_ascii=False).encode("utf-8"))
            return
        
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html_content = self.generate_html()
            self.wfile.write(html_content.encode("utf-8"))
            return

        super().do_GET()

    def generate_html(self):
        return """<!DOCTYPE html>
<html lang="fr" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NocoDB Enterprise CRM Command Center — Euroasia BD System</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Outfit', sans-serif; background-color: #0b0f19; color: #e2e8f0; }
        .glass-card { background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 1rem; }
        .glass-card-hover:hover { border-color: rgba(59, 130, 246, 0.4); transform: translateY(-2px); transition: all 0.2s ease; }
        .gradient-text { background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .gradient-gold { background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.6); }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(51, 65, 85, 0.8); border-radius: 3px; }
        .prose pre { background: #020617; padding: 1rem; border-radius: 0.5rem; border: 1px solid #1e293b; color: #38bdf8; font-family: 'JetBrains Mono', monospace; }
        .prose table { border-collapse: collapse; width: 100%; margin-top: 1rem; margin-bottom: 1rem; }
        .prose th, .prose td { border: 1px solid #334155; padding: 0.5rem 0.75rem; text-align: left; }
        .prose th { background-color: #0f172a; color: #f8fafc; font-weight: 600; }
        .prose h1, .prose h2, .prose h3 { color: #f8fafc; font-weight: 700; margin-top: 1.5rem; margin-bottom: 0.5rem; }
        .prose h1 { font-size: 1.5rem; color: #60a5fa; }
        .prose h2 { font-size: 1.25rem; color: #a78bfa; }
        .prose h3 { font-size: 1.1rem; color: #fbbf24; }
    </style>
</head>
<body class="min-h-screen flex flex-col custom-scrollbar">

    <!-- TOP HEADER / NAVBAR -->
    <header class="glass-card sticky top-0 z-50 rounded-none border-t-0 border-x-0 border-b border-slate-800 px-6 py-4 flex flex-wrap justify-between items-center bg-slate-950/80">
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-500 to-purple-600 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/30 text-lg">
                ⚡
            </div>
            <div>
                <h1 class="text-xl font-bold gradient-text leading-tight">Euroasia Enterprise CRM Command Center</h1>
                <p class="text-xs text-slate-400">NocoDB MCP Connected Base: <span class="font-mono text-emerald-400 font-bold">p0ygj6vufqhhhsc</span> (5 Tables / 386 Records)</p>
            </div>
        </div>

        <div class="flex items-center space-x-4 mt-2 sm:mt-0">
            <div class="flex items-center px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-medium">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping mr-2"></span>
                NocoDB Cloud: <span class="font-mono ml-1 text-emerald-300">5 Tables Active</span>
            </div>
            <button onclick="fetchData()" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold shadow-md shadow-blue-600/20 transition flex items-center gap-2">
                🔄 Sync CRM NocoDB
            </button>
        </div>
    </header>

    <!-- NAVIGATION TABS -->
    <nav class="bg-slate-900/60 border-b border-slate-800 px-6 py-2">
        <div class="flex space-x-2 overflow-x-auto text-sm font-medium">
            <button onclick="switchTab('overview')" id="tab-overview" class="tab-btn px-4 py-2 rounded-lg bg-blue-600/20 text-blue-400 border border-blue-500/30">📊 Dashboard Général</button>
            <button onclick="switchTab('kanban')" id="tab-kanban" class="tab-btn px-4 py-2 rounded-lg text-slate-400 hover:bg-slate-800">📋 Kanban Pipeline CRM (31 Opps)</button>
            <button onclick="switchTab('tables')" id="tab-tables" class="tab-btn px-4 py-2 rounded-lg text-slate-400 hover:bg-slate-800">🗃️ 5 Tables NocoDB Cloud</button>
            <button onclick="switchTab('documents')" id="tab-documents" class="tab-btn px-4 py-2 rounded-lg text-slate-400 hover:bg-slate-800">📝 Mémorandums & Playbooks</button>
            <button onclick="switchTab('whatif')" id="tab-whatif" class="tab-btn px-4 py-2 rounded-lg text-slate-400 hover:bg-slate-800">⚡ Simulateur What-If Sanctions</button>
            <button onclick="switchTab('gases')" id="tab-gases" class="tab-btn px-4 py-2 rounded-lg text-slate-400 hover:bg-slate-800">🧪 Focus Gaz Industriels</button>
        </div>
    </nav>

    <!-- MAIN CONTAINER -->
    <main class="flex-1 p-6 space-y-6 max-w-7xl mx-auto w-full">

        <!-- STATS KPI BANNER -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="glass-card p-5 glass-card-hover border-l-4 border-l-blue-500">
                <div class="text-xs uppercase tracking-wider text-slate-400 font-semibold">Capex Potentiel BD</div>
                <div class="text-3xl font-extrabold text-white mt-1" id="kpi-capex">21.8 M€</div>
                <div class="text-xs text-blue-400 mt-1">31 opportunités qualifiées Tier 1-4</div>
            </div>

            <div class="glass-card p-5 glass-card-hover border-l-4 border-l-emerald-500">
                <div class="text-xs uppercase tracking-wider text-slate-400 font-semibold">Revenu Post-Sanctions (2030)</div>
                <div class="text-3xl font-extrabold text-emerald-400 mt-1" id="kpi-revenue">12.6 M€/an</div>
                <div class="text-xs text-emerald-400 mt-1">Multiplier ×4.2 vs Baseline 2025</div>
            </div>

            <div class="glass-card p-5 glass-card-hover border-l-4 border-l-purple-500">
                <div class="text-xs uppercase tracking-wider text-slate-400 font-semibold">Base NocoDB Active</div>
                <div class="text-3xl font-extrabold text-purple-400 mt-1">386 Rows</div>
                <div class="text-xs text-purple-400 mt-1">5 Tables CRM Synchronisées</div>
            </div>

            <div class="glass-card p-5 glass-card-hover border-l-4 border-l-amber-500">
                <div class="text-xs uppercase tracking-wider text-slate-400 font-semibold">Régions Prioritaires BUY</div>
                <div class="text-3xl font-extrabold text-amber-400 mt-1">2 Régions</div>
                <div class="text-xs text-amber-400 mt-1">Score EIII ≥ 65 (Moscou & Oblast)</div>
            </div>
        </div>

        <!-- TAB 1: OVERVIEW -->
        <section id="content-overview" class="tab-content space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- CHART: Top 10 Regions EIII -->
                <div class="glass-card p-5 lg:col-span-2">
                    <h3 class="text-base font-bold text-slate-200 mb-4 flex justify-between items-center">
                        <span>🏆 Top 10 Régions — Eastern Industrial Investment Index (EIII)</span>
                        <span class="text-xs font-normal text-slate-400">Rosstat 2025</span>
                    </h3>
                    <div class="h-72">
                        <canvas id="chartTop10EIII"></canvas>
                    </div>
                </div>

                <!-- CHART: Pipeline Breakdown by Tier -->
                <div class="glass-card p-5">
                    <h3 class="text-base font-bold text-slate-200 mb-4">💼 Répartition du Pipeline BD (CAPEX M€)</h3>
                    <div class="h-72 flex items-center justify-center">
                        <canvas id="chartTierDoughnut"></canvas>
                    </div>
                </div>
            </div>

            <!-- KEY BD TARGET MATRIX -->
            <div class="glass-card p-5">
                <h3 class="text-base font-bold text-slate-200 mb-4">🎯 Top 5 Opportunités BD Stratégiques (Tier 1 - Critique)</h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-300">
                        <thead class="bg-slate-900/80 text-slate-400 uppercase font-semibold text-[10px]">
                            <tr>
                                <th class="p-3">Code Opp</th>
                                <th class="p-3">Région</th>
                                <th class="p-3">District</th>
                                <th class="p-3">Score EIII</th>
                                <th class="p-3">Capex Est.</th>
                                <th class="p-3">Produit Gaz Cible</th>
                                <th class="p-3">Clients Cibles (Rosstat)</th>
                                <th class="p-3">Revenu 2030 (Post-Sanctions)</th>
                            </tr>
                        </thead>
                        <tbody id="top5-table-body" class="divide-y divide-slate-800/60 font-mono">
                            <!-- Populated dynamically -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- TAB 2: KANBAN PIPELINE -->
        <section id="content-kanban" class="tab-content hidden space-y-6">
            <div class="flex flex-wrap justify-between items-center gap-4">
                <h2 class="text-lg font-bold text-slate-200">📋 Tableau Kanban CRM — Pipeline commercial Air Liquide (31 Opportunités)</h2>
                <div class="text-xs text-slate-400">Glissez ou filtrez les opportunités par priorité</div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <!-- COL 1: TIER 1 CRITIQUE -->
                <div class="glass-card p-4 space-y-3 border-t-4 border-t-red-500 bg-red-950/10">
                    <div class="flex justify-between items-center pb-2 border-b border-slate-800">
                        <span class="font-bold text-red-400 text-xs">🔴 TIER 1 - CRITIQUE</span>
                        <span class="text-xs bg-red-500/20 text-red-300 px-2 py-0.5 rounded font-mono font-bold" id="kanban-cnt-tier1">11</span>
                    </div>
                    <div id="kanban-col-tier1" class="space-y-3 max-h-[600px] overflow-y-auto custom-scrollbar pr-1">
                        <!-- Items -->
                    </div>
                </div>

                <!-- COL 2: TIER 2 HAUTE -->
                <div class="glass-card p-4 space-y-3 border-t-4 border-t-amber-500 bg-amber-950/10">
                    <div class="flex justify-between items-center pb-2 border-b border-slate-800">
                        <span class="font-bold text-amber-400 text-xs">🟡 TIER 2 - HAUTE</span>
                        <span class="text-xs bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded font-mono font-bold" id="kanban-cnt-tier2">20</span>
                    </div>
                    <div id="kanban-col-tier2" class="space-y-3 max-h-[600px] overflow-y-auto custom-scrollbar pr-1">
                        <!-- Items -->
                    </div>
                </div>

                <!-- COL 3: ETAPE PROSPECTION -->
                <div class="glass-card p-4 space-y-3 border-t-4 border-t-blue-500 bg-blue-950/10">
                    <div class="flex justify-between items-center pb-2 border-b border-slate-800">
                        <span class="font-bold text-blue-400 text-xs">🔷 ÉTAPE: PROSPECTION</span>
                        <span class="text-xs bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded font-mono font-bold">31</span>
                    </div>
                    <div id="kanban-col-prospect" class="space-y-3 max-h-[600px] overflow-y-auto custom-scrollbar pr-1">
                        <!-- Items -->
                    </div>
                </div>

                <!-- COL 4: GAGNÉ POST-SANCTIONS -->
                <div class="glass-card p-4 space-y-3 border-t-4 border-t-emerald-500 bg-emerald-950/10">
                    <div class="flex justify-between items-center pb-2 border-b border-slate-800">
                        <span class="font-bold text-emerald-400 text-xs">🟢 CIBLE POST-SANCTIONS (2030)</span>
                        <span class="text-xs bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-mono font-bold">12.6 M€/an</span>
                    </div>
                    <div class="p-4 bg-slate-900/80 rounded-xl text-xs text-slate-400 border border-slate-800 space-y-2">
                        <p class="font-semibold text-emerald-400">Objectif 2030 :</p>
                        <p>Conversion des 31 opportunités en contrats Over-The-Fence (OTF) et VPSA lors du déblocage des sanctions UE.</p>
                        <p class="text-amber-300 font-mono">CAPEX engagé : 21.8 M€</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 3: 5 NOCODB TABLES EXPLORER -->
        <section id="content-tables" class="tab-content hidden space-y-6">
            <div class="glass-card p-5">
                <div class="flex flex-wrap justify-between items-center gap-4 mb-4">
                    <h3 class="text-base font-bold text-slate-200">🗃️ Explorateur des 5 Tables CRM NocoDB (Base: p0ygj6vufqhhhsc)</h3>
                    <div class="flex space-x-2">
                        <button onclick="showNocoTable('pipeline')" id="subtab-pipeline" class="px-3 py-1 bg-blue-600 text-white rounded text-xs">1. Pipeline (31)</button>
                        <button onclick="showNocoTable('regions')" id="subtab-regions" class="px-3 py-1 bg-slate-800 text-slate-300 rounded text-xs">2. Master 85 Régions</button>
                        <button onclick="showNocoTable('eiii')" id="subtab-eiii" class="px-3 py-1 bg-slate-800 text-slate-300 rounded text-xs">3. EIII Scores</button>
                        <button onclick="showNocoTable('gases')" id="subtab-gases" class="px-3 py-1 bg-slate-800 text-slate-300 rounded text-xs">4. Focus Gaz</button>
                        <button onclick="showNocoTable('whatif')" id="subtab-whatif" class="px-3 py-1 bg-slate-800 text-slate-300 rounded text-xs">5. What-If Sanctions</button>
                    </div>
                </div>

                <div id="nocotable-container" class="overflow-x-auto max-h-[600px] custom-scrollbar">
                    <!-- Dynamic Table Content -->
                </div>
            </div>
        </section>

        <!-- TAB 4: DOCUMENTS & MEMORANDUMS -->
        <section id="content-documents" class="tab-content hidden space-y-6">
            <div class="glass-card p-6">
                <div class="flex space-x-2 mb-6 border-b border-slate-800 pb-3">
                    <button onclick="loadDoc('memorandum')" id="docbtn-memorandum" class="px-4 py-2 rounded-lg bg-blue-600/20 text-blue-400 border border-blue-500/30 text-xs font-semibold">🏢 Mémorandum Stratégique 2025-2030</button>
                    <button onclick="loadDoc('playbook')" id="docbtn-playbook" class="px-4 py-2 rounded-lg text-slate-400 hover:bg-slate-800 text-xs font-semibold">📖 Playbook Technique EIII</button>
                    <button onclick="loadDoc('montecarlo')" id="docbtn-montecarlo" class="px-4 py-2 rounded-lg text-slate-400 hover:bg-slate-800 text-xs font-semibold">🎲 Rapport Risque Monte Carlo</button>
                </div>

                <div id="doc-viewer" class="prose max-w-none text-slate-300 text-sm">
                    <!-- Rendered markdown document -->
                </div>
            </div>
        </section>

        <!-- TAB 5: WHAT-IF SIMULATOR -->
        <section id="content-whatif" class="tab-content hidden space-y-6">
            <div class="glass-card p-6 border-l-4 border-l-amber-500">
                <h2 class="text-lg font-bold gradient-gold mb-2">⚡ Simulateur Interactif Monte Carlo — Sanctions 2025-2030</h2>
                <p class="text-xs text-slate-400 mb-6">Ajustez le curseur pour observer la trajectoire des revenus Air Liquide selon le rythme de levée des sanctions économiques.</p>
                
                <div class="bg-slate-900/80 p-5 rounded-xl border border-slate-800 space-y-4">
                    <div class="flex justify-between items-center">
                        <span class="text-sm font-semibold text-slate-300">Année de Scénario : <span id="selected-year" class="text-amber-400 font-bold font-mono">2027</span></span>
                        <span class="text-xs px-3 py-1 bg-amber-500/20 text-amber-300 border border-amber-500/40 rounded-full font-mono" id="scenario-label">Levée Totale (Multiplicateur ×2.0)</span>
                    </div>
                    <input type="range" id="yearSlider" min="2025" max="2030" step="1" value="2027" oninput="updateScenario(this.value)" class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-amber-500">
                    <div class="flex justify-between text-[10px] text-slate-500 font-mono">
                        <span>2025 (Baseline ×1.0)</span>
                        <span>2026 (Partielle ×1.4)</span>
                        <span>2027 (Totale ×2.0)</span>
                        <span>2028 (IDE ×2.8)</span>
                        <span>2030 (Boom ×4.2)</span>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-card p-5">
                    <h3 class="text-base font-bold text-slate-200 mb-4">📈 Trajectoire du Revenu BD (M€/an)</h3>
                    <div class="h-72">
                        <canvas id="chartWhatIfCurve"></canvas>
                    </div>
                </div>

                <div class="glass-card p-5">
                    <h3 class="text-base font-bold text-slate-200 mb-4">🎲 Distribution des Risques (Monte Carlo 10,000 Itérations)</h3>
                    <div class="h-72">
                        <canvas id="chartMonteCarloDist"></canvas>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 6: GAS DEMAND -->
        <section id="content-gases" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-card p-5">
                    <h3 class="text-base font-bold text-slate-200 mb-4">🧪 Scores Relatifs de Demande par Gaz (0-10)</h3>
                    <div class="h-72">
                        <canvas id="chartGasRadar"></canvas>
                    </div>
                </div>

                <div class="glass-card p-5">
                    <h3 class="text-base font-bold text-slate-200 mb-4">🏭 Top Secteurs Consommateurs de Gaz Industriels</h3>
                    <div class="h-72">
                        <canvas id="chartGasSectors"></canvas>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- FOOTER -->
    <footer class="border-t border-slate-800/80 p-6 text-center text-xs text-slate-500 bg-slate-950/60">
        Euroasia Enterprise CRM Command Center &copy; 2026 | Powered by NocoDB MCP Remote Base `p0ygj6vufqhhhsc`
    </footer>

    <!-- SCRIPTS -->
    <script>
        let fullData = null;
        let docsData = null;
        let chartTop10 = null, chartTier = null, chartWhatIf = null, chartMonte = null, chartRadar = null, chartSectors = null;

        async function fetchData() {
            try {
                const res = await fetch('/api/data');
                fullData = await res.json();
                
                const docsRes = await fetch('/api/docs');
                docsData = await docsRes.json();

                renderAll();
                loadDoc('memorandum');
            } catch(e) {
                console.error("Fetch error:", e);
            }
        }

        function switchTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.className = 'tab-btn px-4 py-2 rounded-lg text-slate-400 hover:bg-slate-800';
            });
            document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));

            const activeBtn = document.getElementById('tab-' + tabId);
            if(activeBtn) {
                activeBtn.className = 'tab-btn px-4 py-2 rounded-lg bg-blue-600/20 text-blue-400 border border-blue-500/30';
            }
            const activeContent = document.getElementById('content-' + tabId);
            if(activeContent) activeContent.classList.remove('hidden');
        }

        function renderAll() {
            if(!fullData) return;

            renderTop10Chart();
            renderTierChart();
            renderTop5Table();
            renderKanban();
            showNocoTable('pipeline');
            renderWhatIfCharts();
            renderGasCharts();
        }

        function renderTop10Chart() {
            const ctx = document.getElementById('chartTop10EIII').getContext('2d');
            const regions = (fullData.regions || []).slice(0, 10);
            const labels = regions.map(r => r.Region_Oblast);
            const scores = regions.map(r => parseFloat(r.EIII_Regional_Score) || 0);

            if(chartTop10) chartTop10.destroy();
            chartTop10 = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'EIII Score (0-100)',
                        data: scores,
                        backgroundColor: 'rgba(59, 130, 246, 0.7)',
                        borderColor: '#3b82f6',
                        borderWidth: 1.5,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, max: 100, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 10 } } }
                    }
                }
            });
        }

        function renderTierChart() {
            const ctx = document.getElementById('chartTierDoughnut').getContext('2d');
            const pipeline = fullData.pipeline || [];
            let tier1 = 0, tier2 = 0;
            pipeline.forEach(r => {
                const c = parseFloat(r.Est_CAPEX_Potential_M_EUR) || 0;
                if((r.BD_Priority || '').includes('TIER 1')) tier1 += c;
                else tier2 += c;
            });

            if(chartTier) chartTier.destroy();
            chartTier = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['TIER 1 - Critique', 'TIER 2 - Haute'],
                    datasets: [{
                        data: [tier1.toFixed(1), tier2.toFixed(1)],
                        backgroundColor: ['rgba(239, 68, 68, 0.8)', 'rgba(245, 158, 11, 0.8)'],
                        borderColor: ['#ef4444', '#f59e0b'],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom', labels: { color: '#e2e8f0', font: { size: 11 } } } }
                }
            });
        }

        function renderTop5Table() {
            const tbody = document.getElementById('top5-table-body');
            const pipeline = (fullData.pipeline || []).slice(0, 5);
            tbody.innerHTML = pipeline.map(r => `
                <tr class="hover:bg-slate-800/40">
                    <td class="p-3 text-blue-400 font-bold">${r.Opportunity_ID}</td>
                    <td class="p-3 text-white font-semibold">${r.Region_Oblast}</td>
                    <td class="p-3 text-slate-400">${r.Federal_District}</td>
                    <td class="p-3 text-amber-400 font-bold">${r.EIII_Score}</td>
                    <td class="p-3 text-emerald-400 font-bold">${r.Est_CAPEX_Potential_M_EUR} M€</td>
                    <td class="p-3 text-purple-300">${r.Top_Gas_Product}</td>
                    <td class="p-3 text-slate-400">${r.Key_Clients_Target}</td>
                    <td class="p-3 text-emerald-400 font-bold">${r.Revenue_Post_Sanctions_M_EUR_yr} M€/an</td>
                </tr>
            `).join('');
        }

        function renderKanban() {
            const pipeline = fullData.pipeline || [];
            const t1Col = document.getElementById('kanban-col-tier1');
            const t2Col = document.getElementById('kanban-col-tier2');
            const prCol = document.getElementById('kanban-col-prospect');

            const makeCard = (r) => `
                <div class="glass-card p-3 space-y-2 border-l-2 ${r.BD_Priority.includes('TIER 1') ? 'border-l-red-500' : 'border-l-amber-500'} bg-slate-900/90 text-xs">
                    <div class="flex justify-between items-center font-mono text-[10px]">
                        <span class="text-blue-400 font-bold">${r.Opportunity_ID}</span>
                        <span class="text-amber-400">Score EIII: ${r.EIII_Score}</span>
                    </div>
                    <div class="font-bold text-white">${r.Region_Oblast}</div>
                    <div class="text-slate-400 text-[10px]">District : ${r.Federal_District}</div>
                    <div class="flex justify-between items-center pt-2 border-t border-slate-800 text-[10px]">
                        <span class="text-emerald-400 font-bold">CAPEX : ${r.Est_CAPEX_Potential_M_EUR} M€</span>
                        <span class="text-purple-300">${r.Top_Gas_Product}</span>
                    </div>
                </div>
            `;

            t1Col.innerHTML = pipeline.filter(r => (r.BD_Priority||'').includes('TIER 1')).map(makeCard).join('');
            t2Col.innerHTML = pipeline.filter(r => (r.BD_Priority||'').includes('TIER 2')).map(makeCard).join('');
            prCol.innerHTML = pipeline.slice(0, 10).map(makeCard).join('');
        }

        function showNocoTable(tblType) {
            const container = document.getElementById('nocotable-container');
            if(!fullData) return;

            let headers = [], rows = [];
            if(tblType === 'pipeline') {
                rows = fullData.pipeline || [];
            } else if(tblType === 'regions') {
                rows = fullData.regions || [];
            } else if(tblType === 'eiii') {
                rows = fullData.eiii || [];
            } else if(tblType === 'gases') {
                rows = fullData.sectors || [];
            } else if(tblType === 'whatif') {
                rows = fullData.whatif || [];
            }

            if(rows.length > 0) headers = Object.keys(rows[0]);

            container.innerHTML = `
                <table class="w-full text-left text-xs text-slate-300">
                    <thead class="bg-slate-900 sticky top-0 text-slate-400 uppercase font-semibold text-[10px] z-10">
                        <tr>${headers.map(h => `<th class="p-2 border-b border-slate-800">${h}</th>`).join('')}</tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800/60 font-mono">
                        ${rows.map(r => `
                            <tr class="hover:bg-slate-800/40">
                                ${headers.map(h => `<td class="p-2 truncate max-w-[200px]">${r[h] || ''}</td>`).join('')}
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        }

        function loadDoc(docKey) {
            document.querySelectorAll('[id^="docbtn-"]').forEach(btn => {
                btn.className = 'px-4 py-2 rounded-lg text-slate-400 hover:bg-slate-800 text-xs font-semibold';
            });
            const activeBtn = document.getElementById('docbtn-' + docKey);
            if(activeBtn) {
                activeBtn.className = 'px-4 py-2 rounded-lg bg-blue-600/20 text-blue-400 border border-blue-500/30 text-xs font-semibold';
            }

            if(docsData && docsData[docKey]) {
                document.getElementById('doc-viewer').innerHTML = marked.parse(docsData[docKey]);
            }
        }

        function renderWhatIfCharts() {
            const ctx1 = document.getElementById('chartWhatIfCurve').getContext('2d');
            const years = ['2025', '2026', '2027', '2028', '2030'];
            const revenues = [3.0, 4.2, 6.0, 8.4, 12.6];

            if(chartWhatIf) chartWhatIf.destroy();
            chartWhatIf = new Chart(ctx1, {
                type: 'line',
                data: {
                    labels: years,
                    datasets: [{
                        label: 'Revenu Air Liquide (M€/an)',
                        data: revenues,
                        borderColor: '#fbbf24',
                        backgroundColor: 'rgba(251, 191, 36, 0.15)',
                        fill: true,
                        tension: 0.3,
                        pointRadius: 6,
                        pointBackgroundColor: '#fbbf24'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                    }
                }
            });

            const ctx2 = document.getElementById('chartMonteCarloDist').getContext('2d');
            if(chartMonte) chartMonte.destroy();
            chartMonte = new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: ['P10 (Pessimiste)', 'P50 (Médiane)', 'P90 (Optimiste)'],
                    datasets: [{
                        label: 'Valeur Actuelle Nette (M€)',
                        data: [14.2, 28.5, 45.8],
                        backgroundColor: ['rgba(239, 68, 68, 0.7)', 'rgba(59, 130, 246, 0.7)', 'rgba(16, 185, 129, 0.7)']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } } }
                }
            });
        }

        function updateScenario(val) {
            document.getElementById('selected-year').innerText = val;
            const labels = {
                "2025": "Baseline (Sanctions actives)",
                "2026": "Levée Partielle (Énergie)",
                "2027": "Levée Totale (Contrats)",
                "2028": "Reprise des IDE",
                "2030": "Boom Post-Réintégration"
            };
            document.getElementById('scenario-label').innerText = labels[val] || '';
        }

        function renderGasCharts() {
            const ctx1 = document.getElementById('chartGasRadar').getContext('2d');
            if(chartRadar) chartRadar.destroy();
            chartRadar = new Chart(ctx1, {
                type: 'radar',
                data: {
                    labels: ['Oxygène (O₂)', 'Azote (N₂)', 'Hydrogène (H₂)', 'Dioxyde de Carbone (CO₂)', 'Argon (Ar)'],
                    datasets: [{
                        label: 'Intensité de Demande',
                        data: [9.5, 9.2, 8.8, 7.4, 6.1],
                        borderColor: '#a78bfa',
                        backgroundColor: 'rgba(167, 139, 250, 0.2)',
                        pointBackgroundColor: '#a78bfa'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { r: { grid: { color: 'rgba(255,255,255,0.1)' }, angleLines: { color: 'rgba(255,255,255,0.1)' }, ticks: { display: false } } }
                }
            });

            const ctx2 = document.getElementById('chartGasSectors').getContext('2d');
            if(chartSectors) chartSectors.destroy();
            chartSectors = new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: ['Métallurgie Lourde', 'Pétrochimie / Chimie', 'Énergie & Gaz', 'Agro-alimentaire'],
                    datasets: [{
                        label: 'Consommation Estimée (Mrd ₽)',
                        data: [1420, 980, 750, 310],
                        backgroundColor: 'rgba(96, 165, 250, 0.8)',
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } } }
                }
            });
        }

        window.onload = fetchData;
    </script>
</body>
</html>
"""

def run_server():
    server = socketserver.TCPServer(("", PORT), NocoDBDashboardHandler)
    print(f"\n==================================================")
    print(f" 🚀 ENTERPRISE CRM COMMAND CENTER RUNNING")
    print(f" URL: http://localhost:{PORT}")
    print(f"==================================================\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()

if __name__ == "__main__":
    run_server()
