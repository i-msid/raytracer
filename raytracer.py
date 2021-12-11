from PIL import Image
import math

# we first need a vector class to represent points on a 3-D plane
# class will support basic functions like multiply magnitute, dot product
class Vec3D:
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, v):
		return Vec3D(self.x + v.x, self.y + v.y, self.z + v.z)
	def __mul__(self, scalar):
		return Vec3D(self.x * scalar, self.y * scalar, self.z * scalar)
	def __sub__(self, v):
		return Vec3D(self.x - v.x, self.y - v.y, self.z - v.z)
	def magnitude(self):
		return math.sqrt(self.x * self.x + self.y * self.y + self.z *self.z)
	def normalize(self):
		len = self.magnitude()
		return Vec3D(self.x/len, self.y/len, self.z/len)
	def negative(self):
		return Vec3D(-self.x, -self.y, -self.z)
	def dot_product(self, other):
		return self.x * other.x + self.y * other.y + self.z * other.z
	def cross_product(self, other):
		return Vec3D(self.y * other.z - self.z * other.y,
					 self.z * other.x - self.x * other.z,
					 self.x * other.y - self.y * other.x)


class Triangle(Vec3D):
    def __init__(self, a=Vec3D(1, 0, 0), b=Vec3D(0, 1, 0), c=Vec3D(0, 0, 1)):
        self.a = a
        self.b = b
        self.c = c

        ca = self.c - self.a
        ba = self.b - self.a
        self.normal = ca.cross_product(ba).normalize()
        self.distance = self.normal.dot_product(self.a)

    def intersect(self, origin, Direction):
        dot = Direction.dot_product(self.normal)
        if dot == 0:
            return -1
        else:
            dummy = self.normal.dot_product(origin + (self.normal * self.distance).negative())
            dist_to_triangle = -1 * dummy / dot
            q = Direction * dist_to_triangle + origin
            ca = self.c - self.a
            qa = q - self.a
            bc = self.b - self.c
            qc = q - self.c
            ab = self.a - self.b
            qb = q - self.b
            inside = ca.cross_product(qa).dot_product(self.normal) >= 0 and \
                     bc.cross_product(qc).dot_product(self.normal) >= 0 and \
                     ab.cross_product(qb).dot_product(self.normal) >= 0
            if inside:
                return True
            else:
                return False


# function takes normal ray and incedent ray and returns the reflected ray
def reflect(I, N):
	reflected_ray = I - 2*((I.dot_product(N))*N)
	return reflected_ray.normalize()

if __name__ == "__main__":
	width = 640
	height = 480
	fov = 51.52 #feeling fancy
	scale = math.tan(fov*0.5*(math.pi/180.0))
	imageAspectRatio = float(width) / float(height)
	origin = Vec3D(0,0,0)
	image = Image.new("RGB", (width, height))
	triangle1 = Triangle(Vec3D(-1, -1, -5), Vec3D( 1, -1, -5), Vec3D( 0,  1, -5))
	scene_objs = [triangle1]
	for j in range(0, height):
		for i in range(0, width):
			x = ((2*(i+0.5)/float(width))-1) * imageAspectRatio * scale
			y = (1 - 2*(j+0.5)/float(height))* scale
			dir = Vec3D(x, y, -1)
			dir.normalize()
			p_r = 0
			p_g = 0
			p_b = 0
			for object in range(0, len(scene_objs)):
				if(scene_objs[object].intersect(origin, dir)):
					p_r = 255
					P_g = 165
					p_b = 0
			image.putpixel((i,height - j - 1), (p_r, p_g, p_b))
	image.save("rt1.png")