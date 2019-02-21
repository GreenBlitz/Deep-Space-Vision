def rect_collision(r1, r2):
    return not (r1[0] > r2[0] + r2[2] or
                r1[0] + r1[2] < r1[0] or
                r1[1] > r2[1] + r2[3] or
                r1[1] + r1[3] > r2[1])


def filter_inner_rects(rects):
    filtered_rects = []
    for i, rect in enumerate(rects):
        rect_invalid = False
        for j in range(i):
            rect_invalid = rect_collision(rect, rects[j])
            if rect_invalid:
                break
        if not rect_invalid:
            filtered_rects.append(rect)
    return filtered_rects
