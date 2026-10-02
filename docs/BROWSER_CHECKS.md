# Browser checks needed (sources blocked from the cloud session)

For a session or agent that has a real browser (Claude in Chrome or a person).
For each item: save the file or page into the folder named, then add its
sha256 and an `authenticity` block to that subject's `sources/MANIFEST.yaml`,
and add the Wayback Machine snapshot link (web.archive.org/save/<url>) as `capture`.
Record what was seen in the subject's `log.yaml` (append only).

## flydubai-fz1073  (folder: build/subjects/flydubai-fz1073/sources/)
1. Flightradar24 flight FZ1073 history, 2026 incident date: export CSV (KML also).
2. AirNav RadarBox flight log for the same flight: export CSV.
3. ADS-B Exchange history for ICAO hex 8965D1 on that date, if it loads.
4. Check: squawk 7700 time (AirNav 05:28:48 UTC vs Flightradar24 ~05:31) and 7500 time
   (AirNav ~05:35 vs ~05:38). Report which timestamps the raw files show.

## mcafee-and-surfside  (folder: build/subjects/mcafee-and-surfside/sources/)
5. Internet Archive capture of twitter.com/officialmcafee (src-wayback-profile): is there any
   post dated 8 June 2021 with the "Champlain Towers" wording? Screenshot + note.
6. Miami-Dade Property Appraiser: search Champlain Towers South, 8777 Collins Ave; check
   whether John McAfee or his wife appear as unit owners.
7. Spanish court ruling dated 24 Jul 2023 (suicide finding): find the original document or
   an official court/press release.
8. NIST technical report on the Surfside collapse: download the PDF.

## gulf-of-tonkin  (folder: build/subjects/gulf-of-tonkin/sources/)
9. Herrick flash message of 4 Aug 1964 (as quoted in the Hanyok study).
10. FRUS 1964-68 vol. I, documents dated 4-7 Aug 1964 (history.state.gov).
11. Congressional Record, Senate debate on the Tonkin Gulf Resolution, 6-7 Aug 1964.
12. SNIE 50-2-64.

## General
- Do not save copyrighted full text; keep the sha256, short quotes and the snapshot link.
- Never overwrite an existing source file; add new ones.
