from urllib.request import urlopen
from urllib.error import URLError
from PIL import Image
import turtle


def create_map_image(fi_center, la_center, scale_fi, scale_la):
    try:
        url_str = 'https://static-maps.yandex.ru/1.x/?ll={},{}&spn={},{}&l=sat'.format(
            la_center, fi_center, scale_la, scale_fi)
        result = urlopen(url_str)
        if result.status != 200:
            return None
    except URLError:
        return None

    data = result.read()

    try:
        image_file = open('map.png', "wb")
        image_file.write(data)
        image_file.close()
        im = Image.open('map.png')
        im.save('map.gif')
        return im.size
    except IOError:
        return None


def to_screen(fi, la, sz, fi_c, la_c, sc_fi, sc_la):
    begin_fi = fi_c - sc_fi
    end_fi = fi_c + sc_fi
    range_fi = end_fi - begin_fi
    rel_fi = (fi - fi_c) / range_fi
    y = rel_fi * sz[0]

    begin_la = la_c - sc_la
    end_la = la_c + sc_la
    range_la = end_la - begin_la
    rel_la = (la - la_c) / range_la
    x = rel_la * sz[1]

    return int(x), int(y)


route = [[55.694818, 37.670166],
         [55.738678, 37.654110],
         [55.743530, 37.590175],
         [55.752586, 37.540862],
         [55.773762, 37.490115],
         [55.796541, 37.486388],
         [55.804616, 37.542295],
         [55.804454, 37.599923]]


def calculate_route_box(points_geo):

    fi_min, la_min, fi_max, la_max = points_geo[0][0], points_geo[0][1], points_geo[0][0], points_geo[0][1]
    for pnt in points_geo:
        if pnt[0] < fi_min:
            fi_min = pnt[0]
        if pnt[0] > fi_max:
            fi_max = pnt[0]
        if pnt[1] < la_min:
            la_min = pnt[1]
        if pnt[1] > la_max:
            la_max = pnt[1]

    scale_fi = (fi_max-fi_min)
    scale_la = (la_max-la_min)
    center_fi = fi_min + scale_fi/2.
    center_la = la_min + scale_la/2.
    return center_fi, center_la, scale_fi, scale_la


fi_center_degree, la_center_degree, fi_scale_degree, la_scale_degree = calculate_route_box(route)
print(fi_center_degree, la_center_degree, fi_scale_degree, la_scale_degree)


def add_point(point_geo):
    x, y = to_screen(point_geo[0], point_geo[1], size,
                     fi_center_degree, la_center_degree, fi_scale_degree, la_scale_degree)
    turtle.setpos(x, y)
    print(x, y)


default_size = 640, 480
size = create_map_image(fi_center_degree, la_center_degree, fi_scale_degree, la_scale_degree)
if size:
    turtle.setup(size[0], size[1])
else:
    turtle.setup(default_size[0], default_size[1])

s = turtle.getscreen()
if size:
    s.bgpic('map.gif')
else:
    size = default_size

print("size = ", size)

turtle.penup()
add_point(route[0])
turtle.pendown()
for point in route[1:]:
    add_point(point)

s.mainloop()
