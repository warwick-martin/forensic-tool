import {MetaFunction} from "@remix-run/node";
import {Form, useNavigate} from "@remix-run/react";

export const meta: MetaFunction = () => {
  return [
    {title: "New Remix App"},
    {name: "description", content: "Welcome to Remix!"},
  ];
};

export default function Index() {
  const navigate = useNavigate();
  return (
    <div className={"flex flex-col space-y-2"}>
      <nav className={"flex flex-row space-x-2 h-12 bg-gray-400 items-center justify-center"}>
        <span>Drone Forensic Tool</span>
      </nav>
      <main className={"w-1/3 mx-auto flex flex-col space-y-2 border-2 border-black rounded-lg border-solid p-3"}>
        <button onClick={() => {
          navigate(`/workspaces`)
        }} className={"border-2 border-blue-800 bg-blue-400 hover:bg-blue-500 rounded-lg"}>Select Existing Workspace
        </button>
        <hr/>
        <Form method="post" className={"flex flex-col space-y-1"}>
          <label htmlFor={"workspaceName"}>Workspace Name: </label>
          <input name={"workspaceName"} id={"workspaceName"} type={"text"}
                 className={"border-2 border-black rounded-lg p-0.5"}></input>
          <br/>
          <button type={"submit"} className={"border-2 border-blue-800 bg-blue-400 hover:bg-blue-500 rounded-lg"}>Create
            New Workspace
          </button>
        </Form>
      </main>
    </div>
  );
}
