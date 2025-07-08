from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import networkx as nx

app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: str
    type: str
    position: Dict[str, float]
    data: Dict[str, Any]

class Edge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: str = None
    targetHandle: str = None

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

class PipelineResponse(BaseModel):
    num_nodes: int
    num_edges: int
    is_dag: bool

def is_directed_acyclic_graph(nodes: List[Node], edges: List[Edge]) -> bool:
    """Check if the given nodes and edges form a DAG."""
    if not edges:
        return True
    
    G = nx.DiGraph()
    
    for node in nodes:
        G.add_node(node.id)
    
    for edge in edges:
        G.add_edge(edge.source, edge.target)
    
    return nx.is_directed_acyclic_graph(G)

@app.get("/")
async def root():
    return {"message": "VectorShift Pipeline Parser API", "status": "running"}

@app.get("/test")
async def test():
    return {"test": "success", "timestamp": "2024"}

@app.post("/pipelines/parse", response_model=PipelineResponse)
async def parse_pipeline(pipeline: Pipeline):
    try:
        print(f"Received pipeline with {len(pipeline.nodes)} nodes and {len(pipeline.edges)} edges")
        
        num_nodes = len(pipeline.nodes)
        num_edges = len(pipeline.edges)
        is_dag = is_directed_acyclic_graph(pipeline.nodes, pipeline.edges)
        
        result = PipelineResponse(
            num_nodes=num_nodes,
            num_edges=num_edges,
            is_dag=is_dag
        )
        
        print(f"Returning result: {result}")
        return result
        
    except Exception as e:
        print(f"Error parsing pipeline: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error parsing pipeline: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)