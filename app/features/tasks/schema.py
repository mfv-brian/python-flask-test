from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    """Schema for Task data validation and serialization"""
    id = fields.Int(dump_only=True, description="Task unique identifier")
    title = fields.Str(required=True, description="Task title")
    description = fields.Str(required=True, description="Task description")
    status = fields.Str(
        required=False,
        default="pending",
        validate=validate.OneOf(["pending", "in_progress", "completed"]),
        description="Task status (pending, in_progress, completed)"
    )
    created_at = fields.DateTime(dump_only=True, description="Task creation timestamp")

class TaskListSchema(Schema):
    """Schema for list of tasks"""
    tasks = fields.List(fields.Nested(TaskSchema), description="List of tasks")
    total = fields.Int(description="Total number of tasks") 