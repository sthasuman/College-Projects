### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
#
# Particle effect manager

import particles, gravity, obstacles, sys, pygame


DRAWTYPE_POINT = particles.DRAWTYPE_POINT
DRAWTYPE_CIRCLE = particles.DRAWTYPE_CIRCLE
DRAWTYPE_LINE = particles.DRAWTYPE_LINE
DRAWTYPE_SCALELINE = particles.DRAWTYPE_SCALELINE
DRAWTYPE_BUBBLE = particles.DRAWTYPE_BUBBLE
DRAWTYPE_IMAGE = particles.DRAWTYPE_IMAGE


class ParticleEffect:
	def __init__(self, display, pos, size):
		self.display = display
		self.pos = pos
		self.size = size
		
		self.left = pos[0]
		self.top = pos[1]
		self.right = pos[0] + size[0]
		self.bottom = pos[1] + size[1]
		
		self.particles = []
		self.sources = []
		self.gravities = []
		self.obstacles = []

	def Display(self,display):
		self.display = display

	def Update(self):
		for source in self.sources:
			source.Update()
		
		for gravity in self.gravities:
			gravity.Update()
		
		for obstacle in self.obstacles:
			obstacle.Update()

		for particle in self.particles:
			totalforce = [0.0, 0.0]
			
			for gravity in self.gravities:
				force = gravity.GetForce(particle.pos)
				totalforce[0] += force[0]
				totalforce[1] += force[1]
			
			for obstacle in self.obstacles:
				if (not obstacle.OutOfRange(particle.pos)) and (obstacle.InsideObject(particle.pos)):
					particle.pos = obstacle.GetResolved(particle.pos)
				
				force = obstacle.GetForce(particle.pos, particle.velocity)
				totalforce[0] += force[0]
				totalforce[1] += force[1]
			
			particle.velocity = [particle.velocity[0] + totalforce[0], particle.velocity[1] + totalforce[1]]
			
			particle.Update()
		
		# Delete dead particles
		for particle in self.particles:
			if not particle.alive:
				self.particles.remove(particle)
	
	def Redraw(self):
		for particle in self.particles:
			particle.Draw(self.display)
			
		for obstacle in self.obstacles:
			obstacle.Draw(self.display)
	
	def CreateSource(self, pos = (0, 0), initspeed = 0.0, initdirection = 0.0, initspeedrandrange = 0.0, initdirectionrandrange = 0.0, particlesperframe = 0, particlelife = 0, genspacing = 0, drawtype = 0, colour = (0, 0, 0), radius = 0.0, length = 0.0, image = None):
		newsource = particles.ParticleSource(self, pos, initspeed, initdirection, initspeedrandrange, initdirectionrandrange, particlesperframe, particlelife, genspacing, drawtype, colour, radius, length, image)
		self.sources.append(newsource)
		return newsource  # Effectively a reference
	
	def CreatePointGravity(self, strength = 0.0, strengthrandrange = 0.0, pos = (0, 0)):
		newgrav = gravity.PointGravity(strength, strengthrandrange, pos)
		self.gravities.append(newgrav)
		return newgrav
	
	def CreateDirectedGravity(self, strength = 0.0, strengthrandrange = 0.0, direction = [0, 1]):
		newgrav = gravity.DirectedGravity(strength, strengthrandrange, direction)
		self.gravities.append(newgrav)
		return newgrav
	
	def CreateCircle(self, pos = (0, 0), colour = (0, 0, 0), bounce = 1.0, radius = 0.0):
		newcircle = obstacles.Circle(pos, colour, bounce, radius)
		self.obstacles.append(newcircle)
		return newcircle
	
	def CreateRectangle(self, pos = (0, 0), colour = (0, 0, 0), bounce = 1.0, width = 0.0, height = 0.0):
		newrect = obstacles.Rectangle(pos, colour, bounce, width, height)
		self.obstacles.append(newrect)
		return newrect
	
	def CreateBoundaryLine(self, pos = (0, 0), colour = (0, 0, 0), bounce = 1.0, normal = [0, 1]):
		newline = obstacles.BoundaryLine(pos, colour, bounce, normal)
		self.obstacles.append(newline)
		return newline
	
	def AddParticle(self, particle):
		self.particles.append(particle)




## Begin testing code
if __name__ == '__main__':
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("PyIgnition demo")
	clock = pygame.time.Clock()
	test = ParticleEffect(screen, (0, 0), (800, 600))
	testgrav = test.CreatePointGravity(strength = 1.0, pos = (500, 380))
	testgrav.CreateKeyframe(300, strength = 10.0, pos = (0, 0))
	testgrav.CreateKeyframe(450, strength = 10.0, pos = (40, 40))
	testgrav.CreateKeyframe(550, strength = -2.0, pos = (600, 480))
	testgrav.CreateKeyframe(600, strength = -20.0, pos = (600, 0))

	testgrav.CreateKeyframe(650, strength = 1.0, pos = (500, 380))
	anothertestgrav = test.CreateDirectedGravity(strength = 0.04, direction = [1, 0])
	anothertestgrav.CreateKeyframe(300, strength = 1.0, direction = [-0.5, 1])
	anothertestgrav.CreateKeyframe(600, strength = 1.0, direction = [1.0, -0.1])
	anothertestgrav.CreateKeyframe(650, strength = 0.04, direction = [1, 0])
	testsource = test.CreateSource((10, 10), initspeed = 5.0, initdirection = 2.35619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.0, particlesperframe = 5, particlelife = 125, drawtype = DRAWTYPE_SCALELINE, colour = (255, 255, 255), length = 10.0)

	testsource.CreateParticleKeyframe(50, colour = (0, 255, 0), length = 10.0)
	testsource.CreateParticleKeyframe(75, colour = (255, 255, 0), length = 10.0)
	testsource.CreateParticleKeyframe(100, colour = (0, 255, 255), length = 10.0)
	testsource.CreateParticleKeyframe(125, colour = (0, 0, 0), length = 10.0)
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		
		screen.fill((0, 0, 0))
		test.Update()
		test.Redraw()
		pygame.display.update()
		clock.tick(20)

