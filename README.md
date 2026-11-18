# The World in One Day — 17 November 2026

A 1024×1024 newspaper front page, "THE WORLD IN ONE DAY", summarising
Tuesday 17 November 2026 in seven stories. The lead story is Ukraine
hitting the Crimea bridge again while Russia strikes Kyiv's crossings,
illustrated with a broken bridge, a blast plume and a fallen arch in the
strait. Below it, six more stories in a two-by-three grid: Iran firing
drones at a US base in Bahrain; the Xi–Trump–Putin summit confirmed for
Shenzhen; Japan scrambling jets over Russian planes; five states planning
a Rwanda migrant hub; the Pentagon failing its audit for a ninth year;
and the US moving to close the AI-chip loophole. An "ALSO TODAY" strip
at the foot covers the UN killer-robot talks, UK sanctions on West Bank
settlement firms, and the US losing measles elimination status. Every
illustration is drawn from scratch with Pillow shapes — no photos.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Redraw the poster from scratch:

```sh
python3 gen_poster.py
```

## Files

- `gen_poster.py` — draws the poster with Pillow and saves `entry.png`
- `main.py` — copies `entry.png` into `$MAKEFUN_OUTPUT_DIR` (default `/output`)
- `entry.png` — the finished 1024×1024 poster
