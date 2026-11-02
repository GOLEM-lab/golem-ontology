## OWL 2 DL Validator

This script validates an OWL ontology against the **OWL 2 DL profile**, including its complete import closure.

It uses [ROBOT](https://robot.obolibrary.org/) to resolve ontology imports through their declared IRIs (HTTP/HTTPS), merge the ontology and its imports, and perform profile validation.

### Requirements
- Java
- ROBOT executable JAR (`tools/robot.jar`)

### Usage

From the repository root:

```bash
./scripts/owl2dl_validator/validate.sh <ontology.ttl>
```

Example:

```bash
./scripts/owl2dl_validator/validate.sh releases/v2-0/golem_v2-0.ttl
    
```

### Output

The script:
1. Resolves and merges the ontology import closure.
2. Validates the merged ontology against OWL 2 DL.
3. Prints the validation report and final `PASS` or `FAIL` result to the console.

Intermediate files are stored in temporary storage (by default `/dev/shm` on Linux) and automatically removed when execution terminates.

The Java heap allocation can be configured through the `ROBOT_MEMORY` environment variable (default: `4G`).