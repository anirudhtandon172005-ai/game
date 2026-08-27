"""
KART RUSH - 3D Go-Kart Racing Game
Main Entry Point
"""

from ursina import *

# Simple test to verify ursina works
def test_game():
    app = Ursina()
    window.title = 'Kart Rush'
    window.size = (1280, 720)
    
    # Create a simple scene
    ground = Entity(
        model='plane',
        color=color.rgb(50, 150, 50),
        scale=(100, 1, 100),
        texture='white_cube'
    )
    
    # Create a player kart (simple cube for now)
    player = Entity(
        model='cube',
        color=color.blue,
        scale=(1, 0.5, 2),
        position=(0, 0.5, 0),
        texture='white_cube'
    )
    
    # Camera setup
    camera.position = (0, 5, -10)
    camera.look_at(player)
    
    print("Kart Rush initialized!")
    print("Controls: WASD to move, ESC to quit")
    
    # Simple movement
    speed = 10
    
    def update():
        if held_keys['w']:
            player.z -= speed * time.dt
        if held_keys['s']:
            player.z += speed * time.dt
        if held_keys['a']:
            player.x -= speed * time.dt
        if held_keys['d']:
            player.x += speed * time.dt
        
        # Follow camera
        camera.position = Vec3(player.x, 5, player.z - 10)
        camera.look_at(player)
    
    app.run()

if __name__ == '__main__':
    test_game()
