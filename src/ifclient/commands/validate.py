import click
from ifclient.config.validation.dispatcher import validate_and_resolve
from pydantic import ValidationError
import json

@click.command(name="validate")
@click.argument("config_file", type=click.Path(exists=True, dir_okay=False)) 
@click.option("--skip-empty-files", type=bool, default=False, help="Skip empty files from validation")
def validate_cmd(config_file, skip_empty_files):
    """
    Validate the provided configuration file (and all referenced files).
    """
    try:
        validated_record = validate_and_resolve(config_file, skip_empty_files, is_main=True)
        print(validated_record.model_dump_json(indent=4))
        click.echo(f"Configuration is valid.")
    except ValidationError as e:
        click.echo(f"Validation error: {e}")
        raise click.ClickException("Validation failed.")
    except Exception as e:
        click.echo(f"Exception: {e}")
        raise click.ClickException("Validation failed.")
