import pygame
import pymunk
pygame.init()

clock = pygame.time.Clock()
space = pymunk.Space()
display = pygame.display.set_mode((800, 800))

body = pymunk.Body()
body.position = 400, 400
shape = pymunk.Circle(body, 10)
shape.density = 1
shape.elasticity = .9
space.add(body, shape)

space.gravity = 0, 1000
segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_shape = pymunk.Segment(segment_body, (0, 750), (800, 750), 5)
segment_shape.elasticity = 1
space.add(segment_body, segment_shape) 

def test():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		display.fill((255, 255, 255))

		pos = body.position
		pygame.draw.circle(display, (255, 0, 0), (pos), 10)
		pygame.draw.line(display, (0, 0, 0), (0, 750), (800, 750), 5)

		pygame.display.flip()
		clock.tick(60)
		space.step(1/60)
test()
pygame.quit()