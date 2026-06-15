You are creating a structured comic issue outline for the Drakar campaign.

This outline will later be used as the primary source for NotebookLM to generate a dark fantasy graphic novel PDF. Do not create the PDF. Do not write prose analysis. Do not summarize your reasoning. Output only the final markdown outline document.

## Inputs you must use

1. The session transcript.
    
2. The file `00_drakar_player_visual_guide`.
    

## Source hierarchy

The session transcript is the source for what happened in the session.

The visual guide is the canonical source for character appearance, short character locks, and final PDF visual style.

The generated outline you create must become the primary control document for the current issue.

The transcript is noisy. It may include jokes, rules discussion, wrong spellings, repeated phrases, table talk, and imperfect speech transcription. Use it to identify actual story events, character actions, combats, discoveries, decisions, consequences, travel, and ending hooks. Do not adapt the transcript literally.

Do not invent events, emotional beats, cute details, jokes, rewards, character reactions, or visual moments that are not supported by the transcript or the visual guide. If a detail is uncertain and not needed for the story, omit it.

## Story selection rule

First, silently identify the major story-driving events of the session.

Prioritize:  
major combats,  
major discoveries,  
major decisions,  
new locations,  
character-defining actions,  
important consequences,  
creative problem solving,  
unusual encounter resolutions,  
session ending or cliffhanger.

Deprioritize:  
loot accounting,  
rules discussion,  
repeated tactical clarification,  
minor movement around the map,  
inventory management,  
small discoveries that do not change the story,  
table jokes unless they became important to the session story.

Create an 8-page comic issue outline. Each page should have 3 to 4 panels. Do not exceed 8 pages. If the session has too many events, compress minor events into narration or omit them. Major story events should receive more panel space than minor events.

Loot should receive its own panel only when it becomes story-relevant, creates a transition, changes a character’s equipment, reveals danger, or matters later in the session. Otherwise, summarize loot in narration.

## Creative solution rule

Preserve unusual or memorable encounter solutions from the session.

Do not reduce creative spellwork, traps, deception, environmental tactics, forced movement, negotiation, stealth, rescue plans, or clever player decisions into generic combat.

If the party solves a problem through sleep, levitation, illusion, web, grease, rope, cliffs, terrain, deception, or another specific tactic, show that tactic clearly in the outline.

## Visual panel rule

Each panel visual must show one main action, one main event, or one main subject. Do not put multiple sequential actions into the same visual description.

If several things happen between panels, summarize them in the Spanish narration instead of trying to show everything visually.

Keep panels readable. Prefer 1 to 3 required named player characters per panel. Large group shots are allowed only when story clarity matters more than individual character detail. For group travel, arrival, settlement, farewell, or cliffhanger panels, choose 2 or 3 focal required characters and put the rest of the party as optional visible characters.

Avoid overloaded panels. A single panel should not combine several major spell effects, multiple enemy groups, fleeing civilians, and several named heroes unless the panel is intentionally a chaotic climax. When in doubt, split the moment across panels or simplify the visual and move supporting information into narration.

## Language rule

Write all structural labels and visual instructions in English.

Write every `Narration:` field in Spanish.

Do not include dialogue fields.

## Narration source rule

Treat the DM as the main narrator of the session. For each page and panel, base the Spanish `Narration:` on the DM’s descriptions, scene framing, outcomes, and consequences whenever possible.

Do not invent decorative narration when the transcript already gives a clear story meaning. Clean up noisy transcript wording, but keep the narration close to what the DM established.

Use player statements only when they describe a clear character action or decision. Do not use table jokes, rules explanations, or tactical chatter as narration unless they became an important story beat.

## Narration style rule

Use grounded Spanish comic captions. Keep them concise, serious, and clear.

Avoid exaggerated metaphors, heroic epithets, table slang, jokes, cute phrasing, or poetic language that is not supported by the transcript.

Do not repeat obvious visual traits, colors, weapons, clothing, or visible actions unless they matter to the story.

Avoid game-mechanical phrasing in narration, such as `ronda`, `tirada`, `fallo`, `daño`, `bonificador`, `ventaja`, `desventaja`, `acción`, or similar tabletop mechanics, unless the comic is intentionally showing game mechanics.

The narration should add context, consequence, transition, stakes, or off-panel information.

Before final output, silently check each `Narration:` field by asking: does this add meaning that is not already visible in the panel? If not, rewrite it.

## Character accuracy rule

Use canonical character names from the visual guide, even if the transcript has spelling variations.

For every named player character in a panel, use the visual guide.

The full visual description is the canonical source.

The Short Character Lock is a compact identity anchor, not a replacement for the full description.

When a named character is the focal point of a panel, use richer visual details from the full description.

When multiple named characters appear in one panel, use each character’s Short Character Lock to keep them visually distinct.

Do not replace a named player character with a generic fantasy character or another character from the guide.

Do not invent a named player character’s gender, ancestry, hair, clothing, weapons, magic style, or visual anchors.

## Page character lock rule

For each page, the `Active character locks for this page` section must include every named player character who appears anywhere on that page, including required visible characters and optional visible characters.

Do not list a character as optional in a panel unless that character also appears in the page’s active character locks.

## Temporary visual override rule

If a character uses a temporary spell, weapon form, disguise, injury, condition, or visual effect that differs from their normal visual guide description, describe it clearly as a temporary panel-specific override.

Example:  
For this panel only, Therion’s usual blue-white magical blade is replaced by a smoky dark shadow blade.

Temporary overrides must not permanently replace the character’s normal visual identity in the roster or later panels.

## Noisy transcript cleanup rule

Normalize noisy transcript terms when the intended RPG creature, place, spell, item, or character is clear from context.

Use the visual guide for player character names.

Use the transcript context for monsters, locations, and events.

If the transcript has a corrupted creature or faction name but the intended name is clear, use the corrected fantasy/RPG name. For example, if the transcript clearly points to Thri-kreen hunters, write `Thri-kreen hunters`, not a phonetic or corrupted transcript word.

If you are not sure what the correct name is, use a neutral descriptive label instead of inventing a specific one. Example: `insectoid hunters`, `snow refugees`, `stone guardian`, `mountain beast`.

## Major subjects and enemies rule

For every major recurring non-player subject, monster, creature group, location, or object that appears across multiple panels, create a short visual lock in the section `## Major subjects and enemies visual locks`.

This includes enemies, monsters, important NPC groups, important locations, or story objects that need stable visual continuity.

Each visual lock should be short and concrete. It should describe the subject visually enough for NotebookLM to draw it consistently.

Examples:  
Earth elemental: giant humanoid mass of cracked boulders and red-brown stone slabs, oversized stone-hammer arms, heavy chest, thick legs, small sunken head with glowing cracks for eyes, no sculpted human face.

Frost troll: huge ugly ice troll with pale blue-gray skin, long arms, hunched body, frost mist around its shoulders, sharp claws, and ragged cold-weather scraps.

Thri-kreen hunters: insectoid hunters with mantis-like heads, chitin bodies, long limbs, multiple arms, spears or hunting weapons, and predatory group movement.

Only include locks for subjects that matter to the current issue.

## Output format

Use this exact markdown structure.

---

Parent:

- "[[DND Main]]"
    

---

Important: do not illustrate or include page titles in the final comic. Do not draw or print labels such as "Visual:", "Narration:", "Required visible characters:", "Required visible subjects/enemies:", "Optional visible characters/subjects:", "Panel importance:", "Short character lock:", "Production note:", page purposes, active character rosters, subject locks, or any guide notes. Only the content after `Narration:` should appear as comic narration text.

Title: Drakar  
Issue #[ISSUE_NUMBER]

## Active character roster for this issue

List only the player characters who appear in this session.

For each one, include their Short Character Lock copied or lightly adapted from the visual guide.

Example format:  
Choppa: huge hairless green male orc barbarian with massive muscles, lower tusks, tall bronze winged elven helmet, one-handed war pick, round wooden shield with tree motif, and rough leather-fur gear.

## Major subjects and enemies visual locks

List only the major enemies, creature groups, important locations, or important objects that need visual consistency in this issue.

Example format:  
Earth elemental: giant humanoid mass of cracked boulders and red-brown stone slabs, oversized stone-hammer arms, heavy chest, thick legs, small sunken head with glowing cracks for eyes, no sculpted human face.

## Issue structure

### Page 1

Page purpose: one short sentence explaining what this page accomplishes in the story.

Active character locks for this page:  
List every named player character who appears anywhere on this page, including required and optional visible characters. Use their Short Character Locks from the visual guide.

Major subject locks for this page:  
List only the subject or enemy locks used on this page.

Panel 1

Required visible characters: [character names, or none]  
Required visible subjects/enemies: [subjects, enemies, places, objects, or none]  
Optional visible characters/subjects: [optional elements, or none]  
Panel importance: normal, large focal panel, or transition panel

Visual: Write a clear English visual instruction for one static comic panel. Include character locks or full visual details as needed. Use one main action, one main event, or one main subject only. If a character has a temporary visual override for this panel, state it clearly.

Narration: Write one concise Spanish narration caption for this panel. Base it on the DM’s framing, scene description, outcome, or consequence whenever possible. Do not repeat obvious visible traits.

Panel 2

Required visible characters: [character names, or none]  
Required visible subjects/enemies: [subjects, enemies, places, objects, or none]  
Optional visible characters/subjects: [optional elements, or none]  
Panel importance: normal, large focal panel, or transition panel

Visual: Write a clear English visual instruction for one static comic panel. Include character locks or full visual details as needed. Use one main action, one main event, or one main subject only. If a character has a temporary visual override for this panel, state it clearly.

Narration: Write one concise Spanish narration caption for this panel. Base it on the DM’s framing, scene description, outcome, or consequence whenever possible. Do not repeat obvious visible traits.

Continue the same format for all panels on the page.

### Page 2

Repeat the same structure.

Continue until exactly 8 pages are complete.

## Quality checks before final output

Silently verify all of these before answering:

The output is only the final markdown outline document.

The production note appears immediately after the frontmatter and before the title.

The issue has exactly 8 pages.

Each page has 3 to 4 panels.

Every panel has one clear visual action, event, or subject.

Every `Narration:` field is in Spanish.

Every `Narration:` field is grounded in the DM’s narration, session consequence, or clear story context.

No `Dialogue:` fields are included.

Named player characters use the visual guide accurately.

Every named player character who appears as required or optional on a page is included in that page’s active character locks.

Major monsters, enemy groups, and important subjects have stable visual locks when needed.

Noisy transcript terms are normalized when the intended term is clear.

Large group panels do not require more than 3 named player characters unless absolutely necessary.

Important story beats get more space than minor details.

Minor events are summarized in narration when needed.

Loot is only given its own panel if it matters to the story, creates a transition, or affects the session.

Creative encounter resolutions are preserved and not reduced into generic combat.

Overloaded panels are split, simplified, or supported by narration.

The ending gives the issue a clean closing beat, transition, or cliffhanger.