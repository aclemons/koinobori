if __name__ == "env_py":
    import os

    import structlog
    from alembic import context, ddl
    from sqlalchemy import pool
    from sqlalchemy.engine import create_engine

    ddl.impl._impls["dynamodb"] = ddl.impl.DefaultImpl  # noqa: SLF001

    logger = structlog.stdlib.get_logger(__name__)

    # this is the Alembic Config object, which provides
    # access to the values within the .ini file in use.
    config = context.config

    target_metadata = None

    def run_migrations_offline() -> None:
        """Run migrations in 'offline' mode.

        This configures the context with just a URL
        and not an Engine, though an Engine is acceptable
        here as well.  By skipping the Engine creation
        we don't even need a DBAPI to be available.

        Calls to context.execute() here emit the given string to the
        script output.

        """

        aws_url = (
            os.environ.get("AWS_URL", None)
            or "dynamodb.{region_name}.amazonaws.com:443"
        ).format(region_name=os.environ["AWS_REGION"])
        conn_str = "dynamodb://{aws_url}"

        url = conn_str.format(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            aws_url=aws_url,
        )

        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
            version_table=os.environ["ALEMBIC_VERSION_TABLE"],
        )

        with context.begin_transaction():
            context.run_migrations()

    def run_migrations_online() -> None:
        """Run migrations in 'online' mode.

        In this scenario we need to create an Engine
        and associate a connection with the context.

        """

        logger.info("Running migrations")

        aws_url = (
            os.environ.get("AWS_URL", None)
            or "dynamodb.{region_name}.amazonaws.com:443"
        ).format(region_name=os.environ["AWS_REGION"])
        conn_str = "dynamodb://{aws_url}"

        conn_str = conn_str.format(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            aws_url=aws_url,
        )

        connectable = create_engine(conn_str, poolclass=pool.NullPool)

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                version_table=os.environ["ALEMBIC_VERSION_TABLE"],
            )

            with context.begin_transaction():
                context.run_migrations()

    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()
