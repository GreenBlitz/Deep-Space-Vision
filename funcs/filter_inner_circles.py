def circle_collision(center1, r1, center2, r2):
    return (center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2 < (r1 + r2) ** 2


def filter_inner_circles(circles):
    filtered_circles = []
    for i, circle in enumerate(circles):
        circle_invalid = False
        for j in range(i):
            circle_invalid = circle_collision(circle[0], circle[1], circles[j][0], circles[j][1])
            if circle_invalid:
                break
        if not circle_invalid:
            filtered_circles.append(circle)

    return filtered_circles
