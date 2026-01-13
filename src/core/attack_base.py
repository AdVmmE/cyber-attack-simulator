from abc import ABC, abstractmethod

class AttackEngine(ABC):
    """
    Base class for all attack simulation engines.
    """
    
    @abstractmethod
    def reset(self):
        """Reset the simulation state."""
        pass

    @abstractmethod
    def run_step(self, *args, **kwargs):
        """Run a step of the simulation."""
        pass
