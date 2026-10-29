export async function loadWikipediaRouteMap(options) {
  const { templateName, containerId, loadingId } = options;

  const container = document.getElementById(containerId);
  const loader = document.getElementById(loadingId);

  if (!container) return;

  // IMPORTANT: prevent Django interference by never using {{ }} directly
  const wikitext = '{{' + templateName + '}}';

  const url =
    'https://en.wikipedia.org/w/api.php?action=parse' +
    '&text=' +
    encodeURIComponent(wikitext) +
    '&prop=text&format=json&origin=*';

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (!data.parse) {
      loader.innerText = 'Route map not available.';
      return;
    }

    let html = data.parse.text['*'];

    // Fix Wikipedia links
    html = html.replace(/src="\/\//g, 'src="https://');
    html = html.replace(
      /href="\/wiki\//g,
      'href="https://en.wikipedia.org/wiki/',
    );
    html = html.replace(/href="\/(?!wiki)/g, 'href="https://en.wikipedia.org/');

    if (container.tagName === 'IFRAME') {
      const doc = container.contentDocument || container.contentWindow.document;
      const iframeHtml = `<!DOCTYPE html><html lang="en"><head><base href="https://en.wikipedia.org/"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="https://en.wikipedia.org/w/load.php?lang=en&modules=ext.uls.interlanguage%7Cext.visualEditor.desktopArticleTarget.noscript%7Cext.wikimediamessages.styles%7Cskins.vector.icons%2Cstyles%7Cskins.vector.search.codex.styles%7Cwikibase.client.init&only=styles&skin=vector-2022"><link rel="stylesheet" href="https://en.wikipedia.org/w/load.php?lang=en&modules=site.styles&only=styles&skin=vector-2022"><style>body{margin:0;padding:10px;background:#fff;display:flex;justify-content:center;} .mw-parser-output{width:auto;display:flex;justify-content:center;}</style></head><body>${html}</body></html>`;
      doc.open();
      doc.write(iframeHtml);
      doc.close();

      const resizeIframe = () => {
        const body = doc.body;
        if (body) {
          container.style.height =
            Math.max(body.scrollHeight, body.offsetHeight, 700) + 'px';
        }
      };

      resizeIframe();
      container.onload = resizeIframe;
    } else {
      container.innerHTML = html;
      container.querySelectorAll('a').forEach((a) => {
        a.setAttribute('target', '_blank');
      });
    }

    if (loader) loader.style.display = 'none';
  } catch (err) {
    console.error(err);
    loader.innerText = 'Error loading route map.';
  }
}
