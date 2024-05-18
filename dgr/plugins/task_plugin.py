import abc

class TaskPlugin(abc.ABC):
    @abc.abstractmethod
    def create(self, **kwargs) -> str:
        """Create the task.
        
        Return: str with identifier sufficient to carry out later tasks."""
        ...
    
    @abc.abstractmethod
    def cancel(self, task_id):
        """Cancel the task.
        
        Args: the task id returned from create"""
        ...

    @abc.abstractmethod
    def status(self, task_id):
        """Check status of the task.
        
        Args: the task id returned from create()"""
        ...

    @abc.abstractmethod
    def validate(self, **kwargs):
        """Validate arguments which could be passed to create()"""
        ...

