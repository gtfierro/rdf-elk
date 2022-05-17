import brickschema
import sys
import re
import json
import secrets
from collections import defaultdict

def gensym():
    return secrets.token_hex(8)

def nid(n):
    return re.split(r'[/#]', n.toPython())[-1]

if len(sys.argv) < 2:
    print("Usage: make223p.py <path to model.ttl file>")
    sys.exit(1)

g = brickschema.Graph()
g.load_file(sys.argv[1])
g.load_file("223p.ttl")
g.expand("shacl+shacl+shacl")

seen = set()
doc = {
   "id": "root",
   "layoutOptions": {
       "elk.algorithm": "layered",
       #"aspectRatio": 4
    },
   "children": [],
   "edges": [],
}

nodes = defaultdict(dict)
ports = defaultdict(dict)

res = g.query("""SELECT DISTINCT ?node ?cp ?dir ?cplabel ?nlabel WHERE {
    ?node s223:hasConnectionPoint ?cp .
    ?cp s223:hasDirection ?dir .
    OPTIONAL {?cp rdfs:label ?cplabel}
    OPTIONAL {?node rdfs:label ?nlabel}
}""")
for row in res:
    (node, connpoint, direction, cplabel, nlabel) = row
    node = nid(node)
    nodes[node]["id"] = node
    nodes[node]["width"] = 180
    nodes[node]["height"] = 80
    nodes[node]["labels"] = [{"text": str(nlabel) if nlabel else node, "height": 20, "width": 80}]
    nodes[node]["nodeSize.constraints"] =  "[PORTS, MINIMUM_SIZE]"
    nodes[node]["layoutOptions"] =  {
        "nodeLabels.placement": "[H_CENTER, V_TOP, INSIDE]",
        "portLabels.placement": "[INSIDE]",
        "portConstraints": "FIXED_SIDE",
        "spacing.portPort": "10.0",
    }
    #nodes[node]["properties"] = {
    #    "nodeLabels.placement": "[H_CENTER, V_TOP, INSIDE]",
    #    "portLabels.placement": "[INSIDE]",
    #    "portConstraints": "FIXED_SIDE",
    #    "spacing.portPort": "10.0",
    #}

    if "ports" not in nodes[node]:
        nodes[node]["ports"] = set()
    port = f"{node}:{nid(connpoint)}"
    nodes[node]["ports"].add(port)
    ports[port] = {
        "id": port,
        "layoutOptions": {
            #"port.side": "WEST" if "Inlet" in str(direction) else "EAST",
            "portLabels.placement": "[INSIDE]",
        },
        #"properties": {
        #    "port.side": "WEST" if "Inlet" in str(direction) else "EAST",
        #},
        "width": 8,
        "height": 8,
        "labels": [{"text": str(cplabel) if cplabel else nid(connpoint)}],
        #TODO: use direction/medium to place on side of node?
    }

for node_defn in nodes.values():
    my_ports = node_defn.pop("ports")
    node_defn["ports"] = [
        ports[port_id] for port_id in my_ports
    ]


res = g.query("""SELECT DISTINCT ?n1 ?n2 ?cp1 ?cp2 WHERE {
    ?n1 s223:hasConnectionPoint ?cp1 .
    ?n2 s223:hasConnectionPoint ?cp2 .
    ?cp1 s223:connectsThrough ?conn ;
         s223:hasDirection s223:Direction-Outlet .
    ?cp2 s223:connectsThrough ?conn ;
         s223:hasDirection s223:Direction-Inlet .
    ?conn rdf:type/rdfs:subClassOf* s223:Connection .
    FILTER (?n1 != ?n2)
}""")
for row in res:
    n1, n2, cp1, cp2 = row
    n1 = nid(n1)
    n2 = nid(n2)
    cp1 = f"{n1}:{nid(cp1)}"
    cp2 = f"{n2}:{nid(cp2)}"
    if cp1 not in ports:
        print(f"{cp1} not in ports")
        continue
    if cp2 not in ports:
        print(f"{cp2} not in ports")
        continue
    doc["edges"].append({
        "id": gensym(),
        "sources": [cp1],
        "targets": [cp2],
        "attributes": {"marker-end": "url(#arrow)"},
    })

for node in nodes.values():
    doc["children"].append(node)

# devices = g.query("""SELECT DISTINCT ?dev ?dev2 WHERE {
#     ?dev rdf:type/rdfs:subClassOf* s223:Device .
#     ?dev2 rdf:type/rdfs:subClassOf* s223:Device .
#     ?dev s223:connectedTo ?dev2 .
# }""")
# for i, dev in enumerate(devices):
#     if nid(dev[0]) not in seen:
#         doc["children"].append({
#             "id": nid(dev[0]),
#             "width": 120,
#             "height": 30,
#             "labels": [{"text": nid(dev[0])}],
#         })
#         seen.add(nid(dev[0]))
#     if nid(dev[1]) not in seen:
#         doc["children"].append({
#             "id": nid(dev[1]),
#             "width": 120,
#             "height": 30,
#             "labels": [{"text": nid(dev[1])}],
#         })
#         seen.add(nid(dev[1]))
#     doc["edges"].append({
#         "id": gensym(),
#         "sources": [nid(dev[0])],
#         "targets": [nid(dev[1])],
#     })

js = f"""
const ELK = require('elkjs')
const elksvg = require('elkjs-svg');

const graph = {json.dumps(doc, indent=2)};

const elk = new ELK()
elk.layout(graph)
  .then(data => {{
    var renderer = new elksvg.Renderer();
    var svg = renderer.toSvg(data);
    console.log(svg);
  }})
"""

#print(json.dumps(doc, indent=2))
print(js)
