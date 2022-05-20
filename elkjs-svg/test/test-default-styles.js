const ELK = require('elkjs')
const elksvg = require('../elkjs-svg');

const xml2js = require('xml2js');

const describe = require('mocha').describe;
const it = require('mocha').it;
const assert = require('chai').assert;

var graph = {
  "id": "root",
  "layoutOptions": {
    "elk.algorithm": "layered"
  },
  "children": [
    {"id": "n1", "width": 30, "height": 30},
    {"id": "n2", "width": 30, "height": 30},
    {"id": "n3", "width": 30, "height": 30}
  ],
  "edges": [
    {"id": "e1", "sources": ["n1"], "targets": ["n2"]},
    {"id": "e2", "sources": ["n1"], "targets": ["n3"]}
  ]
}

describe("Correct default styles are returned", () => {
  const elk = new ELK()
  it(`Parsing returns the correct result`, (done) => {
    elk.layout(graph)
      .then(data => {
        var renderer = new elksvg.Renderer();
        var svg = renderer.toSvg(data);

        var expectedCss = renderer._style;
        var expectedDefs = renderer._defs;

        xml2js.parseString(svg, {trim: true}, (err, parsed_result) => {
          var resultCss = parsed_result.svg.defs[0].style[0]._;
          assert.equal(
            expectedCss.replace(/^\s+|\s+$/gm, ""),
            resultCss.replace(/^\s+|\s+$/gm, "")
          );

          var resultDefsJson = parsed_result.svg.defs[0].marker;
          var builder = new xml2js.Builder();
          var resultDefs = builder.buildObject({"marker": resultDefsJson[0]});
          resultDefs = resultDefs.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', "");
          resultDefs = resultDefs.replace("/>", " />");
          assert.deepEqual(
            expectedDefs.render().replace(/^\s+|\s+$/gm, ""),
            resultDefs.replace(/^\s+|\s+$/gm, ""),
          );
          done();
        });
      })
      .catch((err) => {
          done(err);
      });
  });
})
