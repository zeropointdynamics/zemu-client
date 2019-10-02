
'''

Copyright (c) 2019 Zeropoint Dynamics, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''


import os, datetime

API_KEY = os.environ.get(
    'ZEMU_API_KEY', 'PASTE_YOUR_API_KEY_HERE')


def main():
    global API_KEY
    import argparse
    import sys

    info('\nZemu Copyright (c) 2019 Zeropoint Dynamics, LLC\n\n')

    help_text = '''
The following types of remote analysis are supported:
    strace:  returns a trace of system calls executed (with arguments).
    overlay: returns an instruction-level trace viewable in Zemu's IdaPro plugin.
'''

    epilog = '''
Examples:

	python zemu.py strace mirai.bin
	python zemu.py overlay mirai.bin botname > mirai.overlay
'''

    parser = argparse.ArgumentParser(
        description=help_text, epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '--api-key', default=API_KEY,
        help='Specify an API key through this flag, or the ZEMU_API_KEY ' +
        'environment variable')
    parser.add_argument('-o', '--output',
                        help='Write output of results to specified file.',
                        type=argparse.FileType('w'),  default=sys.stdout)
    parser.add_argument('analysis_type',
                        help='The type of analysis Zemu should conduct',
                        type=str.lower, choices=['strace', 'overlay'])
    parser.add_argument('binary', type=argparse.FileType('rb'),
                        help='Binary that will be uploaded for analysis')
    parser.add_argument('cmdline_args', nargs='*', default=[],
                        help='Command line arguments passed to the binary.')
    parser.add_argument('--date', help="Format YYYY-MM-DD. Useful for extracting different values from DGAs", default="2019-02-02", type=valid_date)

    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    API_KEY = args.api_key
    if API_KEY == 'PASTE_YOUR_API_KEY_HERE':
        info('You need to specify a valid API key before using Zemu.\n')
        info('Set API_KEY in the script, or specify with --api-key.\n')
        return

    submit(args)


def await_completion(args, resource, timeout=60):
    '''
    Await completion of the specified resource analysis results.
    '''
    import time

    info('Queued. Awaiting results...')
    end_time = time.time() + timeout
    while time.time() < end_time:
        result = request(method='GET', function=args.analysis_type,
                         params={'resource': resource})
        if result != None:
            info('done.\n\n')
            return [result, True]

        info('.')
        time.sleep(1)
    info('\nNo response after %d seconds.\n'.format(timeout))
    return [None, False]


def submit(args):
    '''
    Submit the specified binary and await analysis results.
    '''
    import base64
    import json

    info('Submitting...')

    try:
        result = request(method='POST', function=args.analysis_type, params={
            'data': base64.b64encode(args.binary.read()).decode(),
            'filename': args.binary.name,
            'cmdline_args': args.cmdline_args,
            'date': args.date
        })
        if result is None:
            return

        result = json.loads(result)
        resource = result.get('resource', None)
        if resource is None:
            info('\nError in request: \n')
            info(json.dumps(result))
            return

        info('..............done.\n')
    except Exception as e:
        info('Error received\n')
        info(e)
        return

    result = await_completion(args, resource)
    if result[1] == True:
        args.output.write(result[0])


def info(msg):
    '''
    Log {msg} to stderr.
    '''
    import sys
    if type(msg) is bytes:
        msg = msg.decode()
    sys.stderr.write(msg)
    sys.stderr.flush()


def request(server='zemu5349apim.azure-api.net', app='zemu5349pfuncapp',
            method='POST', function='strace', params={}):
    '''
    Log {msg} to stderr.
    '''
    import json
    try:
        # Python 2 Support
        from httplib import HTTPSConnection
        from urllib import urlencode
    except ImportError:
        # Python 3 Support
        from http.client import HTTPSConnection
        from urllib.parse import urlencode

    if method == 'GET':
        body = ''
        params = urlencode(params)
    else:
        body = json.dumps(params)
        params = '{}'

    conn = HTTPSConnection(server)
    conn.request(method, '/%s/%s?%s' % (app, function, params), body,
                 {'Ocp-Apim-Subscription-Key': API_KEY})
    response = conn.getresponse()

    data = response.read()
    if type(data) is bytes:
        data = data.decode()

    conn.close()

    if response.status != 200:
        info('\nError in request: \n')
        info(data)
        return None

    if method == 'GET' and response.getheader('content-type') != 'text/plain':
        return None

    return data

def valid_date(s):
    try:
        x = datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)
    return s

if __name__ == '__main__':
    main()
