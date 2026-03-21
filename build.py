import argparse
import json
import os
from time import gmtime, strftime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emulators', default='emulators.json')
    parser.add_argument('--tests', default='tests.json')
    parser.add_argument('--results-dir', default='.')
    parser.add_argument('--output', default='index.html')
    args = parser.parse_args()

    emulators = json.load(open(args.emulators, 'rt', encoding='utf-8'))
    tests = json.load(open(args.tests, 'rt', encoding='utf-8'))

    for name in emulators:
        result_file = os.path.join(args.results_dir, emulators[name]['file'])
        if os.path.exists(result_file):
            data = json.load(open(result_file, 'rt', encoding='utf-8'))
            emulators[name].update(data)
            emulators[name]['passed'] = len([result for result in data['tests'].values() if result['result'] != 'FAIL'])
        else:
            emulators[name].update({'passed': 0, 'tests': {}})

    f = open(args.output, 'wt', encoding='utf-8')
    f.write("""
    <html><head><style>
    table { border-collapse: collapse }
    .emulator { position: sticky; top: 0px; }
    .test { position: sticky; left: 0px; }
    .tooltiptext { visibility: hidden; width: 200px; background-color: black; color: #fff; text-align: center; padding: 5px 0; border-radius: 6px; position: absolute; z-index: 1; left: 102%; }
    tr:hover .tooltiptext { visibility: visible; }
    td, th { border: #333 solid 1px; text-align: center; line-height: 1.5}
    .PASS { background-color: #6e2 }
    .FAIL { background-color: #e44 }
    .UNKNOWN { background-color: #fd6 }
    td {font-size:80%}
    th{background:#eee}
    th:first-child{text-align:right; padding-right:4px}
    .screenshot { width: 160; height: 144; }
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif}
    </style></head><body><table>\n""")
    f.write("<tr><th style=\"text-align:left\">Updated On<br>" + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + "</th>\n")
    for name, emulator in sorted(emulators.items(), key=lambda n: -n[1]['passed']):
        f.write("  <th class='emulator'><a href=\"%s\">%s</a> (%d/%d)</th>\n" % (emulator['url'], name, emulator['passed'], len(emulator['tests'])))
    f.write("</tr>\n")
    for test in tests:
        name = test['name'].replace("/", "/&#8203;")
        if test['url']:
            name = "<a href=\"%s\">%s</a>" % (test['url'], name)
        if test['description']:
            name += "<span class=\"tooltiptext\">%s</span>" % (test['description'])
        f.write("<tr><th class='test'>%s</th>\n" % (name))
        for name, emulator in sorted(emulators.items(), key=lambda n: -n[1]['passed']):
            result = emulator['tests'].get(test['name'])
            if result:
                f.write("  <td class='%s'>%s<br><img class='screenshot' src='data:image/png;base64,%s'></td>\n" % (result['result'], result['result'], result['screenshot']))
            else:
                f.write("  <td>No result</td>\n")
        f.write("</tr>\n")
    f.write("</table></body></html>")


if __name__ == '__main__':
    main()