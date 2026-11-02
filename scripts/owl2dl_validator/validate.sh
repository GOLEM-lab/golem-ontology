
#!/usr/bin/env bash

# ============================================================
# GOLEM OWL 2 DL Validator
# ============================================================
#
# Merges an OWL ontology with its import closure, resolving
# imports through their ontology IRIs (HTTP/HTTPS), and
# validates the resulting ontology against the OWL 2 DL profile.
#
# Temporary files are stored in RAM-backed storage (/dev/shm)
# and automatically removed when the script terminates.
#
# Requirements:
#   - Java
#
# Usage:
#   ./scripts/owl2dl_validator/validate.sh <ontology.ttl>
#
# Example:
#   ./scripts/owl2dl_validator/validate.sh \
#       golem_dev/golem_source/golem_v2-0_dev_new_classes_owl2dl.ttl
#
# Optional environment variables:
#   ROBOT_MEMORY=4G
# ============================================================

set -Eeuo pipefail

# ------------------------------------------------------------
# Paths and configuration
# ------------------------------------------------------------

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/../.." && pwd)"

ROBOT_JAR="$SCRIPT_DIR/tools/robot.jar"

MEMORY="${ROBOT_MEMORY:-4G}"

# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------

error() {
    echo "ERROR: $*" >&2
    exit 1
}

# ------------------------------------------------------------
# Arguments
# ------------------------------------------------------------

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <ontology.ttl>" >&2
    exit 1
fi

SOURCE="$1"

[[ -f "$SOURCE" ]] \
    || error "Ontology source not found: $SOURCE"

[[ "${SOURCE,,}" == *.ttl ]] \
    || error "The input file must have a .ttl extension: $SOURCE"

# Resolve source to an absolute path.
SOURCE_DIR="$(cd -- "$(dirname -- "$SOURCE")" && pwd)"
SOURCE="$SOURCE_DIR/$(basename -- "$SOURCE")"

# ------------------------------------------------------------
# Dependency checks
# ------------------------------------------------------------

command -v java >/dev/null 2>&1 \
    || error "Java is required but was not found in PATH."

[[ -f "$ROBOT_JAR" ]] \
    || error "ROBOT executable not found: $ROBOT_JAR"

# ------------------------------------------------------------
# Temporary workspace (RAM-backed)
# ------------------------------------------------------------

TMP_BASE="${TMPDIR:-/dev/shm}"

[[ -d "$TMP_BASE" && -w "$TMP_BASE" ]] \
    || error "Temporary directory is not available or writable: $TMP_BASE"

TMP_DIR="$(mktemp -d "$TMP_BASE/golem-validator.XXXXXX")"
trap 'rm -rf "$TMP_DIR"' EXIT

CLOSURE="$TMP_DIR/golem-closure.owl"
PROFILE_REPORT="$TMP_DIR/profile-report.txt"

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

echo
echo "============================================================"
echo " GOLEM OWL 2 DL Profile Validator"
echo "============================================================"
echo
echo "Repository: $ROOT_DIR"
echo "Source:     $SOURCE"
echo "ROBOT:      $ROBOT_JAR"
echo "Memory:     $MEMORY"
echo "Temporary:  $TMP_BASE"
echo

# ------------------------------------------------------------
# Step 1: Merge ontology and import closure
# ------------------------------------------------------------

echo "[1/2] Merging ontology and resolving import closure via HTTP..."
echo

java "-Xmx${MEMORY}" -jar "$ROBOT_JAR" merge \
    --input "$SOURCE" \
    --collapse-import-closure true \
    --output "$CLOSURE" \
    || error "ROBOT failed to merge the ontology and its import closure."

[[ -s "$CLOSURE" ]] \
    || error "Merged ontology was not generated or is empty."

echo
echo "Merge completed successfully."
echo "Import closure generated in temporary storage."
echo

# ------------------------------------------------------------
# Step 2: Validate OWL 2 DL profile
# ------------------------------------------------------------

echo "[2/2] Validating OWL 2 DL profile..."
echo

VALIDATION_EXIT=0

java "-Xmx${MEMORY}" -jar "$ROBOT_JAR" validate-profile \
    --input "$CLOSURE" \
    --profile DL \
    --output "$PROFILE_REPORT" \
    || VALIDATION_EXIT=$?

# ------------------------------------------------------------
# Step 3: Display validation report
# ------------------------------------------------------------

echo
echo "============================================================"
echo " Validation report"
echo "============================================================"
echo

if [[ -s "$PROFILE_REPORT" ]]; then
    cat "$PROFILE_REPORT"
else
    echo "No validation report was generated."
fi

echo
echo "============================================================"

# ------------------------------------------------------------
# Step 4: Determine validation result
# ------------------------------------------------------------

if [[ "$VALIDATION_EXIT" -eq 0 ]] \
    && [[ -s "$PROFILE_REPORT" ]] \
    && grep -Fq "Ontology and imports closure in profile" "$PROFILE_REPORT"; then

    echo "RESULT: PASS"
    echo
    echo "The ontology and its import closure conform to OWL 2 DL."
    echo "============================================================"
    exit 0

else
    echo "RESULT: FAIL"
    echo
    echo "OWL 2 DL profile validation failed."
    echo "Inspect the validation report above for details."
    echo "============================================================"
    exit 1
fi
