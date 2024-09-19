from pathlib import Path
from typing import Annotated, List, Any
from uuid import UUID
from .dirs import create_workspaces_dir, get_hierarchical_structure
from .workspaces import Workspace, WorkspaceConfig
from .config import ConfigLoader, Config
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from .modules import get_modules
from .df_logging import logger

# Load the global config
config_loader = ConfigLoader()
ConfigDep = Annotated[Config, Depends(config_loader)]

async def current_workspace(config: ConfigDep, workspace_id: UUID) -> Workspace:
    return Workspace(config, id = workspace_id)

WorkspaceDep = Annotated[Workspace, Depends(current_workspace)]

router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def read_root():
    return {"Hello": "World"}

@router.get("/workspaces")
async def list_workspaces(config: ConfigDep):
    create_workspaces_dir(config)

    workspaces_raw: List[UUID] = Workspace.list(config)
    workspaces = []
    for workspace_id in workspaces_raw:
        workspaces.append(Workspace(config, id = workspace_id))

    return workspaces

class CreateWorkspaceRequest(BaseModel):
    name: str

@router.post("/workspaces")
async def create_workspace(request: CreateWorkspaceRequest, config: ConfigDep):
    workspace = Workspace(config, name=request.name)
    return workspace


@router.get("/workspaces/{workspace_id}")
async def read_workspace(workspace_id: UUID, workspace: WorkspaceDep, config: ConfigDep):
    return workspace

@router.delete("/workspaces/{workspace_id}")
async def delete_workspace(config: ConfigDep, workspace: WorkspaceDep):
    workspace.delete()
    return {"workspace": workspace.id}

@router.get("/workspaces/{workspace_id}/evidence")
async def list_evidence(config: ConfigDep, workspace: WorkspaceDep):
    evidence_folder = config.workspaces_path / Path(str(workspace.id)) / Path("evidence")
    contents = get_hierarchical_structure(evidence_folder)
    return {"evidence": contents}

@router.get("/modules")
async def list_modules(config: ConfigDep):
    modules = get_modules(config)
    names = []

    for module in modules:
        names.append({'name': module.name, 'type': module.module_type})

    return {"modules": names}

class RenderBody(BaseModel):
    investigator_name: str
    case_number: int
    start_date: str
    modules: List[str]
    evidence: str

async def render_body(investigator_name: str = "", case_number: int = 0, start_date: str = "", modules: Annotated[List[str], Query()] = [], evidence: str = ""):
    return RenderBody(
        investigator_name = investigator_name,
        case_number = case_number,
        start_date = start_date,
        modules = modules,
        evidence = evidence
    )

@router.get("/workspaces/{workspace_id}/render", response_class=HTMLResponse)
async def render_report(workspace_id, request: Request, config: ConfigDep, workspace: WorkspaceDep, body: Annotated[dict, Depends(render_body)]):
    modules = get_modules(config)
    using = []
    for u_module in body.modules:
        for module in modules:
            if module.name == u_module:
                using.append(module)


    evidence_folder = config.workspaces_path / Path(str(workspace_id)) / Path("evidence")
    ingest_output: (Any, str) = (None, "")

    for module in using:
        if module.module_type == "IngestModule":
            logger.info(module.module.Ingest().file_types())
            if body.evidence.split('.')[-1] in module.module.Ingest().file_types():
                # Ingest here
                ingest_output = (module.module.Ingest().ingest(evidence_folder / Path(body.evidence)), body.evidence.split('.')[-1])


    analysis_output: (Any, str) = (None, "")

    for module in using:
        if module.module_type == "AnalysisModule":
            logger.info(module.module.Analysis().input_data_structures())
            if ingest_output[1] in module.module.Analysis().input_data_structures():
                # Analyse here
                analysis_output = (module.module.Analysis().analyze(ingest_output[0]), module.module.Analysis().output_data_structures()[0])

    report_output: (Any, str) = (None, "")

    for module in using:
        if module.module_type == "ReportModule":
            if analysis_output[1] in module.module.Report().input_data_structures():
                # Analyse here
                report_output = (module.module.Report().report(analysis_output[0]), '')

    # Render report
    return templates.TemplateResponse(
        request=request, name="report.html", context={'investigator_name': body.investigator_name, 'case_number': body.case_number, 'start_date': body.start_date, 'evidence': body.evidence, 'head': report_output[0]['head'], 'body': report_output[0]['body']}
    )