// export async function loader() {
//   const res: Promise<WorkspacesResponse> = fetch("http://localhost:8000/workspaces").then(res => res.json())
//   return defer({workspaces: res})
// }


import {Dispatch, SetStateAction} from "react";

interface ModuleProps {
  modules: { name: string, type: string }[];
  className?: string;
  selectedModules: string[],
  setSelectedModules: Dispatch<SetStateAction<string[]>>
}

function toggleModule(name: string, selectedModules: string[], setSelectedModules: Dispatch<SetStateAction<string[]>>) {
  if (selectedModules.includes(name)) {
    setSelectedModules(selectedModules.filter(selectedModule => selectedModule !== name));
  } else {
    setSelectedModules([...selectedModules, name]);
  }
}

export default function Module({modules, className, selectedModules, setSelectedModules}: ModuleProps) {
  const ingestModules = modules.filter(module => module.type === "IngestModule");
  const analysisModules = modules.filter(module => module.type === "AnalysisModule");
  const reportModules = modules.filter(module => module.type === "ReportModule");

  console.log(selectedModules)

  return (
    <div className={className}>
      <h2 className={"text-lg"}>Ingest Modules</h2>
      <ul>
        {ingestModules.map((module, index) => (
          <li key={index}
              onClick={() => {
                toggleModule(module.name, selectedModules, setSelectedModules)
              }}
              className={"" + (selectedModules.includes(module.name) ? "bg-blue-600 text-white" : "bg-white text-black")}>
            {module.name} {selectedModules.includes(module.name)}
          </li>))}
      </ul>
      <h2 className={"text-lg"}>Analysis Modules</h2>
      <ul>
        {analysisModules.map((module, index) => (
          <li key={index}
              onClick={() => {
                toggleModule(module.name, selectedModules, setSelectedModules)
              }}
              className={"" + (selectedModules.includes(module.name) ? "bg-blue-600 text-white" : "bg-white text-black")}>
            {module.name}
          </li>))}
      </ul>
      <h2 className={"text-lg"}>Report Modules</h2>
      <ul>
        {reportModules.map((module, index) => (
          <li key={index}
              onClick={() => {
                toggleModule(module.name, selectedModules, setSelectedModules)
              }}
              className={"" + (selectedModules.includes(module.name) ? "bg-blue-600 text-white" : "bg-white text-black")}>
            {module.name}
          </li>))}
      </ul>
    </div>
  );
}
