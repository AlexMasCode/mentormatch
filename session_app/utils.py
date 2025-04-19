from datetime import datetime
def subtract_intervals(avail, busy):
    """
    Subtract busy intervals from availability intervals.
    avail & busy: lists of (start: datetime, end: datetime).
    Returns list of free intervals.
    """
    free = []
    for a_start, a_end in sorted(avail):
        current_start = a_start
        for b_start, b_end in sorted(busy):
            if b_end <= current_start or b_start >= a_end:
                continue
            if b_start > current_start:
                free.append((current_start, b_start))
            current_start = max(current_start, b_end)
            if current_start >= a_end:
                break
        if current_start < a_end:
            free.append((current_start, a_end))
    return free