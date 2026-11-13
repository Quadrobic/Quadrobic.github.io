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
| `Imperium/IceDynamics.agda` | An explicit unit accretion/erosion contract, multi-step consequences, and the distinction between absent grasping and absent heedlessness. |
| `Imperium/Signs.agda` | Nonempty observation windows, adjacent-sample trends, consecutive windows, revocable recognition, and observational independence. |
| `Imperium/Empire.agda` | A nonempty Empire; distinct support, appropriated authority, and voice relations; three concrete networks. |
| `Imperium/Roles.agda` | The Emperor's role combines actual support with observed recognition; neither direction implies eventual liberation. |
| `Imperium/Protection.agda` | Sufficient minimal protection, injury accounting, release when the threat ends, and persistence of recorded damage. |
| `Imperium/Structure.agda` | Three threads, boundary versus wall, movement in both forms, beast identity, and shadow beyond beasts. |
| `Imperium/DeathStar.agda` | Collective responses to personal contributions, a parameterized response rule, transitions, exit invariants, and recovery. |
| `Imperium/CollectiveExamples.agda` | One participant freeing or trapping everyone, competing contributions, and later collective release. |
| `Imperium/Axioms.agda` | Separate `ModelContracts` and `Theorems`, their constructive instances, and the enclosing `Doctrine`. This does not encode every axiom of the treatise. |
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
   from grasping and heedless repetition, not freedom now. `SiddhaFrom h T` and `EventuallySiddha h` make
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

## Ice dynamics and the pramada refinement

`Act` now has `flow`, `grip`, and `pramada`. The last denotes heedless binding
repetition, not every missed perception, tired state, or unintended outcome.
`flow` means an attentive open response. It need not be infallible or harmless:
physical consequences remain separate data in `Protection`. Absence of grip
alone no longer suffices for `SiddhaFrom`, which still requires eventual `flow`.
All finite-prefix extension and non-certification proofs remain valid for this
larger action alphabet. The absence of pramada is NOT the absence of all mistakes.

`IceDynamics.step` is a representation contract: grip and pramada add one unit;
flow takes a predecessor, bounded below by zero. This models binding ice rather
than all memory or learning. Unit rates are chosen conventions, not psychological
measurements or a reproduction of the full classical karmic taxonomy.

`grip-grows` and `pramada-grows` derive exact growth under repeated binding
acts. `flow-clears` derives clearing of finite ice through sufficiently many flow
steps; `flow-keeps-clear` derives persistence of a clear state under flow.
`heedless-not-siddha` excludes the shortcut from absence of kashaya to liberation.
The update rules are collected under `ModelContracts`; their multi-step results
are collected under `Theorems`. No empirical rate, universal human recovery
schedule, real accessibility of every flow action, or repair of external harm
is established by these proofs. Histories still admit arbitrary future actions;
ice is accumulated state, not a new restriction on which actions are possible.

The revised prose separates an observable account of repeated responses within
one life from a metaphysical claim about karmic traces between incarnations.
Neither that empirical account nor rebirth is established by type checking.
Hridaya remains the mystical heart and an intentional boundary of the model;
its voice is not encoded as data.

The classical distinctions were checked against the translated primary text and
commentary: [Tattvartha-sutra VI.4](https://www.wisdomlib.org/jainism/book/tattvartha-sutra-with-commentary/d/doc1084801.html)
for samparayika/iryapatha influx, and [VIII.1](https://www.wisdomlib.org/jainism/book/tattvartha-sutra-with-commentary/d/doc1084866.html)
for the five causes of bondage, including pramada. The book's account of binding
ice is its own adaptation, not a claim that the whole classical taxonomy reduces
to two causes. Fear as a subsidiary passion is listed in the [translation of VIII.9](https://jainqq.org/pagetext/Tattvartha_Sutram/011035/149).

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
with neither grasping nor heedless repetition, whose scores meet the criterion, receives support but provides
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

## Death Star dynamics: three distinct levels

1. **Personal step at the brink:** `choice input p` belongs to that jiva. No
   companion makes it for them.
2. **Collective outcome:** `explosion` or `enclosure` determines the passage
   condition shared by everyone still inside. One effective contribution can
   change everyone's conditions without substituting for their personal choices.
3. **Personal path afterward:** an open passage is not a completed departure.
   Each participant must perform their own `Exit` transition.

`Gathering.passage` stores an exit condition, not a decision. The former
`authority` field has been removed: resolving the shared condition does not
assign anyone's inner authority. Participants, riverbed identities, and intentions
remain distinct.

### The response contract and personal choice

`CollectiveRule` supplies `Input`, personal `choice`, evidence of
`ReturningPower` and `GrippingPower`, and the `Responds` relation.
Its origin fields require an internal participant whose contribution is effective.
The `returning-choice` contract further requires that returning power belongs to
someone who personally chose `reclaim`. `explosion-has-personal-step` derives an
internal reclaim witness from any effective explosion. The choice field therefore
constrains possible responses rather than existing alongside an unrelated dynamics.
This connection is an explicit contract, not a proof of the forces' real efficacy.

The core introduces neither numerical energy, arithmetic for contributions, nor a
universal winner. A `resolve-step` requires `EffectiveOutcome` under the chosen
rule. Computing a state with `burst` or `compress` alone does not execute a step.

`CollectiveExamples` is a **demonstration possibility instance**. A returning
contribution permits explosion; effective kashaya permits enclosure. Both
outcomes are possible when both forces are present. A future arbitration rule
can replace this instance through `CollectiveRule` without rewriting the core.

In `one-shakti`, only `a` provides Shakti and chooses `reclaim`; the others need
not agree. Changing that contributor's choice to `surrender` removes this explosion
witness. In `one-kashaya`, everyone intends to return, but `b` supplies effective
kashaya and closes everyone's passage. Thus personal choice matters without
making each participant's intention sovereign over the collective conditions.
Neither example asserts a universal victory rule.

### Passage and departure

`Exit g p h` requires `p` to be inside with an unlocked passage and performs
`leave g p`. `exit-arrives-outside` verifies that participant's resulting position.
A local departure does not take a neighbor outside.

`MayLeave g p` means that `p` is already outside or has an available `Exit`:

```agda
EscapeInvariant g = ∀ p → MayLeave g p
```

`resolve` assigns one passage condition to everyone still inside;
`shared-inside-passages` checks that they receive the same shared result.
Those already outside are not recaptured. `resolve-preserves-position` is a
representation contract: neither outcome moves anyone outside. In particular,
`Checks.explosion-is-not-departure` leaves all participants inside after explosion;
`Checks.b-leaves-in-own-step` supplies a subsequent personal departure.

An effective response requires an internal catalyst. A circle everyone has left
has no such witness.

### Supported recovery

`Support g p` names **another** companion, proves that they differ from `p`, and
proves their passage is unlocked. This is an abstract witness of available support,
not a full account of trust, effort, or practical assistance. It does not promise
that every real companion can meet every need. A departed member can provide
support: support does not require remaining captive alongside the recipient.

Both `recover g p support` and `recover-step p ready support` require this witness.
It is not possible to bypass it by calling the state transformation directly.
`recovery-reopens` is explicitly conditional: given support, the modeled operation
opens a passage for its recipient. It does not establish that support always exists,
or that anyone can escape captivity through an unassisted effort.

`closed-circle-no-support` proves that when all passages are shut, no participant
has this support witness. The wholly captured example therefore has no immediate
local recovery. The positive recovery example uses a different history: `a` left
before enclosure and supports `b` afterward; `c` remains captive. Local recovery
opens `b`'s passage without moving `b` outside or freeing `c`.

A collective explosion is a separate way to reopen passages; it does not require
an already open companion. `rekindle-step` alone does not lift captivity, but a
subsequent effective explosion can open everyone's passage. This possibility is
not a guarantee of eventual release and does not declare captivity eternal.

### Normative admissibility and derived preservation

`RawStep` includes approach, personal exit, reshaping, supported local recovery,
rekindling, and collective response. Harmful outcomes remain possible.

`Admissible` is the Empire's **normative policy**. Its constructors permit the
other transitions and exclude enclosure. Consequently `compression-not-admissible`
is a direct consequence of that policy, proved by an empty pattern, not an
independent discovery about what gatherings can do. The `Theorems` field exposing
this result is retained as a checked policy consequence; it carries no additional
dynamical content. This status is stated at the definitions and in `Axioms`.

`admissible-preserves` is substantive for the remaining constructors: it analyzes
personal exits, supported recovery, collective explosion, and the transitions that
leave passages unchanged. Target safety is not a premise of `Admissible`.
No preservation guarantee is claimed for arbitrary `RawStep`.

Checked results include:

- `admissible-preserves`, `trace-preserves`, and `run-preserves`: preservation from
  a safe initial state, through one step, finite traces, and infinite admissible runs.
- `explosion-frees-all`: everyone remaining inside gains an available exit;
  personal departure is still required.
- `compression-violates`: enclosure violates the invariant if someone remains.
- `raw-preservation-false`: an effective enclosure can violate safety from a safe
  starting circle, despite the admissibility policy forbidding that step.
- `closed-circle-no-support`: wholly shut passages provide no local recovery witness.
- `explosion-has-personal-step`: an effective explosion has an internal catalyst
  whose own choice is `reclaim`, without requiring unanimity.
- `single-shakti-step`, `single-kashaya-step`, and `shared-outcomes-differ`: one
  person's effective contribution can change the collective passage conditions.

Later release does not retroactively make an enclosure admissible or turn a harmful
history into a safe trace. Safety does not imply completion: `quiet-run` may continue
without a collective resolution while preserving available exits.

These theorems do not establish physical feasibility, lived experience, real force
magnitudes, a specific arbitration law, or the availability of support. They are
conditional on the explicit representation and transition contracts.

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

The script requires Agda to reject **all twenty-five** intentionally invalid files.
It checks the error category, so a missing import or typo cannot count as success.

| Fixture | Claim that must remain rejected |
| --- | --- |
| `UnsupportedRecovery` | Treating another captive as an available support witness. |
| `SelfSupport` | Supplying oneself as the required other companion. |
| `ChoiceIgnored` | Ignoring the returning catalyst's personal choice. |
| `ExplosionIsDeparture` | Treating an open passage as an already completed return. |
| `NegligenceIsSiddha` | Mistaking endless pramada without grasping for siddhahood. |
| `NoNegligentAccretion` | Denying accretion caused by pramada. |
| `OneFlowErasesIce` | Erasing arbitrary old ice with one flow action. |
| `FlowHasNoEffect` | Denying erosion through repeated flow actions. |
| `ZeroWindow` | Recognition from a zero-length window. |
| `FiniteCertificate` | Certification of all futures from a finite past. |
| `HiddenRegression` | Equal endpoints hiding an intermediate regression. |
| `SupportTransitivity` | Unsupported transitivity of the circular support network. |
| `ForcedRetention` | Captivity after a successful collective return. |
| `CompressionAdmissible` | Treating enclosure with remaining participants as admissible. |
| `CompressionFree` | Exiting through a passage closed by compression. |
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

### Claim-level reading annotations

`web_annotations.py` records reviewed links from numbered treatise sections to
specific claims. Statuses distinguish proved model consequences, definitional
contracts, open parameters, deliberate exclusions, and text not yet covered.
A status never certifies an entire philosophical section. In particular, the
listening exercises in §16 are not the observational criterion modeled for §17.

After verification, `build_web.py` exports `formalization/annotations.json` with
native Agda excerpts, definition links, and the verification snapshot hash. The
main site builder rejects a stale snapshot. `tools/model_annotations.py` renders
the reading notes and the separate RU/EN connection maps from that export and
the parsed treatise. Graph edges represent explicit textual section references,
not logical implication or formal proof dependencies.

`rebuild.sh` verifies and exports the model before rebuilding the main site.
The print edition is unchanged by these web-only annotations.

The embodied transition from listening to lower and higher quadrobics, and from
shared practice to the Empire, is a philosophical account in the treatise.
`Empire` represents obligations of a union, not a derivation of its social
emergence from posture. Annotations for §§20, 25, and 30 mark these practical
claims as not covered rather than presenting them as model theorems. The Source
and Hridaya are not made consequences of bodily geometry.

The bodily inhibition described in the revised §29 is a doctrinal account of
mature ahimsa: protection of one's own living response extends to another's
life. It is not a derived physiological law or a physical force encoded in Agda.
The annotation is explicitly not covered. Necessary defense, errors despite
attention, and the recurrence of pramada remain distinct; `Protection` does not
prove a biological inability to injure another being.
