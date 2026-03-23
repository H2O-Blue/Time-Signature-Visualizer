# Time Signature Visualizer
Python utility to expand shorthand musical time signatures and visualize them at a given tempo.

## Overview

This project provides two main functions:

- **`eval_time_sigs(text: str) -> List[str]`**  
  Expands shorthand musical time signature notation into explicit lists of signatures.

- **`visualize_time_sig(bpm: float, time_sigs: List[str]) -> None`**  
  Prints beat sequences for given time signatures at a specified tempo.

Together, they allow you to parse compact rhythm notation and simulate beats in real time.

## Features

- Expand shorthand notation like `3*9/4` or `13*[12,11]/8` into full sequences.  
- Handle repeats, lists, and spacing corrections automatically.  
- Visualize beats at a chosen tempo (BPM) with console output.  
- Input validation with clear error messages.  

## Installation

Clone the repository:

```
git clone https://github.com/your-username/time-signature-visualizer.git
cd time-signature-visualizer
```

No external dependencies are required beyond Python 3.

## Usage

### Expand time signatures

```python
from your_module import eval_time_sigs

print(eval_time_sigs("3*9/4 2*[12,11]/8 5/4"))
# Output: ['9/4', '9/4', '9/4', '12/8', '11/8', '12/8', '11/8', '5/4']
```

### Visualize beats

```python
from your_module import visualize_time_sig

visualize_time_sig(120, ["3/4", "5/4"])
# Output:
# 1 2 3
# 1 2 3 4 5
```

## Notes

- `time.sleep()` is used for beat timing, which may introduce slight drift over time.  
- A numerator of `0` results in an empty line.  
- Denominators must be positive integers.  
- This current version of the code doesn't support list denominators, because who in their right mind would do that?
## License

This project is licensed under the MIT License – see the LICENSE file for details.
