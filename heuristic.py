"""HeuDiConv heuristic for the fMRI Course JLU 2026 dataset."""

import re


def create_key(template, outtype=("nii.gz",), annotation_classes=None):
    if not template:
        raise ValueError("Template must be a valid format string")
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    t1w = create_key("sub-{subject}/anat/sub-{subject}_T1w")
    bold = create_key(
        "sub-{subject}/func/sub-{subject}_task-main_run-{item:02d}_bold"
    )
    fmap_mag = create_key("sub-{subject}/fmap/sub-{subject}_magnitude")
    fmap_phase = create_key("sub-{subject}/fmap/sub-{subject}_phasediff")

    info = {t1w: [], bold: [], fmap_mag: [], fmap_phase: []}
    bold_series = []

    for s in seqinfo:
        proto = (s.protocol_name or "").lower()
        image_type = tuple(str(x).upper() for x in (s.image_type or ()))

        # Skip localizers and scanner reports.
        if "aahead_scout" in proto or "phoenix" in proto:
            continue

        # Anatomical T1w.
        if "mprage" in proto:
            info[t1w].append(s.series_id)
            continue

        # Task BOLD (ep2d_bold_<N>_...). Sort by the numeric index embedded
        # in the protocol name so run-01..run-06 follow acquisition order.
        m = re.match(r"ep2d_bold_(\d+)", proto)
        if m:
            bold_series.append((int(m.group(1)), s.series_id))
            continue

        # Siemens gre_field_mapping: magnitude (image_type contains "M")
        # vs phase-difference (image_type contains "P").
        if "gre_field_mapping" in proto or "field_map" in proto:
            if "P" in image_type:
                info[fmap_phase].append(s.series_id)
            else:
                info[fmap_mag].append(s.series_id)
            continue

    for _, sid in sorted(bold_series):
        info[bold].append(sid)

    return info
