import json


def parse(data_raw):

    return json.loads(data_raw)


class Colors:
    """
    Basic information about the provided colors.
    """
    def __init__(self, colorteller) -> None:

        if not isinstance(colorteller, list):
            raise TypeError(f"colorteller has to be a list of dictionaries; {colorteller}")
        self.colorteller = colorteller

    @property
    def colors(self):
        return self._colorteller_to_colors(self.colorteller)

    @staticmethod
    def _colorteller_to_colors(colorteller):
        raise NotImplementedError("not implemented")

    def metrics(self, colors):
        self.metrics = {
            "name_difference": self._name_difference(colors),
            "perceptual_distance": self._perceptual_distance(colors),
            "pair_preference": self._pair_preference(colors)
        }

    @staticmethod
    def _name_difference(colors):
        raise NotImplementedError(f"_name_difference has not yet been implamented.")

    @staticmethod
    def _perceptual_distance(colors):
        raise NotImplementedError(f"_perceptual_distance has not yet been implamented.")

    @staticmethod
    def _pair_preference(colors):
        raise NotImplementedError(f"_pair_preference has not yet been implamented.")

    @staticmethod
    def _name_uniqueness(colors):
        raise NotImplementedError(f"_name_uniqueness has not yet been implamented.")



class ColorsBenchmark:
    """
    Create charts to benchmark the color palettes.
    """
    def __init__(self) -> None:
        pass

    def save(self):
        pass




if __name__ == "__main__":

    data_raw = '[{"author":"KausalFlow","colors":[{"hex":"#8de4d3","name":""},{"hex":"#344b46"},{"hex":"#74ee65"},{"hex":"#238910"},{"hex":"#a6c363"},{"hex":"#509d99"}],"date":1637142696,"expirydate":-62135596800,"file":"bobcat-yellow","hex":["8de4d3","344b46","74ee65","238910","a6c363","509d99"],"images":null,"objectID":"e0e129c8ed58316127909db84c67efcb","permalink":"//localhost:1234/colors/bobcat-yellow/","publishdate":"2021-11-17T10:51:36+01:00","summary":"This is an experiment","tags":null,"title":"Bobcat Yellow"}]'

    data = parse(data_raw)

    print(data)

    print(list(data[0].keys()))

    print(data[0]["hex"])
