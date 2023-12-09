""" Advent of Code 2023 Day 05 """
from typing import List, Callable

from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="AOC2023",
))

WORKING_DIR = '2023/Day09/'

class History:
    """ A history of readings (or deltas between readings) and postdict/predict methods """
    def __init__(self, history: List[int]):
        self.history = history

    def render_prediction(self,
                          history: List[int],
                          prediction: int,
                          log_func: Callable=logger.info) -> None:
        """ Render the prediction """
        spacing = len(max([str(h) for h in self.history], key=len)) + 1
        front_spacing = round(spacing / 2)
        history_string = f"{' ' * front_spacing * (len(self.history) - len(history))}"
        history_string += "".join([f"{h:{spacing}}" for h in history])
        history_string += f"{prediction:{spacing}}"
        log_func(history_string)

    def render_postdictions(self,
                            history: List[int],
                            postdiction: int,
                            log_func: Callable=logger.info) -> None:
        """ Render the postdiction """
        spacing = len(max([str(h) for h in self.history], key=len)) + 1
        front_spacing = round(spacing / 2)
        history_string = f"{' ' * front_spacing * (len(self.history) - len(history))}"
        history_string += f"{postdiction:{spacing}}"
        history_string += "".join([f"{h:{spacing}}" for h in history])
        log_func(history_string)

    def get_postdiction(self, history=None) -> int:
        """ Get the next postdiction from a history """
        history = history or self.history
        if all ([reading == 0 for reading in history]):
            self.render_postdictions(history=history, postdiction=0)
            return 0

        deltas = [history[i] - history[i-1] for i in range(1, len(history))]
        postdiction: int = history[0] - self.get_postdiction(deltas)
        self.render_postdictions(history=history, postdiction=postdiction)
        if self.history == history:
            logger.debug(f"Postdiction: {postdiction}")
        return postdiction

    def get_prediction(self, history=None) -> int:
        """ Get the next prediction from a history """
        history = history or self.history
        if all ([reading == 0 for reading in history]):
            self.render_prediction(history=history, prediction=0)
            return 0

        deltas = [history[i] - history[i-1] for i in range(1, len(history))]
        prediction: int = self.get_prediction(deltas) + history[-1]
        self.render_prediction(history=history, prediction=prediction)
        if self.history == history:
            logger.debug(f"Prediction: {prediction}")
        return prediction


class OASIS:
    """ Oasis And Sand Stability Sensor """
    def __init__(self, filename: str):
        self.filename = filename
        self.histories: List[History] = []
        self.parse()

    def parse(self) -> None:
        """ Parse the input file """
        with open(self.filename, 'r', encoding="utf-8") as file:
            for line in file:
                self.histories.append(History([int(reading) for reading in line.split()]))

    def get_predictions(self) -> List[int]:
        """ Get the a list of all predictions """
        return [h.get_prediction() for h in self.histories]

    def get_postdictions(self) -> List[int]:
        """ Get the a list of all postdictions """
        return [h.get_postdiction() for h in self.histories]

def test_sanity():
    """Sanity check """
    assert True

def test_get_prediction():
    """ Test get_prediction """
    logger.info("")
    history = History([0, 3, 6, 9, 12, 15])
    assert history.get_prediction() == 18

    history = History([9, 15, 18, 18, 15, 9])
    prediction = history.get_prediction()
    assert prediction == 0

def test_get_postdiction():
    """ Test get_postdiction """
    logger.info("")
    history = History([10,  13,  16,  21,  30,  45])
    postdiction = history.get_postdiction()
    assert postdiction == 5


def test_sample_1():
    """ Test Sample 1"""
    logger.info("")
    oasis = OASIS(filename=WORKING_DIR + 'input_sample.txt')
    predictions = oasis.get_predictions()
    logger.info(sum(predictions))
    assert sum(predictions) == 114


def test_part_1():
    """Test part 1"""
    logger.info("")
    oasis = OASIS(filename=WORKING_DIR + 'input.txt')
    predictions = oasis.get_predictions()
    logger.info(sum(predictions))
    assert sum(predictions) == 1953784198


def test_sample_2():
    """Test part 2"""
    logger.info("")
    oasis = OASIS(filename=WORKING_DIR + 'input_sample.txt')
    predictions = oasis.get_postdictions()
    logger.info(sum(predictions))
    assert sum(predictions) == 2


def test_part_2():
    """Test part 2"""
    logger.info("")
    oasis = OASIS(filename=WORKING_DIR + 'input.txt')
    predictions = oasis.get_postdictions()
    logger.info(sum(predictions))
