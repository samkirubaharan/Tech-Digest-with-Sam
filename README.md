# Tech Digest with Sam

This repository holds the raw data, tagging framework, synthesis scripts, and the newsletters for "Tech Digest with Sam".

## Directory Structure

- `data/`
  Raw data files fetched from sources (e.g., `loveit_1_raw.html`, `mr&mrscurious_raw.html`, `thebyline_raw.html`).
- `src/`
  Contains the backend logic for processing, tagging, and structuring the data:
  - `framework/tagging/`: Framework directory for tagging approaches.
    - `loader.py`: Loads the raw data.
    - `tagger.py`: Tags content (e.g., Love it, Curious, Byline).
    - `models.py` & `ranker.py`: Core logic for managing and ranking data.
  - `framework/synthesis/`: Framework directory for synthesis and formatting.
    - `formatter.py` & `newsletter.py`: Formats and generates the final newsletter structures.
  - `framework/tests.py`: Evaluation and test suite.
- `newsletter/current/`
  Contains the currently worked on newsletters. This will have the synthesized markdown files (`..._synth.md`), corresponding HTML renders, and the final PDF (`Week <X> - <Year>.pdf`).
- `newsletter/archives/`
  Contains archived newsletters organized by week.
