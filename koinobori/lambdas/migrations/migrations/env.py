if __name__ == "env_py":
    import os

    import structlog
    from alembic import context, ddl
    from sqlalchemy import pool
    from sqlalchemy.engine import create_engine
    from yarl import URL

    ddl.impl._impls["dynamodb"] = ddl.impl.DefaultImpl  # noqa: SLF001

    logger = structlog.stdlib.get_logger(__name__)

    # this is the Alembic Config object, which provides
    # access to the values within the .ini file in use.
    config = context.config

    target_metadata = None

    def get_aws_url() -> str:
        custom_url = os.environ.get("AWS_URL", None)

        if custom_url:
            parsed = URL(custom_url)
            if not parsed.host:
                msg = f"Custom url {custom_url} could not be parsed"
                raise ValueError(msg)

            aws_url = parsed.host

            if parsed.port:
                aws_url += f":{parsed.port}"

            aws_url += "?region_name={region_name}&endpoint_url={custom_url}"
            aws_url = aws_url.format(
                region_name=os.environ["AWS_REGION"],
                custom_url=custom_url,
            )

        else:
            aws_url = "dynamodb.{region_name}.amazonaws.com:443"
            aws_url = aws_url.format(region_name=os.environ["AWS_REGION"])

        conn_str = "dynamodb://{aws_url}"

        return conn_str.format(aws_url=aws_url)

    def run_migrations_offline() -> None:
        """Run migrations in 'offline' mode.

        This configures the context with just a URL
        and not an Engine, though an Engine is acceptable
        here as well.  By skipping the Engine creation
        we don't even need a DBAPI to be available.

        Calls to context.execute() here emit the given string to the
        script output.

        """

        context.configure(
            url=get_aws_url(),
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

        url = get_aws_url()

        logger.info("Running migrations", url=url)

        connectable = create_engine(url, poolclass=pool.NullPool)

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
