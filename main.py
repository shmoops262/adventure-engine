import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional

MAP_PATH = Path("journey_map.txt")


@dataclass
class Choice:
    key: str
    description: str
    target: str


@dataclass
class StoryNode:
    title: str
    text: str
    choices: List[Choice]


def render_map() -> Path:
    """Render a simple ASCII route map from Michigan to Las Vegas."""
    if MAP_PATH.exists():
        return MAP_PATH

    map_lines = [
        "  ┌───────────────────────────────────────────┐",
        "  │               Journey West               │",
        "  ├───────────────────────────────────────────┤",
        "  │                                           │",
        "  │   Lansing ●───Chicago ●                  │",
        "  │             \\                            │",
        "  │              \\                           │",
        "  │               Denver ●────────Las Vegas ● │",
        "  │                                           │",
        "  └───────────────────────────────────────────┘",
    ]

    MAP_PATH.write_text("\n".join(map_lines))
    return MAP_PATH


def draw_turtle_map(taken_choices: Optional[List[Tuple[str, str]]] = None) -> bool:
    """Open a turtle window summarizing the user's chosen path.

    `taken_choices` may be None (show only the route) or a list of
    (section title, choice description) pairs to display in a legend.
    Returns True if the window was shown, False on failure.
    """
    try:
        import turtle

        screen = turtle.Screen()
        screen.title("Eli's Journey: Michigan to Las Vegas")
        screen.setup(width=900, height=520)
        screen.bgcolor("midnight blue")

        route = turtle.Turtle()
        route.hideturtle()
        route.speed("fastest")
        route.color("gold")
        route.pensize(4)

        points = {
            "Lansing": (-340, 140),
            "Chicago": (-240, 80),
            "Denver": (-50, 40),
            "Las Vegas": (240, -40),
        }

        taken_choices = taken_choices or []
        accepted_offer = any("Accept the job offer" in desc for (_title, desc) in taken_choices)

        visited_cities = ["Lansing"]
        if accepted_offer:
            visited_cities.extend(["Chicago", "Denver", "Las Vegas"])

        # Draw the polyline for the visited cities
        route.penup()
        route.goto(points[visited_cities[0]])
        route.pendown()
        for city in visited_cities[1:]:
            route.goto(points[city])

        # Draw city markers and labels
        marker = turtle.Turtle()
        marker.hideturtle()
        marker.speed("fastest")
        marker.color("white")
        for city, coords in points.items():
            marker.penup()
            marker.goto(coords)
            marker.dot(16, "orange")
            marker.goto(coords[0], coords[1] + 12)
            marker.write(city, align="center", font=("Arial", 11, "bold"))

        # Legend / selections
        legend = turtle.Turtle()
        legend.hideturtle()
        legend.color("light sky blue")
        legend.penup()
        legend.goto(-460, -230)
        legend.write(
            "Click anywhere in the window to close. Your selections:",
            font=("Arial", 13, "bold"),
        )

        text_y = -255
        for idx, (title, description) in enumerate(taken_choices, start=1):
            legend.goto(-460, text_y + idx * 18)
            legend.write(f"{idx}. {title}: {description}", font=("Arial", 11, "normal"))

        legend.goto(-380, -200)
        legend.write("Click anywhere in the window to close the route view.", font=("Arial", 12, "normal"))

        screen.exitonclick()
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"Unable to open turtle visualization: {exc}")
        # Fallback: create a simple HTML+SVG visualization and open it in the browser.
        try:
            import webbrowser

            file_path = Path("journey_route.html")
            # Prepare SVG coordinates (flip Y for SVG coordinate system)
            width, height = 900, 520
            cx, cy = width // 2, height // 2
            scale = 1

            def svgy(x, y):
                return f"{cx + int(x * scale)},{cy - int(y * scale)}"

            points_list = [
                ("Lansing", -340, 140),
                ("Chicago", -240, 80),
                ("Denver", -50, 40),
                ("Las Vegas", 240, -40),
            ]

            pts = {name: (x, y) for name, x, y in points_list}
            visited = ["Lansing"]
            if any("Accept the job offer" in desc for (_t, desc) in taken_choices):
                visited.extend(["Chicago", "Denver", "Las Vegas"])

            poly_points = " ".join(svgy(*pts[c]) for c in visited)

            markers = []
            for name, (x, y) in pts.items():
                markers.append(f"<circle cx=\"{svgy(x,y).split(',')[0]}\" cy=\"{svgy(x,y).split(',')[1]}\" r=\"8\" fill=\"orange\"/>\n")
                markers.append(f"<text x=\"{svgy(x,y).split(',')[0]}\" y=\"{int(svgy(x,y).split(',')[1]) - 12}\" font-size=\"12\" fill=\"white\" text-anchor=\"middle\">{name}</text>\n")

            legend_lines = []
            for idx, (title, description) in enumerate(taken_choices or [], start=1):
                legend_lines.append(f"<div>{idx}. <strong>{title}</strong>: {description}</div>")

            html_parts = []
            html_parts.append(f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>Eli's Journey - Fallback View</title></head>
<body style="background:#001; color:#ddd; font-family:Arial,Helvetica,sans-serif;">
<h2 style="color:#fff;">Eli's Journey - Fallback Route View</h2>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" style="background:midnightblue; display:block; margin:8px 0;">
  <polyline points="{poly_points}" fill="none" stroke="gold" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
""")
            html_parts.append("\n".join(markers))
            html_parts.append("</svg>\n")
            html_parts.append(f"<div style=\"margin-top:10px;color:#cfe;\">{''.join(legend_lines)}</div>\n")
            html_parts.append("</body></html>")
            html_content = "".join(html_parts)

            file_path.write_text(html_content, encoding="utf-8")
            try:
                webbrowser.open(file_path.resolve().as_uri())
            except Exception:
                # If opening the browser fails, just inform the user where the file is.
                pass
            print(f"Fallback route visualization saved to: {file_path.resolve()}")
            return True
        except Exception as exc2:
            print(f"Also failed to create fallback visualization: {exc2}")
            return False


def build_story() -> Dict[str, StoryNode]:
    return {
        "offer": StoryNode(
            title="The Offer Letter",
            text=(
                "Eli Klunder just graduated from Michigan State University. "
                "The Circa Management Trainee program in Las Vegas sent an offer. "
                "Does he accept and start packing for the desert, or stay in Michigan?"
            ),
            choices=[
                Choice("1", "Accept the job offer and chase the Vegas adventure", "travel_method"),
                Choice("2", "Stay in Michigan and postpone the move", "stay_home"),
            ],
        ),
        "stay_home": StoryNode(
            title="Staying Put",
            text=(
                "Eli keeps his Spartan roots in Michigan for now. The Strip will have to wait, "
                "but the Circa team sends a friendly note encouraging him to reapply later."
            ),
            choices=[],
        ),
        "travel_method": StoryNode(
            title="Planning the Move",
            text=(
                "With the offer accepted, Eli must choose how to travel west. A road trip offers "
                "open highways, but a flight would get him to training faster."
            ),
            choices=[
                Choice("1", "Drive cross-country with playlists and podcasts", "drive_prep"),
                Choice("2", "Fly to Las Vegas and ship the essentials", "fly_prep"),
            ],
        ),
        "drive_prep": StoryNode(
            title="Packing the Car",
            text=(
                "Eli loads his hatchback. He can overpack with souvenirs from East Lansing or travel "
                "light to keep the car nimble over the Rockies."
            ),
            choices=[
                Choice("1", "Pack heavy: memorabilia, winter coats, and gadgets", "midwest_leg"),
                Choice("2", "Minimalist: only essentials and a lucky MSU pennant", "midwest_leg"),
            ],
        ),
        "midwest_leg": StoryNode(
            title="Crossing the Midwest",
            text=(
                "The Michigan sunsets fade in the rearview. Eli approaches Chicago and debates a detour."
            ),
            choices=[
                Choice("1", "Stop in Chicago for deep dish and a skyline photo", "great_plains"),
                Choice("2", "Push straight through toward the Great Plains", "great_plains"),
            ],
        ),
        "great_plains": StoryNode(
            title="Great Plains Night",
            text=(
                "Nebraska's open skies stretch for miles. The road hums under Eli's tires."
            ),
            choices=[
                Choice("1", "Camp under the stars to recharge", "rockies"),
                Choice("2", "Drive overnight with neon podcasts", "rockies"),
            ],
        ),
        "rockies": StoryNode(
            title="Rocky Mountain Pass",
            text=(
                "Mountain air greets Eli near Denver. He must choose between speed and scenery."
            ),
            choices=[
                Choice("1", "Take the scenic route through mountain towns", "vegas_arrival"),
                Choice("2", "Stick to the interstate to arrive ahead of schedule", "vegas_arrival"),
            ],
        ),
        "fly_prep": StoryNode(
            title="Booking the Flight",
            text=(
                "A one-way ticket from Detroit to Las Vegas pops up with a layover in Denver. Eli "
                "balances cost against comfort for the big leap."
            ),
            choices=[
                Choice("1", "Choose the cheap redeye and nap on the plane", "airport_wait"),
                Choice("2", "Pick the daytime flight with a window seat", "airport_wait"),
            ],
        ),
        "airport_wait": StoryNode(
            title="Airport Vibes",
            text=(
                "Suitcase tagged for LAS, Eli has time before boarding. He can grind through onboarding paperwork "
                "or explore the terminal."
            ),
            choices=[
                Choice("1", "Finish Circa onboarding modules early", "vegas_arrival"),
                Choice("2", "Chat with fellow travelers about Vegas tips", "vegas_arrival"),
            ],
        ),
        "vegas_arrival": StoryNode(
            title="Welcome to Las Vegas",
            text=(
                "After miles or miles above the clouds, the Strip's glow rises. Circa's Management Trainee program "
                "begins Monday, but Eli has the weekend to settle in and choose his vibe."
            ),
            choices=[
                Choice("1", "Explore Fremont Street with new teammates", "first_weekend"),
                Choice("2", "Spend a quiet evening organizing his apartment", "first_weekend"),
            ],
        ),
        "first_weekend": StoryNode(
            title="First Weekend Decisions",
            text=(
                "Eli's choices set the tone for his Vegas chapter. The city is wide open, and the Circa team is ready."
            ),
            choices=[
                Choice("1", "Celebrate with a rooftop view and envision the career ahead", "ending_rooftop"),
                Choice("2", "Take a sunrise jog on the Strip to center himself", "ending_sunrise"),
            ],
        ),
        "ending_rooftop": StoryNode(
            title="Rooftop Resolve",
            text=(
                "Music and neon spill across the skyline. Eli toasts to the Circa program, feeling ready to learn, lead, "
                "and represent his Spartan grit in a new city."
            ),
            choices=[],
        ),
        "ending_sunrise": StoryNode(
            title="Sunrise Focus",
            text=(
                "Cool desert air and sunrise colors calm his nerves. The Management Trainee badge sits on his desk, "
                "waiting for Monday's first briefing."
            ),
            choices=[],
        ),
    }


def prompt_choice(node: StoryNode, allow_quit: bool = True) -> str:
    for choice in node.choices:
        print(f"  {choice.key}. {choice.description}")
    if allow_quit:
        print("  Q. Quit the adventure")
    return input("Your choice: ").strip().upper()


def play_story(
    nodes: Dict[str, StoryNode],
    scripted_choices: Optional[List[str]] = None,
    auto_turtle: bool = False,
) -> None:
    current = "offer"
    script_index = 0
    taken_choices: List[Tuple[str, str]] = []
    reached_ending = False
    map_announced = False

    while True:
        node = nodes[current]
        print(f"\n== {node.title} ==\n{node.text}\n")

        if not node.choices:
            print("The adventure ends here. Thanks for guiding Eli!\n")
            reached_ending = True
            break

        if current == "travel_method" and not map_announced:
            map_path = render_map()
            print(f"A simple map of Eli's journey was generated at: {map_path}\n")
            map_announced = True

            if auto_turtle:
                print("Opening a turtle route view... Close the window to continue.\n")
                draw_turtle_map()
            elif scripted_choices is None:
                wants_turtle = input("Would you like to open a turtle window of the route? (Y/N): ").strip().upper()
                if wants_turtle == "Y":
                    print("Launching turtle visualization. Close the window to continue.\n")
                    draw_turtle_map()

        user_choice = (
            scripted_choices[script_index].upper()
            if scripted_choices and script_index < len(scripted_choices)
            else prompt_choice(node)
        )

        if scripted_choices:
            print(f"[auto-choice] {user_choice}")

        if user_choice == "Q":
            print("You chose to quit. Safe travels, wherever they lead.\n")
            break

        selected_choice = next((c for c in node.choices if c.key == user_choice), None)
        if selected_choice is None:
            print("Invalid choice. Please try again.")
            continue

        taken_choices.append((node.title, selected_choice.description))
        current = selected_choice.target
        script_index += 1

    # After the loop, optionally show a map/summary of the taken path
    if taken_choices and reached_ending:
        map_path = render_map()
        print(f"A simple map of Eli's journey was saved to: {map_path}")

        if auto_turtle:
            print("Opening a turtle summary of your path... Close the window when done.\n")
            draw_turtle_map(taken_choices)
        elif scripted_choices is None:
            wants_turtle = input("Would you like to open a turtle summary of your choices? (Y/N): ").strip().upper()
            if wants_turtle == "Y":
                print("Launching turtle visualization. Close the window to continue.\n")
                draw_turtle_map(taken_choices)
        else:
            print("Turtle visualization skipped (demo mode). Use --turtle to auto-open.\n")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Eli Klunder's move to Las Vegas adventure engine")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Automatically play through a sample path without interactive input.",
    )
    parser.add_argument(
        "--turtle",
        action="store_true",
        help="Automatically open the turtle route view when appropriate (map/summary).",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    nodes = build_story()
    demo_choices = ["1", "1", "2", "1", "1", "1", "1", "1"] if args.demo else None
    play_story(nodes, scripted_choices=demo_choices, auto_turtle=args.turtle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
