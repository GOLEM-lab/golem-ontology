from pathlib import Path
from copy import deepcopy
from core.loader import build_world, inject_axiom
from core.reasoner import check_coherence, check_coherence_silent
from core.reporter import persist_axiom, failed_axiom
from core.state import save_world, load_world


# def run_phase(
#     phase_name: str,
#     base_state: Path,
#     output_state: Path,
#     stack: list[str],
#     candidates: list[tuple[str, str]],
#     alignment_file: Path,
#     failed_file: Path,
# ):

#     print(f"\n=== {phase_name} ===")

#     if base_state.exists():
#         from core.state import load_world
#         base_world = load_world(base_state)
#     else:
#         base_world = build_world(stack)

#     accepted = []

#     for i, (label, snippet) in enumerate(candidates):

#         print(f"Testing [{i}]: {label}")

#         # rebuild fresh test world
#         if base_state.exists():
#             test_world = load_world(base_state)
#         else:
#             test_world = build_world(stack)

#         # replay accepted axioms
#         for _, accepted_snippet in accepted:
#             inject_axiom(test_world, accepted_snippet)

#         # add candidate
#         inject_axiom(test_world, snippet)

#         # check coherence ONCE
#         unsat = check_coherence_silent(test_world)

#         # decision boundary INSIDE loop
#         if not unsat:
#             print(f"✔ ACCEPTED!")
#             persist_axiom(alignment_file, snippet)

#             accepted.append((label, snippet))

#         else:
#             print(f"✘ REJECTED!")
#             failed_axiom(failed_file, label, snippet, unsat)
#             #break

#     #save_world(test_world, output_state)
#     save_world(
#     test_world,
#     output_state,
#     stack_iris=stack,
#     state_iri=f"https://w3id.org/golem/validation/state/{output_state.stem}"
# )

#     print(f"Saved state → {output_state}")
#     return test_world, accepted



def run_phase(
    phase_name: str,
    base_state: Path,
    output_state: Path,
    stack: list[str],
    candidates: list[tuple[str, str]],
    alignment_file: Path,
    failed_file: Path,
):
    print(f"\n=== {phase_name} ===")

    accepted = []

    for i, (label, snippet) in enumerate(candidates):
        print(f"Testing [{i}]: {label}")

        # rebuild fresh test world from base state or stack
        if base_state.exists():
            test_world = load_world(base_state)
        else:
            test_world = build_world(stack)

        # replay all accepted axioms so far
        for _, accepted_snippet in accepted:
            inject_axiom(test_world, accepted_snippet)

        # inject candidate
        inject_axiom(test_world, snippet)

        # check coherence
        unsat = check_coherence_silent(test_world)

        if not unsat:
            print(f"  ✔ ACCEPTED: {label}")
            persist_axiom(alignment_file, snippet)
            accepted.append((label, snippet))
        else:
            print(f"  ✘ REJECTED: {label}")
            failed_axiom(failed_file, label, snippet, unsat)

    # rebuild final state from accepted axioms only — never from test_world
    if base_state.exists():
        final_world = load_world(base_state)
    else:
        final_world = build_world(stack)

    for _, accepted_snippet in accepted:
        inject_axiom(final_world, accepted_snippet)

    save_world(final_world, output_state, stack_iris=stack)
    print(f"\nSaved state → {output_state}")
    print(f"Accepted: {len(accepted)} / {len(candidates)}")

    return final_world, accepted