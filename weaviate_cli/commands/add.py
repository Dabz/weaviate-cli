import click
import sys
from weaviate_cli.managers.user_manager import UserManager
from weaviate_cli.managers.role_manager import RoleManager
from weaviate_cli.utils import get_client_from_context
from weaviate_cli.defaults import PERMISSION_HELP_STRING


@click.group()
def add() -> None:
    """Add resources to other resources in Weaviate."""
    pass


@add.command("role")
@click.option(
    "--role_name",
    multiple=True,
    required=True,
    help="The name of the role to add. Can be specified multiple times. Example: --role_name MoviesAdmin --role_name TenantAdmin",
)
@click.option(
    "--user_name",
    required=True,
    help="The user to add the role to.",
)
@click.pass_context
def add_role_cli(ctx: click.Context, role_name: tuple[str], user_name: str) -> None:
    """Add a role to a user."""
    client = None
    try:
        client = get_client_from_context(ctx)
        user_manager = UserManager(client)
        user_manager.add_role(role_name=role_name, user_name=user_name)
    except Exception as e:
        click.echo(f"Error: {e}")
        if client:
            client.close()
        sys.exit(1)
    finally:
        if client:
            client.close()


@add.command("permission")
@click.option(
    "-p",
    "--permission",
    multiple=True,
    required=True,
    help=PERMISSION_HELP_STRING,
)
@click.option(
    "--role_name",
    required=True,
    help="The name of the role to add the permission to.",
)
@click.pass_context
def add_permission_cli(
    ctx: click.Context, permission: tuple[str], role_name: str
) -> None:
    """Add a permission to a role."""

    client = None
    try:
        client = get_client_from_context(ctx)
        role_manager = RoleManager(client)
        role_manager.add_permission(permission=permission, role_name=role_name)
    except Exception as e:
        click.echo(f"Error: {e}")
        if client:
            client.close()
        sys.exit(1)
    finally:
        if client:
            client.close()
