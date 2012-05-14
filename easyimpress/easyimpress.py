import os
import markdown2

from jinja2 import Template
from opster import command

IMPRESS_FOLDER = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)), '..', 'impress.js')

TEMPLATE = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=1024" />
    <style>
      {# FIXME: I can't not get include working, let's do it hard way :p #}
      {{ impress_css }}
      {# {% include "../impress.js/css/impress-demo.css" %} #}
    </style>
    <link href="http://fonts.googleapis.com/css?family=Open+Sans:regular,semibold,italic,italicsemibold|PT+Sans:400,700,400italic,700italic|PT+Serif:400,700,400italic,700italic" rel="stylesheet" />
  </head>

  <body class="impress-not-supported">
  <div class="fallback-message">
    <p>Your browser <b>doesn't support the features required</b> by impress.js, so you are presented with a simplified version of this presentation.</p>
    <p>For the best experience please use the latest <b>Chrome</b>, <b>Safari</b> or <b>Firefox</b> browser.</p>
  </div>

  <div id="impress">
  {% for slide in slides %}
    <div id="slide{{ loop.index0 }}" class="step slide" data-x="{{ loop.index0 * 1000 }}">
      {{ slide }}
    </div>
  {% endfor %}
  </div>

  <div class="hint">
  <p>Use a spacebar or arrow keys to navigate</p>
  </div>
  <script>
    if ("ontouchstart" in document.documentElement) {
      document.querySelector(".hint").innerHTML = "<p>Tap on the left or right to navigate</p>";
    }
  </script>
  <script>
    {{ impress_js }}
    {# {% include "../impress.js/js/impress.js" %} #}
  </script>
  <script>impress().init();</script>
</body>
</html>
'''


class Slide(object):
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return self.content


def write_to_file(handler, slides):
    impress_css = open(
            os.path.join(IMPRESS_FOLDER, 'css', 'impress-demo.css')).read()
    impress_js = open(
            os.path.join(IMPRESS_FOLDER, 'js', 'impress.js')).read()
    template = Template(TEMPLATE)
    handler.write(template.render(slides=slides,
                                  impress_js=impress_js,
                                  impress_css=impress_css))


@command(usage='filename')
def main(filename):
    '''Generate HTML slides from a markdown file.

    '''
    if os.path.basename(filename).split('.')[1] == 'md':
        processor = markdown2.markdown
    else:
        raise command.Error('File extension not supported!')
    if os.path.exists(filename):
        content = processor(open(filename).read())
    else:
        raise command.Error('The file doesn\'t exists!')

    slides = []
    for slide in content.split('<hr />'):  # RST will write <hr /> in same way?
        slides.append(Slide(
            content=markdown2.markdown(slide)
        ))

    with open('/dev/stdout', 'w') as handler:
        write_to_file(handler, slides)


if __name__ == '__main__':
    main.command()
