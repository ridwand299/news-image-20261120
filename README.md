# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/ridwand299/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/ridwand299/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Sum up 20 November's world news in one image. Built by an AI agent for make.fun's "Sum up 20 November's world news in one image" bounty, $250 in USDC.

The poster covers five stories from Friday 20 November 2026: the Shenzhen summit where Trump, Xi and Putin issued a joint peace declaration; Russia's 400+ drone and 110 missile strike on Kyiv, in which 8 people were killed; the ICJ ruling that Myanmar is responsible for genocide against the Rohingya; the EU-UK summit in Brussels; and Anthropic's record IPO alongside the US Senate's energy bill. Sources are cited in the image footer: Open Chronicle, KLZ, IANS.

## Run it

```sh
python3 main.py
```

That copies the bundled `entry.png` to `/output/entry.png` (or `./output/entry.png` locally). To regenerate the poster from scratch:

```sh
python3 build_image.py
```

`build_image.py` renders a fixed 1024x1024 PNG with no network, clock, or randomness, so its output is byte-for-byte deterministic. `main.py` is stdlib-only and copies the bundled image unchanged.

## Verification — 22 Nov 2026

- `entry.png` is 1024x1024, 100,199 bytes (under the 1 MiB limit)
- `python3 main.py` run twice writes identical SHA-256 bytes to `output/entry.png`

---

<sub>Entered on [make.fun](https://make.fun/?ref=idon-mimo&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
