#!/usr/bin/env python3
"""Tests for publication status (rules PS1-PS4 in build/conformance.py, rendering in build/tools/pubstatus.py).

    python3 build/tools/test_publication_status.py

Uses synthetic subjects in a temporary folder; touches no real dig. Includes the neutrality test:
the same retraction injected into subjects that point opposite ways gives the same result."""
import os, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import yaml
import conformance as cf
import pubstatus as ps

RETRACTED = {"status": "retracted", "date": "2010-02-02", "notice": "https://example.org/retraction", "reason": "Data could not be verified."}


def make(files, sources, base=None):
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "sources"))
    with open(os.path.join(d, "sources", "MANIFEST.yaml"), "w") as f:
        yaml.safe_dump({"sources": sources}, f)
    for name, doc in files.items():
        with open(os.path.join(d, name), "w") as f:
            yaml.safe_dump(doc, f)
    return d


def run(d, nodes_dir=None):
    r = cf.Report()
    claims_doc = cf.load(os.path.join(d, "claims.yaml")) if os.path.exists(os.path.join(d, "claims.yaml")) else {}
    cf.check_publication(r, "s", d, claims_doc.get("claims") or [], claims_doc, nodes_dir=nodes_dir or tempfile.mkdtemp())
    return r


def src(pub=None, sid="src-a"):
    s = {"id": sid, "title": "A paper"}
    if pub is not None:
        s["publication"] = pub
    return s


def claim(cid="c1", state="established", flagged=None, sid="src-a"):
    c = {"id": cid, "state": state, "anchor": {"type": "x", "description": "d", "sources": [sid]}}
    if flagged:
        c["flagged_sources"] = flagged
    return c


NOTICE = [{"source": "src-a", "notice": "This paper was retracted."}]


class Rules(unittest.TestCase):
    def test_clean_when_flagged_and_noticed(self):
        d = make({"claims.yaml": {"source_notices": NOTICE, "claims": [claim(flagged=["src-a"])]}}, [src(RETRACTED)])
        r = run(d)
        self.assertEqual((r.errors, r.warnings), ([], []))

    def test_ps1_bad_status(self):
        r = run(make({"claims.yaml": {"claims": []}}, [src({"status": "bogus"})]))
        self.assertTrue(any("PS1" in e for e in r.errors))

    def test_ps2_needs_date_and_notice(self):
        for st in ("retracted", "withdrawn", "expression_of_concern"):
            r = run(make({"claims.yaml": {"claims": []}}, [src({"status": st})]))
            self.assertTrue(any("PS2" in e for e in r.errors), st)

    def test_ps3_claim_and_ps4(self):
        r = run(make({"claims.yaml": {"claims": [claim()]}}, [src(RETRACTED)]))
        self.assertEqual(sum("PS3" in e for e in r.errors), 1)
        self.assertEqual(sum("PS4" in e for e in r.errors), 1)

    def test_ps3_other_files(self):
        files = {"claims.yaml": {"source_notices": NOTICE, "claims": []},
                 "timeline.yaml": {"events": [{"id": "e1", "sources": ["src-a"]}]},
                 "tests.yaml": {"discriminating_tests": [{"id": "t1", "result": {"sources": ["src-a"]}}]},
                 "transmission.yaml": {"chains": [{"id": "x1", "events": [{"id": "ev", "source": "src-a"}]}]},
                 "actors.yaml": {"actors": [{"id": "p", "statements": [{"id": "st", "source": "src-a"}]}]}}
        r = run(make(files, [src(RETRACTED)]))
        self.assertEqual(sorted(e.split(":")[1] for e in r.errors), ["actors.yaml", "tests.yaml", "timeline.yaml", "transmission.yaml"])

    def test_ack_on_item_clears_other_file_hit(self):
        files = {"claims.yaml": {"source_notices": NOTICE, "claims": []},
                 "timeline.yaml": {"events": [{"id": "e1", "sources": ["src-a"], "flagged_sources": ["src-a"]}]}}
        r = run(make(files, [src(RETRACTED)]))
        self.assertEqual(r.errors, [])

    def test_file_level_ack_does_not_count(self):
        files = {"claims.yaml": {"source_notices": NOTICE, "claims": []},
                 "timeline.yaml": {"flagged_sources": ["src-a"], "events": [{"id": "e1", "sources": ["src-a"]}]}}
        r = run(make(files, [src(RETRACTED)]))
        self.assertEqual(len(r.errors), 1)

    def test_log_and_review_are_not_citations(self):
        files = {"claims.yaml": {"source_notices": NOTICE, "claims": []},
                 "log.yaml": {"entries": [{"id": "l1", "sources": ["src-a"]}]},
                 "review.yaml": {"checked": ["src-a"]}}
        self.assertEqual(run(make(files, [src(RETRACTED)])).errors, [])

    def test_expression_of_concern_is_warning_only(self):
        eoc = {"status": "expression_of_concern", "date": "2020-01-01", "notice": "n"}
        r = run(make({"claims.yaml": {"claims": [claim()]}}, [src(eoc)]))
        self.assertEqual(r.errors, [])
        self.assertEqual(len(r.warnings), 1)

    def test_corrected_unpublished_published_and_unrecorded_are_silent(self):
        for pub in ({"status": "corrected"}, {"status": "unpublished"}, {"status": "published"}, None):
            r = run(make({"claims.yaml": {"claims": [claim()]}}, [src(pub)]))
            self.assertEqual((r.errors, r.warnings), ([], []), pub)

    def test_unresolved_ids(self):
        files = {"claims.yaml": {"source_notices": [{"source": "src-zz", "notice": "n"}] + NOTICE,
                                 "claims": [claim(flagged=["src-a", "src-yy"])]}}
        r = run(make(files, [src(RETRACTED)]))
        self.assertEqual(sum("src-zz" in e for e in r.errors), 1)
        self.assertEqual(sum("src-yy" in e for e in r.errors), 1)

    def test_neutrality_state_and_direction_do_not_matter(self):
        out = []
        for state in ("established", "contested", "refuted", "proposed", "searched_gap"):
            for text in ("The lamp was invented by X.", "The lamp was not invented by X."):
                c = claim(state=state)
                c["statement"] = text
                r = run(make({"claims.yaml": {"claims": [c]}}, [src(RETRACTED)]))
                out.append(sorted(e.split(": ", 1)[1] for e in r.errors))
        self.assertTrue(all(o == out[0] for o in out))
        self.assertEqual(len(out[0]), 2)

    def test_node_reach(self):
        nd = tempfile.mkdtemp()
        for nid, subj in (("n1", "s"), ("n2", "other")):
            with open(os.path.join(nd, nid + ".yaml"), "w") as f:
                yaml.safe_dump({"id": nid, "manifest": {"subject": subj, "source": "src-a"}}, f)
        def only_node(nid, flagged=None):
            c = {"id": "c1", "state": "established", "anchor": {"type": "x", "description": "d", "nodes": [{"node": nid, "verb": "supports"}]}}
            if flagged:
                c["flagged_sources"] = flagged
            return c
        base = lambda c: make({"claims.yaml": {"source_notices": NOTICE, "claims": [c]}}, [src(RETRACTED)])
        r = run(base(only_node("n1")), nd)
        self.assertEqual(sum("PS3" in e for e in r.errors), 1)
        self.assertEqual(run(base(only_node("n1", ["src-a"])), nd).errors, [])
        self.assertEqual(run(base(only_node("n2")), nd).errors, [])   # node points into another subject
        self.assertEqual(run(base({"id": "c1", "state": "established", "anchor": {"type": "x", "description": "d", "nodes": ["n1"]}}), nd).errors.__len__(), 1)  # bare node id form

    def test_ack_inside_anchor_does_not_count(self):
        c = claim()
        c["anchor"]["flagged_sources"] = ["src-a"]
        r = run(make({"claims.yaml": {"source_notices": NOTICE, "claims": [c]}}, [src(RETRACTED)]))
        self.assertTrue(any("on the claim itself" in e for e in r.errors))
        self.assertTrue(any("cites `src-a`" in e for e in r.errors))

    def test_malformed_values_give_errors_not_a_crash(self):
        r = run(make({"claims.yaml": {"claims": []}}, [src({"status": ["retracted"]})]))
        self.assertTrue(any("PS1" in e for e in r.errors))
        r = run(make({"claims.yaml": {"source_notices": [{"source": ["src-a"], "notice": "n"}, "junk"], "claims": []}}, [src(RETRACTED)]))
        self.assertTrue(any("PS4" in e and "no `source` id" in e for e in r.errors))
        r = run(make({"claims.yaml": {"claims": [claim()]}}, [{"id": ["x"], "title": "t"}, src(RETRACTED)]))
        self.assertTrue(any("PS3" in e for e in r.errors))


class Rendering(unittest.TestCase):
    man = {"src-a": {"id": "src-a", "title": "A <paper>", "publication": RETRACTED},
           "src-b": {"id": "src-b", "title": "B", "publication": {"status": "corrected", "date": "2015-01-01"}},
           "src-c": {"id": "src-c", "title": "C"}}

    def test_claim_notice(self):
        h = ps.claim_notice_html({"flagged_sources": ["src-a", "src-b"]}, self.man)
        self.assertEqual(h.count('class="pubnote"'), 2)
        self.assertIn("Retracted source.", h)
        self.assertIn("Corrected source.", h)
        self.assertIn("A &lt;paper&gt;", h)
        self.assertIn('href="https://example.org/retraction"', h)

    def test_no_notice_when_not_flagged(self):
        self.assertEqual(ps.claim_notice_html({"id": "c"}, self.man), "")

    def test_notices_list(self):
        h = ps.notices_html({"source_notices": NOTICE}, self.man)
        self.assertIn("Source notices", h)
        self.assertIn("This paper was retracted.", h)
        self.assertEqual(ps.notices_html({}, self.man), "")

    def test_source_list_and_note(self):
        tag, ident = ps.source_li_extra(self.man["src-a"])
        self.assertIn("retracted", tag)
        self.assertEqual(ident, ' id="src-a"')
        self.assertEqual(ps.source_li_extra(self.man["src-c"]), ("", ""))
        self.assertEqual(ps.sources_note([self.man["src-c"]]), "")
        self.assertIn("not the same as clean", ps.sources_note(list(self.man.values())))


if __name__ == "__main__":
    unittest.main(verbosity=2)
