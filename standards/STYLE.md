# How we write

This guide covers everything that reaches readers outside the team: study pages
(`FINDINGS.md`), blog posts, READMEs and the website. Lab logs can be terser, but they still use
full sentences.

Our readers are our supervisors and examiners, other researchers, and people who are curious
about the project. Write so that a final-year engineering student from a different field could
follow along.

## Voice

- **We write as the researchers who did the work**: first person plural ("we trained", "we
  expected", "we were wrong about"). The tone is friendly and direct, not promotional.
- **Use full sentences, and no fragments.** "Accuracy drops 10 points" is a fragment in a list.
  "When we retrain only the final layer, accuracy drops by 10.5 points" is a finding.
- **Explain before you show.** Every table and figure is introduced by a sentence that says why
  it is there.
- **Keep claims to the size of the evidence.** "On Conv2Net with CIFAR-10, over three seeds" is
  better than "in general".

## Abbreviations and terms

- **Spell out every abbreviation the first time it appears on each page**, with the short form
  in brackets: "Principal Gradient Importance (PGI)". After that the short form is fine.
- Link the first use of a technical term to the website glossary when one exists.
- Prefer a plain word when it is just as precise: "kept filters" rather than "survivor set".

These terms come up most often:

| Short form | Full form |
|---|---|
| ASF-S | Artificial Structure Function Search, the pruning method we build on |
| AFC | Artificial Functional Connectivity |
| PGI | Principal Gradient Importance |
| PG1 | the first principal gradient of the AFC graph |
| TIL | Task-Incremental Learning |
| ACC, BWT, FWT | average accuracy, backward transfer, forward transfer |
| ECE | expected calibration error |
| FC | fully connected (layer), or functional connectivity; always say which |

## Structure of a result

Every study page and post answers these questions, in this order:

1. **The question.** What did we want to know, and why does it matter for the project?
2. **What we expected.** What was the hypothesis, and what result would have confirmed it?
3. **What we did.** Describe the setup in plain words, and link to the code and the runs.
4. **What happened.** Give the numbers, saying which split (validation or test) and how many
   seeds, with a spread (standard deviation or confidence interval) whenever we have more than
   one seed.
5. **Why we think it happened.** Give our explanation, how confident we are, and what would
   change our mind.
6. **What comes next.** State the decision this result leads to.

## Figures and tables

- **Every figure has a caption that says what to look at and what it means**, not just what it
  plots. For example: "Accuracy change against the share of parameters removed. The PGI curve
  sits below L1 at every budget, so the corrected PGI never beats magnitude here."
- Axes have names and units. Colours stay the same for the same method across figures.
- Tables give units in the header and say which split the numbers come from.
- **Diagrams of methods are our own**, drawn in Excalidraw or draw.io and exported as SVG. We do
  not copy figures from papers.

## Negative and partial results

- **State them plainly, with the same care as positive ones.** "Our reproduction does not reach
  the paper's number: −10.5 points against −3.78" is the right sentence. "Results were
  somewhat lower" is not.
- Separate what we know from what we suspect. A failed reproduction has several possible
  causes: our bug, an unstated detail in the paper, or an error in the paper. Say which ones we
  have ruled out.
- Being fair to the authors is part of being honest. Describe what their paper reports
  accurately, and note where its description was ambiguous rather than assuming the worst.

## Citing

- Cite papers by author and year, with a link: "(Mallya and Lazebnik, 2018)". Put the full
  reference at the end of the post.
- Explain other people's methods in our own words. Quote only a sentence or two, and only when
  the exact wording matters.
- Credit teammates and supervisors by name when their idea or work is being described.

## Before you set `draft: false`

- [ ] There is no `TODO` left, and every abbreviation is spelled out on first use.
- [ ] Every number has a split and a seed count. Every figure has a "what to look at" caption.
- [ ] The six questions above are answered.
- [ ] A teammate has read it. For results about the ASF-S paper, a supervisor has read it.
