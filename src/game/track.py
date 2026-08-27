"""
Kart Rush - Track System
Surface sampling, checkpoint logic, and track data.
"""

from panda3d.core import Vec3
import math


class Track:
    """Procedural track with surface sampling and checkpoints."""
    
    def __init__(self, name, control_points, width=12.0, checkpoints=None):
        self.name = name
        self.control_points = [Vec3(*p) for p in control_points]
        self.width = width
        self.length = self._calculate_length()
        self.checkpoints = checkpoints or self._generate_checkpoints()
        
    def _calculate_length(self):
        """Calculate total track length."""
        total = 0.0
        for i in range(len(self.control_points)):
            p1 = self.control_points[i]
            p2 = self.control_points[(i + 1) % len(self.control_points)]
            total += (p2 - p1).length()
        return total
    
    def _generate_checkpoints(self):
        """Generate evenly spaced checkpoints."""
        num_checkpoints = 8
        checkpoints = []
        segment_length = self.length / num_checkpoints
        
        for i in range(num_checkpoints):
            t = i / num_checkpoints
            pos = self.get_position_at_t(t)
            tangent = self.get_tangent_at_t(t)
            checkpoints.append({
                'index': i,
                'position': pos,
                'tangent': tangent,
                'respawn_point': pos + Vec3(0, 0, 0.5)
            })
        
        return checkpoints
    
    def get_position_at_t(self, t):
        """Get position along track (0-1)."""
        t = t % 1.0
        target_dist = t * self.length
        
        cumulative = 0.0
        for i in range(len(self.control_points)):
            p1 = self.control_points[i]
            p2 = self.control_points[(i + 1) % len(self.control_points)]
            seg_len = (p2 - p1).length()
            
            if cumulative + seg_len >= target_dist:
                local_t = (target_dist - cumulative) / seg_len if seg_len > 0 else 0
                return p1 + (p2 - p1) * local_t
            
            cumulative += seg_len
        
        return self.control_points[0]
    
    def get_tangent_at_t(self, t):
        """Get tangent vector at position."""
        epsilon = 0.001
        p1 = self.get_position_at_t(t)
        p2 = self.get_position_at_t(t + epsilon)
        tangent = (p2 - p1).normalized()
        return tangent if tangent.length() > 0 else Vec3(0, 0, 1)
    
    def surface_at(self, position):
        """Sample surface at world position."""
        closest_t = self.find_closest_t(position)
        closest_pos = self.get_position_at_t(closest_t)
        
        dist_from_center = (Vec3(position[0], 0, position[2]) - 
                           Vec3(closest_pos[0], 0, closest_pos[2])).length()
        
        on_road = dist_from_center <= self.width * 0.5
        
        return {
            'on_road': on_road,
            'dist_from_center': dist_from_center,
            't': closest_t,
            'tangent': self.get_tangent_at_t(closest_t)
        }
    
    def find_closest_t(self, position, samples=100):
        """Find track parameter t closest to position."""
        min_dist = float('inf')
        closest_t = 0.0
        
        for i in range(samples):
            t = i / samples
            pos = self.get_position_at_t(t)
            dist = (Vec3(position[0], 0, position[2]) - 
                   Vec3(pos[0], 0, pos[2])).length()
            
            if dist < min_dist:
                min_dist = dist
                closest_t = t
        
        return closest_t
    
    def get_checkpoint_at_index(self, index):
        """Get checkpoint by index."""
        if 0 <= index < len(self.checkpoints):
            return self.checkpoints[index]
        return None
    
    def snap(self):
        """Return snapshot for QA."""
        return {
            'name': self.name,
            'length': self.length,
            'width': self.width,
            'num_checkpoints': len(self.checkpoints),
            'control_points': len(self.control_points)
        }


# Default test track (closed oval - perfectly symmetric, closed loop)
TEST_TRACK_POINTS = [
    [0, 0, 100],     # Start/finish straight (top center)
    [60, 0, 100],    # Top right straight
    [100, 0, 60],    # Top right corner
    [100, 0, 0],     # Right straight
    [100, 0, -60],   # Bottom right corner
    [60, 0, -100],   # Bottom right straight
    [0, 0, -100],    # Back straight (bottom center)
    [-60, 0, -100],  # Bottom left straight
    [-100, 0, -60],  # Bottom left corner
    [-100, 0, 0],    # Left straight
    [-100, 0, 60],   # Top left corner
    [-60, 0, 100],   # Top left straight
    [0, 0, 100],     # Close the loop explicitly
]

def create_test_track():
    """Create default test track."""
    return Track("Test Oval", TEST_TRACK_POINTS, width=12.0)
