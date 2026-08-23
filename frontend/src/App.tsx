import { useEffect, useState } from "react";

type Case = {
  id: number;
  brand: string;
  model: string;
  form_factor: string;
}; // we do this because tsx doesnt know the data types used below
type CPU = {
    id: number;
    brand: string;
    model: string;
};
type MB = {
    id: number;
    brand: string;
    model: string;   
};
type RAM = {
    id: number;
    brand: string;
    model: string;   
};
type GPU = {
    id: number;
    brand: string;
    model: string;   
};
type PSU = {
    id: number;
    brand: string;
    model: string;   
};
type COOL = {
    id: number;
    brand: string;
    model: string;   
};
type STORE = {
    id: number;
    brand: string;
    model: string;   
};

function App() {
    // To fetch the display of each item
    const [cases, setCases] = useState<Case[]>([]);
    const [cpus, setCPUs] = useState<CPU[]>([]);
    const [mbs, setMBs] = useState<MB[]>([]);
    const [gpus, setGPUs] = useState<GPU[]>([]);
    const [rams, setRAMs] = useState<RAM[]>([]);
    const [psus, setPSUs] = useState<PSU[]>([]);
    const [cools, setCLRs] = useState<COOL[]>([]);
    const [store, setStores] = useState<STORE[]>([]);
    const [loading, setLoad] = useState<boolean>(true);

    // To click each item and change the colour
    const [selectedCase,setSelectedCase] = useState<number | null>(null);
    const [selectedCPU,setSelectedCPU] = useState<number | null>(null);
    const [selectedGPU,setSelectedGPU] = useState<number | null>(null);
    const [selectedMB,setSelectedMB] = useState<number | null>(null);
    const [selectedRAM,setSelectedRAM] = useState<number | null>(null);
    const [selectedStore,setSelectedStore] = useState<number | null>(null);
    const [selectedCool,setSelectedCool] = useState<number | null>(null);
    const [selectedPSU,setSelectedPSU] = useState<number | null>(null);

    // To save the selected items and send the id back
     

    useEffect(() => {
        Promise.all([fetch("/api/cases"),
                    fetch("/api/cpus"),
                    fetch("/api/gpus"),
                    fetch("/api/rams"),
                    fetch("/api/motherboards"),
                    fetch("/api/storage"),
                    fetch("/api/cooler"),
                    fetch("/api/psu")
                ])
        .then(([casesResponse, cpusResponse, gpusResponse, ramsResponse,mbsResponse,storeResponse,coolsResponse,psusResponse]) => {
        return Promise.all([casesResponse.json(), cpusResponse.json(),gpusResponse.json(), ramsResponse.json(), mbsResponse.json(), storeResponse.json(), coolsResponse.json(), psusResponse.json()]);
        })
        .then(([casesData, cpusData, gpusData, ramsData, mbsData, storesData, coolsData, psusData]) => {
            setCases(casesData);
            setCPUs(cpusData);
            setGPUs(gpusData);
            setRAMs(ramsData);
            setMBs(mbsData);
            setStores(storesData);
            setCLRs(coolsData);
            setPSUs(psusData);
            setLoad(false);
        })
        .catch(error => {
            console.error("Error connecting to server: ",error);
            setLoad(false);
        });
    },
    []);

    async function check(){
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
        try{
            const response = await fetch('/api/check',{
                method: 'POST',
                headers: {
                    'Content-type': 'application/json',
                },
                body: JSON.stringify(selectedBuild),
            });
            const result = await response.json();
            console.log("Server response:", result);
            // Reset the selected items after clicking submit button
            setSelectedCase(null);
            setSelectedCPU(null);
            setSelectedGPU(null);
            setSelectedMB(null);
            setSelectedRAM(null);
            setSelectedStore(null);
            setSelectedCool(null);
            setSelectedPSU(null);

        } catch (error){
            console.error("Error sending selected build:", error);
        }

    }
    async function save(){
        console.log("hi");
    }
    if(loading){
        return(
            <div>
                <h3>Connecting to the database server...</h3>
            </div>
        )
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
                            onClick = {() => setSelectedCase(pcCase.id)}
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
                            onClick = {() => setSelectedCPU(pcCPU.id)}
                        >
                            {pcCPU.brand} {pcCPU.model}
                        </p>
                    ))
                ) : (
                    <p>Loading or no cases found...</p>
                )}
                </div>
                <div className="parts">
                    <h2>GPU</h2>
                    {Array.isArray(gpus) && gpus.length > 0 ? (
                    gpus.map((pcGPU) => (
                        <p 
                            key={pcGPU.id} 
                            className={`partItems ${selectedGPU === pcGPU.id ? 'selected' : ''}`}
                            onClick = {() => setSelectedGPU(pcGPU.id)}
                        >
                            {pcGPU.brand} {pcGPU.model}
                        </p>
                    ))
                ) : (
                    <p>Loading or no cases found...</p>
                )}
                </div>
                <div className="parts">
                    <h2>Motherboard</h2>
                    {Array.isArray(mbs) && mbs.length > 0 ? (
                    mbs.map((pcCPU) => (
                        <p 
                            key={pcCPU.id} 
                            className={`partItems ${selectedMB === pcCPU.id ? 'selected' : ''}`}
                            onClick = {() => setSelectedMB(pcCPU.id)}
                        >
                            {pcCPU.brand} {pcCPU.model}
                        </p>
                    ))
                ) : (
                    <p>Loading or no cases found...</p>
                )}
                </div>
                <div className="parts">
                    <h2>RAM</h2>
                    {Array.isArray(rams) && rams.length > 0 ? (
                    rams.map((pcCPU) => (
                        <p 
                            key={pcCPU.id} 
                            className={`partItems ${selectedRAM === pcCPU.id ? 'selected' : ''}`}
                            onClick = {() => setSelectedRAM(pcCPU.id)}
                        >
                            {pcCPU.brand} {pcCPU.model}
                        </p>
                    ))
                ) : (
                    <p>Loading or no cases found...</p>
                )}
                </div>
                <div className="parts">
                    <h2>Storage</h2>
                    {Array.isArray(store) && store.length > 0 ? (
                    store.map((pcCPU) => (
                        <p 
                            key={pcCPU.id} 
                            className={`partItems ${selectedStore === pcCPU.id ? 'selected' : ''}`}
                            onClick = {() => setSelectedStore(pcCPU.id)}
                        >
                            {pcCPU.brand} {pcCPU.model}
                        </p>
                    ))
                ) : (
                    <p>Loading or no cases found...</p>
                )}
                </div>
                <div className="parts">
                    <h2>CPU Cooler</h2>
                    {Array.isArray(cools) && cools.length > 0 ? (
                    cools.map((pcCPU) => (
                        <p 
                            key={pcCPU.id} 
                            className={`partItems ${selectedCool === pcCPU.id ? 'selected' : ''}`}
                            onClick = {() => setSelectedCool(pcCPU.id)}
                        >
                            {pcCPU.brand} {pcCPU.model}
                        </p>
                    ))
                ) : (
                    <p>Loading or no cases found...</p>
                )}
                </div>
                <div className="parts">
                    <h2>PSU</h2>
                    {Array.isArray(psus) && psus.length > 0 ? (
                    psus.map((pcCPU) => (
                        <p 
                            key={pcCPU.id} 
                            className={`partItems ${selectedPSU === pcCPU.id ? 'selected' : ''}`}
                            onClick = {() => setSelectedPSU(pcCPU.id)}
                        >
                            {pcCPU.brand} {pcCPU.model}
                        </p>
                    ))
                ) : (
                    <p>Loading or no cases found...</p>
                )}
                </div>

                <div className="forms">
                    <form onSubmit={(e) => {e.preventDefault();check();}}>
                        <button type="submit" className="smt-btn">Check Compatibility</button>
                    </form>
                    <form onSubmit={(e) => {e.preventDefault();save();}}>
                        <button type="submit" className="smt-btn">Save Build</button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default App; 