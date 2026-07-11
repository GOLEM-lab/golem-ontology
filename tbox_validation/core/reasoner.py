import os
import owlready2
from owlready2 import sync_reasoner_hermit, OwlReadyInconsistentOntologyError
from contextlib import redirect_stdout, redirect_stderr



def check_consistency(world: owlready2.World) -> bool:
    try:
        with world:
            sync_reasoner_hermit(world, infer_property_values=True)
        return True
    except OwlReadyInconsistentOntologyError:
        return False


def check_coherence(world: owlready2.World) -> list[str]:
    """
    Run HermiT over the full world. Returns IRIs of all unsatisfiable
    named classes. Empty list means coherent.
    """
    try:
        with world:
            sync_reasoner_hermit(world, infer_property_values=True)
    except OwlReadyInconsistentOntologyError:
        return ["INCONSISTENT: ontology is outright inconsistent"]

    unsatisfiable = [
        cls.iri
        for cls in world.classes()
        if owlready2.Nothing in cls.ancestors()
        and cls is not owlready2.Nothing
    ]
    return unsatisfiable




def check_coherence_silent(world):
    """
    Run reasoner without producing Owlready/HermiT logs.
    """
    with open(os.devnull, "w") as fnull:
        with redirect_stdout(fnull), redirect_stderr(fnull):
            return check_coherence(world)    