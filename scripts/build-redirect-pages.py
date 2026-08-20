# -*- coding: utf-8 -*-
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SITE = "https://q3a.space/osp2"
PAGES = [
    "acknowledgements",
    "commands",
    "compilations",
    "gallery",
    "index",
    "tools",
]

T = {
    "lead_ru": "Сайт OSP2-BE переехал на новый адрес.",
    "lead_en": "The OSP2-BE website has moved to a new address.",
    "hint_ru": "перейти на новый сайт",
    "hint_en": "go to the new website",
    "redirect_ru": 'Перенаправление на новый сайт через <span class="sec">5</span> сек...',
    "redirect_en": 'Redirecting to the new site in <span class="sec">5</span> sec...',
    "now_ru": "Перейти сейчас",
    "now_en": "Go now",
}


def render(
    lang,
    redirect_page,
    *,
    forced_lang=None,
    redirect_mode="lang",
    redirect_hash="",
    show_lang_active=True,
):
    if redirect_mode == "root":
        target = "{0}/{1}".format(SITE, redirect_page)
    else:
        target = "{0}/{1}/{2}".format(SITE, lang, redirect_page)
    if redirect_hash:
        target = "{0}#{1}".format(target, redirect_hash)

    attrs = ['lang="{0}"'.format(lang), 'data-redirect-page="{0}"'.format(redirect_page)]
    if forced_lang:
        attrs.append('data-forced-lang="{0}"'.format(forced_lang))
    if redirect_mode != "lang":
        attrs.append('data-redirect-mode="{0}"'.format(redirect_mode))
    if redirect_hash:
        attrs.append('data-redirect-hash="{0}"'.format(redirect_hash))

    if show_lang_active:
        ru_active = ' class="is-active"' if lang == "ru" else ""
        en_active = ' class="is-active"' if lang == "en" else ""
    else:
        ru_active = ' class="is-active"'
        en_active = ""

    return """<!DOCTYPE html>
<html {attrs}>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="5;url={target}">
  <title>OSP2-BE</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/redirect.css">
</head>
<body>
  <div class="bg-grid" aria-hidden="true"></div>
  <div class="bg-orb" aria-hidden="true"></div>
  <nav class="lang" aria-label="Language">
    <button type="button" data-set-lang="ru"{ru_active}>RU</button>
    <button type="button" data-set-lang="en"{en_active}>EN</button>
  </nav>
  <main>
    <h1>OSP2-BE</h1>
    <p class="lead" data-lang="ru">{lead_ru}</p>
    <p class="lead" data-lang="en">{lead_en}</p>
    <a class="site-link" data-outbound href="{target}" rel="noopener">
      <span class="site-link-url">q3a.space/osp2</span>
      <span class="site-link-hint" data-lang="ru">{hint_ru}</span>
      <span class="site-link-hint" data-lang="en">{hint_en}</span>
    </a>
    <p class="redirect" data-lang="ru" aria-live="polite">{redirect_ru}</p>
    <p class="redirect" data-lang="en" aria-live="polite">{redirect_en}</p>
    <p class="redirect-now" data-lang="ru"><a data-outbound href="{target}">{now_ru}</a></p>
    <p class="redirect-now" data-lang="en"><a data-outbound href="{target}">{now_en}</a></p>
  </main>
  <footer>OSP2-BE</footer>
  <script src="/assets/redirect.js"></script>
</body>
</html>
""".format(
        attrs=" ".join(attrs),
        target=target,
        ru_active=ru_active,
        en_active=en_active,
        lead_ru=T["lead_ru"],
        lead_en=T["lead_en"],
        hint_ru=T["hint_ru"],
        hint_en=T["hint_en"],
        redirect_ru=T["redirect_ru"],
        redirect_en=T["redirect_en"],
        now_ru=T["now_ru"],
        now_en=T["now_en"],
    )


def write(path, text):
    path.write_text(text, encoding="utf-8", newline="\n")


def main():
    # Root chooser (no forced lang) — separate EN/RU "go now" fallbacks
    root = render("ru", "index.html", show_lang_active=True)
    root = root.replace(
        '<p class="redirect-now" data-lang="en"><a data-outbound href="https://q3a.space/osp2/ru/index.html">Go now</a></p>',
        '<p class="redirect-now" data-lang="en"><a data-outbound href="https://q3a.space/osp2/en/index.html">Go now</a></p>',
    )
    write(BASE / "index.html", root)

    for lang in ("en", "ru"):
        out_dir = BASE / lang
        out_dir.mkdir(parents=True, exist_ok=True)
        for page in PAGES:
            write(
                out_dir / "{0}.html".format(page),
                render(lang, "{0}.html".format(page), forced_lang=lang),
            )

    support = render("ru", "index.html", redirect_hash="support", show_lang_active=True)
    support = support.replace(
        '<p class="redirect-now" data-lang="en"><a data-outbound href="https://q3a.space/osp2/ru/index.html#support">Go now</a></p>',
        '<p class="redirect-now" data-lang="en"><a data-outbound href="https://q3a.space/osp2/en/index.html#support">Go now</a></p>',
    )
    write(BASE / "support.html", support)
    write(
        BASE / "service.html",
        render("ru", "service.html", redirect_mode="root", show_lang_active=True),
    )
    write(
        BASE / "preview-generator.html",
        render("ru", "preview-generator.html", redirect_mode="root", show_lang_active=True),
    )

    print(
        "Built index, support, service, preview-generator, and {0} lang pages.".format(
            len(PAGES) * 2
        )
    )


if __name__ == "__main__":
    main()
