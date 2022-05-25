import brickschema
from brickschema.namespaces import RDF, BRICK, RDFS
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
g.load_file("Brick.ttl")
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

# TODO: handle more than 1 level of "hasPart"
# define nodes
res = g.query("""SELECT ?entity ?label WHERE {
        { ?entity rdf:type/rdfs:subClassOf* brick:Equipment }
        UNION
        { ?entity rdf:type/rdfs:subClassOf* brick:Location }
        OPTIONAL {?entity rdfs:label ?label }
}""")
for row in res:
    assert isinstance(row, tuple)
    og_node, label = row
    # if "is part" of something else, skip it
    part_of_equip = g.query(f"""ASK {{
        {og_node.n3()} brick:isPartOf ?node .
        {{ ?node rdf:type/rdfs:subClassOf* brick:Equipment }}
        UNION
        {{ ?node rdf:type/rdfs:subClassOf* brick:Location }}
    }}""")
    if part_of_equip:
        continue
    cls = g.value(og_node, RDF.type)
    node = nid(og_node)
    nodes[node]["id"] = node
    nodes[node]["width"] = 180
    nodes[node]["height"] = 80
    nodes[node]["labels"] = [{"text": str(label) if label else node, "height": 20, "width": 60}, {"text": nid(cls), "height": 20, "width": 60}]
    nodes[node]["layoutOptions"] =  {
        "nodeLabels.placement": "[H_LEFT, V_TOP, INSIDE]",
    }
    nodes[node]["ports"] = []
    nodes[node]["children"] = []
    node_types = set(g.transitive_objects(cls, RDFS.subClassOf))
    if BRICK.Equipment in node_types:
        nodes[node]["class"] = ["equipment"]
    elif BRICK.Location in node_types:
        nodes[node]["class"] = ["location"]


    # get parts
    parts = g.query(f"""SELECT DISTINCT ?part ?label WHERE {{
        {og_node.n3()} brick:hasPart+ ?part .
        OPTIONAL {{ ?part rdfs:label ?label }}
    }}""")
    for part in parts:
        (part, label) = part
        cls = g.value(part, RDF.type)
        node_types = set(g.transitive_objects(cls, RDFS.subClassOf))
        if BRICK.Equipment in node_types:
            svg_classes = ["equipment"]
        elif BRICK.Location in node_types:
            svg_classes = ["location"]
        else:
            svg_classes = []
        part = nid(part)
        nodes[node]["children"].append({
            "id": part,
            "width": 60,
            "height": 60,
            "labels": [{"text": str(label) if label else part, "height": 20, "width": 60}, {"text": nid(cls), "height": 20, "width": 60}],
            "layoutOptions": {
                "nodeLabels.placement": "[H_LEFT, V_TOP, INSIDE]",
            },
            "ports": [],
            "class": svg_classes,
        })

# define topology (edges)
res = g.query("""SELECT ?e1 ?e2 WHERE {
      ?e1 brick:feeds ?e2 .
}""")
for row in res:
    assert isinstance(row, tuple)
    n1, n2 = row
    n1 = nid(n1)
    n2 = nid(n2)
    doc["edges"].append({
        "id": gensym(),
        "sources": [n1],
        "targets": [n2],
        "attributes": {"marker-end": "url(#arrow)"}
    })

# add points
res = g.query("""SELECt ?point ?label ?host WHERE {
        ?point rdf:type/rdfs:subClassOf* brick:Point .
        ?point brick:isPointOf ?host .
        OPTIONAL {?point rdfs:label ?label}
}""")
for row in res:
    assert isinstance(row, tuple)
    point, label, host = row
    cls = g.value(point, RDF.type)
    point = nid(point)
    host = nid(host)
    nodes[point]["id"] = point
    nodes[point]["width"] = 140
    nodes[point]["height"] = 40
    nodes[point]["labels"] = [{"text": str(label) if label else point, "height": 20, "width": 60}, {"text": nid(cls), "height": 20, "width": 60}]
    nodes[point]["layoutOptions"] =  {
        "nodeLabels.placement": "[H_LEFT, V_TOP, INSIDE]",
    }
    nodes[point]["ports"] = []
    nodes[point]["class"] = ["point"]

# associate points
res = g.query("""SELECT ?p ?e WHERE {
      ?p brick:isPointOf ?e .
}""")
for row in res:
    assert isinstance(row, tuple)
    p, e = row
    p = nid(p)
    e = nid(e)
    doc["edges"].append({
        "id": gensym(),
        "sources": [p],
        "targets": [e],
        "attributes": {"stroke-dasharray": "2,2"},
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
rect.equipment {
    fill: #b5d7aa;
}
rect.location {
    fill: #ea9999;
}
rect.location {
    fill: #f5dc97;
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
with open("output.js", "w") as f:
    f.write(js)
