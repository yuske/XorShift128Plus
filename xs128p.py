import math
from z3 import *

from ChromeRandomnessPredictor import ChromeRandomnessPredictor
from FirefoxAndSafariRandomnessPredictor import FirefoxAndSafariRandomnessPredictor


# Print 'last seen' random number
#   and winning numbers following that.
# This was for debugging. We know that Math.random()
#   is called in the browser zero times (updated) for each page click
#   in Chrome and once for each page click in Firefox.
#   Since we have to click once to enter the numbers
#   and once for Play, we indicate the winning numbers
#   with an arrow.
def power_ball(browser, generated, skip=4):
    # for each random number (skip 4 of 5 that we generated)
    for idx in range(len(generated[skip:])):
        # powerball range is 1 to 69
        poss = list(range(1, 70))
        # base index 4 to skip
        gen = generated[skip + idx :]
        # get 'last seen' number
        g0 = gen[0]
        gen = gen[1:]
        # make sure we have enough numbers
        if len(gen) < 6:
            break
        print(g0)

        # generate 5 winning numbers
        nums = []
        for jdx in range(5):
            index = int(gen[jdx] * len(poss))
            val = poss[index]
            poss = poss[:index] + poss[index + 1 :]
            nums.append(val)

        # print indicator
        if idx == 0 and browser == "chrome":
            print("--->", end="")
        elif idx == 2 and browser == "firefox":
            print("--->", end="")
        else:
            print("    ", end="")
        # print winning numbers
        print(sorted(nums), end="")

        # generate / print power number or w/e it's called
        double = gen[skip + 1]
        val = int(math.floor(double * 26) + 1)
        print(val)


def main():
    browser = "chrome"  # | 'safari' | 'firefox'
    print("BROWSER: %s" % browser)

    # In your browser's JavaScript console:
    #  - For Chrome/Firefox : `Array.from({ length: 5 }, Math.random);`
    #  - For Safari : `JSON.stringify(Array.from({ length: 5 }, Math.random), null, 2);`
    # Enter at least the 5 first random numbers you observed here:
    # Observations show all browsers need ~5
    sequence = [
        0.5368584449767335,
        0.883588766746984,
        0.7895949638905317,
        0.5106241305628436,
        0.49965622623126693,
    ]

    print(sequence)
    # Add original created random numbers to generated (copy the list)
    generated = sequence[:]

    RANDOM_NUMBERS_TO_GENERATE = 10

    if browser == "chrome":
        predictor = ChromeRandomnessPredictor(sequence)
    elif browser == "firefox" or browser == "safari":
        predictor = FirefoxAndSafariRandomnessPredictor(sequence)
    else:
        raise Exception(f"unknown browser {browser}")

    for _ in range(RANDOM_NUMBERS_TO_GENERATE):
        next = predictor.predict_next()
        generated.append(next)
    # use generated numbers to predict powerball numbers
    power_ball(browser=browser, generated=generated, skip=len(sequence))


main()
