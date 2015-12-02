import base64
from cStringIO import StringIO
from PIL import Image
import os
import re

X = 10
Y = 18
N = 3

NX = N * X + 6

def get_stats():
    fh = os.popen("top -l 2 | grep 'CPU usage' | tail -n 1")
    match = re.search(r'(\d+)(\.\d+)?% idle', fh.read())
    if match:
        cpu = 100 - int(match.groups()[0])
    else:
        cpu = 0

    fh = os.popen("df -H / | tail -n 1")
    match = re.search(r'(\d+)%', fh.read())
    if match:
        disk = int(match.groups()[0])
    else:
        disk = 0

    fh = os.popen("memory_pressure -Q | tail -n 1")
    match = re.search(r'(\d+)%', fh.read())
    if match:
        mem = 100 - int(match.groups()[0])
    else:
        mem = 0

    return cpu, mem, disk

def draw_bar(data, x_offset, pct, color):
    GRAY = (220, 220, 220, 255)
    for i in xrange(0, int((Y - 2) * pct / 100)):
        i = Y - i - 2
        for j in xrange(X):
            data[i * NX + j + x_offset] = color

    for i in xrange(Y):
        data[i * NX + x_offset] = GRAY
        data[i * NX + x_offset + X - 1] = GRAY

    for j in xrange(X):
        data[0 * NX + j + x_offset] = GRAY
        data[(Y - 1) * NX + j + x_offset] = GRAY

image = Image.new("RGBA", (NX, Y))
data = list(image.getdata())

cpu, mem, disk = get_stats()

draw_bar(data, 0, cpu, (255, 0, 0, 255))
draw_bar(data, X + 3, mem, (242, 190, 95, 255))
draw_bar(data, 2 * X + 6, disk, (80, 220, 250, 255))



image.putdata(data)
output = StringIO()
image.save(output, format="PNG")


b64_data = base64.b64encode(output.getvalue())

print """<html>
<head>
    <style>
    #img {
        font-size: 26px;
    }
    </style>
</head>
<body>
    <label id="img">
        <img src="data:image/png;base64,%s"/>
    </label>
</body>
</html>""".replace('\n', '') % (b64_data,)
