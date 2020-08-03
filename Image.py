import cv2


# 이미지 클래스
def get_image(path):
    chars = ' .,-~:;=!*#$@'
    nw = 60

    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = img.shape
    nh = int(h / w * nw)

    img = cv2.resize(img, (nw * 2, nh))
    out_count = 0
    in_count = 0

    data = [[0 for col in range(120)] for row in range(len(img))]

    for row in img:
        for pixel in row:
            index = int(pixel / 256 * len(chars))
            data[out_count][in_count] = chars[index]
            in_count += 1

        in_count = 0
        out_count += 1

    return data

