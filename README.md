# University of Bath AI MSc coursework portfolio

Selected coursework by Graziano Brady from the University of Bath's online MSc in Artificial Intelligence. The projects below show algorithm implementation, systems design, critical reading of research, and ethical analysis.

## Selected projects

| Project | What to look for | Deliverable |
| --- | --- | --- |
| [Queens genetic algorithm](Further_AI/Queens_Genetic_Algorithm/) | Tournament selection, adaptive mutation, elitism and population resets; extension to a toroidal board | Runnable Python, independent tests and original report |
| [Film recommender system design](AI_Systems_Engineering/Film_Recommender/) | Architecture, functional requirements, deployment trade-offs, risk mitigation and telemetry | Completed design report; a proposal, not a deployed application |
| [Deepfake detection paper review](Foundations_and_Frontiers/Deepfake_Paper_Review/) | Evaluation of methodology, benchmark evidence, generalisation and fairness assumptions | Critical literature review; no claim of implementing the reviewed model |
| [AI and the future of work](Humans_and_Intelligent_Machines/AI_and_Work/) | Ethical argument, economic evidence and stakeholder responsibilities | Completed coursework essay |

Start with the queens project for a code sample. Each project has a short guide explaining its scope, provenance and limitations. Reports retain their original wording and references; they represent coursework at the time of writing, rather than an up-to-date survey or production validation.

## Earlier uploads

- [Principles of Programming](Principles_of_Programming/): Enigma implementations and notebook.
- [Foundations of Artificial Intelligence](Foundations_Artificial_Intelligence/): dice-game and spam-classification work.

These earlier uploads are preserved. The October 2026 verification below applies to the new selected projects, not to every historical file in this repository.

## Verification and scope

The queens project passed seven automated tests on Python 3.12.14 and NumPy 2.3.5 on Windows. Tests compare both board-cost functions against an independent implementation, check board operations, run five classic and four toroidal seeded searches, and check bounded termination on an unsolved case. See [validation details](Further_AI/Queens_Genetic_Algorithm/VALIDATION.md).

The four reports were reviewed for substantive content and rendered for a page-by-page layout check. Their reported experiments and cited literature were not independently reproduced in full. No production-readiness or grade claims are made.

## Attribution

This is a personal coursework portfolio, not an official University of Bath repository. The queens state representation builds on course-provided starter code, and the report identifies references and the use of coding assistants. Figures, quotations and research results attributed within the reports belong to their respective sources; reproduced results in the deepfake review are the paper authors' results. No blanket licence over third-party content is asserted.
