#
#
#
#another commitasdfasdfasdfsdvdvasasdfasdfdfasdfasdfasdfasdf
#another commitasdflkjaölsdflkjaslödasdfasdfjflkjasdölkfjlökajsdf
from psynet.page import \
    InfoPage, \
    SuccessfulEndPage
import psynet.experiment
from psynet.timeline import \
    PageMaker, \
    Timeline, \
    Module,\
    CodeBlock, \
    conditional, \
    while_loop
from psynet.consent import MainConsent, AudiovisualConsent, NoConsent
from psynet.modular_page import \
    ModularPage, \
    AudioPrompt, \
    PushButtonControl, \
    TextControl, \
    Prompt
from psynet.js_synth import Chord, InstrumentTimbre, JSSynth, Note, Rest, ShepardTimbre
from dominate import tags
from psynet.utils import get_logger
import random
major_arpeggio = ModularPage(
    "major_js_synth",
    JSSynth(
        "Here we go! That is your major arpeggio!",
        [
            Note(60, pan=1),
            Note(59, pan=-1),
            Note(57, pan=1),
            Note(55, pan=-1),
            Note(53, pan=1),
            Note(52, pan=1),
            Note(50, pan=1),
            Note(48, pan=(-1,0,1)),
            Chord([50, 53, 57]),
        ],
    ),
    time_estimate=5,
)

# major_arpeggio = ModularPage(
#     "major_js_synth",
#     JSSynth(
#         "Here we go! That is your major arpeggio!",
#         [
#             Note(60),
#             Note(59),
#             Note(57),
#             Note(55),
#             Note(53),
#             Note(52),
#             Note(50),
#             Note(48),
#             Chord([50, 53, 57]),
#         ],
#         timbre=InstrumentTimbre("piano"),
#         default_duration=0.5,
#     ),
#     time_estimate=5,
# )


minor_arpeggio = ModularPage(
    "minor_js_synth",
    JSSynth(
        "Here we go! That is your minor arpeggioasdfasdfasdf!",
        [
            Note(60, pan=1),
            Note(58, pan=-1),
            Note(56, pan=1),
            Note(55, pan=-1),
            Note(53, pan=1),
            Note(51, pan=-1),
            Note(50, pan=1),
            Note(48, pan=(-1,0,1), duration=1),
            Chord([50, 53, 57]),
        ],
    ),
    time_estimate=5,
)

either_major_minor = Module(
            "mi_ma_arpeggio",
            ModularPage(
                "mood",
                Prompt("Would you like to hear a major or minor scale or something else?"),
                control=PushButtonControl(["Minor","Major"]),
                time_estimate=5,
            ),
            conditional(
                "like_mi_ma",
                lambda participant: participant.answer== "Minor",
                minor_arpeggio,
                major_arpeggio,
                fix_time_credit=False,
            ),
        )

play_random_sequence = ModularPage(
    "rand_tones",
    JSSynth(
        "Here we go! That is your major arpeggio!",
        random.choices([
            Note(60),
            Note(59),
            Note(57),
            Note(55),
            Note(53),
            Note(52),
            Note(50),
            Note(48),
        ],k=20),
        timbre=InstrumentTimbre("piano"),
        default_duration=0.5,
    ),
    time_estimate=5,
)
rating_sequ = Module(
    "rat_sequ",
    ModularPage(
        "sequence_to_be_rated",
        JSSynth(
            "How would you rate the melody that you hear?",
            random.choices([
                Note(60),
                Note(59),
                Note(57),
                Note(55),
                Note(53),
                Note(52),
                Note(50),
                Note(48),
            ],k=20),
        timbre=InstrumentTimbre("piano"),
        default_duration=0.1,
        ),
        PushButtonControl(
            choices=[1, 2, 3, 4, 5],
            labels=["dislike", "a little unpleasant", "somewhat pleasant", "pleasant", "perfect"],
            arrange_vertically=False,
        ),
    time_estimate=5,
    ),
)




class Exp(psynet.experiment.Experiment):
    label = "choose_mi_ma",
    timeline = Timeline(
        NoConsent(),
        CodeBlock(lambda participant: participant.set_answer("Yes")),
        while_loop(
            "rating",
            lambda participant: participant.answer == "Yes",
            Module(
                "loop",
                ModularPage(
                    "loopp",
                    Prompt("Would you like to rate an other melody"),
                    control=PushButtonControl(["YES","NO"],arrange_vertically=False),
                    time_estimate=5,
                ),
                rating_sequ,
            ),
            expected_repetitions =2,
            fix_time_credit= True,
        ),
        SuccessfulEndPage(),
    )
