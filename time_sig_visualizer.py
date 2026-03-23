from time import sleep
from ast import literal_eval as leval
def eval_time_sigs(text: str) -> list[str]:
    """
    Expand shorthand musical time signature notation into an explicit list of signatures.

    The input string may contain tokens in the following forms:
    - 'X/Y' : a single time signature, appended once.
    - 'n*X/Y' : repeat the time signature X/Y n times.
    - '[a, b, ...]/Y' : expand the list [a, b, ...] into individual signatures a/Y, b/Y, ...
    - 'n*[a, b, ...]/Y' : expand the list [a, b, ...] into individual signatures a/Y, b/Y, ...
      and repeat the entire sequence n times.
    - Separate each token by a space.

    Parameters
    ----------
    text : str
        A whitespace-separated string of shorthand time signature expressions.
    
    Notes
    -----
    - Obviously, multiplying a time signature by 0 is valid, but adds nothing to the list.
    - Making the numerator 0 is valid and makes the visualize_time_sig() function just print an empty line.
    - No list denominators, because who in the right mind would do that?
    - The function corrects errors in spacing (e.g. 13 * [12, 11] / 8 -> 13*[12,11]/8)

    Returns
    -------
    List[str]
        A list of expanded time signatures in 'numerator/denominator' format.
    
    Raises
    ------
    ValueError
        - If the repetition number is invalid (not an integer or negative).
        - If the denominator is an integer and less than 0.
        - If the denominator is a list and contains non-integers or values less than 0.
        - If the denominator is neither an integer nor a list.
        - If the numerator is less than 1.
        - If the numerator is not an integer.

    Examples
    --------
    >>> eval_time_sigs('3*9/4 2*[12,11]/8 5/4')
    ['9/4', '9/4', '9/4', '12/8', '11/8', '12/8', '11/8', '5/4']
    >>> eval_time_sigs('-2*5/4')
    Traceback (most recent call last):
      File "<python-input-5>", line 1, in <module>
        eval_time_sigs('-2*5/4')
        ~~~~~~~~~~~~~~^^^^^^^^^^
      File "<python-input-3>", line 68, in eval_time_sigs
        raise ValueError(f'Invalid repetition number: {rep}')
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ValueError: Invalid repetition number: -2
    """
    time_sigs = []
    text = text.replace(', ',',').replace(' * ','*').replace(' / ','/').split() # Replacing stuff to avoid error in splitting
    for i in text:
        i = i.split('*')
        length = len(i)
        fraction = i[length - 1].split('/')
        
        # Some validating
        if len(fraction) != 2:
            raise ValueError(f'Invalid time signature: {fraction}')  
        
        evrep = 1 # Failsafe if evrep is actually checked to be defined in line 83, 85 and 87 in future Python updates
        if length==2:
            rep = i[0]
            evrep = leval(rep)
        numer, denom = fraction
        evnumer = leval(numer)
        evdenom = leval(denom)
        
        # Mass validating
        if length == 2:
            if not isinstance(evrep, int):
                raise ValueError(f'Invalid repetition number: {rep}')
            if evrep < 0:
                raise ValueError(f'Invalid repetition number: {rep}')
        if isinstance(evnumer, list):
            if not all(isinstance(x, int) for x in evnumer):
                raise ValueError(f'Invalid numerator list: {evnumer}')
        elif not isinstance(evnumer, int):
            raise ValueError(f'Invalid numerator: {evnumer}')
        elif evnumer <= 0:
            raise ValueError(f'Invalid numerator: {evnumer}')
        if not isinstance(evdenom, int):
            raise ValueError(f'Invalid denominator: {evdenom}') 
        if denom <= -1:
            raise ValueError(f'Invalid denominator: {evdenom}')
        
        # Normal case: just 2 numbers between slashes
        if not isinstance(evnumer, list):
            time_sigs += [f'{evnumer}/{evdenom}'] * (evrep if length == 2 else 1)
        # Abnormal case: the numerinator is a list
        else:
            time_sigs+=[f'{i}/{denom}' for i in evnumer] * (evrep if length == 2 else 1)
    return time_sigs

def visualize_time_sigs(bpm: float, time_sigs: list):
    """
    Visualize time signatures at a given tempo by printing beats in sequence.

    Each time signature is expressed as 'numerator/denominator'. The function
    prints beat numbers for each measure, pausing according to the tempo.

    Parameters
    ----------
    bpm : float
        Beats per minute (tempo). Must be greater than 0.
    time_sigs : list of str
        A list of time signatures in 'numerator/denominator' format.

    Notes
    -----
    - Uses time.sleep() for beat timing, which may introduce slight drift over time.
    - A numerator of 0 results in an empty line.
    - Denominators are assumed to be positive integers.
    - This function is intended : for simple console visualization, not precise musical notation; 
    to be paired with eval_time_sigs() in the second argument.
    - This function actually just prints stuff and not returning anything.
    Raises
    ------
    ValueError
        - If bpm is less than or equal to 0.
        - If a time signature cannot be parsed into integers.
        - If denominator is less than or equal to 0.
        - If numerator is negative.

    Examples
    --------
    >>> visualize_time_sig(120, ['3/4', '5/4'])
    1 2 3
    1 2 3 4 5

    >>> visualize_time_sig(90, ['0/4'])
    # prints an empty line
    """
    # Validate bpm
    if bpm <= 0:
        raise ValueError(f"Invalid bpm: {bpm}. Must be greater than 0.")

    quarter_note_length = 60 / bpm

    for time_sig in time_sigs:
        try:
            rep, denom = map(int, time_sig.split('/'))
        except Exception:
            raise ValueError(f"Invalid time signature format: {time_sig}")

        if rep < 0:
            raise ValueError(f"Invalid numerator (beats per measure): {rep}")
        if denom <= 0:
            raise ValueError(f"Invalid denominator: {denom}. Must be > 0.")

        beat_length = quarter_note_length * (4 / denom)

        # Print beats
        for beat in range(1, rep + 1):
            print(beat, end=' ', flush=True)
            sleep(beat_length)
        print()
