
const ELK = require('elkjs')
const elksvg = require('elkjs-svg');

const graph = {
  "id": "root",
  "layoutOptions": {
    "elk.algorithm": "layered"
  },
  "children": [
    {
      "id": "zone1-hvac-space",
      "width": 180,
      "height": 80,
      "labels": [
        {
          "text": "zone1-hvac-space",
          "height": 20,
          "width": 80
        }
      ],
      "nodeSize.constraints": "[PORTS, MINIMUM_SIZE]",
      "layoutOptions": {
        "nodeLabels.placement": "[H_CENTER, V_TOP, INSIDE]",
        "portLabels.placement": "[INSIDE]",
        "portConstraints": "FIXED_SIDE",
        "spacing.portPort": "10.0"
      },
      "ports": [
        {
          "id": "zone1-hvac-space:zone1-hvac-space-out",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "zone1-hvac-space-out"
            }
          ]
        },
        {
          "id": "zone1-hvac-space:zone1-hvac-space-in",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "zone1-hvac-space-in"
            }
          ]
        }
      ]
    },
    {
      "id": "cooling-coil-2stage",
      "width": 180,
      "height": 80,
      "labels": [
        {
          "text": "cooling-coil-2stage",
          "height": 20,
          "width": 80
        }
      ],
      "nodeSize.constraints": "[PORTS, MINIMUM_SIZE]",
      "layoutOptions": {
        "nodeLabels.placement": "[H_CENTER, V_TOP, INSIDE]",
        "portLabels.placement": "[INSIDE]",
        "portConstraints": "FIXED_SIDE",
        "spacing.portPort": "10.0"
      },
      "ports": [
        {
          "id": "cooling-coil-2stage:cooling-coil-out",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "cooling-coil-out"
            }
          ]
        },
        {
          "id": "cooling-coil-2stage:cooling-coil-in",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "cooling-coil-in"
            }
          ]
        }
      ]
    },
    {
      "id": "heating-coil-1stage",
      "width": 180,
      "height": 80,
      "labels": [
        {
          "text": "heating-coil-1stage",
          "height": 20,
          "width": 80
        }
      ],
      "nodeSize.constraints": "[PORTS, MINIMUM_SIZE]",
      "layoutOptions": {
        "nodeLabels.placement": "[H_CENTER, V_TOP, INSIDE]",
        "portLabels.placement": "[INSIDE]",
        "portConstraints": "FIXED_SIDE",
        "spacing.portPort": "10.0"
      },
      "ports": [
        {
          "id": "heating-coil-1stage:heating-coil-out",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "heating-coil-out"
            }
          ]
        },
        {
          "id": "heating-coil-1stage:heating-coil-in",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "heating-coil-in"
            }
          ]
        }
      ]
    },
    {
      "id": "fan",
      "width": 180,
      "height": 80,
      "labels": [
        {
          "text": "fan",
          "height": 20,
          "width": 80
        }
      ],
      "nodeSize.constraints": "[PORTS, MINIMUM_SIZE]",
      "layoutOptions": {
        "nodeLabels.placement": "[H_CENTER, V_TOP, INSIDE]",
        "portLabels.placement": "[INSIDE]",
        "portConstraints": "FIXED_SIDE",
        "spacing.portPort": "10.0"
      },
      "ports": [
        {
          "id": "fan:fan-in",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "fan-in"
            }
          ]
        },
        {
          "id": "fan:fan-out",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "fan-out"
            }
          ]
        }
      ]
    },
    {
      "id": "economizer",
      "width": 180,
      "height": 80,
      "labels": [
        {
          "text": "economizer",
          "height": 20,
          "width": 80
        }
      ],
      "nodeSize.constraints": "[PORTS, MINIMUM_SIZE]",
      "layoutOptions": {
        "nodeLabels.placement": "[H_CENTER, V_TOP, INSIDE]",
        "portLabels.placement": "[INSIDE]",
        "portConstraints": "FIXED_SIDE",
        "spacing.portPort": "10.0"
      },
      "ports": [
        {
          "id": "economizer:economizer-outside-air",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "economizer-outside-air"
            }
          ]
        },
        {
          "id": "economizer:economizer-return-air",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "economizer-return-air"
            }
          ]
        },
        {
          "id": "economizer:economizer-mixed-air",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "economizer-mixed-air"
            }
          ]
        }
      ]
    },
    {
      "id": "vav1-dmp",
      "width": 180,
      "height": 80,
      "labels": [
        {
          "text": "vav1-dmp",
          "height": 20,
          "width": 80
        }
      ],
      "nodeSize.constraints": "[PORTS, MINIMUM_SIZE]",
      "layoutOptions": {
        "nodeLabels.placement": "[H_CENTER, V_TOP, INSIDE]",
        "portLabels.placement": "[INSIDE]",
        "portConstraints": "FIXED_SIDE",
        "spacing.portPort": "10.0"
      },
      "ports": [
        {
          "id": "vav1-dmp:vav1-dmp-in",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "vav1-dmp-in"
            }
          ]
        },
        {
          "id": "vav1-dmp:vav1-dmp-out",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "vav1-dmp-out"
            }
          ]
        }
      ]
    },
    {
      "id": "vav1-rhc",
      "width": 180,
      "height": 80,
      "labels": [
        {
          "text": "vav1-rhc",
          "height": 20,
          "width": 80
        }
      ],
      "nodeSize.constraints": "[PORTS, MINIMUM_SIZE]",
      "layoutOptions": {
        "nodeLabels.placement": "[H_CENTER, V_TOP, INSIDE]",
        "portLabels.placement": "[INSIDE]",
        "portConstraints": "FIXED_SIDE",
        "spacing.portPort": "10.0"
      },
      "ports": [
        {
          "id": "vav1-rhc:vav1-rhc-in",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "vav1-rhc-in"
            }
          ]
        },
        {
          "id": "vav1-rhc:vav1-rhc-out",
          "layoutOptions": {
            "portLabels.placement": "[INSIDE]"
          },
          "width": 8,
          "height": 8,
          "labels": [
            {
              "text": "vav1-rhc-out"
            }
          ]
        }
      ]
    }
  ],
  "edges": [
    {
      "id": "c13cd6eae6627b69",
      "sources": [
        "economizer:economizer-mixed-air"
      ],
      "targets": [
        "cooling-coil-2stage:cooling-coil-in"
      ],
      "attributes": {
        "marker-end": "url(#arrow)"
      }
    },
    {
      "id": "6959fe04f7dc45f6",
      "sources": [
        "cooling-coil-2stage:cooling-coil-out"
      ],
      "targets": [
        "heating-coil-1stage:heating-coil-in"
      ],
      "attributes": {
        "marker-end": "url(#arrow)"
      }
    },
    {
      "id": "0d92b1f3322e5983",
      "sources": [
        "heating-coil-1stage:heating-coil-out"
      ],
      "targets": [
        "fan:fan-in"
      ],
      "attributes": {
        "marker-end": "url(#arrow)"
      }
    },
    {
      "id": "78a00c6fd6aa8461",
      "sources": [
        "fan:fan-out"
      ],
      "targets": [
        "vav1-dmp:vav1-dmp-in"
      ],
      "attributes": {
        "marker-end": "url(#arrow)"
      }
    },
    {
      "id": "126c85532112a313",
      "sources": [
        "vav1-dmp:vav1-dmp-out"
      ],
      "targets": [
        "vav1-rhc:vav1-rhc-in"
      ],
      "attributes": {
        "marker-end": "url(#arrow)"
      }
    },
    {
      "id": "0d9d79c9ea62c80f",
      "sources": [
        "vav1-rhc:vav1-rhc-out"
      ],
      "targets": [
        "zone1-hvac-space:zone1-hvac-space-in"
      ],
      "attributes": {
        "marker-end": "url(#arrow)"
      }
    },
    {
      "id": "5c4b4b8c3c96c9f1",
      "sources": [
        "zone1-hvac-space:zone1-hvac-space-out"
      ],
      "targets": [
        "economizer:economizer-return-air"
      ],
      "attributes": {
        "marker-end": "url(#arrow)"
      }
    }
  ]
};

const elk = new ELK()
elk.layout(graph)
  .then(data => {
    var renderer = new elksvg.Renderer();
    var svg = renderer.toSvg(data);
    console.log(svg);
  })

