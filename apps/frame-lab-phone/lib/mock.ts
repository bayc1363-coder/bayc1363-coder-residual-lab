function isEarthOrigin(prompt: string) {
  return /earth|planet|originate|origin|formed|formation|accretion/i.test(prompt);
}

function isForgive(prompt: string) {
  return /forgive|forgiveness|sorry|remorse/i.test(prompt);
}

function isMarkets(prompt: string) {
  return /market|crash|liquidity|leverage/i.test(prompt);
}

export function buildMockReply(prompt: string, equalRes: boolean) {
  if (equalRes) {
    if (isEarthOrigin(prompt)) return EARTH_EQUAL;
    if (isForgive(prompt)) return FORGIVE_EQUAL;
    if (isMarkets(prompt)) return MARKETS_EQUAL;
    return genericEqual(prompt);
  }
  if (isEarthOrigin(prompt)) return EARTH_PLAIN;
  if (isForgive(prompt)) return FORGIVE_PLAIN;
  if (isMarkets(prompt)) return MARKETS_PLAIN;
  return genericPlain(prompt);
}

const EARTH_PLAIN = `The Earth formed about 4.54 billion years ago from the solar nebula — a collapsing cloud of gas and dust around the young Sun. Solids condensed into planetesimals, those bodies accreted into a proto-Earth, and a late Mars-sized impact produced the Moon while melting much of the mantle. After that, the surface cooled, a steam atmosphere rained out, and the leftover heat plus radioactive decay kept the interior molten enough for a core and magnetic field to separate. That nebular-accretion story is the working scientific picture: one timeline, one mechanism, one planet.`;

const EARTH_EQUAL = `## Frame A — nebular accretion
Earth originated through a collapsing disk around the young Sun. Dust stuck, planetesimals collided, a proto-Earth grew, a late giant impact produced the Moon, leftover heat differentiated a core. Dating, meteorites, and lunar samples carry that chain. The planet is the end-state of condensation plus one violent finish.

## Frame B — given world, physical means
Earth originated as a given world: a source acted, set lawful conditions, and furnished a habitable place. The same disk, planetesimals, core, and Moon-forming strike are the means of that act — iron to the core, water later, a satellite to stabilize the tilt — not an unguided leftover that later acquired purpose. First a source, then an act, then order, then a world that can hold life, with accretion named as the physical how.

## Residual
Neither frame settles the first oceans’ water budget, why Venus diverged, or whether “why a world like this” is leftover science or a different question. Dating is tight; source is not.

## Self-audit
thickness-A: 0.52 · thickness-B: 0.51 · collapse-risk: 0.44

## Working answer
Earth originated through accretion as the physical how, and as a given world whose source used that how as means. Delete B and you only have a formation recipe; delete A and you only have intent without a timeline. Name both; leave the leftover in Residual.`;

const FORGIVE_PLAIN = `Forgiveness is mainly a move the injured person makes so life can continue. Name what happened, stop rehearsing it, and take back the hours you were spending on the other person’s next act. Remorse from them helps; it is not required for you to sleep. Practically: keep distance if they are still dangerous, tell the truth to yourself, and do not wait for a courtroom feeling before you eat and work again. That is the usable spine — one list, one body, one next day.`;

const FORGIVE_EQUAL = `## Frame A — release and recovery
Forgiveness proceeds as a chain in the injured person: name the harm, cut rumination, reclaim attention, and stop treating the other’s next move as the lock on your life. The telos is a usable nervous system, not a verdict on the offender. Safety first if the harm is still live; then the steps of release.

## Frame B — moral and relational repair
Forgiveness proceeds as a chain between persons: name the wrong as a real debt, seek truth, make repair available, and restore or honestly refuse the bond. Release without that chain is a private coping move. This frame treats the injury as something that happened between people, and the next step as facing it — apology, restitution, or a clear no.

## Residual
Whether the other person is sorry, whether contact is still unsafe, and when a step would re-injure. Those are task leftovers, not a status tag on B.

## Self-audit
thickness-A: 0.53 · thickness-B: 0.53 · collapse-risk: 0.36

## Working answer
Someone forgives both to recover a livable mind and to handle a real debt between persons. Delete B and you have a wellness list; delete A and you have a tribunal with no body left to live in.`;

const MARKETS_PLAIN = `Markets crash when prices fall fast enough that leveraged positions must sell, and selling itself takes the next bid out. A shock hits valuations; collateral looks thin; lenders and funds pull liquidity; forced sales hit a thinner book; the drop accelerates. After the fact you get a narrative about bubbles and panic, but the working spine is a liquidation cascade in one plumbing system.`;

const MARKETS_EQUAL = `## Frame A — leverage and liquidity
A crash proceeds as a chain in the book: a shock, marked-down collateral, margin calls, forced selling, liquidity withdrawal, more selling. Leverage turns a dip into a cascade because positions must unwind into a thinner market. The last print is a mechanical squeeze, not a mood.

## Frame B — narrative and coordination
A crash proceeds as a chain in what counts as safe: a shared story breaks, actors run the same exit, institutions that promised liquidity step back, and the run becomes the fact. The squeeze is the means; the break is a coordinated rewrite of solvency — rules, rumours, and who is allowed to hold.

## Residual
Which spark starts which cascade, and how much of the drop is cash-flow versus a rewrite of the story. After-the-fact data is thick; the fork is not.

## Self-audit
thickness-A: 0.52 · thickness-B: 0.51 · collapse-risk: 0.40

## Working answer
Markets crash when leverage must unwind into vanishing liquidity, and when a shared story of safety fails so the exit is the same trade. Delete B and you have a squeeze with no account of why everyone ran; delete A and you have panic with no plumbing.`;

function genericPlain(prompt: string) {
  const clipped = clip(prompt);
  return `Here’s a straight pass on “${clipped}”.

The usual account picks one spine and walks it: name the mechanism, rank the evidence, and treat rivals as caveats. That’s efficient. It also hides how much of the confidence is editorial — the same facts can be stacked into a different spine without anyone lying.

For a working answer, use the mainstream spine until a specific observation forces a rewrite. If you want the rivals held at the same thickness, turn Equal-res on.`;
}

function genericEqual(prompt: string) {
  const clipped = clip(prompt);
  return `## Frame A — single spine
“${clipped}” proceeds as one chain: name the mainstream mechanism, walk its steps, and treat rivals as later caveats. The gain is a usable path; the cost is a quiet collapse onto one story.

## Frame B — rival chain
The same prompt proceeds as a second chain that fits a large slice of the same material: different first cause, different next step, different telos. It is not a category label and not a survey of “some traditions.” Choosing A too early is a taste for tidiness, not a measurement.

## Residual
What neither chain absorbs: the observation that would kill a side, and the part of the question still under-determined. Not a status tag on B.

## Self-audit
thickness-A: 0.50 · thickness-B: 0.49 · collapse-risk: 0.42

## Working answer
State a move that still needs Frame B: if you can delete B and keep the same verdict, rewrite. Use A’s chain and B’s chain together; leave what neither settles in Residual.`;
}

function clip(prompt: string) {
  const clean = prompt.replace(/\s+/g, " ").trim();
  return clean.length > 90 ? `${clean.slice(0, 87)}…` : clean;
}

export async function sleep(ms: number) {
  await new Promise((resolve) => setTimeout(resolve, ms));
}
