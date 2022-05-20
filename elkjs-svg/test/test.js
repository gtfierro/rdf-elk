const ELK = require('elkjs')
const elksvg = require('../elkjs-svg');

const fs = require('fs');
const util = require('util');
const xml2js = require('xml2js');

const describe = require('mocha').describe;
const it = require('mocha').it;
const assert = require('chai').assert;

const testcase_directory = "test/testcases"
var files = fs.readdirSync(testcase_directory);
files = files.filter(filename => filename.endsWith(".json"));

if (process.env.ONLY_TEST) {
    files = files.filter(filename => filename.includes(process.env.ONLY_TEST));
}

const elk = new ELK()
const renderer = new elksvg.Renderer();

files.forEach(json_filename => {
    describe("Parsing files returns correct result", () => {

        const data = fs.readFileSync(testcase_directory + "/" + json_filename, "utf-8");
        const graph = JSON.parse(data)

        it(`Parsing ${testcase_directory}/${json_filename} returns the correct result`, (done) => {
            elk.layout(graph)
                .then(data => {
                    const result = renderer.toSvg(data, styles=null, defs=null);
                    const svg_filename = json_filename.replace(".json", ".svg");
                    fs.readFile(testcase_directory + "/" + svg_filename, "utf-8", (err, expected) => {
                        xml2js.parseString(result, {trim: true}, (err, parsed_result) => {
                            xml2js.parseString(expected, {trim: true}, (err, parsed_expected) => {
                                assert.deepEqual(parsed_result, parsed_expected);
                                done();
                            })
                        });
                    });
                })
                .catch((err) => {
                    done(err);
                });
        });
    });
});
