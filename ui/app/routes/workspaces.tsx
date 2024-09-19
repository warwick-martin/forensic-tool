import {json} from "@remix-run/node";
import {Link, Outlet, useLoaderData, useNavigate, useParams} from "@remix-run/react";

interface WorkspacesResponse {
  workspaces: [Workspace]
}

export async function loader() {
  const res: Promise<WorkspacesResponse> = fetch("http://localhost:8000/workspaces").then(res => res.json())
  return json({workspaces: await res})
}

export default function Index() {
  const {workspaces} = useLoaderData<typeof loader>()
  const navigate = useNavigate();
  const params = useParams();
  return (
    <div className={"flex flex-col space-y- h-full"}>
      <nav className={"flex flex-row space-x-2 h-12 bg-gray-400 items-center justify-center"}>
        <label htmlFor={"workspaceSelector"}>Workspace</label>
        <select name={"workspaceSelector"} id={"workspaceSelector"}
                value={workspaces.find((workspace: Workspace) => workspace.id == params.workspace)?.workspace_config._name || "none"}
                onChange={(event) => {
                  if (event.target !== null) {
                    const select = event.target as HTMLSelectElement;
                    const key = select.options[select.selectedIndex].getAttribute("id")
                    if (key === null) {
                      navigate(`/workspaces`)
                    } else {
                      navigate(`/workspaces/${key}`)
                    }
                  }
                }}>
          <option value={"none"}>None</option>
          {workspaces.map((workspace: Workspace) => {
            return <option key={workspace.id} id={workspace.id}>{workspace.workspace_config._name}</option>
          })}
        </select>
      </nav>
      <main className={"px-2 h-full"}>
        {params.workspace !== undefined ? <Outlet/> :
          <h1>Select a workspace using the dropdown above or go <Link to={"/"}
                                                                      className={"underline hover:text-blue-700 text-blue-400"}>here</Link> to
            create a new one.</h1>}
      </main>
    </div>
  );
}
