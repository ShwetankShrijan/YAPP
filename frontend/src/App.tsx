import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

type Case = { id: number; brand: string; model: string; form_factor: string; };
type CPU = { id: number; brand: string; model: string; };
type MB = { id: number; brand: string; model: string; };
type RAM = { id: number; brand: string; model: string; };
type GPU = { id: number; brand: string; model: string; };
type PSU = { id: number; brand: string; model: string; };
type COOL = { id: number; brand: string; model: string; };
type STORE = { id: number; brand: string; model: string; };

type Prediction = {
    date: string;
    ram_type: string;
    form_factor: string;
    actual_price: number;
    predicted_price: number;
};

function App() {
    const [cases, setCases] = useState<Case[]>([]);
    const [cpus, setCPUs] = useState<CPU[]>([]);
    const [mbs, setMBs] = useState<MB[]>([]);
    const [gpus, setGPUs] = useState<GPU[]>([]);
    const [rams, setRAMs] = useState<RAM[]>([]);
    const [psus, setPSUs] = useState<PSU[]>([]);
    const [cools, setCLRs] = useState<COOL[]>([]);
    const [store, setStores] = useState<STORE[]>([]);
    const [loading, setLoad] = useState<boolean>(true);

    const [selectedCase, setSelectedCase] = useState<number | null>(null);
    const [selectedCPU, setSelectedCPU] = useState<number | null>(null);
    const [selectedGPU, setSelectedGPU] = useState<number | null>(null);
    const [selectedMB, setSelectedMB] = useState<number | null>(null);
    const [selectedRAM, setSelectedRAM] = useState<number | null>(null);
    const [selectedStore, setSelectedStore] = useState<number | null>(null);
    const [selectedCool, setSelectedCool] = useState<number | null>(null);
    const [selectedPSU, setSelectedPSU] = useState<number | null>(null);

    // Filter states for chart
    const [selectedRamType, setSelectedRamType] = useState<string>("ddr4");
    const [selectedFormFactor, setSelectedFormFactor] = useState<string>("dimm");

    // ML Predictions
    const [predictions, setPredictions] = useState<Prediction[]>([]);

    useEffect(() => {
        Promise.all([
            fetch("/api/cases"),
            fetch("/api/cpus"),
            fetch("/api/gpus"),
            fetch("/api/rams"),
            fetch("/api/motherboards"),
            fetch("/api/storage"),
            fetch("/api/cooler"),
            fetch("/api/psu"),
            fetch("/api/predict")
        ])
        .then(([casesRes, cpusRes, gpusRes, ramsRes, mbsRes, storeRes, coolsRes, psusRes, predictRes]) => {
            return Promise.all([
                casesRes.json(), cpusRes.json(), gpusRes.json(), ramsRes.json(),
                mbsRes.json(), storeRes.json(), coolsRes.json(), psusRes.json(), predictRes.json()
            ]);
        })
        .then(([casesData, cpusData, gpusData, ramsData, mbsData, storesData, coolsData, psusData, predictData]) => {
            setCases(casesData);
            setCPUs(cpusData);
            setGPUs(gpusData);
            setRAMs(ramsData);
            setMBs(mbsData);
            setStores(storesData);
            setCLRs(coolsData);
            setPSUs(psusData);
            setPredictions(predictData);
            setLoad(false);
        })
        .catch(error => {
            console.error("Error connecting to server: ", error);
            setLoad(false);
        });
    }, []);

    async function check() {
        const selectedBuild = {
            caseID: selectedCase,
            cpuID: selectedCPU,
            mbID: selectedMB,
            gpuID: selectedGPU,
            ramID: selectedRAM,
            storID: selectedStore,
            coolID: selectedCool,
            psuID: selectedPSU
        };
        try {
            const response = await fetch('/api/check', {
                method: 'POST',
                headers: { 'Content-type': 'application/json' },
                body: JSON.stringify(selectedBuild),
            });
            const result = await response.json();
            console.log("Server response:", result);
            setSelectedCase(null);
            setSelectedCPU(null);
            setSelectedGPU(null);
            setSelectedMB(null);
            setSelectedRAM(null);
            setSelectedStore(null);
            setSelectedCool(null);
            setSelectedPSU(null);
        } catch (error) {
            console.error("Error sending selected build:", error);
        }
    }

    async function save() {
        console.log("hi");
    }

    // Filter predictions by selected ram_type & form_factor, then sort chronologically
    const filteredAndSortedPredictions = predictions
        .filter(
            (p) =>
                p.ram_type.toLowerCase() === selectedRamType.toLowerCase() &&
                p.form_factor.toLowerCase() === selectedFormFactor.toLowerCase()
        )
        .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

    if (loading) {
        return (
            <div>
                <h3>Connecting to the database server...</h3>
            </div>
        );
    }

    return (
        <div>
            <nav className="navbar">
                <div className="nav-logo">
                    <h1>BuildForge</h1>
                    <h3>Price Analyzer and Compatibility Checker</h3>
                </div>
                <ul className="nav-links">
                    <li><a href="#parts">Parts</a></li>
                    <li><a href="#analyzer">Analyzer</a></li>
                    <li><a href="#saved">Saved Builds</a></li>
                </ul>
            </nav>

            <div id="compat">
                <h2>Build PC</h2>
            </div>
            <div className="grid-container">
                <div className="parts">
                    <h2>Case</h2>
                    {Array.isArray(cases) && cases.length > 0 ? (
                        cases.map((pcCase) => (
                            <p 
                                key={pcCase.id} 
                                className={`partItems ${selectedCase === pcCase.id ? 'selected' : ''}`}
                                onClick={() => setSelectedCase(pcCase.id)}
                            >
                                {pcCase.brand} {pcCase.model}
                            </p>
                        ))
                    ) : (
                        <p>Loading or no cases found...</p>
                    )}
                </div>

                <div className="parts">
                    <h2>CPU</h2>
                    {Array.isArray(cpus) && cpus.length > 0 ? (
                        cpus.map((pcCPU) => (
                            <p 
                                key={pcCPU.id} 
                                className={`partItems ${selectedCPU === pcCPU.id ? 'selected' : ''}`}
                                onClick={() => setSelectedCPU(pcCPU.id)}
                            >
                                {pcCPU.brand} {pcCPU.model}
                            </p>
                        ))
                    ) : (
                        <p>Loading or no CPUs found...</p>
                    )}
                </div>

                <div className="parts">
                    <h2>GPU</h2>
                    {Array.isArray(gpus) && gpus.length > 0 ? (
                        gpus.map((pcGPU) => (
                            <p 
                                key={pcGPU.id} 
                                className={`partItems ${selectedGPU === pcGPU.id ? 'selected' : ''}`}
                                onClick={() => setSelectedGPU(pcGPU.id)}
                            >
                                {pcGPU.brand} {pcGPU.model}
                            </p>
                        ))
                    ) : (
                        <p>Loading or no GPUs found...</p>
                    )}
                </div>

                <div className="parts">
                    <h2>Motherboard</h2>
                    {Array.isArray(mbs) && mbs.length > 0 ? (
                        mbs.map((pcMB) => (
                            <p 
                                key={pcMB.id} 
                                className={`partItems ${selectedMB === pcMB.id ? 'selected' : ''}`}
                                onClick={() => setSelectedMB(pcMB.id)}
                            >
                                {pcMB.brand} {pcMB.model}
                            </p>
                        ))
                    ) : (
                        <p>Loading or no motherboards found...</p>
                    )}
                </div>

                <div className="parts">
                    <h2>RAM</h2>
                    {Array.isArray(rams) && rams.length > 0 ? (
                        rams.map((pcRAM) => (
                            <p 
                                key={pcRAM.id} 
                                className={`partItems ${selectedRAM === pcRAM.id ? 'selected' : ''}`}
                                onClick={() => setSelectedRAM(pcRAM.id)}
                            >
                                {pcRAM.brand} {pcRAM.model}
                            </p>
                        ))
                    ) : (
                        <p>Loading or no RAM found...</p>
                    )}
                </div>

                <div className="parts">
                    <h2>Storage</h2>
                    {Array.isArray(store) && store.length > 0 ? (
                        store.map((pcStore) => (
                            <p 
                                key={pcStore.id} 
                                className={`partItems ${selectedStore === pcStore.id ? 'selected' : ''}`}
                                onClick={() => setSelectedStore(pcStore.id)}
                            >
                                {pcStore.brand} {pcStore.model}
                            </p>
                        ))
                    ) : (
                        <p>Loading or no storage found...</p>
                    )}
                </div>

                <div className="parts">
                    <h2>CPU Cooler</h2>
                    {Array.isArray(cools) && cools.length > 0 ? (
                        cools.map((pcCool) => (
                            <p 
                                key={pcCool.id} 
                                className={`partItems ${selectedCool === pcCool.id ? 'selected' : ''}`}
                                onClick={() => setSelectedCool(pcCool.id)}
                            >
                                {pcCool.brand} {pcCool.model}
                            </p>
                        ))
                    ) : (
                        <p>Loading or no coolers found...</p>
                    )}
                </div>

                <div className="parts">
                    <h2>PSU</h2>
                    {Array.isArray(psus) && psus.length > 0 ? (
                        psus.map((pcPSU) => (
                            <p 
                                key={pcPSU.id} 
                                className={`partItems ${selectedPSU === pcPSU.id ? 'selected' : ''}`}
                                onClick={() => setSelectedPSU(pcPSU.id)}
                            >
                                {pcPSU.brand} {pcPSU.model}
                            </p>
                        ))
                    ) : (
                        <p>Loading or no PSUs found...</p>
                    )}
                </div>

                <div className="forms">
                    <form onSubmit={(e) => { e.preventDefault(); check(); }}>
                        <button type="submit" className="smt-btn">Check Compatibility</button>
                    </form>
                    <form onSubmit={(e) => { e.preventDefault(); save(); }}>
                        <button type="submit" className="smt-btn">Save Build</button>
                    </form>
                </div>
            </div>

            <div className="predict_head">
                <h2>Ram Price Predictions</h2>
            </div>

            {/* Filter Buttons Controls */}
            <div className="filter-container" style={{ display: 'flex', gap: '20px', justifyContent: 'center', marginBottom: '15px' }}>
                <div className="filter-group">
                    <span style={{ marginRight: '8px', fontWeight: 'bold' }}>Type:</span>
                    <button 
                        className={`smt-btn ${selectedRamType === 'ddr4' ? 'selected' : ''}`}
                        onClick={() => setSelectedRamType('ddr4')}
                        style={{ marginRight: '5px' }}
                    >
                        DDR4
                    </button>
                    <button 
                        className={`smt-btn ${selectedRamType === 'ddr5' ? 'selected' : ''}`}
                        onClick={() => setSelectedRamType('ddr5')}
                    >
                        DDR5
                    </button>
                </div>

                <div className="filter-group">
                    <span style={{ marginRight: '8px', fontWeight: 'bold' }}>Form Factor:</span>
                    <button 
                        className={`smt-btn ${selectedFormFactor === 'dimm' ? 'selected' : ''}`}
                        onClick={() => setSelectedFormFactor('dimm')}
                        style={{ marginRight: '5px' }}
                    >
                        DIMM
                    </button>
                    <button 
                        className={`smt-btn ${selectedFormFactor === 'sdimm' ? 'selected' : ''}`}
                        onClick={() => setSelectedFormFactor('sdimm')}
                    >
                        SO-DIMM
                    </button>
                </div>
            </div>

            <div className="graph">
                <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={filteredAndSortedPredictions}>
                        <CartesianGrid strokeDasharray="3 3" />

                        <XAxis
                            dataKey="date"
                            tick={{ fontSize: 12 }}
                            tickFormatter={(str) => {
                                const d = new Date(str);
                                return isNaN(d.getTime()) ? str : d.toLocaleDateString();
                            }}
                        />

                        <YAxis
                            tick={{ fontSize: 12 }}
                            domain={["auto", "auto"]}
                        />

                        <Tooltip
                            formatter={(value, name) => [
                                `$${Number(value).toFixed(4)}`,
                                name === "actual_price" ? "Actual Price" : "Predicted Price"
                            ]}
                            labelFormatter={(label) => new Date(String(label)).toLocaleDateString()}
                        />

                        <Legend
                            formatter={(value) =>
                                value === "actual_price"
                                    ? "Actual Price"
                                    : "Predicted Price"
                            }
                        />

                        <Line
                            type="monotone"
                            dataKey="actual_price"
                            stroke="#22c55e"
                            strokeWidth={2}
                            dot={false}
                            activeDot={{ r: 5 }}
                            isAnimationActive={false}
                        />

                        <Line
                            type="monotone"
                            dataKey="predicted_price"
                            stroke="#ef4444"
                            strokeWidth={2}
                            dot={false}
                            activeDot={{ r: 5 }}
                            isAnimationActive={false}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

export default App;