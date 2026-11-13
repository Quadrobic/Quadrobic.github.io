# Formal model of the treatise

Checked with Agda 2.8.0.2 and the installed Agda standard library. This directory
contains the model and verification tools. The public pages are generated from
a verified snapshot of these sources.

## Verification

From the repository root:

```sh
python3 agda/check.py
```

From this directory:

```sh
python3 check.py
```

The first run compiles the required library modules and takes longer. The script
does not download dependencies or modify the system installation. It copies the
standard library sources into the ignored `_build/stdlib` directory, where Agda
can write interface files. The default source is `/usr/share/agda-stdlib`.
To use another installation:

```sh
python3 check.py --stdlib /path/to/agda-stdlib
# Alternatively: AGDA_STDLIB=/path/to/agda-stdlib python3 check.py
```

`python3 check.py --fresh` removes only generated `.agdai` files under this
directory and checks everything again. The complete log is `_build/check.log`.
After library preparation, open `All.agda` in an Agda-enabled editor;
`imperium.agda-lib` supplies the local include paths. The intentionally invalid
files under `tests/reject/` are excluded from `All.agda`.

Verification uses `--safe --without-K`. Unsolved holes, postulates, and bypasses
for termination, positivity, or coverage checking are not permitted. Warnings
are errors, with one exception: `UnsupportedIndexedMatch`, also suppressed by
the installed standard library for its Cubical transport computation warning.
This project does not claim Cubical Agda compatibility.

## Modules

| Module | Content |
| --- | --- |
| `Imperium/Core.agda` | Histories, two extensions of any finite past, and impossibility of finite certification or condemnation. |
| `Imperium/Signs.agda` | Nonempty observation windows, adjacent-sample trends, consecutive windows, revocable recognition, and observational independence. |
| `Imperium/Empire.agda` | A nonempty Empire; distinct support, appropriated authority, and voice relations; three concrete networks. |
| `Imperium/Roles.agda` | The Emperor's role combines actual support with observed recognition; neither direction implies eventual liberation. |
| `Imperium/Protection.agda` | Sufficient minimal protection, injury accounting, release when the threat ends, and persistence of recorded damage. |
| `Imperium/Structure.agda` | Three threads, boundary versus wall, movement in both forms, beast identity, and shadow beyond beasts. |
| `Imperium/DeathStar.agda` | Collective responses to personal contributions, a parameterized response rule, transitions, exit invariants, and recovery. |
| `Imperium/CollectiveExamples.agda` | One participant freeing or trapping everyone, competing contributions, and later collective release. |
| `Imperium/Axioms.agda` | Separate `ModelContracts` and `Theorems`, their constructive instances, and the enclosing `Doctrine`. This does not encode all six axioms of the treatise. |
| `Imperium/Checks.agda` | Positive examples and checks of theorem boundaries. |
| `All.agda` | The single entry point for all valid modules. |

Code comments and technical documentation are in English. Russian transliterations
in identifiers are replaced with descriptive English names. Sanskrit and Jain terms
retain their established spellings: `Siddha`, `SiddhaFrom`, `EventuallySiddha`,
`shakti`, and `kashaya`. A jiva is a participant; Shakti and kashaya denote the
returning and grasping influences represented by the example labels. These terms
are not replaced by English approximations. The public explanation remains bilingual.

## Corrections to the initial model

1. Module names such as `Imperium.Core` require files under `Imperium/`, rather
   than directly under `agda/`. Once relocated, the original five modules passed
   type checking; their main weaknesses concerned interpretation, not proof terms.
2. `Siddha h = ∃ T. ∀ t ≥ T. h t = flow` means eventual permanent freedom
   from grasping, not freedom now. `SiddhaFrom h T` and `EventuallySiddha h` make
   the distinction explicit; `Siddha` is a documented alias for the latter.
3. The original zero-length recognition window accepted every observation.
   `Recognized` now requires positive length and checks every adjacent sample,
   preventing equal endpoints from hiding regression. `Sustained` joins windows.
4. Support was conflated with authority. Prohibiting anyone from supporting
   everyone is stronger than prohibiting a throne. `Holds`, `Rules`, and
   `Voices` now describe distinct relations.
5. A single nontransitive support example cannot establish that every network
   must be nontransitive. Both transitive and nontransitive instances are supplied.
6. Opposing numerical bounds originally made restriction equal threat by
   definition. Sufficiency now concerns residual harm; minimality compares
   available sufficient actions on the restriction scale.
7. Failure to construct a `Doctrine` instance does not itself prove inconsistency.
   A lemma, assumption, or proof strategy may be missing. Refutation requires
   a corresponding proof term or countermodel.
8. Personal choices originally produced independent gates. This excluded a
   collective explosion or captivity caused by one participant. The corrected
   model distinguishes personal contributions from shared outcomes.

## Finite histories and liberation

`Agrees n h h′` means agreement on `[0,n)`, excluding time `n`. `thaw n h`
extends that past with `flow` forever; `freeze n h` extends it with `grip`.
The constructive witnesses are named `thawing-extension` and
`gripping-extension`. Their epistemic consequences are separate theorems:

- `no-finite-certificate`: a finite past cannot certify eventual liberation
  across all compatible continuations.
- `no-finite-condemnation`: a finite past cannot rule out eventual liberation
  across all compatible continuations.

**Assumption:** `History = ℕ → Act` permits arbitrary continuations. No dynamics
exclude future actions. The extension theorems therefore establish possibilities
in this model, not the immediate accessibility of any future to a real person.
A constrained dynamical model would require new admissibility proofs.

`SiddhaFrom` also quantifies over an infinite future. It is neither a computable
present state nor evidence obtainable from today's experience.
`Checks.not-free-now` exhibits eventual freedom alongside present grasping.

## Observation and the Emperor's role

`Obs` uses three natural numbers as abstract ordinal scores. Neither these
numbers, an observation unit, nor the duration of a year is specified by the
treatise.

`Recognized` is a deliberately conservative criterion for an **observable basis**
of recognition, not a complete definition of maturity. Stable scores are allowed;
strict improvement at every sample is unnecessary. Adjacent-sample checking is
stronger than endpoint checking. This does not assert that the doctrine forbids
temporary freezing or that every fluctuation refutes maturity. A closer model
would need smoothing, observational error, and recovery after regression. None
of that statistics is present: the finite criterion is an explicit modeling choice.

`Sustained` requires a positive number of consecutive windows. The example
`many-windows` satisfies ten windows of length 12 without certifying liberation.
These units are abstract; this is not a claim that 120 months suffice.

`Life.acts` and `Life.observed` are independent. Counterexamples therefore prove
independence of predicates **within this model**, not psychological facts about
liberated people. Observation may be incomplete.

`EmperorStatus` adds actual support for someone else to the observable criterion.
The reverse counterexample does not depend on deteriorating scores: a person
without grasping, whose scores meet the criterion, receives support but provides
none. Every participant still has another supporter. Liberation and the Emperor's
role do not form a hierarchy. `revocable-status` also shows recognition of the
whole role being withdrawn while the capacity to support remains.

## Support, authority, and voice

`Rules` means an **appropriated right to decide for another riverbed**, not
temporary coordination of a shared task. `no-throne` prohibits this relation.
It is a normative obligation of an instance, not a consequence of arbitrary
graph structure.

`no-whole-voice` gives each voice an `Aspect` it does not express. `heard`
requires every aspect to be expressed by someone. Together with `member`,
these exclude both an empty model and a model containing only an inexpressible
aspect. `Aspect` is a representation parameter, not a Source type or a final
classification of its manifestations.

The three-person circle witnesses possible nontransitive support. The network
where everyone can support everyone witnesses transitive support without
appropriated authority or a single complete voice. Relaying help does not itself
create subordination.

## Protection and its cost

`Problem` specifies available actions and three separate quantities for each:

- `restriction`: the imposed constraint;
- `residual`: the remaining threat or harm;
- `wound`: injury inflicted by the intervention itself.

The explicit `idle` assumptions say that inaction imposes no restriction,
inflicts no new injury, and leaves the original threat unchanged.
`Proportionate` requires sufficiency, least restriction among sufficient actions,
and least injury among equally restrictive actions. The final tie-breaking rule
is an explicit formal policy consistent with avoiding unnecessary harm.

When the threat is zero, `idle` is a sufficient competitor. `released-choice`
and `released-no-new-wound` derive zero restriction and zero new injury.
This releases constraints; it does not erase history.

In the concrete episode, restriction 1 stops threat 3; restriction 2 is excessive.
The necessary action inflicts injury 1. At the next step the threat is gone and
restriction is lifted, but recorded damage remains 1. Each new injury adds to
previously recorded damage: one entry cannot absorb several successive injuries.
Sufficiency thus means neither equality with threat nor harmlessness nor complete
repair. Monotone `damage` records what was inflicted; it does not forbid healing.

This remains an abstract choice model, not a definition of harm to particular
living beings. It does not establish that consequences are always accurately
known. Interaction between riverbeds, uncertainty, respect for another's boundary,
and duties of repair need further modeling. `Proportionate` contains no moral
valuation; no theorem declares a necessary injury good.

## Structural distinctions

`Encounter` stores three structural components. `Connection` is an external
parameter witnessing a connection, not a model of the Source or the content of
the inner voice. There is no Source type.

`MovingForm` requires movement for both repetition and renewal. This is a
structural distinction, not a physical model of crystals or biology.
`acknowledge` changes a beast's recognition status while preserving its identity.
`ShadowItem` also includes a rejected human feeling, so shadow is not reduced
to beasts. Removing a wall preserves the participant's own boundary.

## Death Star dynamics: personal choices, collective effects

Personal ownership of a choice does not imply independent consequences.
The model distinguishes intention, effective contribution, and the shared
`explosion` or `enclosure` outcome for everyone still inside. This is neither
majority voting nor a right to choose another person's inner life. One person's
life force can help destroy the common center; another's grasping force can trap
even those who intended to return. Participants, identities, and intentions
remain distinct.

### The response contract

`CollectiveRule` is an explicit circle parameter. It supplies `Input`, personal
`choice`, evidence of `ReturningPower` and `GrippingPower`, the `Responds`
relation, and an internal participant witnessing the effective contribution.

The core introduces neither numerical energy nor arithmetic for contributions
nor a universal priority of life over grasping. An actual `resolve-step` needs
`EffectiveOutcome` evidence under the chosen rule. A state update alone is not
an executed transition.

`CollectiveExamples` provides a **demonstration possibility instance**: a returning
contribution permits explosion; a grasping contribution permits enclosure.
When both are present, both outcomes are possible. This does not settle what
actually happens when the forces compete. A balance, threshold, or priority rule
can later replace this instance through `CollectiveRule` without changing the
core or its general proofs.

In the return example, only `a` supplies effective life force; `b` and `c` choose
differently. In the captivity example, all three intend to return, but `b` supplies
effective grasping force and closes everyone's exit. These are concrete witnesses
of the requested possibilities, not universal victory rules for either force.

### Exit and collective response

`Exit g p h` is an executable local action: `p` is inside with an unlocked gate
and ends outside. `exit-arrives-outside` verifies that participant's position.
A local departure does not automatically take a neighbor out. Collective explosion
is a different transition, opening exits for everyone remaining inside.

`MayLeave g p` means that `p` is already outside or has an available `Exit`:

```agda
EscapeInvariant g = ∀ p → MayLeave g p
```

`resolve g outcome shape` applies a shared outcome to those still inside.
`shared-inside-gates` excludes independent gate results within one resolution.
Those who left are not recaptured. An effective response needs an internal
catalyst; a circle everyone has left has no such witness.

### Possible and admissible transitions

`RawStep` includes approaching the brink, local exit, reshaping, local assistance,
rekindling, and collective response under `CollectiveRule`. Harmful nights remain
possible. `Admissible` does not require unanimous `reclaim`: explosion enabled by
one participant is admissible; collective enclosure is possible but inadmissible.
The target state's safety is not assumed in `Admissible`.

The following results are checked:

- `admissible-preserves`: an admissible step preserves everyone's exit from a
  safe starting state.
- `trace-preserves` and `run-preserves`: preservation through finite traces and
  at every step of an infinite admissible run.
- `explosion-frees-all`: a collective explosion opens every remaining person's
  exit, not only the catalyst's.
- `compression-violates` and `compression-not-admissible`: enclosure violates
  the invariant when someone remains and cannot be an admissible step.
- `raw-preservation-false`: effective grasping can produce a safety violation
  from a safe starting circle.
- `single-shakti-step` and `single-kashaya-step`: one participant's
  effective contribution can affect everyone immediately.
- `same-c-contribution` and `shared-outcomes-differ`: another person's contribution
  can change the shared result while one's own complete contribution stays fixed.

Contributions may be mixed; a single shared outcome does not create independent
personal doors. Two resolutions of the contested demonstration input expose the
response rule's explicitly unresolved arbitration rather than silently choosing
a winner.

### After captivity

`recover g p` is local assistance to one participant, not a collective explosion.
This limits the particular action; it does not prohibit one person helping everyone.

`rekindle-step` returns the circle to the brink without automatically lifting
captivity. A later effective life-force contribution can then enable a collective
explosion freeing everyone (`later-explosion-frees-all`). Captivity is not made
an eternal verdict contradicting the opening described in §11.

Later release does not retroactively make a harmful transition admissible, nor
turn the entire history into a safe trace. Safety also does not imply eventual
completion: `quiet-run` may continue without a collective resolution while keeping
exits available.

These theorems do not establish real efficacy of either force, lived experience,
a specific arbitration law, or physical feasibility. They are conditional on the
explicit model dynamics.

## Contracts and theorems

```agda
record Doctrine : Set₁ where
  field
    contracts : ModelContracts
    theorems : Theorems
```

`ModelContracts` collects representation properties: initial openness, shared
responses, and preservation of riverbed, boundary, and beast identity. Agda checks
these equalities, but they are not presented as discoveries about gathering dynamics.

`Theorems` collects derived consequences: no finite certificate, revocable
recognition, protection results, invariant preservation, and the compression
counterexample. They are conditional theorems in the chosen model, not proof
that actual gatherings always follow the protocol. This distinction does not
remove the dependence of theorems on definitions.

Example access:

```agda
Theorems.ax-no-finite-cert (Doctrine.theorems imperium)
```

The experience of the Death Star, the content of the inner voice, and the nature
of the Source are not encoded as data or postulates. Qualitative contribution
labels describe neither the complete nature of the forces nor their magnitude.

## Negative checks

The script requires Agda to reject **all seventeen** intentionally invalid files.
It checks the error category, so a missing import or typo cannot count as success.

| Fixture | Claim that must remain rejected |
| --- | --- |
| `ZeroWindow` | Recognition from a zero-length window. |
| `FiniteCertificate` | Certification of all futures from a finite past. |
| `HiddenRegression` | Equal endpoints hiding an intermediate regression. |
| `SupportTransitivity` | Unsupported transitivity of the circular support network. |
| `ForcedRetention` | Captivity after a successful collective return. |
| `CompressionAdmissible` | Treating enclosure with remaining participants as admissible. |
| `CompressionFree` | Exiting through a gate closed by compression. |
| `NoPrivateExitDuringCapture` | Deriving exit from personal intention during shared captivity. |
| `NeighbourExit` | A local departure automatically taking a neighbor outside. |
| `LocalRepairIsNotBurst` | Equating local assistance with collective explosion. |
| `UnanimityRequired` | Deriving unanimity from an explosion enabled by one person. |
| `OutsideCatalyst` | Treating a departed participant as an internal catalyst. |
| `NoCollectiveInfluence` | Claiming another person's grasping leaves one's shared outcome unchanged. |
| `FutureIsNow` | Replacing eventual liberation with present freedom. |
| `ErasedWound` | Erasing recorded damage after restrictions end. |
| `UnsafePostulate` | Completing a proof with an arbitrary postulate. |
| `UnsolvedHole` | Leaving a hole instead of a proof. |

Exit status 0 from `check.py` means both positive acceptance and expected negative
rejection succeeded.

## Publishing the bilingual pages

From the repository root:

```sh
python3 agda/build_web.py
```

The builder first runs `check.py`. Only after success does it invoke
`agda --html --highlight-occurrences` and generate `formalization.html` and
`formalization.en.html`. Published excerpts come from native Agda highlighting
and are checked against the source text. Links lead to definitions in full modules.

`web_content.py` supplies bilingual explanations and stage order;
`web_template.html` supplies the page template. Technical sources remain here.
`formalization/` contains generated module pages, the source archive including
verification tools, and `verification.json` with source hashes. The system standard
library is not published: its names retain highlighting without broken module links.

The build is integrated into `rebuild.sh`; `tools/watch.py` watches Agda sources.
The browser displays build-time verification results, not a local Agda execution.
After model changes, rebuild the pages: the archive and manifest describe the
published source snapshot.
