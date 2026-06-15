You are creating a structured comic issue outline for the Pathfinder 2e campaign Age of Ashes.

This outline will later be used as the primary source for NotebookLM to generate a dark fantasy graphic novel PDF. Do not create the PDF. Do not write prose analysis. Do not summarize your reasoning. Output only the final markdown outline document.

### Prompt to use with this file
Use the outline generator prompt, the PF2 visual guide, and the session transcript to generate the structured comic issue outline for Pathfinder: Age of Ashes, Issue #[number]. Output only the final markdown outline document.

## Inputs you must use

1. The session transcript.

2. The file `00_PF2 - Player visual guide.md`.

## Source hierarchy

The session transcript is the source for what happened in the session.

The visual guide is the canonical source for player character appearance, companion appearance, short character locks, and final PDF visual style.

The generated outline you create must become the primary control document for the current issue.

The transcript is noisy. It may include jokes, rules discussion, wrong spellings, repeated phrases, table talk, Foundry setup, player troubleshooting, and imperfect speech transcription. Use it to identify actual story events, character actions, combats, discoveries, decisions, consequences, travel, social scenes, investigations, and ending hooks. Do not adapt the transcript literally.

Do not invent events, emotional beats, cute details, jokes, rewards, character reactions, visual moments, NPCs, monsters, or locations that are not supported by the transcript or the visual guide. If a detail is uncertain and not needed for the story, omit it.

## Story selection rule

First, silently identify the major story-driving events of the session.

Prioritize:
major combats,
major discoveries,
major decisions,
new locations,
important NPC encounters,
important faction or town information,
character-defining actions,
important consequences,
creative problem solving,
unusual encounter resolutions,
session ending or cliffhanger.

Deprioritize:
loot accounting,
rules discussion,
Foundry setup,
token setup,
character sheet troubleshooting,
action-counting clarification,
repeated tactical clarification,
minor movement around the map,
inventory management,
small discoveries that do not change the story,
table jokes unless they became important to the session story.

Create an 8-page comic issue outline. Each page should have 3 to 4 panels. Do not exceed 8 pages. If the session has too many events, compress minor events into narration or omit them. Major story events should receive more panel space than minor events.

Loot should receive its own panel only when it becomes story-relevant, creates a transition, changes a character’s equipment, reveals danger, or matters later in the session. Otherwise, summarize loot in narration.

## Pathfinder 2e mechanics filter

Ignore Pathfinder 2e rules explanation unless the result creates a visible story consequence.

Do not write narration about `acciones`, `tiradas`, `fallos`, `críticos`, `Recall Knowledge`, `Hero Points`, `panache`, `reload`, `targeting`, `Foundry`, `initiative`, `conditions`, `bonuses`, `penalties`, `MAP`, `prone`, `off-guard`, `dying`, `persistent damage`, or similar mechanics unless the comic is intentionally showing game mechanics.

Translate mechanics into story action only when useful.

Examples:
Do not narrate: “Jago usó una acción para hacer Trip.”
Use instead: “Jago enganchó al enemigo con su arma y lo derribó.”

Do not narrate: “Cassian hizo Recall Knowledge.”
Use instead: “Cassian reconoció la naturaleza de las criaturas entre las llamas.”

Do not narrate: “Sari ganó panache.”
Use instead: “Sari aprovechó el descuido del enemigo y se movió con precisión.”

## Session premise and exposition rule

Because some sessions may include long town, lore, or NPC exposition, include only the exposition needed to understand the issue’s main mission, danger, or decision.

Use narration to compress background history. Do not spend many panels on static lore unless the lore changes the story direction.

For early campaign sessions, preserve the campaign premise and first mission clearly. Show the town, key NPCs, public request, first crisis, or first expedition only if they drive the issue.

## Creative solution rule

Preserve unusual or memorable encounter solutions from the session.

Do not reduce creative spellwork, traps, deception, environmental tactics, forced movement, negotiation, stealth, rescue plans, use of companions, alchemy, firearms, healing, or clever player decisions into generic combat.

If the party solves a problem through a specific tactic, show that tactic clearly in the outline.

## Visual panel rule

Each panel visual must show one main action, one main event, or one main subject. Do not put multiple sequential actions into the same visual description.

Required visible subjects/enemies must only include subjects physically visible in the panel. Do not list missing NPCs, mission targets, suspects, rumors, remembered groups, future threats, unseen enemies, or off-panel story information as required visible subjects. Put those in `Narration:` instead.

Examples:  
Do not list `Bumblebrashers` as a required visible subject if the panel only shows Warbal talking about them.  
Do not list `Calmont Hale` as a required visible subject if the panel only shows townspeople accusing him after he has fled.  
Do not list `unknown threat inside the citadel` as a required visible subject if the panel only shows the party outside the gate.

If several things happen between panels, summarize them in the Spanish narration instead of trying to show everything visually.

Keep panels readable. Prefer 1 to 3 required named player characters per panel. Large group shots are allowed only when story clarity matters more than individual character detail. For group travel, arrival, settlement, farewell, council scenes, tavern scenes, or cliffhanger panels, choose 2 or 3 focal required characters and put the rest of the party as optional visible characters.

Avoid overloaded panels. A single panel should not combine several major spell effects, multiple enemy groups, fleeing civilians, and several named heroes unless the panel is intentionally a chaotic climax. When in doubt, split the moment across panels or simplify the visual and move supporting information into narration.

## Language rule

Write all structural labels and visual instructions in English.

Write every `Narration:` field in Spanish.

Do not include dialogue fields.

## Narration source rule

Treat the GM as the main narrator of the session. For each page and panel, base the Spanish `Narration:` on the GM’s descriptions, scene framing, outcomes, and consequences whenever possible.

Do not invent decorative narration when the transcript already gives a clear story meaning. Clean up noisy transcript wording, but keep the narration close to what the GM established.

Use player statements only when they describe a clear character action or decision. Do not use table jokes, rules explanations, or tactical chatter as narration unless they became an important story beat.

## Narration style rule

Use grounded Spanish comic captions. Keep them concise, serious, and clear.

Avoid exaggerated metaphors, heroic epithets, table slang, jokes, cute phrasing, or poetic language that is not supported by the transcript.

Do not repeat obvious visual traits, colors, weapons, clothing, or visible actions unless they matter to the story.

Avoid game-mechanical phrasing in narration, such as `ronda`, `tirada`, `fallo`, `crítico`, `daño`, `bonificador`, `ventaja`, `desventaja`, `acción`, `iniciativa`, `condición`, or similar tabletop mechanics, unless the comic is intentionally showing game mechanics.

The narration should add context, consequence, transition, stakes, or off-panel information.

Before final output, silently check each `Narration:` field by asking: does this add meaning that is not already visible in the panel? If not, rewrite it.

## Character accuracy rule

Use canonical character names from the visual guide, even if the transcript has spelling variations.

For every named player character or companion in a panel, use the visual guide.

The full visual description is the canonical source.

The Short Character Lock is a compact identity anchor, not a replacement for the full description.

When a named player character or companion is the focal point of a panel, use richer visual details from the full description.

When multiple named characters appear in one panel, use each character’s Short Character Lock to keep them visually distinct.

Do not replace a named player character with a generic fantasy character or another character from the guide.

Do not invent a named player character’s gender, ancestry, hair, clothing, weapons, class identity, companion, magic style, or visual anchors.

Do not confuse similarly named characters. If the visual guide says two characters are distinct, preserve that distinction strictly.

## Companion accuracy rule

If a companion, familiar, animal companion, or pet appears in the transcript and visual guide, treat it as a named visual subject.

Do not replace companions with generic animals.

Only include companions in panels when they are story-relevant, visually useful, or explicitly present in the scene.

Examples:
Deimos is Redflack’s black male wolf animal companion.
Bigotes is Tippi Bellyspark’s plump squirrel familiar.

## Page character lock rule

For each page, the `Active character locks for this page` section must include every named player character or named companion who appears anywhere on that page, including required visible characters and optional visible characters.

Optional visible characters/subjects must be treated as real visible panel elements, not casual background suggestions. Do not list a character or named companion as optional unless that character appears in that panel and is also included in the page’s `Active character locks for this page`. When a character is not important to the panel, write `none` instead of listing them as optional.

## Temporary visual override rule

If a character uses a temporary spell, weapon form, disguise, injury, condition, alchemical effect, mutagen, shield position, drawn weapon, active aura, or visual effect that differs from their normal visual guide description, describe it clearly as a temporary panel-specific override.

Example:
For this panel only, Tippi’s skin glows green and forms hard scale-like patches from an alchemical mutagen.

Temporary overrides must not permanently replace the character’s normal visual identity in the roster or later panels.

## Noisy transcript cleanup rule

Normalize noisy transcript terms when the intended Pathfinder creature, place, spell, item, faction, NPC, or character is clear from context.

Use the visual guide for player character and companion names.

Use the transcript context for monsters, NPCs, locations, factions, and events.

If the transcript has a corrupted creature, faction, NPC, or place name but the intended name is clear, use the corrected Pathfinder name.

If you are not sure what the correct name is, use a neutral descriptive label instead of inventing a specific one. Example: `fire creatures`, `town councilors`, `goblin ambassador`, `roadside bandits`, `citadel ruins`.

## Major subjects, NPCs, factions, and enemies rule

For every major recurring non-player subject, NPC, faction, monster, creature group, location, or object that appears across multiple panels, create a short visual lock in the section `## Major subjects, NPCs, factions, and enemies visual locks`.

This includes enemies, monsters, important NPCs, important factions, important locations, important objects, or civilian groups that need stable visual continuity.

Each visual lock should be short and concrete. It should describe the subject visually enough for NotebookLM to draw it consistently.

Examples:
Town council chamber: large public meeting room with wooden benches, raised council table, town banners, anxious townspeople, and formal local officials at the front.

Goblin ambassador: small anxious goblin public representative in neat town clothing, visibly worried but formal, with a Desna butterfly symbol at the neck.

Fire mephits: small winged fire imps made of smoke, ember, and living flame, with sharp faces, clawed hands, and bodies glowing from within.

Roadside bandits: coordinated armed ambushers in rough leather armor, cloaks, masks or scarves, crossbows and blades, positioned along rocks and trees.

Only include locks for subjects that matter to the current issue.

## Output format

Use this exact markdown structure.

---
Parent:
  - "[[DND Main]]"
---

Important: do not illustrate or include page titles in the final comic. Do not draw or print labels such as "Visual:", "Narration:", "Required visible characters:", "Required visible subjects/enemies:", "Optional visible characters/subjects:", "Panel importance:", "Short character lock:", "Production note:", page purposes, active character rosters, subject locks, NPC locks, faction locks, or any guide notes. Only the content after `Narration:` should appear as comic narration text.

Mini title: Pathfinder
Title: Age of Ashes
Issue #[ISSUE_NUMBER]

## Active character roster for this issue

List only the player characters and named companions who appear in this session.

For each one, include their Short Character Lock copied or lightly adapted from the visual guide.

Example format:
Jago: gray-skinned hobgoblin warrior with severe elf-like features, pointed ears with small ring piercings, small lower-jaw canines, long black hair tied back in a loose rough topknot, red tribal war paint, heavy worn pale full plate armor, and a disciplined guarded expression.

## Major subjects, NPCs, factions, and enemies visual locks

List only the major NPCs, factions, enemies, creature groups, important locations, important civilian groups, or important objects that need visual consistency in this issue.

Example format:
Fire mephits: small winged fire imps made of smoke, ember, and living flame, with sharp faces, clawed hands, and bodies glowing from within.

## Issue structure

### Page 1

Page purpose: one short sentence explaining what this page accomplishes in the story.

Active character locks for this page:
List every named player character or named companion who appears anywhere on this page, including required and optional visible characters. Use their Short Character Locks from the visual guide.

Major subject locks for this page:
List every major subject, NPC, faction, enemy, place, companion, or object lock used on this page.

Panel 1

Required visible characters: [player character names, named companions, or none]
Required visible subjects/enemies: [subjects, enemies, NPCs, places, objects, factions, civilian groups, or none]
Optional visible characters/subjects: [optional elements, or none]
Panel importance: normal, large focal panel, or transition panel

Visual: Write a clear English visual instruction for one static comic panel. Include character locks, companion locks, NPC locks, enemy locks, or full visual details as needed. Use one main action, one main event, or one main subject only. If a character has a temporary visual override for this panel, state it clearly.

Narration: Write one concise Spanish narration caption for this panel. Base it on the GM’s framing, scene description, outcome, or consequence whenever possible. Do not repeat obvious visible traits.

Panel 2

Required visible characters: [player character names, named companions, or none]
Required visible subjects/enemies: [subjects, enemies, NPCs, places, objects, factions, civilian groups, or none]
Optional visible characters/subjects: [optional elements, or none]
Panel importance: normal, large focal panel, or transition panel

Visual: Write a clear English visual instruction for one static comic panel. Include character locks, companion locks, NPC locks, enemy locks, or full visual details as needed. Use one main action, one main event, or one main subject only. If a character has a temporary visual override for this panel, state it clearly.

Narration: Write one concise Spanish narration caption for this panel. Base it on the GM’s framing, scene description, outcome, or consequence whenever possible. Do not repeat obvious visible traits.

Continue the same format for all panels on the page.

### Page 2

Repeat the same structure.

Continue until exactly 8 pages are complete.

## Quality checks before final output

Silently verify all of these before answering:

The output is only the final markdown outline document.

The production note appears immediately after the frontmatter and before the mini title and title.

The issue has exactly 8 pages.

Each page has 3 to 4 panels.

Every panel has one clear visual action, event, or subject.

Every required visible subject/enemy is physically visible in that panel, not only mentioned, suspected, remembered, missing, or implied.

Every `Narration:` field is in Spanish.

Every `Narration:` field is grounded in the GM’s narration, session consequence, or clear story context.

No `Dialogue:` fields are included.

Named player characters and companions use the visual guide accurately.

Every named player character or companion who appears as required or optional on a page is included in that page’s active character locks.

Major NPCs, factions, monsters, enemy groups, locations, civilian groups, and important subjects have stable visual locks when needed.

Every required or optional subject/enemy/NPC/faction/location that has a global visual lock also appears in that page’s `Major subject locks for this page`.

Noisy transcript terms are normalized when the intended term is clear.

Large group panels do not require more than 3 named player characters unless absolutely necessary.

Important story beats get more space than minor details.

Minor events are summarized in narration when needed.

Loot is only given its own panel if it matters to the story, creates a transition, or affects the session.

Creative encounter resolutions are preserved and not reduced into generic combat.

Long exposition is compressed into narration unless it drives the main mission.

Pathfinder 2e mechanics and Foundry instructions are not included unless translated into visible story consequences.

Overloaded panels are split, simplified, or supported by narration.

The ending gives the issue a clean closing beat, transition, or cliffhanger.
