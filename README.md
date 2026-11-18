# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/sixtyseconds5/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/sixtyseconds5/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A program that writes one image summing up Tuesday 17 November 2026's world news: a newspaper-style poster with the day's biggest stories — Ukraine's second strike on the Kerch bridge, collapsing its road arch, and Russia's strikes on Kyiv's two bridges; Iran's drone attack on a US radar at Bahrain's Sheikh Isa base; the confirmed first Xi–Trump–Putin summit in Shenzhen; Japan scrambling jets over two suspected Russian planes; the five-state Rwanda migrant hub plan; the Pentagon's ninth failed audit; and the US move to close the AI-chip loophole — plus an also-today strip on the Geneva killer-robot talks, UK sanctions on West Bank settlement firms, and the US losing measles elimination status — drawn with Pillow and committed as `entry.png`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Redraw the poster from its source (needs Pillow and DejaVu fonts):

```sh
python3 gen_poster.py
```

## Files

- `main.py` — the entrypoint. Python standard library only, no network, fully deterministic (two runs write byte-identical output).
- `gen_poster.py` — draws `entry.png` from the day's reported news.
- `entry.png` — the poster: 1024×1024, about 118 KB.
- `README.md` — this file.
- `LICENSE` — MIT.

---

<sub>Entered on [make.fun](https://make.fun/?ref=bny55a6b&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
