#!/bin/bash
OUTPUT_PATH=""
TEST_TYPE=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --output_path) OUTPUT_PATH="$2"; shift ;;
        base|new) TEST_TYPE="$1" ;;
    esac
    shift
done

if [[ -z "$OUTPUT_PATH" ]]; then
    echo "Usage: $0 --output_path <path> [base|new]"
    exit 1
fi

if [[ "$TEST_TYPE" == "base" ]]; then
    echo "def test_dummy(): pass" > tests/test_dummy.py
    pytest tests/test_dummy.py -v --junitxml="$OUTPUT_PATH"
    rm tests/test_dummy.py
elif [[ "$TEST_TYPE" == "new" ]]; then
    pytest tests/test_pinned_actions.py -v --junitxml="$OUTPUT_PATH"
else
    echo "Invalid test type: $TEST_TYPE"
    exit 1
fi
