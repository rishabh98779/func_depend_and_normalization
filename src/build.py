#!/usr/bin/env python3
"""Assemble DATABASE MANAGEMENT SYSTEMS — COMPLETE EXAM-READY NOTES.

Reads HTML fragments from src/ and writes a single self-contained HTML file,
then renders it to PDF with WeasyPrint.
"""
import os, re, sys
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

TITLE = "DATABASE MANAGEMENT SYSTEMS — COMPLETE EXAM-READY NOTES"

# (level, title, anchor)  level 1 = part, 2 = chapter, 3 = section
TOC = [
    (1, "How to Use These Notes", "howto"),
    (1, "Source, Scope and Coverage Statement", "coverage"),
    (1, "PART 1 — Relational Foundations and Database Keys", "part1"),
    (2, "1. Relational Model Foundations and the Idea of a Key", "c1"),
    (3, "1.1 Relation, Tuple, Attribute and Domain", "c1-1"),
    (3, "1.2 Why a Database Needs Keys", "c1-2"),
    (3, "1.3 The Vocabulary Trap: Relation = Table, Tuple = Record", "c1-3"),
    (2, "2. The Ten Keys in Detail", "c2"),
    (3, "2.1 Super Key", "c2-1"),
    (3, "2.2 Candidate Key", "c2-2"),
    (3, "2.3 Primary Key", "c2-3"),
    (3, "2.4 Alternate Key", "c2-4"),
    (3, "2.5 Foreign Key and Referential Integrity", "c2-5"),
    (3, "2.6 Partial Key", "c2-6"),
    (3, "2.7 Composite Key and Compound Key", "c2-7"),
    (3, "2.8 Unique Key", "c2-8"),
    (3, "2.9 Surrogate Key", "c2-9"),
    (3, "2.10 Secondary Key", "c2-10"),
    (3, "2.11 Key Classification at a Glance", "c2-11"),
    (3, "2.12 Commonly Confused Pairs", "c2-12"),
    (3, "2.13 Key Identification Exercises", "c2-13"),
    (1, "PART 2 — Functional Dependencies", "part2"),
    (2, "3. Functional Dependencies: Meaning and Notation", "c3"),
    (3, "3.1 What a Functional Dependency Says", "c3-1"),
    (3, "3.2 Determinant and Dependent", "c3-2"),
    (3, "3.3 Reading a Dependency Correctly", "c3-3"),
    (3, "3.4 Finding Dependencies in a Table", "c3-4"),
    (3, "3.5 Trivial, Non-Trivial and Completely Non-Trivial", "c3-5"),
    (3, "3.6 Why Functional Dependencies Matter", "c3-6"),
    (2, "4. Armstrong's Axioms and Reasoning with Dependencies", "c4"),
    (3, "4.1 The Three Primary Axioms", "c4-1"),
    (3, "4.2 Derived Rules", "c4-2"),
    (3, "4.3 Closure of a Set of Attributes", "c4-3"),
    (3, "4.4 Worked Closure Computations", "c4-4"),
    (3, "4.5 Equivalence of Dependency Sets", "c4-5"),
    (2, "5. Special Dependencies: Transitive, Multivalued and Join", "c5"),
    (3, "5.1 Transitive Dependency", "c5-1"),
    (3, "5.2 Multivalued Dependency", "c5-2"),
    (3, "5.3 Join Dependency", "c5-3"),
    (3, "5.4 Dependency Types and the Normal Forms They Drive", "c5-4"),
    (1, "PART 3 — Normalization", "part3"),
    (2, "6. Normalization Fundamentals and First Normal Form", "c6"),
    (3, "6.1 What Normalization Is", "c6-1"),
    (3, "6.2 The Three Anomalies", "c6-2"),
    (3, "6.3 The Ladder of Normal Forms", "c6-3"),
    (3, "6.4 First Normal Form (1NF)", "c6-4"),
    (3, "6.5 Worked 1NF Example", "c6-5"),
    (2, "7. Second Normal Form (2NF)", "c7"),
    (3, "7.1 Prime and Non-Prime Attributes", "c7-1"),
    (3, "7.2 The 2NF Rule: Full Functional Dependency", "c7-2"),
    (3, "7.3 Partial Dependency and How to Remove It", "c7-3"),
    (3, "7.4 Worked 2NF Example", "c7-4"),
    (2, "8. Third Normal Form (3NF)", "c8"),
    (3, "8.1 The 3NF Rule", "c8-1"),
    (3, "8.2 Transitive Dependency in a Real Relation", "c8-2"),
    (3, "8.3 Worked 3NF Example", "c8-3"),
    (2, "9. Boyce-Codd Normal Form (BCNF)", "c9"),
    (3, "9.1 Why 3NF Is Not Always Enough", "c9-1"),
    (3, "9.2 The BCNF Rule", "c9-2"),
    (3, "9.3 Worked BCNF Example: Employees and Departments", "c9-3"),
    (3, "9.4 BCNF and Lossless Join", "c9-4"),
    (2, "10. Fourth Normal Form (4NF)", "c10"),
    (3, "10.1 Multivalued Dependency Revisited", "c10-1"),
    (3, "10.2 The 4NF Rule", "c10-2"),
    (3, "10.3 Worked 4NF Example: Students", "c10-3"),
    (3, "10.4 Worked 4NF Example: Subject, Lecturer, Books", "c10-4"),
    (2, "11. Fifth Normal Form (5NF) and Join Dependency", "c11"),
    (3, "11.1 The 5NF Rule", "c11-1"),
    (3, "11.2 Worked 5NF Example: Agent, Company, Product", "c11-2"),
    (3, "11.3 Why 5NF Is Largely of Academic Interest", "c11-3"),
    (2, "12. Lossless Decomposition", "c12"),
    (3, "12.1 What Lossless Means", "c12-1"),
    (3, "12.2 The Lossless-Join Test", "c12-2"),
    (3, "12.3 Worked Test on a Student Relation", "c12-3"),
    (3, "12.4 Dependency Preservation", "c12-4"),
    (2, "13. A Complete Worked Normalization Case Study", "c13"),
    (3, "13.1 The Unnormalized Relation", "c13-1"),
    (3, "13.2 Step 1: To 1NF", "c13-2"),
    (3, "13.3 Step 2: To 2NF", "c13-3"),
    (3, "13.4 Step 3: To 3NF", "c13-4"),
    (3, "13.5 Step 4: To BCNF", "c13-5"),
    (3, "13.6 Step 5: To 4NF", "c13-6"),
    (3, "13.7 The Final Schema", "c13-7"),
    (2, "14. Denormalization", "c14"),
    (3, "14.1 Definition and Motivation", "c14-1"),
    (3, "14.2 A Concrete Example", "c14-2"),
    (3, "14.3 Benefits and Trade-Offs", "c14-3"),
    (1, "PART 4 — Database Security", "part4"),
    (2, "15. Database Security: Meaning, Importance and Scope", "c15"),
    (3, "15.1 Definition", "c15-1"),
    (3, "15.2 The Five Things Security Must Protect", "c15-2"),
    (3, "15.3 The Usability Paradox", "c15-3"),
    (3, "15.4 Why Database Security Matters", "c15-4"),
    (2, "16. Threats and the CIA Triad", "c16"),
    (3, "16.1 What a Threat Is", "c16-1"),
    (3, "16.2 Loss of Integrity, Availability and Confidentiality", "c16-2"),
    (3, "16.3 Threat Categories", "c16-3"),
    (2, "17. Levels of Data Security, Physical and OS Security", "c17"),
    (3, "17.1 Types of Security Issues", "c17-1"),
    (3, "17.2 The Six Levels of Data Security", "c17-2"),
    (3, "17.3 Physical-Level Security", "c17-3"),
    (3, "17.4 Operating-System-Level Security", "c17-4"),
    (2, "18. Encryption and Key Management", "c18"),
    (3, "18.1 Why Encrypt", "c18-1"),
    (3, "18.2 Storage-Level Encryption and Key Management", "c18-2"),
    (3, "18.3 Practical Guidance from the Source", "c18-3"),
    (2, "19. Authentication, Authorization and Access-Control Models", "c19"),
    (3, "19.1 Authentication versus Authorization", "c19-1"),
    (3, "19.2 Discretionary Access Control (DAC)", "c19-2"),
    (3, "19.3 Mandatory Access Control (MAC)", "c19-3"),
    (3, "19.4 Role-Based Access Control (RBAC)", "c19-4"),
    (3, "19.5 Comparing the Three Models", "c19-5"),
    (2, "20. Network and Human-Level Security", "c20"),
    (3, "20.1 Network-Level Threats", "c20-1"),
    (3, "20.2 Passwords", "c20-2"),
    (3, "20.3 Smartcards", "c20-3"),
    (2, "21. Control Methods of Database Security", "c21"),
    (3, "21.1 The Six Control Measures", "c21-1"),
    (3, "21.2 Authentication", "c21-2"),
    (3, "21.3 Access Control", "c21-3"),
    (3, "21.4 Inference Control", "c21-4"),
    (3, "21.5 Flow Control and Covert Channels", "c21-5"),
    (3, "21.6 Statistical Database Security", "c21-6"),
    (3, "21.7 Encryption", "c21-7"),
    (3, "21.8 Threat-to-Control Mapping", "c21-8"),
    (2, "22. The DBA, Privileges and Statistical Database Security", "c22"),
    (3, "22.1 Who the DBA Is", "c22-1"),
    (3, "22.2 DBA Responsibilities", "c22-2"),
    (3, "22.3 The DBA / Superuser Account", "c22-3"),
    (1, "PART 5 — PL/SQL Control Structures", "part5"),
    (2, "23. PL/SQL Control Structures: Overview", "c23"),
    (3, "23.1 What Control Structures Are For", "c23-1"),
    (3, "23.2 The Three Categories", "c23-2"),
    (3, "23.3 The Anonymous Block", "c23-3"),
    (3, "23.4 SET SERVEROUTPUT and the Substitution Variable", "c23-4"),
    (2, "24. Conditional Control: IF and CASE", "c24"),
    (3, "24.1 IF-THEN", "c24-1"),
    (3, "24.2 IF-THEN-ELSE", "c24-2"),
    (3, "24.3 IF-THEN-ELSIF", "c24-3"),
    (3, "24.4 IF-THEN-ELSIF-ELSE", "c24-4"),
    (3, "24.5 The CASE Statement", "c24-5"),
    (3, "24.6 Worked Conditional Programs", "c24-6"),
    (2, "25. Iterative Control: LOOP, WHILE and FOR", "c25"),
    (3, "25.1 The Basic LOOP", "c25-1"),
    (3, "25.2 EXIT and EXIT-WHEN", "c25-2"),
    (3, "25.3 Loop Labels and Nested Loops", "c25-3"),
    (3, "25.4 WHILE-LOOP", "c25-4"),
    (3, "25.5 Building a Loop-That-Runs-At-Least-Once", "c25-5"),
    (3, "25.6 FOR-LOOP and REVERSE", "c25-6"),
    (3, "25.7 Worked Iterative Programs", "c25-7"),
    (2, "26. Sequential Control: GOTO and NULL", "c26"),
    (3, "26.1 The GOTO Statement", "c26-1"),
    (3, "26.2 Worked GOTO Programs", "c26-2"),
    (3, "26.3 Restrictions on GOTO", "c26-3"),
    (3, "26.4 The NULL Statement", "c26-4"),
    (1, "PART 6 — PL/SQL Cursors", "part6"),
    (2, "27. Cursors: Concept and Implicit Cursors", "c27"),
    (3, "27.1 What a Cursor Is", "c27-1"),
    (3, "27.2 The Context Area and the Active Set", "c27-2"),
    (3, "27.3 Implicit Cursors", "c27-3"),
    (3, "27.4 Implicit Cursor Attributes", "c27-4"),
    (3, "27.5 Worked Implicit Cursor Program", "c27-5"),
    (2, "28. Explicit Cursors and Cursor Loops", "c28"),
    (3, "28.1 Declaring, Opening, Fetching and Closing", "c28-1"),
    (3, "28.2 The Cursor Life Cycle", "c28-2"),
    (3, "28.3 Worked Explicit Cursor Program", "c28-3"),
    (3, "28.4 Implicit versus Explicit Cursors", "c28-4"),
    (3, "28.5 Cursor Errors and Exam Traps", "c28-5"),
    (1, "PART 7 — SQL Views", "part7"),
    (2, "29. SQL Views: Concept and Creation", "c29"),
    (3, "29.1 Definition and Base Tables", "c29-1"),
    (3, "29.2 Benefits of Views", "c29-2"),
    (3, "29.3 The Sample Tables Used Throughout", "c29-3"),
    (3, "29.4 Creating a View from a Single Table", "c29-4"),
    (3, "29.5 Creating a View from Multiple Tables", "c29-5"),
    (3, "29.6 Querying a View", "c29-6"),
    (2, "30. Modifying, Dropping and Updating Views", "c30"),
    (3, "30.1 Dropping a View", "c30-1"),
    (3, "30.2 Creating or Replacing a View", "c30-2"),
    (3, "30.3 Conditions Required to Update a View", "c30-3"),
    (3, "30.4 Inserting a Row Through a View", "c30-4"),
    (3, "30.5 Deleting a Row Through a View", "c30-5"),
    (3, "30.6 WITH CHECK OPTION", "c30-6"),
    (3, "30.7 Uses of a View", "c30-7"),
    (1, "PART 8 — Revision and Examination", "part8"),
    (2, "31. Consolidated Comparison Tables and Formula Sheet", "c31"),
    (3, "31.1 Key Comparison Tables", "c31-1"),
    (3, "31.2 Normal-Form Summary Table", "c31-2"),
    (3, "31.3 Dependency Rules and Axioms", "c31-3"),
    (3, "31.4 PL/SQL Control-Structure Summary", "c31-4"),
    (3, "31.5 Cursor and View Summary", "c31-5"),
    (3, "31.6 Security Summary", "c31-6"),
    (2, "32. Question Bank with Answers", "c32"),
    (3, "32.1 Two-Mark Questions", "c32-1"),
    (3, "32.2 Five-Mark Questions", "c32-2"),
    (3, "32.3 Ten-Mark / Descriptive Questions", "c32-3"),
    (3, "32.4 Output-Prediction Questions", "c32-4"),
    (3, "32.5 Debugging Questions", "c32-5"),
    (3, "32.6 Normalization Problems with Step-by-Step Solutions", "c32-6"),
    (2, "33. MCQ Bank with Answer Key", "c33"),
    (2, "34. Viva Questions", "c34"),
    (2, "35. Last-Minute Revision Sheet", "c35"),
    (2, "36. Source Coverage Checklist and References", "c36"),
]


def toc_html():
    out = ['<section class="toc"><h1>Contents</h1>',
           '<p class="small">A complete DBMS chapter built from the supplied Chandigarh University lecture '
           'material (UNIT 2): relational keys, functional dependencies, normalization, database security, '
           'PL/SQL control structures, cursors and SQL views — taught from first principles, then revised '
           'for exams, practicals and viva.</p><ul>']
    for lvl, title, anchor in TOC:
        out.append(f'<li class="lvl{lvl}"><a href="#{anchor}">{title}</a></li>')
    out.append('</ul>')
    out.append('<p class="tocnote">Note: page numbers in the Contents above are printed page numbers. '
               'The two front-matter pages that precede it are labelled <b>i</b> and <b>ii</b>; the cover '
               'and the eight Part-divider pages carry no printed number, so the printed sequence 1–182 '
               'skips them.</p>')
    out.append('</section>')
    return "\n".join(out)


def load(name):
    p = os.path.join(HERE, name)
    with open(p, encoding="utf-8") as f:
        return f.read()


CONTENT_FILES = [
    "content_part1.html",    # keys
    "content_part2.html",    # functional dependencies
    "content_part3a.html",   # normalization: 1NF .. BCNF
    "content_part3b.html",   # normalization: 4NF, 5NF, lossless, case study, denormalization
    "content_part4.html",    # database security
    "content_part5.html",    # PL/SQL control structures
    "content_part6.html",    # cursors
    "content_part7.html",    # SQL views
    "content_part8a.html",   # revision: comparison tables, question bank
    "content_part8b.html",   # MCQ, viva, last-minute sheet, coverage
]


def build_html():
    css = load("book.css")
    front = load("front.html")
    parts = "".join(load(f) for f in CONTENT_FILES)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{TITLE}</title>
<style>{css}</style>
</head>
<body>
{front}
{toc_html()}
{parts}
</body></html>"""


def main():
    html = build_html()
    out_html = os.path.join(ROOT, "DBMS_Complete_Exam_Ready_Notes.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    out_pdf = os.path.join(ROOT, "DBMS_Complete_Exam_Ready_Notes.pdf")
    HTML(string=html, base_url=HERE).write_pdf(out_pdf)
    import pymupdf
    d = pymupdf.open(out_pdf)
    print(f"HTML : {out_html}")
    print(f"PDF  : {out_pdf}  ({d.page_count} pages)")


if __name__ == "__main__":
    main()
