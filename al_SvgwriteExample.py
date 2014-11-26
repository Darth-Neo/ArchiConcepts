__author__ = 'morrj140'
import svgwrite

dwg = svgwrite.Drawing('test.svg', profile='tiny')
dwg.add(dwg.line((0, 0), (10, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.text('Test', insert=(0, 0.2)))
dwg.save()

svg_document = svgwrite.Drawing(filename = "test-svgwrite.svg", size = ("800px", "600px"))

svg_document.add(svg_document.rect(insert = (0, 0),
                                   size = ("200px", "100px"),
                                   stroke_width = "1",
                                   stroke = "black",
                                   fill = "rgb(255,255,0)"))

svg_document.add(svg_document.text("Hello World",
                                   insert = (210, 110)))

print(svg_document.tostring())

svg_document.save()

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

drawing = svg2rlg("test-svgwrite.svg")
renderPDF.drawToFile(drawing, "file.pdf")