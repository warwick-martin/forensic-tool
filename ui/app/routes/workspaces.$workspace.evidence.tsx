// export async function loader() {
//   const res: Promise<WorkspacesResponse> = fetch("http://localhost:8000/workspaces").then(res => res.json())
//   return defer({workspaces: res})
// }


import {Dispatch, SetStateAction, useState} from "react";

interface EvidenceProps {
  data: any;
  name: string;
  selectedEvidence: string,
  setSelectedEvidence: Dispatch<SetStateAction<string>>,
  className?: string;
}

export default function Evidence({data, name, className, selectedEvidence, setSelectedEvidence}: EvidenceProps) {
  const [collapsed, setCollapsed] = useState(false);
  const isFolder = typeof data === 'object' && !Array.isArray(data);

  return (
    <div className={className}>
      <div className={""}>
        <div onClick={() => setCollapsed(!collapsed)} className={"flex flex-row hover:cursor-pointer"}>
          <span>{isFolder ? (collapsed ? '📁 ' : '📂 ') : '📄 '}</span>
          <span>{name}</span>
        </div>

        {/* If it's a folder and not collapsed, render children */}
        {isFolder && !collapsed && (
          <div>
            {Object.keys(data).map((key) => {
              if (key === "files") {
                return (
                  <ul className={"ml-5 min-w-fit"}>
                    {data[key].map((file: string, index: number) => (
                      <li key={index} onClick={() => setSelectedEvidence(file)}
                          className={"" + (selectedEvidence === file ? "bg-blue-600 text-white" : "bg-white text-black")}>📄 {file}</li>
                    ))}
                  </ul>
                )
              }
              return (
                <Evidence key={key} data={data[key]} name={key} className={"ml-5"} selectedEvidence={selectedEvidence}
                          setSelectedEvidence={setSelectedEvidence}/>
              )
            })}
          </div>
        )}
      </div>
    </div>
  );
}
