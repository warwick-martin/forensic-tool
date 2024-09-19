import {Form, useActionData, useLoaderData} from "@remix-run/react";
import {ActionFunctionArgs, json, LoaderFunctionArgs} from "@remix-run/node";
import Evidence from "~/routes/workspaces.$workspace.evidence";
import {useState} from "react";
import Module from "~/routes/modules";

interface ReportForm {
  investigator_name: string;
  case_number: number;
  start_date: string;
  modules: string[];
  evidence: string;
}

export async function action({request, params}: ActionFunctionArgs) {
  const body = await request.formData();
  const ReportForm: ReportForm = {
    investigator_name: body.get("investigator_name") as string,
    case_number: +(body.get("case_number") as string),
    start_date: body.get("start_date") as string,
    modules: (body.get("modules") as string).split(",") as string[],
    evidence: body.get("evidence") as string
  }
  // const res = fetch(`http://localhost:8000/workspaces/${body.get("workspace")}/render`, {
  //   method: "POST",
  //   body: JSON.stringify(ReportForm),
  //   headers: {
  //     'Content-Type': 'application/json'
  //   }
  // }).then(res => res.text())
  // return redirect(`/workspaces/${workspace}/render?`)
  // return json({render: await res})
  return json({render: "http://localhost:8000/workspaces/" + body.get("workspace") + "/render?" + `investigator_name=${ReportForm.investigator_name}&case_number=${ReportForm.case_number}&start_date=${ReportForm.start_date}${ReportForm.modules.map((r) => `&modules=${r}`).join('')}&evidence=${ReportForm.evidence}`})
}

export async function loader({params}: LoaderFunctionArgs) {
  const res: Promise<Workspace> = fetch(`http://localhost:8000/workspaces/${params.workspace}`).then(res => res.json())
  const evidence_tree: Promise<JSON> = fetch(`http://localhost:8000/workspaces/${params.workspace}/evidence`).then(res => res.json())
  const modules: Promise<JSON> = fetch(`http://localhost:8000/modules`).then(res => res.json())
  return json({workspace: await res, evidence: await evidence_tree, modules: await modules})
}

export default function Index() {
  const {workspace, evidence, modules} = useLoaderData<typeof loader>()
  const render = useActionData<typeof action>();
  // const params = useParams();
  const [selectedEvidence, setSelectedEvidence] = useState<string>("");
  const [selectedModules, setSelectedModules] = useState<string[]>([]);

  return (
    <div className={"flex flex-col space-y-2 h-full"}>
      <h1 className={"text-4xl underline"}>{workspace.workspace_config._name}</h1>
      <hr/>
      <div className={"flex flex-row space-x-2 h-full w-full"}>
        <div className={"flex flex-col space-y-2 divide-y-4 h-full border-r-black border-r-[1px]"}>
          <div className={"min-h-fit grow"}>
            <h1 className={"text-xl underline"}>Evidence</h1>
            <Evidence data={evidence.evidence} name={"evidence"} className={"mr-10"} selectedEvidence={selectedEvidence}
                      setSelectedEvidence={setSelectedEvidence}/>
          </div>
          <div className={"h-full"}>
            <h1 className={"text-xl underline"}>Modules</h1>
            <Module modules={modules.modules} selectedModules={selectedModules}
                    setSelectedModules={setSelectedModules}/>
          </div>
        </div>

        <div className={"h-full w-full"}>
          <h1 className={"text-xl underline"}>Report</h1>
          <Form className={"flex flex-col space-y-2 border-b-2 border-black py-2"} method="post" reloadDocument>
            <label htmlFor={"investigator_name"}>Investigator: </label>
            <input type={"text"} name={"investigator_name"} id={"investigator_name"}
                   className={"border-[1px] border-black rounded-lg p-0.5"}/>
            <label htmlFor={"case_number"}>Case Number: </label>
            <input type={"number"} name={"case_number"} id={"case_number"}
                   className={"border-[1px] border-black rounded-lg p-0.5"}/>
            <label htmlFor={"start_date"}>Start Date: </label>
            <input type={"date"} name={"start_date"} id={"start_date"}
                   className={"border-[1px] border-black rounded-lg p-0.5"}/>
            <input type={"hidden"} name={"evidence"} value={selectedEvidence}/>
            <input type={"hidden"} name={"modules"} value={selectedModules.join(",")}/>
            <input type={"hidden"} name={"workspace"} value={workspace.id}/>
            <button className={"h-8 bg-green-300 hover:bg-green-400 click:bg-green-500 w-1/4 mx-auto"}>Render</button>
          </Form>
          {/*dangerouslySetInnerHTML={{__html: render.render}}*/}
          {render?.render ?
            <iframe title={"Report"} src={render.render} className={"w-full h-full"}></iframe> :
            <div>Rendered report output goes here!</div>}
        </div>
      </div>
    </div>
  );
}
