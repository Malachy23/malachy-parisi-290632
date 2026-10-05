from collections import defaultdict
import sys


class Metro:
    def __init__(self):
        self.inside = set()
        self.fare_totals = defaultdict(int)
        self.trip_counts = defaultdict(int)
        self.regular_counts = defaultdict(lambda: defaultdict(int))

        self.output = []

        self.INV_COMMAND = "ERROR invalid command"
        self.INV_STATION = "ERROR unknown station"

        self.VALID_COMMANDS = {
            "TAPIN",
            "TAPOUT",
            "PENDING",
            "PENDINGS",
            "FARE",
            "REGULARS",
        }

        self.VALID_STATIONS = {
            "garibaldi",
            "universita",
            "municipio",
            "toledo",
            "dante",
            "museo",
            "materdei",
            "vanvitelli",
            "augusteo",
            "fuga",
            "mergellina",
            "manzoni",
        }

    def _station_is_valid(self, station):
        return station in self.VALID_STATIONS

    def _trip_price(self, trips_done_so_far):
        if trips_done_so_far <= 3:
            return 2
        if trips_done_so_far <= 5:
            return 1
        return 0

    def _check_token_len(self, tokens, expected_len):
        if len(tokens) != expected_len:
            self.output.append(self.INV_COMMAND)
            return False
        return True

    def tapin(self, tokens):
        if not self._check_token_len(tokens, 3):
            return

        card, station = tokens[1], tokens[2]

        if not self._station_is_valid(station):
            self.output.append(self.INV_STATION)
            return

        if card in self.inside:
            self.output.append("ERROR already in")
            return

        self.inside.add(card)
        self.regular_counts[station][card] += 1
        self.output.append("OK")

    def tapout(self, tokens):
        if not self._check_token_len(tokens, 3):
            return

        card, station = tokens[1], tokens[2]

        if not self._station_is_valid(station):
            self.output.append(self.INV_STATION)
            return

        if card not in self.inside:
            self.output.append("ERROR not in")
            return

        self.inside.remove(card)
        self.trip_counts[card] += 1
        price = self._trip_price(self.trip_counts[card])
        self.fare_totals[card] += price
        self.regular_counts[station][card] += 1
        self.output.append(str(price))

    def pendings(self, tokens):
        if not self._check_token_len(tokens, 1):
            return

        if not self.inside:
            self.output.append("none")
            return

        self.output.append(" ".join(sorted(self.inside)))

    def fare(self, tokens):
        if not self._check_token_len(tokens, 2):
            return

        card = tokens[1]
        self.output.append(str(self.fare_totals.get(card, 0)))

    def regulars(self, tokens):
        if not self._check_token_len(tokens, 2):
            return

        station = tokens[1]
        if not self._station_is_valid(station):
            self.output.append(self.INV_STATION)
            return

        entries = self.regular_counts.get(station, {})
        if not entries:
            self.output.append("none")
            return

        ordered = sorted(entries.items(), key=lambda pair: (-pair[1], pair[0]))
        self.output.append(" ".join(f"{card}:{count}" for card, count in ordered))

    def dispatch(self, tokens):
        self.output = []
        if not tokens:
            return

        cmd = tokens[0]

        if not cmd.isupper() or cmd not in self.VALID_COMMANDS:
            self.output.append(self.INV_COMMAND)
            return

        if cmd == "TAPIN":
            self.tapin(tokens)
        elif cmd == "TAPOUT":
            self.tapout(tokens)
        elif cmd in {"PENDING", "PENDINGS"}:
            self.pendings(tokens)
        elif cmd == "FARE":
            self.fare(tokens)
        elif cmd == "REGULARS":
            self.regulars(tokens)
        else:
            self.output.append(self.INV_COMMAND)


if __name__ == "__main__":
    metro = Metro()
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        metro.dispatch(line.split())
        if metro.output:
            print(metro.output[0])
