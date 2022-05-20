const ELK = require('elkjs')
const elksvg = require('../elkjs-svg');

const fs = require('fs');

const testcase_directory = "test/testcases"
var files = fs.readdirSync(testcase_directory);
files = files.filter(filename => filename.endsWith(".json"));

if (process.env.ONLY_RENDER) {
    files = files.filter(filename => filename.includes(process.env.ONLY_RENDER));
}

const elk = new ELK()
const renderer = new elksvg.Renderer();

files.forEach(json_filename => {
    const data = fs.readFileSync(testcase_directory + "/" + json_filename, "utf-8");
    const graph = JSON.parse(data)
    elk.layout(graph)
        .then(data => {
        	console.error(JSON.stringify(data, null, 4));
            const result = renderer.toSvg(data, styles=null, defs=null);
            console.log(result);
        })
        .catch((err) => {
            console.error(err);
        });
});
