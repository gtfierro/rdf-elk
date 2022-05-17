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
g.serialize("debug.ttl", format="turtle")

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
    if "ports" not in nodes[node]:
        nodes[node]["ports"] = set()
    port = f"{node}:{nid(connpoint)}"
    nodes[node]["ports"].add(port)
    ports[port] = {
        "id": port,
        "layoutOptions": {
            #"port.side": "[WEST, SOUTH]" if "Inlet" in str(direction) else "EAST",
            "portLabels.placement": "[INSIDE]",
        },
        "width": 8,
        "height": 8,
        "labels": [{"text": str(cplabel) if cplabel else nid(connpoint)}],
        "class": ["port", "inlet"],
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
        "attributes": {"marker-end": "url(#arrow)"}
    })

# get properties
res = g.query("""SELECT DISTINCT ?node ?loc ?prop ?proplabel WHERE {
        ?loc s223:hasProperty ?prop .
        ?loc s223:isConnectionPointOf ?node .
        ?prop rdf:type/rdfs:subClassOf* s223:Property .
        OPTIONAL {?prop rdfs:label ?proplabel}
}""")
seen_props = set()
for row in res:
    (node, loc, prop, plabel) = row
    node = nid(node)
    loc = nid(loc)
    prop = nid(prop)

    # only add each property once; otherwise we can get multiple edges and it is confusing
    if prop in seen_props:
        continue
    seen_props.add(prop)

    # add 'property' as a new node
    nodes[prop]["id"] = prop
    nodes[prop]["width"] = 120
    nodes[prop]["height"] = 20
    nodes[prop]["labels"] = [{"text": str(plabel) if plabel else prop, "height": 20, "width": 20}]
    nodes[prop]["nodeSize.constraints"] =  "[PORTS, MINIMUM_SIZE]"
    nodes[prop]["layoutOptions"] =  {
        "nodeLabels.placement": "[INSIDE]",
    }
    nodes[prop]["ports"] = []
    nodes[prop]["class"] = ["node", "s223property"]

    # add edge to property
    doc["edges"].append({
        "id": gensym(),
        "sources": [f"{node}:{loc}"],
        "targets": [prop],
        # TODO: dashed
        "attributes": {"stroke-dasharray": "2,2"},
        #"attributes": {"marker-end": "url(#arrow)"}
    })


for node in nodes.values():
    doc["children"].append(node)

styles = """
rect {
  opacity: 0.8;
  fill: #6094CC;
  stroke-width: 1;
  stroke: #222222;
}
rect.port {
  opacity: 1;
  fill: #FD4659;
}
text {
  font-size: 10px;
  font-family: sans-serif;
  /* in elk's coordinates "hanging" would be the correct value" */
  dominant-baseline: hanging;
  text-align: left;
}
g.port > text {
  font-size: 8px;
}
polyline {
  fill: none;
  stroke: black;
  stroke-width: 1;
}
path {
  fill: none;
  stroke: black;
  stroke-width: 1;
}
s223property {
  fill: #32BF84;
}
"""

js = f"""
const ELK = require('elkjs')
const elksvg = require('elkjs-svg');

const graph = {json.dumps(doc, indent=2)};

const elk = new ELK()
elk.layout(graph)
  .then(data => {{
    var renderer = new elksvg.Renderer();
    var svg = renderer.toSvg(data, styles=`{styles}`);
    console.log(svg);
  }})
"""

#print(json.dumps(doc, indent=2))
print(js)
