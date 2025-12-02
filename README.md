# Adventure Engine: Eli's Move to Las Vegas

This Python adventure engine follows Eli Klunder after graduating from Michigan State University and accepting the Circa Management Trainee position in Las Vegas. The story begins with a my-choice moment to accept or decline the move and branches through at least four decision layers as Eli travels from Michigan to Nevada.

## Features
- **Interactive branching narrative** with multiple endings and meaningful options at each step.
- **Quit option** available on every prompt.
- **ASCII route map** automatically generated at `journey_map.txt` once the job offer is accepted to provide a simple visual of the move.
- **Optional turtle visualization** that plots the journey from Lansing to Las Vegas when you accept the job offer.
- **Modular structure** using data classes for story nodes and choices, keeping content separate from the engine logic.
- **Demo mode** (`--demo`) to auto-play a complete path for quick verification.

## Running the adventure
```bash
python main.py              # Play interactively
python main.py --demo       # Auto-play a sample path (useful for grading or quick checks)
python main.py --turtle     # Auto-open the turtle route view when the offer is accepted
```

When playing interactively, enter the number for a choice or `Q` to exit at any time. Once you accept the offer, you'll be prompted to open a turtle window showing the route (or you can auto-open it with `--turtle`). The generated ASCII map can be opened with any text editor.
python main.py          # Play interactively
python main.py --demo   # Auto-play a sample path (useful for grading or quick checks)
```

When playing interactively, enter the number for a choice or `Q` to exit at any time. The generated ASCII map can be opened with any text editor.

## Project organization
- `main.py` contains the engine logic, story graph, input handling, and map generation. Story content is defined in `build_story()` while navigation and I/O are handled by `play_story()`.
- `journey_map.txt` is created on demand when the offer is accepted.

## Author statement
To make the narrative feel intentional, I separated the branching logic from the story content using data classes (`StoryNode`, `Choice`) and a reusable `play_story` loop. This mirrors course discussions about modularity and makes it easy to grow the story tree without changing engine code. The optional `--demo` mode leverages the same engine, demonstrating reuse of logic while providing a quick automated path for testing.
