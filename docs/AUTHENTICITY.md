# How a document is shown to be forged, or genuine (draft method note, 2026-10-02)

Status: a proposal for the Strata framework. Cases below were checked against search-level sources; none was read at the primary level, so treat each as an illustration of method, not as a claim.

## 1. The question has three different parts
| Question | Example |
|---|---|
| Is the document **what it says it is**? (authentic or forged) | The Hitler Diaries were not Hitler's. |
| Is it **what it claims to be about**, unaltered? (whole, or interpolated) | A genuine letter with a passage added later. |
| Is what it **says true**? | A genuine NSA report that was mistranslated: real, but misleading. |

A genuine document can be wrong, and a forged one can describe something true. Strata keeps authenticity apart from the truth of the content. In the Tonkin dig, Report 13 is a genuine NSA report; the problem was what it was taken to mean.

## 2. Five kinds of test, from hardest to softest
1. **Material tests (the object itself).** Age and composition of paper, ink, thread, pigment, binding, printing. These give the sharpest results because a forger cannot easily avoid them.
2. **Anachronism (something that could not yet exist).** A word, a name, a fact, a material or a technique that appeared after the document's claimed date.
3. **Provenance (where it has been).** An unbroken chain of owners and records. A gap does not prove forgery, but a document that appears from nowhere, with a convenient story, is weak.
4. **Internal consistency.** Dates, places, people and handwriting or style that agree with each other and with the author's known habits (stylometry is a statistical version).
5. **External corroboration.** Independent records of the same events: other documents, logs, physical traces, witnesses, data from another system.

## 3. The asymmetry
- **One decisive anachronism can prove a forgery.** If a material did not exist until 1954, a document claiming 1943 cannot be genuine unless the anachronism itself has an innocent explanation (later repair, a later copy).
- **No test can prove genuineness absolutely.** A document passes every test that was run. "Authentic" means: survived tests that could have failed, with a sound provenance. It is a weight, not a certainty.
- **So forgery claims need convergence or a decisive test; genuineness claims need a test that could have failed.**

## 4. How well-known forgeries were actually exposed
| Case | What exposed it |
|---|---|
| **Hitler Diaries (1983)** | The German Federal Archives tested the objects, not the handwriting: the ink was less than about a year old, the paper contained a whitening additive not used until 1954, and the thread in the seals was post-war. The forger later confessed, but the tests came first. [Britannica](https://www.britannica.com/topic/Hitler-Diaries); [ABC News](https://www.abc.net.au/news/2023-05-26/fake-hitler-diaries-published-by-stern-in-1983-media-scandal/102367442) |
| **Vinland Map** | Yale (2021) used X-ray fluorescence and Raman microscopy and found much of the ink was titanium-based (anatase), a pigment not made until the 1920s; medieval iron-gall ink has no significant titanium. [NPR](https://www.npr.org/2021/09/30/1042029881/the-vinland-map-thought-to-be-the-oldest-map-of-america-is-officially-a-fake) |
| **Donation of Constantine** | Lorenzo Valla (1440) showed by language that it could not be 4th-century Latin: terms such as "fief" and "satrap" did not exist then. No lab needed. [History of Information](https://www.historyofinformation.com/detail.php?id=1817) |
| **Piltdown Man (1953)** | Chemical tests (fluorine content), staining and examination of the teeth showed the jaw and skull did not belong together and the teeth had been filed. Already a Strata dig. |
| **The Protocols of the Elders of Zion** | In 1921 the Times showed large parts were copied from an 1864 satire by Maurice Joly: a source comparison, not a lab test. (Method known; not re-checked here.) |

## 5. Digital items (posts, screenshots, PDFs, metadata)
- A **screenshot is the weakest form**: it can be made in seconds. Treat it as an unchecked claim.
- Stronger: a capture by an independent archive made near the time, the platform's own record or API, the account holder's own data archive, or several independent captures that agree.
- A post that cannot be found in any capture or platform record, though others from the same account and period can, is evidence it was never posted. That is an absence anchor and is capped, but it can be strengthened by showing the capture method would have caught it.
- File metadata can be edited; fonts, software versions and compression traces can show anachronism (a "2009" file made with 2015 software).

## 6. Proposed Strata rules
1. Every source gets an `authenticity` entry: `status` (authenticated | disputed | forged | unchecked), `basis`, `tests`, `tested_by` and whether the tester is independent of the claimant, and a date.
2. **Authenticity is a separate axis** from the weight of any claim that cites the source.
3. A claim anchored on a source whose authenticity is `unchecked` cannot be `anchor_checked: primary`.
4. A **forgery finding** names either a decisive anachronism (with the date the thing first became possible) or at least two independent lines of evidence.
5. A **genuineness finding** names provenance and at least one test that could have failed.
6. **Copies and mirrors**: record the URL and a checksum, and where possible compare against the holder's own copy. (We do this in `sources/MANIFEST.yaml`.)
7. **Digital items** need an archive capture or a platform record; a screenshot alone stays `unchecked`.
8. **Interpolation and translation** are checked separately: whole-document authenticity does not cover a changed passage or a mistranslated one.

## 7. Where we already apply this, and the gaps
- Tonkin: the intercept reports and the Bundy memo are genuine NSA and White House documents as hosted by the National Security Archive; we have not byte-compared the study's mirror with NSA's own copy (recorded in the manifest). OCR is a transcription, not the document.
- McAfee and Surfside: the central item is an alleged post attributed to the late John McAfee, which fact-checkers say was never posted. That is exactly a digital-authenticity question and the next worked example.
- Casket Letters (B-001): the originals are lost, so authenticity can only be tested through copies, translations and style.
