import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

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


def draw_turtle_map() -> bool:
    """Open a turtle window showing Eli's route west. Returns True if drawn."""
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
            "Lansing": (-320, 120),
            "Chicago": (-220, 60),
            "Denver": (-50, 40),
            "Las Vegas": (230, -40),
        }

        route.penup()
        route.goto(points["Lansing"])
        route.pendown()
        for city in ("Chicago", "Denver", "Las Vegas"):
            route.goto(points[city])

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

        legend = turtle.Turtle()
        legend.hideturtle()
        legend.color("light sky blue")
        legend.penup()
        legend.goto(-380, -200)
        legend.write(
            "Click anywhere in the window to close the route view.",
            font=("Arial", 12, "normal"),
        )

        screen.exitonclick()
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"Unable to open turtle visualization: {exc}")
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
    scripted_choices: List[str] | None = None,
    auto_turtle: bool = False,
) -> None:
    current = "offer"
    script_index = 0
    map_announced = False

    while True:
        node = nodes[current]
        print(f"\n== {node.title} ==\n{node.text}\n")

        if not node.choices:
            print("The adventure ends here. Thanks for guiding Eli!\n")
            break

        if current == "travel_method" and not map_announced:
            map_path = render_map()
            print(f"A simple map of Eli's journey was generated at: {map_path}\n")
            map_announced = True

            if auto_turtle:
                print("Opening a turtle route view... Close the window to continue.\n")
                draw_turtle_map()
            elif scripted_choices is None:
                wants_turtle = input(
                    "Would you like to open a turtle window of the route? (Y/N): "
                ).strip().upper()
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

        next_node = next((c.target for c in node.choices if c.key == user_choice), None)
        if next_node is None:
            print("Invalid choice. Please try again.")
            continue

        current = next_node
        script_index += 1


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
        help="Automatically open the turtle route view once the job offer is accepted.",
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
