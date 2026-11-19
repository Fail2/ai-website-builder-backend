import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum as SQLAlchemyEnum, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import ProjectStatus
from app.database.session import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    brand_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    niche: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[ProjectStatus] = mapped_column(
        SQLAlchemyEnum(
            ProjectStatus,
            values_callable=lambda enum: [item.value for item in enum],
            native_enum=False,
        ),
        default=ProjectStatus.CREATED,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
