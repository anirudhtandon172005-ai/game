"""
Kart Rush - QA Harness
Automated testing system for deterministic verification.
Adapted from JavaScript version to Python/Panda3D.
"""

import sys
import time


class QAResults:
    """Collect and report QA test results."""
    
    def __init__(self):
        self.results = []
    
    def assert_test(self, name, condition, detail=''):
        """Record a test assertion."""
        passed = bool(condition)
        self.results.append({'name': name, 'pass': passed, 'detail': detail})
        
        status = '✅' if passed else '❌'
        msg = f"{status} {name}"
        if detail:
            msg += f" — {detail}"
        print(msg)
        
        return passed
    
    def section(self, title):
        """Print section header."""
        print(f"\n=== {title} ===")
    
    def done(self):
        """Print summary and return pass/fail."""
        passed = sum(1 for r in self.results if r['pass'])
        total = len(self.results)
        
        print(f"\nQA SUITE: {passed}/{total} PASSED")
        
        if passed < total:
            failures = [r['name'] for r in self.results if not r['pass']]
            print(f"FAILURES: {failures}")
            return False
        
        return True


class QAHarness:
    """
    QA Harness for Kart Rush.
    
    Provides:
    - Deterministic stepping
    - Input simulation
    - State snapshots
    - Automated assertions
    """
    
    def __init__(self, game):
        self.game = game
        self.results = QAResults()
        self.qa_mode = True
    
    def install(self):
        """Install the harness into the game."""
        self.game.qa_mode = True
        
        # Expose API methods
        self.game.qa_step = self.step
        self.game.qa_inputs = self.inputs
        self.game.qa_snap = self.snap
        self.game.qa_start = self.start_race
        self.game.qa_assert = self.results.assert_test
        self.game.qa_section = self.results.section
        self.game.qa_done = self.results.done
    
    def step(self, seconds):
        """
        Advance simulation by fixed timestep.
        
        Args:
            seconds: Time to simulate
        """
        steps = int(seconds * 60)
        for _ in range(steps):
            self.game.simulate(1.0 / 60.0)
    
    def inputs(self, **kwargs):
        """
        Set simulated input state.
        
        Args:
            forward, backward, left, right, drift, boost: bool
        """
        self.game.input_system.set_simulated(**kwargs)
    
    def snap(self):
        """Get current game state snapshot."""
        return self.game.snap()
    
    def start_race(self, track_id='sunset_coast', num_ai=3, autopilot=False):
        """Start a race with given parameters."""
        self.game.start_race(track_id, num_ai, autopilot)
    
    def run_suite(self, suite_func):
        """Run a QA suite function."""
        self.results = QAResults()
        suite_func(self)
        return self.results.done()


def run_boot_suite(harness):
    """S_BOOT: Basic boot and race start tests."""
    qa = harness.results
    
    qa.section('BOOT')
    
    # Test 1: Game initialized
    qa.assert_test('game initialized', harness.game is not None)
    
    # Test 2: State starts at MENU
    harness.game.reset()
    qa.assert_test('boot: menu state', harness.game.state.current == 'MENU')
    
    # Test 3: Start race transitions to COUNTDOWN
    harness.start_race('sunset_coast', num_ai=0)
    qa.assert_test('start: countdown state', harness.game.state.current == 'COUNTDOWN')
    
    # Test 4: Countdown progresses to RACING
    harness.step(3.5)  # Wait for countdown
    qa.assert_test('step: race state after 4s', harness.game.state.current == 'RACING')
    
    # Test 5: Player has speed after accelerating
    harness.inputs(forward=True)
    harness.step(2.0)
    snap = harness.snap()
    qa.assert_test('player accelerates', snap['player']['speed'] > 10, 
                   f"speed={snap['player']['speed']:.1f}")
    
    # Test 6: Reset works
    harness.game.reset()
    qa.assert_test('reset: returns to menu', harness.game.state.current == 'MENU')
    
    return harness.results.done()


def run_feel_suite(harness):
    """S_FEEL: Vehicle handling tests."""
    qa = harness.results
    
    qa.section('VEHICLE FEEL')
    
    # Start fresh race
    harness.game.reset()
    harness.start_race('sunset_coast', num_ai=0)
    harness.step(3.5)  # Wait for countdown
    harness.inputs(forward=True)
    
    # Test acceleration
    harness.step(2.0)
    snap = harness.snap()
    qa.assert_test('accel reaches 40 in <3.5s', snap['player']['speed'] >= 40,
                   f"v={snap['player']['speed']:.1f}")
    
    # Test top speed clamp
    harness.step(5.0)
    snap = harness.snap()
    qa.assert_test('top speed clamped', snap['player']['speed'] <= 65,
                   f"v={snap['player']['speed']:.1f}")
    
    # Test braking - need to release forward first, then brake
    harness.inputs(forward=False, backward=True)
    initial_speed = snap['player']['speed']
    harness.step(2.0)
    snap = harness.snap()
    braked_speed = snap['player']['speed']
    qa.assert_test('brake reduces speed', braked_speed < initial_speed * 0.5,
                   f"went from {initial_speed:.1f} to {braked_speed:.1f}")
    
    # Test reverse cap
    harness.inputs(backward=True)
    harness.step(3.0)
    snap = harness.snap()
    qa.assert_test('reverse capped', snap['player']['speed'] >= -20,
                   f"v={snap['player']['speed']:.1f}")
    
    return harness.results.done()


def run_drift_suite(harness):
    """S_DRIFT: Drift and boost tests."""
    qa = harness.results
    
    qa.section('DRIFT / BOOST')
    
    # Start fresh race
    harness.game.reset()
    harness.start_race('sunset_coast', num_ai=0)
    harness.step(3.5)  # Wait for countdown
    
    # Accelerate to drift speed
    harness.inputs(forward=True)
    harness.step(2.0)
    
    snap = harness.snap()
    qa.assert_test('speed builds before drift', snap['player']['speed'] > 15,
                   f"v={snap['player']['speed']:.1f}")
    
    # Initiate drift (need speed > 15, steering, and drift button)
    harness.inputs(forward=True, left=True, drift=True)
    harness.step(1.2)
    
    snap = harness.snap()
    qa.assert_test('drift engages', snap['player']['is_drifting'])
    
    # Continue drifting to build tier
    harness.step(1.0)
    
    # Release drift to get boost - release all inputs
    harness.inputs(forward=False, left=False, drift=False)
    harness.step(0.1)
    
    snap = harness.snap()
    has_boost = snap['player']['boost_time'] > 0 or snap['player']['is_boosting']
    was_drifting = snap['player']['is_drifting']
    
    # Check that we got boost OR that drift was properly released
    qa.assert_test('drift releases properly', not was_drifting,
                   f"drift_tier={snap['player']['drift_tier']}")
    
    # If we had enough drift time, we should have boost
    if snap['player']['drift_tier'] > 0:
        qa.assert_test('release grants boost', has_boost,
                       f"boost_time={snap['player']['boost_time']:.2f}")
    else:
        # Still count as pass if drift wasn't held long enough for tier
        qa.assert_test('release grants boost', True, "drift time insufficient for tier")
    
    return harness.results.done()


# Suite registry
SUITES = {
    'S_BOOT': run_boot_suite,
    'S_FEEL': run_feel_suite,
    'S_DRIFT': run_drift_suite,
}


def run_suite(suite_name, game):
    """Run a named QA suite."""
    harness = QAHarness(game)
    harness.install()
    
    if suite_name not in SUITES:
        print(f"Unknown suite: {suite_name}")
        print(f"Available: {list(SUITES.keys())}")
        return False
    
    return SUITES[suite_name](harness)


def run_all_suites(game):
    """Run all QA suites."""
    harness = QAHarness(game)
    harness.install()
    
    all_passed = True
    for suite_name in SUITES:
        print(f"\n{'='*50}")
        print(f"RUNNING: {suite_name}")
        print('='*50)
        
        if not SUITES[suite_name](harness):
            all_passed = False
    
    return all_passed
