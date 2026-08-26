from fastapi import FastAPI
from .database import sessionLocal

from .models import Case,Motherboard,RAM,CPU,GPU,Storage,CPUCooler,PSU

from .compatibility import (check_case_motherboard,check_cpu_motherboard,check_ram_motherboard,check_gpu_case,check_gpu_motherboard,check_storage_motherboard,check_cooler_cpu,check_cooler_case,check_psu_case,check_psu_gpu)

from .schemas import PCSelection

from fastapi.middleware.cors import CORSMiddleware # this is the import for the not understood part 

from ml.src.predict import predict_price

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) # what does this do did it because the api was working but frontend site wasnt showing anything ans - allow the website running at localhost:5173 to make requests to fastapi

@app.get("/")
def home():
    return {"message" : "Connected"}

@app.get("/cases")
def get_parts():
    db = sessionLocal()
    result = db.query(Case).all()
    cases = []

    for case in result:
        cases.append({
            "id":case.id,
            "brand":case.brand,
            "model":case.model,
            "form_factor":case.form_factor
        })
    db.close()

    return cases

@app.get("/motherboards")
def get_parts():
    db = sessionLocal()
    result = db.query(Motherboard).all()
    mbs = []

    for mb in result:
        mbs.append({
            "id":mb.id,
            "brand":mb.brand,
            "model":mb.model,
            "form_factor":mb.form_factor
        })
    db.close()

    return mbs

@app.get("/cpus")
def get_parts():
    db = sessionLocal()
    result = db.query(CPU).all()
    cpus = []

    for cpu in result:
        cpus.append({
            "id":cpu.id,
            "brand":cpu.brand,
            "model":cpu.model
        })
    db.close()

    return cpus

@app.get("/rams")
def get_parts():
    db = sessionLocal()
    result = db.query(RAM).all()
    rams = []

    for ram in result:
        rams.append({
            "id":ram.id,
            "brand":ram.brand,
            "model":ram.model,
            "ram_type":ram.ram_type
        })
    db.close()

    return rams

@app.get("/gpus")
def get_parts():
    db = sessionLocal()
    result = db.query(GPU).all()
    gpus = []

    for gpu in result:
        gpus.append({
            "id":gpu.id,
            "brand":gpu.brand,
            "model":gpu.model,
        })
    db.close()

    return gpus

@app.get("/storage")
def get_parts():
    db = sessionLocal()
    result = db.query(Storage).all()
    storages = []

    for storage in result:
        storages.append({
            "id":storage.id,
            "brand":storage.brand,
            "model":storage.model,
            "storage_type":storage.storage_type
        })
    db.close()

    return storages

@app.get("/cooler")
def get_parts():
    db = sessionLocal()
    result = db.query(CPUCooler).all()
    coolers = []

    for cooler in result:
        coolers.append({
            "id":cooler.id,
            "brand":cooler.brand,
            "model":cooler.model,
        })
    db.close()

    return coolers

@app.get("/psu")
def get_parts():
    db = sessionLocal()
    result = db.query(PSU).all()
    psus = []

    for psu in result:
        psus.append({
            "id":psu.id,
            "brand":psu.brand,
            "model":psu.model,
        })
    db.close()

    return psus

@app.post("/check")
def check_compatibility(selection: PCSelection):
    db = sessionLocal()

    case = db.query(Case).filter(Case.id == selection.case_id).first()
    motherboard = db.query(Motherboard).filter(Motherboard.id == selection.motherboard_id).first()
    cpu = db.query(CPU).filter(CPU.id == selection.cpu_id).first()
    ram = db.query(RAM).filter(RAM.id == selection.ram_id).first()
    gpu = db.query(GPU).filter(GPU.id == selection.gpu_id).first()
    storage = db.query(Storage).filter(Storage.id == selection.storage_id).first()
    cooler = db.query(CPUCooler).filter(CPUCooler.id == selection.cooler_id).first()
    psu = db.query(PSU).filter(PSU.id == selection.psu_id).first()


    if any(x is None for x in [case, motherboard, cpu, ram, gpu, storage, cooler, psu]):
        missing = []
        if case is None:
            missing.append("case")
        if motherboard is None:
            missing.append("motherboard")
        if cpu is None:
            missing.append("cpu")
        if ram is None:
            missing.append("ram")
        if gpu is None:
            missing.append("gpu")
        if storage is None:
            missing.append("storage")
        if cooler is None:
            missing.append("cooler")
        if psu is None:
            missing.append("psu")
        return {
            "error":"Crucial component missing!",
            "missing":missing
            }
    
    case_motherboard = check_case_motherboard(case, motherboard)
    cpu_motherboard = check_cpu_motherboard(cpu, motherboard)
    ram_motherboard = check_ram_motherboard(ram, motherboard)
    gpu_case = check_gpu_case(gpu, case)
    gpu_motherboard = check_gpu_motherboard(gpu, motherboard)
    storage_motherboard = check_storage_motherboard(storage, motherboard)
    cooler_cpu = check_cooler_cpu(cooler, cpu)
    cooler_case = check_cooler_case(cooler, case)
    psu_case = check_psu_case(psu, case)
    psu_gpu = check_psu_gpu(psu, gpu)

    compatible = all([
        case_motherboard,
        cpu_motherboard,
        ram_motherboard,
        gpu_case,
        gpu_motherboard,
        storage_motherboard,
        cooler_cpu,
        cooler_case,
        psu_case,
        psu_gpu
    ])

    issues = []
    if case_motherboard is False:
        issues.append("Motherboard does not fit case")
    if cpu_motherboard is False:
        issues.append("CPU and Motherboard not compatible")
    if ram_motherboard is False:
        issues.append("RAM and Motherboard not compatible")
    if gpu_case is False:
        issues.append("GPU does not fit case")
    if gpu_motherboard is False:
        issues.append("GPU and Motherboard not compatible")
    if storage_motherboard is False:
        issues.append("Storage and Motherboard not compatible")
    if cooler_cpu is False:
        issues.append("CPU and CPU Cooler not compatible")
    if cooler_case is False:
        issues.append("Cooler too big for case")
    if psu_case is False:
        issues.append("PSU and Case not compatible")
    if psu_gpu is False:
        issues.append("PSU and GPU not compatible")
        
    db.close()

    return {
        "compatible":compatible,
        "checks":{
            "case_motherboard":case_motherboard,
            "cpu_motherboard":cpu_motherboard,
            "ram_motherboard":ram_motherboard,
            "gpu_case":gpu_case,
            "gpu_motherboard":gpu_motherboard,
            "storage_motherboard":storage_motherboard,
            "cooler_cpu":cooler_cpu,
            "cooler_case":cooler_case,
            "psu_case":psu_case,
            "psu_gpu":psu_gpu
        },
        "issues":issues
    }

@app.get("/predict")
def prediction():

    results = predict_price("ml/data/raw/ramradar-price-index.csv")

    return results.to_dict(orient="records")
