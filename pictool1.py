"""
Application for processing images.

This application contains the core code for reading and saving images, as well as
processing the command line arguments. While there is a bit of advanced code in this 
file, you have learned enough Python by now to be able to understand a lot 
(but not all) of this file. 

Author: Ian Ifill
Date: June 9, 2025
"""

from PIL import Image as CoreImage
import traceback
from rgb import RGB
import os.path
import plugins2
import sys

PROGRESS = 10

def read_image(file):
    try:
        image = CoreImage.open(file)
        print(('Loading ' + repr(file)), end='', flush=True)
        image = image.convert("RGBA")
        width, height = image.size
        size = width * height
        block = max(size // PROGRESS, 1)
        source = iter(image.getdata())
        buffer = []
        for r in range(height):
            row = []
            for c in range(width):
                tups = next(source)
                row.append(RGB(*tups))
                if (r * width + c) % block == 0:
                    print('.', end='', flush=True)
            buffer.append(row)
        print('done')
        return buffer
    except:
        traceback.print_exc()
        print('Could not load the file ' + repr(file))
        return None

def verify_image(buffer):
    if type(buffer) != list or len(buffer) == 0:
        return False
    first = buffer[0]
    if type(first) != list or len(first) == 0:
        return False
    width = len(first)
    for row in buffer:
        if len(row) != width:
            return False
        for item in row:
            if type(item) != RGB:
                return False
    return True

def save_image(buffer, file):
    assert verify_image(buffer), 'A plug-in has corrupted the image data'
    try:
        height = len(buffer)
        width = len(buffer[0])
        size = width * height
        block = max(size // PROGRESS, 1)
        print(('Saving ' + repr(file)), end='', flush=True)
        im = CoreImage.new('RGBA', (width, height))
        output = []
        for r in range(height):
            for c in range(width):
                pixel = buffer[r][c]
                output.append(pixel.rgba())
                if (r * width + c) % block == 0:
                    print('.', end='', flush=True)
        im.putdata(output)
        im.save(file, 'PNG')
        print('done')
    except:
        traceback.print_exc()
        print('Could not save the file ' + repr(file))

def parse_args(args):
    options = extract_options(args)
    result = {}
    usage = 'usage: python3 pictool.py command [options] input [output]'
    if not len(args) in [3, 4]:
        result['error'] = usage
    else:
        command = lookup_command(args[1], options)
        if type(command) == str:
            result['error'] = command
        else:
            result['command'] = command
            result['options'] = options
        result['input'] = args[2]
        if len(args) == 4:
            result['output'] = args[3]
    return result

def lookup_command(command, options):
    if not hasattr(plugins2, command):
        return 'error: unrecognized command ' + repr(command)
    error = None
    function = getattr(plugins2, command)
    param = function.__code__.co_varnames[:function.__code__.co_argcount]
    dsize = 0 if function.__defaults__ is None else len(function.__defaults__)
    if len(param) != dsize + 1:
        error = 'error: plugin ' + repr(command) + ' does not have default values after first parameter'
    else:
        badargs = [key for key in options if key not in param]
        if badargs:
            flags = ', '.join('--' + x for x in badargs)
            error = 'error: plugin ' + repr(command) + ' does not recognize the following options: ' + flags
    return function if error is None else error

def extract_options(args):
    options = {}
    pos = 1
    while pos < len(args):
        item = args[pos]
        if item.startswith('--') and '=' in item:
            split = item.find('=')
            value = item[split + 1:]
            if value in ['True', 'False']:
                value = eval(value)
            elif value.isdigit():
                value = int(value)
            else:
                try:
                    value = float(value)
                except:
                    pass
            options[item[2:split]] = value
            del args[pos]
        else:
            pos += 1
    return options

def main():
    import datetime
    args = parse_args(sys.argv[:])
    if 'error' in args:
        print(args['error'])
        return
    buffer = read_image(args['input'])
    if buffer is None:
        return
    start = datetime.datetime.now()
    print('Processing ' + repr(args['input']), end='', flush=True)
    process = args['command'](buffer, **args['options'])
    print('..done')
    end = datetime.datetime.now()
    print('Time: ' + str(end - start))
    if process and 'output' in args:
        save_image(buffer, args['output'])

if __name__ == '__main__':
    main()