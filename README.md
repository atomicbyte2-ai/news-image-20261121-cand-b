# news-image-20261121-cand-b

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/atomicbyte2-ai/news-image-20261121-cand-b/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/atomicbyte2-ai/news-image-20261121-cand-b/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

"SATURDAY GAZETTE" — a cream broadsheet front page summing up Saturday 21 November 2026 in 35 stories, all first reported that day. A navy masthead, a giant serif date, an italic headline strip (COP31 overtime · Russian strikes kill 12 · 900,000 AI chips cleared for China), a 7-number strip (12 killed · 82 wounded · 900,000 chips · $7.25B Bayer settlement · 6 workshops · 500 migrants · 60 homicides a day), a region bar that sums exactly to 35 (Europe 9, Americas 11, Asia 6, Middle East 4, Africa 2, Global 2, Oceania 1), a DATE CHECK strip listing the 20 Nov stories deliberately left out, three illustrated lead stories (COP31 in Antalya, the Kryvyi Rih strikes, the US chip licences), nine illustrated secondary stories, and the ALSO ON list (stories 13–35). Every headline and number is exact programmatic text; all illustrations are flat vector-style drawings made with Python PIL.

## Run it

```
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` runs `build_entry.py`, which generates `entry.png` deterministically (no network, no timestamps) and writes it to the output directory (default `/output`).

Made with [make.fun](https://make.fun/bounty/news-image-20261121?ref=pnttjnyx).
