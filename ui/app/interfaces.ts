interface Workspace {
  id: string
  workspace_config: {
    _name: string
    _modules: []
  }
}

interface EvidenceTree {
  files: string
}

/**
 * [
 *   {
 *     "id": "1f954eab-7d3b-4c59-acb9-c20727422ca2",
 *     "workspace_config": {
 *       "_name": "project",
 *       "_modules": []
 *     }
 *   },
 *   {
 *     "id": "f2594312-57e8-4a66-b98f-123e8cc94bab",
 *     "workspace_config": {
 *       "_name": "Example_Investigation",
 *       "_modules": []
 *     }
 *   }
 * ]
 */