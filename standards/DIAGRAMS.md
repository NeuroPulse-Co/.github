# Diagrams

Every study page opens with a diagram of what we did. A reader should understand the method from the picture before reading a word of text. This page explains how a diagram is stored, how a person makes one, and how an AI agent makes one.

## The format: one file, `<name>.excalidraw.svg`

We draw diagrams with [Excalidraw](https://excalidraw.com). A diagram is saved as **one file**, `studies/<id>/diagrams/<name>.excalidraw.svg`. It is an ordinary SVG image with the Excalidraw drawing embedded inside it, so the same file is:
- **the picture** the website shows (the hand-drawn font is built into the file)
- **the editable source**: open it in Excalidraw and every box and arrow can still be moved.

There is no separate source file and no export step that can fall out of date. `record.py check` refuses a diagram that has lost its embedded drawing, because then nobody could edit it.

List it in the study's `study.yaml` like any other evidence ([RECORDS.md](RECORDS.md), Evidence):

```yaml
evidence:
  - type: diagram
    source: diagrams/method.excalidraw.svg
    title: How we tested each step against the paper
    caption: >-
      Each box is one step of ASF-S, and each step has a check against the paper. Steps 0 to 7
      match; the amber step is where our numbers part ways with the paper's.
```

## What makes a good diagram

1. **It answers one question**, the caption's question, such as "How does ASF-S choose which filters to keep?". If you cannot say the question in one sentence, the diagram is doing two jobs; draw two.
2. **It shows our real method**: the steps, data and decisions in our code and LOG, with their real names and numbers. It is never a generic "input → model → output" picture.
3. **It is small.** At most 12 boxes. One entry point, reading left to right or top to bottom.
4. **It uses words.** Labels are full words. Abbreviations appear only if they are in the website glossary, and the caption spells them out.
5. **It highlights one thing.** The step the caption is about gets the accent colour. Everything else stays neutral.

### House style

| Element | Setting |
|---|---|
| Lines and text | `#1e1e1e`, stroke width 2, roughness 1 ("artist"), hand-drawn font (Excalifont) |
| Neutral fill | `#f6f7f9` |
| Accent, the thing the caption is about | stroke `#1d4ed8`, fill `#dbe5fd` |
| Warning, where something went wrong (a failed check, a bug) | stroke `#b45309`, fill `#fef3c7` |
| Background | white. The website shows the diagram on a white card in both light and dark mode. |
| Text size | 20 for box labels, 16 for small notes |

At most three colours in one diagram: the neutral one plus one accent and, if needed, the warning colour.

## How a person makes one

1. Open [excalidraw.com](https://excalidraw.com), or install the **Excalidraw** extension in VS Code (`pomdtr.excalidraw-editor`). The extension opens `.excalidraw.svg` files directly.
2. Draw. Follow the house style above.
3. Save:
   - **In VS Code**, create the file as `studies/<id>/diagrams/<name>.excalidraw.svg` and save it. The scene is embedded automatically.
   - **On excalidraw.com**, use **Export image → SVG** with **Embed scene** switched on, and name the file `<name>.excalidraw.svg`.
4. To edit it later, open the same file in the extension, or drag it onto excalidraw.com.
5. Add it to `evidence:` in `study.yaml`, then run `record.py check` and `record.py promote`.

## How an AI agent makes one

An AI agent cannot drag shapes around, so it writes the Excalidraw scene as JSON and uses `tools/export-diagrams.mjs` to turn the JSON into the diagram. The export runs Excalidraw's own exporter in headless Chrome, so the result is exactly what excalidraw.com would save.

**Rules for the agent:**
1. **Read first.** Read the study's `study.yaml`, `FINDINGS.md`, `LOG.md` and the code it names. Write the caption's question down before drawing. Every box must correspond to something real in those files.
2. **Write the scene** to a scratch file, `<name>.excalidraw` (not committed), using the skeleton below. Keep the house style.
   - Every label sits inside its box: the text element has `containerId` set to the box, and the box lists the text in `boundElements`.
   - Every arrow is bound at both ends (`startBinding`, `endBinding`), and both boxes list the arrow in `boundElements`, so the drawing stays editable.
   - Use readable, stable ids (`step-train`, `label-step-train`, `arrow-train-afc`), so later edits give small diffs.
   - Lay out on a grid. For example, boxes 200 × 80 with 80 px gaps between them. Leave room for the arrows.
3. **Export:** `node tools/export-diagrams.mjs <name>.excalidraw studies/<id>/diagrams/<name>.excalidraw.svg`
4. **Look at the result:** `node tools/export-diagrams.mjs --png studies/<id>/diagrams/<name>.excalidraw.svg /tmp/<name>.png`, then open the PNG as an image. Check for:
   - text that overflows or is cut off
   - overlapping boxes
   - arrows that point at nothing or cross labels
   - anything that does not match the caption.

   Fix the JSON, export again, and repeat until it is clean.
5. **To change an existing diagram**, get its JSON back with `node tools/export-diagrams.mjs --extract <file>.excalidraw.svg <name>.excalidraw`, edit it, and export again.
6. **Hand it over; do not commit it.** A diagram is a claim about how our method works, so the study owner opens it in Excalidraw, corrects it and approves it. Say so in your reply.

**Skeleton** (one box with a label, and an arrow to a second box; copy the pattern):

```json
{
  "type": "excalidraw", "version": 2, "source": "neuropulse",
  "appState": { "viewBackgroundColor": "#ffffff" },
  "files": {},
  "elements": [
    { "id": "step-train", "type": "rectangle", "x": 0, "y": 0, "width": 200, "height": 80,
      "strokeColor": "#1e1e1e", "backgroundColor": "#f6f7f9", "fillStyle": "solid",
      "strokeWidth": 2, "roughness": 1, "roundness": { "type": 3 }, "seed": 1,
      "boundElements": [ { "id": "label-step-train", "type": "text" },
                         { "id": "arrow-train-afc", "type": "arrow" } ] },
    { "id": "label-step-train", "type": "text", "x": 10, "y": 27, "width": 180, "height": 25,
      "text": "Train the network", "originalText": "Train the network",
      "fontSize": 20, "fontFamily": 5, "textAlign": "center", "verticalAlign": "middle",
      "lineHeight": 1.25, "strokeColor": "#1e1e1e", "containerId": "step-train", "seed": 2 },
    { "id": "arrow-train-afc", "type": "arrow", "x": 205, "y": 40, "width": 70, "height": 0,
      "points": [[0, 0], [70, 0]], "strokeColor": "#1e1e1e", "strokeWidth": 2, "roughness": 1,
      "startBinding": { "elementId": "step-train", "focus": 0, "gap": 5 },
      "endBinding": { "elementId": "step-afc", "focus": 0, "gap": 5 },
      "endArrowhead": "arrow", "seed": 3 },
    { "id": "step-afc", "type": "rectangle", "x": 280, "y": 0, "width": 200, "height": 80,
      "strokeColor": "#1d4ed8", "backgroundColor": "#dbe5fd", "fillStyle": "solid",
      "strokeWidth": 2, "roughness": 1, "roundness": { "type": 3 }, "seed": 4,
      "boundElements": [ { "id": "label-step-afc", "type": "text" },
                         { "id": "arrow-train-afc", "type": "arrow" } ] },
    { "id": "label-step-afc", "type": "text", "x": 290, "y": 15, "width": 180, "height": 50,
      "text": "Measure functional\nconnectivity", "originalText": "Measure functional connectivity",
      "fontSize": 20, "fontFamily": 5, "textAlign": "center", "verticalAlign": "middle",
      "lineHeight": 1.25, "strokeColor": "#1e1e1e", "containerId": "step-afc", "seed": 5 }
  ]
}
```

Excalidraw fills in every field the skeleton leaves out. Break long labels with `\n` in `text` and keep the unbroken version in `originalText`. A text element's `height` is 25 per line at size 20.

## Running the export tool

`tools/export-diagrams.mjs` is vendored into every research repo next to `record.py`. It needs:
- Node 20 or newer
- Chrome or Chromium (`npx playwright install chromium` if you have neither)
- internet access the first time, because it installs `playwright-core` into `~/.cache/np-diagrams` and loads Excalidraw from esm.sh.

| Command | What it does |
|---|---|
| `node tools/export-diagrams.mjs scene.excalidraw [out.excalidraw.svg]` | JSON scene → diagram |
| `node tools/export-diagrams.mjs --png diagram.excalidraw.svg [out.png]` | diagram → PNG preview, to check it by eye |
| `node tools/export-diagrams.mjs --extract diagram.excalidraw.svg [out.excalidraw]` | diagram → JSON, to edit it as text |
