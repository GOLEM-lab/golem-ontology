## OWL 2 DL Validator

This script validates an OWL ontology against the **OWL 2 DL profile**, including its complete import closure.

It uses [ROBOT](https://robot.obolibrary.org/) to resolve ontology imports through their declared IRIs (HTTP/HTTPS), merge the ontology with its imports, and perform profile validation.

### Requirements

- Java
- ROBOT executable JAR (downloaded separately, not included in the repository)

### Usage

From the repository root:

```bash
./scripts/owl2dl_validator/validate.sh <ontology.ttl> <robot.jar>
```

Example:

```bash
./scripts/owl2dl_validator/validate.sh \
    releases/v2-0/golem_v2-0.ttl \
    /path/to/robot.jar
```

### Output

The script:

1. Resolves and merges the ontology import closure.
2. Validates the merged ontology against the OWL 2 DL profile.
3. Prints the validation report and final `PASS` or `FAIL` result to the console.

Intermediate files are stored in temporary storage (by default, `/dev/shm` on Linux) and automatically removed when execution terminates.

The Java heap allocation can be configured through the `ROBOT_MEMORY` environment variable (default: `4G`).

### GitHub Actions

In the publication workflow, ROBOT is downloaded at runtime to the runner's temporary directory (`$RUNNER_TEMP`) and passed to the validation script. The JAR is not stored in the repository.