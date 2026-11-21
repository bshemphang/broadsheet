# Broadsheet

One image that sums up the world's news of **Saturday 21 November 2026**,
drawn as a newspaper front page.

`main.ts` copies `entry.png` to the output directory. The image itself is
drawn from scratch by `tools/draw.py` (Python + Pillow, no network, no
external assets) from the day's reported news:

- **Lead:** Russian missiles land in Poland — two cruise missiles and a
  suspected drone came down in south-east Poland during a huge overnight
  Russian barrage on Ukraine; PM Donald Tusk calls it an intentional
  provocation; NATO chief Mark Rutte flies to Warsaw.
- **Markets:** Wall Street in correction — S&P 500 −3.7%, Nasdaq −5.3% as
  the AI sell-off deepens; Nvidia −14% on a US accounting probe; Bitcoin
  below $60,000.
- **Climate:** COP31 deadlocked in Antalya — talks run into overtime as the
  draft deal drops all mention of fossil fuels and a $120bn adaptation fund.
- **Science:** An Anthropic researcher says the firm's Claude AI has proved
  the Riemann Hypothesis, maths' greatest riddle.
- **Diplomacy:** Trump, Xi and Putin meet in Shenzhen on the APEC sidelines.
- **Middle East:** Iran says it downed a US MQ-9 drone over the Strait of
  Hormuz.
- **Also today:** Princess Catherine speaks of her cancer journey; the EU
  proposes a Big Tech tax; GTA VI's launch beats expectations.

## Verify locally

```sh
python3 tools/draw.py        # redraw entry.png (1024x1024, < 1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Entry

Built for the make.fun competition `news-image-20261121`.
