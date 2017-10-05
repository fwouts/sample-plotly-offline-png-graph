"""A script that produces a PNG graph using Plotly."""

import os
import cairosvg
import plotly
from plotly.graph_objs import Scatter, Layout
from selenium import webdriver

CHROME_BINARY_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CHROMELESS_BINARY_PATH = "/usr/local/bin/chromedriver"
HTML_FILENAME = "temp-plot.html"
OUTPUT_FILENAME = "output.png"

WIDTH = 1000
HEIGHT = 1000


def generate_html_graph(filename, data, title):
    """Generates an HTML file containing an SVG graph."""
    plotly.offline.plot({
        "data": data,
        "layout": Layout(title=title, width=WIDTH, height=HEIGHT)
    }, auto_open=False, filename=filename)


def extract_svg_code(html_file_path):
    """Extracts the SVG code from a HTML file produced by generate_html_graph()."""
    try:
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = CHROME_BINARY_PATH
        driver = webdriver.Chrome(
            executable_path=CHROMELESS_BINARY_PATH, chrome_options=chrome_options)
        driver.get("file://" + html_file_path)
        svg_element = driver.find_element_by_css_selector("svg.main-svg")
        svg_outer_html = svg_element.get_attribute('outerHTML')
        return svg_outer_html
    finally:
        if driver:
            driver.quit()


def make_png_graph(data, title):
    """Generates the PNG graph."""
    html_file_path = os.path.join(os.getcwd(), HTML_FILENAME)
    svg_file_path = os.path.join(os.getcwd(), OUTPUT_FILENAME)
    generate_html_graph(html_file_path, data, title)
    svg_code = extract_svg_code(html_file_path)
    os.remove(html_file_path)
    cairosvg.svg2png(bytestring=svg_code, write_to=svg_file_path)


if __name__ == "__main__":
    make_png_graph(
        [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
        "Hello, World!")
